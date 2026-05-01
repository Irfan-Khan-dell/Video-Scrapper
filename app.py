import streamlit as st
import os

# Import the functions we built in Phases 1-4
from ingestion import download_audio
from transcription import transcribe_audio
from scraper import extract_text_from_url
from intelligence import generate_notes

# --- UI Configuration ---
st.set_page_config(page_title="AI Video Extractor", page_icon="🧠", layout="wide")

st.title("🧠 AI-Powered Video Knowledge Extractor")
st.markdown("Turn hour-long videos and external articles into structured study notes in minutes.")

# --- Sidebar for Settings ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.markdown("[Get your free API key here](https://aistudio.google.com/)")
    
    # Optional: Let the user pick the Whisper model size
    whisper_model = st.selectbox("Local Whisper Model", ["base", "tiny", "small"], index=0)

# --- Main Interface ---
yt_url = st.text_input("🔗 YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")
context_url = st.text_input("📄 External Context URL (Optional):", placeholder="Link to a research paper, article, or Wikipedia page")

if st.button("Generate Notes", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar first.")
    elif not yt_url:
        st.warning("Please provide a YouTube link.")
    else:
        # Set the API key for the LangChain script to use
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # We use st.status to show a cool progress tracker to the user
        with st.status("Processing Request...", expanded=True) as status:
            
            st.write("📥 Step 1: Downloading audio track...")
            audio_path = download_audio(yt_url)
            
            if not audio_path:
                status.update(label="Failed to download audio.", state="error")
                st.stop()

            st.write(f"🎙️ Step 2: Transcribing audio locally (Model: {whisper_model})...")
            # Note: Whisper can take a few minutes depending on hardware and video length
            transcript = transcribe_audio(audio_path, model_size=whisper_model)
            
            if not transcript:
                status.update(label="Failed to transcribe audio.", state="error")
                st.stop()

            external_text = None
            if context_url:
                st.write("🌐 Step 3: Scraping external context link...")
                external_text = extract_text_from_url(context_url)

            st.write("🧠 Step 4: Generating structured notes via Gemini...")
            final_notes = generate_notes(transcript, external_context=external_text)
            
            if not final_notes:
                status.update(label="Failed to generate notes.", state="error")
                st.stop()
                
            status.update(label="Extraction Complete!", state="complete", expanded=False)

        # --- Output the Results ---
        st.success("Notes successfully generated!")
        
        # Display the notes in a clean container
        with st.container(border=True):
            st.markdown(final_notes)
            
        # Provide a download button for the Markdown file
        st.download_button(
            label="Download Notes (.md)",
            data=final_notes,
            file_name="video_notes.md",
            mime="text/markdown"
        )