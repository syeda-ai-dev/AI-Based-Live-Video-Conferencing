import os
import time
import subprocess
from typing import Dict, Any, Optional
from fastapi import HTTPException

from com.mhire.app.config.config import Config
from com.mhire.app.common.utility import generate_request_id

class VideoService:
    def __init__(self):
        self.config = Config()
        self.sadtalker_path = self.config.sadtalker_path
        self.video_assets_path = self.config.video_assets_path
        
        # Create video assets directory if it doesn't exist
        os.makedirs(self.video_assets_path, exist_ok=True)
        
        # Check if SadTalker exists
        if not os.path.exists(self.sadtalker_path):
            print(f"Warning: SadTalker not found at {self.sadtalker_path}")
            print("Please clone SadTalker repository to the specified path")
    
    async def generate_talking_avatar(self, image_file: bytes, audio_path: str) -> Dict[str, Any]:
        """Generate a talking avatar video using SadTalker"""
        request_id = generate_request_id(f"video_{time.time()}")
        
        try:
            # Save image file temporarily
            temp_image_path = os.path.join(self.video_assets_path, f"{request_id}.png")
            with open(temp_image_path, 'wb') as f:
                f.write(image_file)
            
            # Output video path
            output_video_path = os.path.join(self.video_assets_path, f"{request_id}.mp4")
            
            # Run SadTalker subprocess
            cmd = [
                "python", 
                os.path.join(self.sadtalker_path, "inference.py"),
                "--driven_audio", audio_path,
                "--source_image", temp_image_path,
                "--result_dir", self.video_assets_path,
                "--enhancer", "gfpgan",  # Optional face enhancer
                "--pose_style", "0",     # Pose style (0 for still)
                "--batch_size", "1",
                "--size", "256",         # Size of the generated video
                "--expression_scale", "1.0",  # Expression intensity
                "--still",                # Keep the face still
                "--preprocess", "full",  # Full face detection
                "--output_video_name", f"{request_id}.mp4"
            ]
            
            # Execute SadTalker
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.sadtalker_path,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"SadTalker error: {stderr}")
                raise HTTPException(status_code=500, detail=f"Video generation failed: {stderr}")
            
            # Check if output video exists
            if not os.path.exists(output_video_path):
                raise HTTPException(status_code=500, detail="Video generation failed: Output file not found")
            
            # Clean up temporary image file
            os.remove(temp_image_path)
            
            return {
                "video_path": output_video_path,
                "request_id": request_id
            }
        
        except Exception as e:
            # Clean up any temporary files
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
            
            raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")
    
    def get_video_path(self, video_id: str) -> str:
        """Get the path to a generated video by ID"""
        video_path = os.path.join(self.video_assets_path, f"{video_id}.mp4")
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail=f"Video not found: {video_id}")
        return video_path

# Create a singleton instance
video_service = VideoService()