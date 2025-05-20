from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import time

from com.mhire.app.config.config import Config
from com.mhire.app.services.audio_service.audio_service import audio_service
from com.mhire.app.common.network_responses import NetworkResponse, HTTPCode

router = APIRouter(prefix=f"{Config().api_prefix}/audio", tags=["audio"])
network_response = NetworkResponse()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), use_groq: bool = Form(True)):
    """Transcribe audio using Groq Whisper API or Silero fallback"""
    start_time = time.time()
    
    try:
        # Read audio file content
        audio_content = await file.read()
        
        # Call audio service to transcribe
        result = await audio_service.transcribe_audio(audio_content, use_groq)
        
        return network_response.success_response(
            HTTPCode.SUCCESS,
            result,
            "audio/transcribe",
            start_time
        )
    except Exception as e:
        return network_response.error_response(
            HTTPCode.INTERNAL_SERVER_ERROR,
            50000,
            str(e),
            "audio/transcribe",
            start_time
        )

@router.post("/speak")
async def text_to_speech(text: str = Form(...), voice: Optional[str] = Form("alloy")):
    """Convert text to speech using Groq TTS API"""
    start_time = time.time()
    
    try:
        # Call audio service for text-to-speech
        result = await audio_service.text_to_speech(text, voice)
        
        return network_response.success_response(
            HTTPCode.SUCCESS,
            result,
            "audio/speak",
            start_time
        )
    except Exception as e:
        return network_response.error_response(
            HTTPCode.INTERNAL_SERVER_ERROR,
            50000,
            str(e),
            "audio/speak",
            start_time
        )