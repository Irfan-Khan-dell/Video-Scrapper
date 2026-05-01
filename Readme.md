# 🧠 AI-Powered Video Knowledge Extractor

An end-to-end AI application that transforms long YouTube videos and lectures into highly structured, actionable study notes. It uses a multi-agent architecture to extract audio, transcribe speech locally, scrape external web context, and generate comprehensive Markdown notes using Large Language Models.

---

## ✨ Features

* **YouTube Audio Ingestion:** Rapidly extracts audio tracks from any YouTube video using `yt-dlp`, minimizing bandwidth and compute requirements.
* **Local AI Transcription:** Utilizes **OpenAI's Whisper** model to run accurate, offline speech-to-text processing directly on your machine.
* **Web Context Enrichment:** Features an autonomous scraping agent that can follow external links (like research papers or Wikipedia articles) to verify facts and enrich the final notes.
* **Intelligent Summarization:** Leverages the **Gemini 1.5 API** via **LangChain** to synthesize massive transcripts into executive summaries, key concepts, and actionable insights.
* **Interactive Dashboard:** A clean, modern frontend built with **Streamlit** that allows users to process videos, track the extraction pipeline in real-time, and download the final Markdown notes.

---

## 🏗️ System Architecture

The project is built on a modular, multi-phase pipeline:

1. `ingestion.py`: Handles downloading and converting YouTube video streams to MP3 files.
2. `transcription.py`: Loads the local Whisper AI model and processes the MP3 into a raw text transcript.
3. `scraper.py`: Extracts clean, readable text from user-provided URLs using BeautifulSoup4.
4. `intelligence.py`: Orchestrates the LangChain pipeline, passing the transcript and scraped context to the Gemini API with strict formatting prompts.
5. `app.py`: The Streamlit frontend that wires all modules together into a unified user interface.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **AI & NLP:** OpenAI Whisper (Local), Google Gemini API, LangChain
* **Data Extraction:** yt-dlp, BeautifulSoup4, Requests
* **Frontend:** Streamlit

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.10 or higher** installed on your system.
2. **FFmpeg** must be installed and added to your system's PATH (required for `yt-dlp` and `whisper` to process audio files).
3. A free **Google Gemini API Key** (Get one at [Google AI Studio](https://aistudio.google.com/)).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/ai-video-extractor.git](https://github.com/yourusername/ai-video-extractor.git)
   cd ai-video-extractor