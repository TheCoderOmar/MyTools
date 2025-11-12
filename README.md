# 🚀 Omar's Tools - Complete Setup Guide

## 📁 Final Project Structure

```
C:\Users\Omar\Music\
│
├── backend/
│   ├── main.py                      # Main FastAPI app
│   ├── routes/
│   │   ├── __init__.py              # Empty file
│   │   ├── youtube.py               # YouTube routes
│   │   └── converter.py             # Converter routes
│   ├── services/
│   │   ├── __init__.py              # Empty file
│   │   ├── youtube_service.py       # YouTube logic
│   │   └── converter_service.py     # Converter logic
│   └── downloads/                   # Auto-created temp folder
│
├── frontend/
│   └── index.html                   # Complete frontend with all tools
│
└── requirements.txt                  # Python dependencies
```

---

## 🛠️ Installation Steps

### Step 1: Create Folders

```bash
cd "C:\Users\Omar\Music"
mkdir backend
mkdir backend\routes
mkdir backend\services
mkdir frontend
```

### Step 2: Create Empty `__init__.py` Files

Create these empty files to make Python recognize the folders as packages:

**`backend/routes/__init__.py`**
```python
# Empty file
```

**`backend/services/__init__.py`**
```python
# Empty file
```

### Step 3: Copy All the Code Files

Copy each code file from the artifacts above into the correct location:

- ✅ `backend/main.py`
- ✅ `backend/routes/youtube.py`
- ✅ `backend/routes/converter.py`
- ✅ `backend/services/youtube_service.py`
- ✅ `backend/services/converter_service.py`
- ✅ `frontend/index.html`

### Step 4: Create `requirements.txt`

**`requirements.txt`** (in root Music folder)
```txt
fastapi
uvicorn
yt-dlp
mutagen
pillow
requests
python-multipart
xmltodict
```

### Step 5: Install Dependencies

```bash
cd "C:\Users\Omar\Music"
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Start Backend

```bash
cd "C:\Users\Omar\Music\backend"
python main.py
```

✅ You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`

### Open Frontend

Simply **double-click** `frontend/index.html` or use Python server:

```bash
cd "C:\Users\Omar\Music\frontend"
python -m http.server 3000
```

Then open: `http://localhost:3000`

---

## ✨ How It Works

### Home Page
- Shows "Welcome Omar!" with tool boxes
- Click any tool to open it

### YouTube Music Tool
- Search or paste YouTube URLs
- Download high-quality MP3s with metadata
- Real-time progress bar

### XML/JSON Converter
- Convert XML → JSON or JSON → XML
- Swap and convert back instantly
- Clean, formatted output

---

## 🎯 API Endpoints

### YouTube
- `POST /api/youtube/search` - Search videos
- `GET /api/youtube/video-info?url=...` - Get video info
- `GET /api/youtube/thumbnail/{video_id}` - Get thumbnail
- `POST /api/youtube/download` - Download MP3

### Converter
- `POST /api/converter/xml-to-json` - Convert XML to JSON
- `POST /api/converter/json-to-xml` - Convert JSON to XML

---

## 📝 Adding More Tools (Future)

To add a new tool:

1. **Create route**: `backend/routes/newtool.py`
2. **Create service**: `backend/services/newtool_service.py`
3. **Add to main.py**: `app.include_router(newtool.router, prefix="/api/newtool")`
4. **Add to frontend**: Create new page component and add to home page

---

## 🐛 Troubleshooting

**Backend won't start?**
- Make sure you're in the `backend` folder
- Check all dependencies are installed: `pip list`

**Frontend can't connect?**
- Ensure backend is running on port 8000
- Check browser console for errors (F12)

**Downloads not working?**
- Make sure FFmpeg is installed (required by yt-dlp)
- Check the `downloads` folder is created

---

## 🎉 Done!

Your multi-tool application is ready! Each tool is completely separate and modular.
