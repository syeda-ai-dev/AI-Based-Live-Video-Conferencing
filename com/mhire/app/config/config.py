import os
from dotenv import load_dotenv
            
load_dotenv()

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # Groq API configuration
            cls._instance.groq_api_key = os.getenv("GROQ_API_KEY", "")
            cls._instance.groq_tts_model = os.getenv("GROQ_TTS_MODEL", "mixtral-8x7b-32768")
            cls._instance.groq_stt_model = os.getenv("GROQ_STT_MODEL", "whisper-large-v3")
            
            # SadTalker configuration
            cls._instance.sadtalker_path = os.getenv("SADTALKER_PATH", "./com/mhire/app/services/video_service/video_assets/SadTalker")
            
            # File paths configuration
            cls._instance.audio_assets_path = os.getenv("AUDIO_ASSETS_PATH", "./com/mhire/app/services/audio_service/audio_assets")
            cls._instance.video_assets_path = os.getenv("VIDEO_ASSETS_PATH", "./com/mhire/app/services/video_service/video_assets")
            cls._instance.ui_assets_path = os.getenv("UI_ASSETS_PATH", "./com/mhire/app/ui/app_assets")
            
            # API configuration
            cls._instance.api_version = os.getenv("API_VERSION", "v1")
            cls._instance.api_prefix = f"/api/{cls._instance.api_version}"
            
            # Silero models (fallback)
            cls._instance.silero_encoder_path = os.path.join(cls._instance.audio_assets_path, "silero_encoder_v5.onnx")
            cls._instance.silero_decoder_path = os.path.join(cls._instance.audio_assets_path, "silero_decoder_v5.onnx")

        return cls._instance