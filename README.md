# AI-Based Live Video Conferencing System

A cutting-edge AI-powered video conferencing system that enables real-time conversations with AI-generated avatars. This system combines speech recognition, natural language processing, and video generation to create an immersive communication experience.

## Features

- **AI Avatar Generation**: Create realistic video avatars for conferencing
- **Real-time Audio Processing**: Convert speech to text and process audio inputs
- **Natural Language Understanding**: Process and respond to user queries intelligently
- **Video Asset Management**: Generate and serve video content dynamically
- **Streamlit Frontend**: User-friendly interface for interaction
- **FastAPI Backend**: High-performance API services
- **Containerized Deployment**: Easy setup with Docker

## System Architecture

The system consists of three main components:

1. **Frontend (Streamlit)**: User interface for video conferencing
2. **Backend (FastAPI)**: API services for audio/video processing
3. **Nginx Proxy**: Handles routing and serves static assets

## Prerequisites

- Docker and Docker Compose
- Python 3.10+ (for local development)
- Sufficient disk space for audio/video assets

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Based-Live-Video-Conferencing
```

### 2. Environment Configuration

Create a `.env` file in the project root with the following variables:

```
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Audio Service Configuration
AUDIO_ASSETS_DIR=/app/com/mhire/app/services/audio_service/audio_assets

# Video Service Configuration
VIDEO_ASSETS_DIR=/app/com/mhire/app/services/video_service/video_assets

# Add any API keys or service credentials here
```

### 3. Build and Start the Services

```bash
docker-compose up -d --build
```

### 4. Access the Application

- Frontend UI: http://localhost:80
- API Documentation: http://localhost:80/api/docs

## Development Guide

### Project Structure

```
├── com/mhire/app/         # Main application code
│   ├── common/            # Shared utilities and helpers
│   ├── config/            # Configuration settings
│   ├── services/          # Backend services
│   │   ├── audio_service/ # Audio processing service
│   │   └── video_service/ # Video generation service
│   └── ui/                # Streamlit frontend
├── nginx/                 # Nginx configuration
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Backend service Dockerfile
└── Dockerfile.streamlit   # Frontend service Dockerfile
```

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the backend service:
   ```bash
   python -m com.mhire.app.main
   ```

3. Run the frontend service:
   ```bash
   streamlit run com/mhire/app/ui/app.py
   ```

## Troubleshooting

- **Container startup issues**: Check Docker logs with `docker-compose logs`
- **Asset loading problems**: Ensure volume mappings are correct in docker-compose.yml
- **Network connectivity**: Verify the avatar-network is properly configured

## License

[Specify your license here]

## Contributors

[List of contributors]