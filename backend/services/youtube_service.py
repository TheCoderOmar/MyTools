import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from PIL import Image
import os
import uuid
import requests
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def search_youtube_videos(query: str):
    """Search YouTube and return top 6 results"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch6:{query}", download=False)
        
        results = []
        for video in search_results['entries']:
            duration_sec = int(video.get('duration', 0)) if video.get('duration') else 0
            minutes = duration_sec // 60
            seconds = duration_sec % 60
            
            results.append({
                'id': video['id'],
                'title': video.get('title', 'Unknown'),
                'channel': video.get('channel', 'Unknown'),
                'duration': f"{minutes}:{seconds:02d}",
                'thumbnail': f"http://localhost:8000/api/youtube/thumbnail/{video['id']}",
                'url': f"https://youtube.com/watch?v={video['id']}"
            })
        
        return results

def get_video_information(url: str):
    """Get video info from URL"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        duration_sec = int(info.get('duration', 0)) if info.get('duration') else 0
        minutes = duration_sec // 60
        seconds = duration_sec % 60
        
        video_id = info.get('id', '')
        
        return {
            'id': video_id,
            'title': info.get('title', 'Unknown'),
            'channel': info.get('channel', info.get('uploader', 'Unknown')),
            'duration': f"{minutes}:{seconds:02d}",
            'thumbnail': f"http://localhost:8000/api/youtube/thumbnail/{video_id}",
            'url': url
        }

def get_thumbnail_proxy(video_id: str):
    """Proxy YouTube thumbnails to avoid CORS issues"""
    thumbnail_urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
    ]
    
    for url in thumbnail_urls:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return StreamingResponse(BytesIO(response.content), media_type="image/jpeg")
    
    raise HTTPException(status_code=404, detail="Thumbnail not found")

def download_youtube_video(url: str):
    """Download video as MP3 with metadata and stream it"""
    unique_id = str(uuid.uuid4())[:8]
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{unique_id}_%(title)s.%(ext)s',
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '0'},
        ],
        'quiet': True,
    }

    os.makedirs('downloads', exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Unknown Title')
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_', '.') else '_' for c in title)
        safe_title = ' '.join(safe_title.split())
        filename = f"downloads/{unique_id}_{title}.mp3"
        artist = info.get('artist', info.get('uploader', 'Unknown Artist'))
        album = info.get('album', 'YouTube')

    if os.path.exists(filename):
        possible_thumbnails = [
            f"downloads/{unique_id}_{title}.webp",
            f"downloads/{unique_id}_{title}.jpg",
            f"downloads/{unique_id}_{title}.png",
        ]
        
        thumbnail_file = None
        for thumb in possible_thumbnails:
            if os.path.exists(thumb):
                thumbnail_file = thumb
                break
        
        try:
            audio = EasyID3(filename)
        except:
            audio = EasyID3()
            audio.save(filename)
            audio = EasyID3(filename)
        
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio.save()

        if thumbnail_file:
            jpeg_file = f"downloads/{unique_id}_{title}_cover.jpg"
            if thumbnail_file.endswith('.webp'):
                img = Image.open(thumbnail_file)
                rgb_img = img.convert('RGB')
                rgb_img.save(jpeg_file, 'JPEG', quality=95)
                os.remove(thumbnail_file)
                thumbnail_file = jpeg_file
            
            audio = ID3(filename)
            with open(thumbnail_file, 'rb') as f:
                audio['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=f.read()
                )
            audio.save(v2_version=3)
            os.remove(thumbnail_file)

        def file_iterator():
            with open(filename, 'rb') as file:
                chunk_size = 8192
                while chunk := file.read(chunk_size):
                    yield chunk
            os.remove(filename)

        return StreamingResponse(
            file_iterator(),
            media_type='audio/mpeg',
            headers={
                "Content-Disposition": f'attachment; filename="{safe_title}.mp3"',
                "Content-Length": str(os.path.getsize(filename)),
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    else:
        raise HTTPException(status_code=500, detail="Download failed")