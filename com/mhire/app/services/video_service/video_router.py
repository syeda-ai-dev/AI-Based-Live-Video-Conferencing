from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import time
import os

from com.mhire.app.config.config import Config
from com.mhire.app.services.video_service.video_service import video_service
from com.mhire.app.common.network_responses import NetworkResponse, HTTPCode

router = APIRouter(prefix=f"{Config().api_prefix}/video", tags=["video"])
network_response = NetworkResponse()

@router.post("/generate")
async def generate_video(image: UploadFile = File(...), audio_path: str = Form(...)):
    """Generate a talking avatar video using SadTalker"""
    start_time = time.time()
    
    try:
        # Validate audio path
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail=f"Audio file not found: {audio_path}")
        
        # Read image file content
        image_content = await image.read()
        
        # Call video service to generate talking avatar
        result = await video_service.generate_talking_avatar(image_content, audio_path)
        
        return network_response.success_response(
            HTTPCode.SUCCESS,
            result,
            "video/generate",
            start_time
        )
    except Exception as e:
        return network_response.error_response(
            HTTPCode.INTERNAL_SERVER_ERROR,
            50000,
            str(e),
            "video/generate",
            start_time
        )

@router.get("/stream/{video_id}")
async def stream_video(video_id: str):
    """Stream a generated video by ID"""
    start_time = time.time()
    
    try:
        # Get video path
        video_path = video_service.get_video_path(video_id)
        
        return network_response.success_response(
            HTTPCode.SUCCESS,
            {"video_path": video_path},
            "video/stream",
            start_time
        )
    except Exception as e:
        return network_response.error_response(
            HTTPCode.INTERNAL_SERVER_ERROR,
            50000,
            str(e),
            "video/stream",
            start_time
        )