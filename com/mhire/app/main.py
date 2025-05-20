from fastapi import FastAPI
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from com.mhire.app.config.config import Config
from com.mhire.app.services.audio_service.audio_router import router as audio_router
from com.mhire.app.services.video_service.video_router import router as video_router

config = Config()

app = FastAPI(
    title="AI-Based Live Video Conferencing",
    description="Live video conferencing system with AI-powered avatars",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(audio_router)
app.include_router(video_router)

# Mount static directories for serving files
app.mount("/audio-assets", StaticFiles(directory=config.audio_assets_path), name="audio-assets")
app.mount("/video-assets", StaticFiles(directory=config.video_assets_path), name="video-assets")

@app.get("/", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def health_check():
    return "AI-powered Live Video Conferencing system is running and healthy"
