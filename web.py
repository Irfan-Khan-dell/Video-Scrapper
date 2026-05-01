import streamlit as st
import os

# --- NEW IMPORTS ---
from cloud_transcriber import get_youtube_transcript
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

# --- Main Interface ---
yt_url = st.text_input("🔗 YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")
context_url = st.text_input("📄 External Context URL (Optional):", placeholder="Link to a research paper, article, or Wikipedia page")

if st.button("Generate Notes", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar first.")
    elif not yt_url:
        st.warning("Please provide a YouTube link.")
    else:
        os.environ["GOOGLE_API_KEY"] = api_key
        
        with st.status("Processing Request...", expanded=True) as status:
            
            st.write("📥 Fetching Transcript from YouTube API...")
            # --- NEW CLOUD-NATIVE PIPELINE ---
            transcript = get_youtube_transcript(yt_url)
            
            if not transcript:
                status.update(label="Failed to fetch transcript. Video might not have closed captions enabled.", state="error")
                st.stop()

            external_text = None
            if context_url:
                st.write("🌐 Scraping external context link...")
                external_text = extract_text_from_url(context_url)

            st.write("🧠 Generating structured notes via Gemini...")
            final_notes = generate_notes(transcript, external_context=external_text)
            
            if not final_notes:
                status.update(label="Failed to generate notes.", state="error")
                st.stop()
                
            status.update(label="Extraction Complete!", state="complete", expanded=False)

        # --- Output the Results ---
        st.success("Notes successfully generated!")
        
        with st.container(border=True):
            st.markdown(final_notes)
            
        st.download_button(
            label="Download Notes (.md)",
            data=final_notes,
            file_name="video_notes.md",
            mime="text/markdown"
        )
