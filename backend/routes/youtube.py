from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from services.youtube_service import (
    search_youtube_videos,
    get_video_information,
    download_youtube_video,
    get_thumbnail_proxy,
    get_video_formats
)

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

class DownloadRequest(BaseModel):
    url: str

class VideoDownloadRequest(BaseModel):
    url: str
    format_id: str

class SearchResult(BaseModel):
    id: str
    title: str
    channel: str
    duration: str
    thumbnail: str
    url: str

class VideoInfoResponse(BaseModel):
    id: str
    title: str
    channel: str
    duration: str
    thumbnail: str
    url: str

class VideoFormat(BaseModel):
    format_id: str
    resolution: str
    ext: str
    filesize: str
    fps: int

@router.post("/search", response_model=List[SearchResult])
async def search(request: SearchRequest):
    """Search YouTube and return top 6 results"""
    try:
        return search_youtube_videos(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video-info", response_model=VideoInfoResponse)
async def video_info(url: str):
    """Get video info from URL"""
    try:
        return get_video_information(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video-formats")
async def video_formats(url: str):
    """Get available video formats/qualities"""
    try:
        return get_video_formats(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/thumbnail/{video_id}")
async def thumbnail(video_id: str):
    """Proxy YouTube thumbnails to avoid CORS issues"""
    try:
        return get_thumbnail_proxy(video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download")
async def download(request: DownloadRequest):
    """Download video as MP3 with metadata"""
    try:
        return download_youtube_video(request.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download-video")
async def download_video(request: VideoDownloadRequest):
    """Download video with selected quality"""
    try:
        from services.youtube_service import download_youtube_video_quality
        return download_youtube_video_quality(request.url, request.format_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))