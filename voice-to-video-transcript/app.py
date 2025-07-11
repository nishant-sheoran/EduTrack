"""
Streamlit App for Voice-to-Educational Video Generator
Transforms voice messages into animated educational videos and PDFs.
"""

import streamlit as st
import os
import tempfile
import asyncio
from pathlib import Path
from typing import Optional, Tuple
import io

# Import our modules
from transcriber import AudioTranscriber
from script_generator import ScriptGenerator
from narrator import Narrator
from animator import VideoAnimator
from pdf_generator import PDFGenerator
from video_merger import VideoMerger

# Configure Streamlit page
st.set_page_config(
    page_title="Voice to Educational Video",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'last_outputs' not in st.session_state:
    st.session_state.last_outputs = None

class VoiceToEducationalApp:
    """Main application class for the voice-to-educational-video pipeline."""
    
    def __init__(self):
        """Initialize the application with all components."""
        self.transcriber = AudioTranscriber()
        self.script_generator = ScriptGenerator()
        self.narrator = Narrator()
        self.animator = VideoAnimator()
        self.pdf_generator = PDFGenerator()
        self.video_merger = VideoMerger()
        
        # Create output directory
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    async def process_audio(self, audio_file, topic_hint: str = "") -> Tuple[str, str]:
        """
        Process audio file through the complete pipeline.
        
        Args:
            audio_file: Uploaded audio file
            topic_hint: Optional topic hint for better processing
            
        Returns:
            Tuple of (video_path, pdf_path)
        """
        with st.spinner("🎙️ Transcribing audio..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                tmp_audio.write(audio_file.read())
                audio_path = tmp_audio.name
            
            try:
                # Step 1: Transcribe audio
                transcript = await self.transcriber.transcribe(audio_path)
                st.success(f"✅ Transcription complete ({len(transcript)} characters)")
                
                # Display transcript
                with st.expander("📝 View Transcript", expanded=False):
                    st.text_area("Raw Transcript", transcript, height=200)
                
                # Step 2: Generate structured script
                with st.spinner("🧠 Generating educational script..."):
                    script_data = await self.script_generator.generate_script(
                        transcript, topic_hint
                    )
                    st.success("✅ Educational script generated")
                
                # Display script structure
                with st.expander("📚 View Educational Script", expanded=False):
                    st.json(script_data)
                
                # Step 3: Generate narration
                with st.spinner("🎵 Creating narration audio..."):
                    narration_path = await self.narrator.create_narration(
                        script_data['full_text']
                    )
                    st.success("✅ Narration audio created")
                
                # Step 4: Create animations
                with st.spinner("🎬 Generating 3Blue1Brown-style animations..."):
                    animation_path = await self.animator.create_animation(script_data)
                    st.success("✅ Animations rendered")
                
                # Step 5: Merge video and audio
                with st.spinner("🎞️ Combining audio and visuals..."):
                    final_video_path = await self.video_merger.merge_audio_video(
                        animation_path, narration_path
                    )
                    st.success("✅ Final video created")
                
                # Step 6: Generate PDF
                with st.spinner("📄 Creating PDF transcript..."):
                    pdf_path = await self.pdf_generator.create_pdf(script_data)
                    st.success("✅ PDF transcript generated")
                
                return final_video_path, pdf_path
                
            finally:
                # Clean up temporary audio file
                if os.path.exists(audio_path):
                    os.unlink(audio_path)

def main():
    """Main Streamlit application."""
    st.title("🎓 Voice to Educational Video Generator")
    st.markdown("""
    Transform your voice recordings into **3Blue1Brown-style animated educational videos** and **structured PDF transcripts**.
    
    **How it works:**
    1. 🎙️ Upload an audio file with your explanation
    2. 🧠 AI converts it to a structured educational script
    3. 🎬 Creates beautiful animated visuals using Manim
    4. 📄 Generates a clean PDF transcript
    """)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key configuration
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Required for script generation and improvement"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Animation style options
        st.subheader("🎨 Animation Style")
        animation_style = st.selectbox(
            "Visual Style",
            ["3Blue1Brown", "Minimal", "Academic", "Colorful"],
            index=0
        )
        
        # Voice options
        st.subheader("🎵 Voice Options")
        voice_speed = st.slider("Narration Speed", 0.5, 2.0, 1.0, 0.1)
        voice_language = st.selectbox("Language", ["en", "es", "fr", "de", "it"], index=0)
        
        # Quality settings
        st.subheader("⚡ Quality Settings")
        video_quality = st.selectbox("Video Quality", ["720p", "1080p", "4K"], index=1)
        animation_fps = st.slider("Animation FPS", 15, 60, 30, 5)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📤 Upload Audio")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=['wav', 'mp3', 'mp4', 'm4a', 'ogg', 'flac'],
            help="Supported formats: WAV, MP3, MP4, M4A, OGG, FLAC"
        )
        
        # Topic hint
        topic_hint = st.text_input(
            "Topic Hint (Optional)",
            placeholder="e.g., Linear Algebra, Calculus, Machine Learning",
            help="Helps the AI better understand and structure your content"
        )
        
        # Processing button
        if uploaded_file is not None:
            if st.button("🚀 Generate Educational Video", type="primary", disabled=st.session_state.processing):
                if not api_key:
                    st.error("⚠️ Please provide your OpenAI API Key in the sidebar")
                else:
                    st.session_state.processing = True
                    
                    try:
                        # Initialize app
                        app = VoiceToEducationalApp()
                        
                        # Process the audio
                        video_path, pdf_path = asyncio.run(
                            app.process_audio(uploaded_file, topic_hint)
                        )
                        
                        # Store results
                        st.session_state.last_outputs = (video_path, pdf_path)
                        st.session_state.processing = False
                        
                        st.balloons()
                        st.success("🎉 **Processing Complete!** Your educational video and PDF are ready.")
                        
                    except Exception as e:
                        st.session_state.processing = False
                        st.error(f"❌ Error during processing: {str(e)}")
                        st.exception(e)
    
    with col2:
        st.header("ℹ️ About")
        st.markdown("""
        **Features:**
        - 🎙️ **Whisper** for accurate transcription
        - 🧠 **GPT-4** for educational script generation
        - 🎬 **Manim** for beautiful animations
        - 📄 **WeasyPrint** for clean PDF generation
        - 🎵 **gTTS** for natural narration
        
        **Output:**
        - High-quality educational video (MP4)
        - Structured PDF transcript
        """)
        
        # Audio file info
        if uploaded_file is not None:
            st.subheader("📁 File Info")
            st.write(f"**Name:** {uploaded_file.name}")
            st.write(f"**Size:** {len(uploaded_file.getvalue()) / 1024 / 1024:.2f} MB")
            st.write(f"**Type:** {uploaded_file.type}")
    
    # Results section
    if st.session_state.last_outputs:
        st.header("📥 Download Results")
        video_path, pdf_path = st.session_state.last_outputs
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎥 Educational Video")
            if os.path.exists(video_path):
                # Display video
                st.video(video_path)
                
                # Download button
                with open(video_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Video (MP4)",
                        data=file.read(),
                        file_name=os.path.basename(video_path),
                        mime="video/mp4"
                    )
        
        with col2:
            st.subheader("📄 PDF Transcript")
            if os.path.exists(pdf_path):
                # Display PDF info
                st.write(f"**File:** {os.path.basename(pdf_path)}")
                st.write(f"**Size:** {os.path.getsize(pdf_path) / 1024:.1f} KB")
                
                # Download button
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=file.read(),
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Built with ❤️ using Streamlit, OpenAI, Manim, and other open-source tools
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
