import os
import time
import httpx
import numpy as np
import onnxruntime as ort
from typing import Optional, Dict, Any, List
from fastapi import HTTPException

from com.mhire.app.config.config import Config
from com.mhire.app.common.utility import generate_request_id

class AudioService:
    def __init__(self):
        self.config = Config()
        self.groq_api_key = self.config.groq_api_key
        self.groq_tts_model = self.config.groq_tts_model
        self.groq_stt_model = self.config.groq_stt_model
        
        # Initialize Silero models for fallback
        self.silero_encoder_path = self.config.silero_encoder_path
        self.silero_decoder_path = self.config.silero_decoder_path
        self.silero_initialized = False
        
        # Create audio assets directory if it doesn't exist
        os.makedirs(self.config.audio_assets_path, exist_ok=True)
    
    def _initialize_silero(self):
        """Initialize Silero ONNX models for local fallback"""
        try:
            self.encoder_session = ort.InferenceSession(self.silero_encoder_path)
            self.decoder_session = ort.InferenceSession(self.silero_decoder_path)
            self.silero_initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize Silero models: {str(e)}")
            return False
    
    async def transcribe_audio(self, audio_file: bytes, use_groq: bool = True) -> Dict[str, Any]:
        """Transcribe audio using Groq Whisper API or Silero fallback"""
        request_id = generate_request_id(f"transcribe_{time.time()}")
        
        if use_groq and self.groq_api_key:
            try:
                # Save audio file temporarily
                temp_audio_path = os.path.join(self.config.audio_assets_path, f"{request_id}.wav")
                with open(temp_audio_path, 'wb') as f:
                    f.write(audio_file)
                
                # Call Groq Whisper API
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}"
                }
                
                async with httpx.AsyncClient() as client:
                    files = {'file': open(temp_audio_path, 'rb')}
                    response = await client.post(
                        "https://api.groq.com/openai/v1/audio/transcriptions",
                        headers=headers,
                        files=files,
                        data={"model": self.groq_stt_model}
                    )
                
                # Clean up temp file
                os.remove(temp_audio_path)
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "text": result.get("text", ""),
                        "request_id": request_id
                    }
                else:
                    print(f"Groq API error: {response.text}")
                    raise HTTPException(status_code=response.status_code, detail=response.text)
            
            except Exception as e:
                print(f"Error using Groq API: {str(e)}")
                # Fall back to Silero if Groq fails
                if not use_groq:
                    return await self._transcribe_with_silero(audio_file, request_id)
                raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
        else:
            # Use Silero for transcription
            return await self._transcribe_with_silero(audio_file, request_id)
    
    async def _transcribe_with_silero(self, audio_file: bytes, request_id: str) -> Dict[str, Any]:
        """Fallback to Silero models for transcription"""
        if not self.silero_initialized:
            if not self._initialize_silero():
                raise HTTPException(status_code=500, detail="Failed to initialize Silero models")
        
        try:
            # Implementation would depend on how you want to use Silero ONNX models
            # This is a placeholder for the actual implementation
            return {
                "text": "Silero transcription not fully implemented",
                "request_id": request_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Silero transcription failed: {str(e)}")
    
    async def text_to_speech(self, text: str, voice: str = "alloy") -> Dict[str, Any]:
        """Convert text to speech using Groq TTS API"""
        request_id = generate_request_id(f"tts_{time.time()}")
        
        if not self.groq_api_key:
            raise HTTPException(status_code=400, detail="Groq API key not configured")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.groq_tts_model,
                "input": text,
                "voice": voice
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/audio/speech",
                    headers=headers,
                    json=payload
                )
            
            if response.status_code == 200:
                # Save audio file
                audio_path = os.path.join(self.config.audio_assets_path, f"{request_id}.mp3")
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                
                return {
                    "audio_path": audio_path,
                    "request_id": request_id
                }
            else:
                print(f"Groq API error: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {str(e)}")

# Create a singleton instance
audio_service = AudioService()