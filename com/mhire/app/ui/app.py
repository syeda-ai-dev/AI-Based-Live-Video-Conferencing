import os
import time
import streamlit as st
import requests
import tempfile
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="AI Avatar Conversation",
    page_icon="🎭",
    layout="wide"
)

# API endpoints
API_BASE_URL = "http://localhost:8000/api/v1"
TRANSCRIBE_ENDPOINT = f"{API_BASE_URL}/audio/transcribe"
SPEAK_ENDPOINT = f"{API_BASE_URL}/audio/speak"
GENERATE_VIDEO_ENDPOINT = f"{API_BASE_URL}/video/generate"

# Initialize session state
if 'avatar_image' not in st.session_state:
    st.session_state.avatar_image = None
if 'generated_video' not in st.session_state:
    st.session_state.generated_video = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# App title and description
st.title("AI Avatar Conversation")
st.markdown("Have a live conversation with an AI-powered avatar that responds with lip-synced video.")

# Sidebar for avatar selection and settings
with st.sidebar:
    st.header("Avatar Settings")
    
    # Avatar image upload
    uploaded_file = st.file_uploader("Upload Avatar Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Avatar", use_column_width=True)
        
        # Save the image to session state
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        st.session_state.avatar_image = img_bytes.getvalue()
    
    # Voice selection
    voice_option = st.selectbox(
        "Select Voice",
        options=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        index=0
    )
    
    # Use Groq API or local fallback
    use_groq = st.checkbox("Use Groq API (recommended)", value=True)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "This application uses SadTalker for video generation and Groq APIs for "
        "text-to-speech and speech-to-text processing."
    )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Your Input")
    
    # Text input option
    text_input = st.text_area("Type your message", height=100)
    
    # Audio input option (for future implementation)
    st.markdown("Or record your voice (coming soon)")
    
    # Submit button
    if st.button("Generate Response"):
        if not st.session_state.avatar_image:
            st.error("Please upload an avatar image first!")
        elif not text_input.strip():
            st.error("Please enter a message!")
        else:
            with st.spinner("Generating response..."):
                try:
                    # Step 1: Generate speech from text
                    files = {
                        'text': (None, text_input),
                        'voice': (None, voice_option)
                    }
                    
                    tts_response = requests.post(SPEAK_ENDPOINT, files=files)
                    if tts_response.status_code != 200:
                        st.error(f"Error generating speech: {tts_response.text}")
                    else:
                        tts_result = tts_response.json()["data"]
                        audio_path = tts_result["audio_path"]
                        
                        # Step 2: Generate video with the avatar
                        files = {
                            'image': ('avatar.png', st.session_state.avatar_image, 'image/png'),
                            'audio_path': (None, audio_path)
                        }
                        
                        video_response = requests.post(GENERATE_VIDEO_ENDPOINT, files=files)
                        if video_response.status_code != 200:
                            st.error(f"Error generating video: {video_response.text}")
                        else:
                            video_result = video_response.json()["data"]
                            video_path = video_result["video_path"]
                            
                            # Save to session state
                            st.session_state.generated_video = video_path
                            
                            # Add to conversation history
                            st.session_state.conversation_history.append({
                                "user_input": text_input,
                                "video_path": video_path,
                                "timestamp": time.time()
                            })
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with col2:
    st.header("AI Avatar Response")
    
    # Display the generated video if available
    if st.session_state.generated_video and os.path.exists(st.session_state.generated_video):
        # Convert server path to web path
        video_filename = os.path.basename(st.session_state.generated_video)
        video_url = f"/video-assets/{video_filename}"
        
        # Display video
        st.video(video_url)
    else:
        st.info("Avatar response will appear here after you submit a message.")

# Conversation history
st.header("Conversation History")
if not st.session_state.conversation_history:
    st.info("Your conversation history will appear here.")
else:
    for i, entry in enumerate(reversed(st.session_state.conversation_history)):
        with st.expander(f"Conversation {len(st.session_state.conversation_history) - i}", expanded=(i == 0)):
            st.markdown(f"**You said:** {entry['user_input']}")
            
            # Convert server path to web path
            video_filename = os.path.basename(entry['video_path'])
            video_url = f"/video-assets/{video_filename}"
            
            st.video(video_url)