from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import youtube, converter

app = FastAPI(title="Omar's Tools API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(youtube.router, prefix="/api/youtube", tags=["YouTube"])
app.include_router(converter.router, prefix="/api/converter", tags=["Converter"])

@app.get("/")
async def root():
    return {
        "message": "Omar's Tools API",
        "tools": ["YouTube Music Downloader", "XML/JSON Converter"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)