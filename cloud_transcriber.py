from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import re

def extract_video_id(url):
    """Extracts the 11-character video ID from various YouTube URL formats."""
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p.get('v', [None])[0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    
    # Fallback regex for tricky URLs
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def get_youtube_transcript(video_url):
    """
    Fetches the transcript directly from YouTube's subtitle API.
    """
    video_id = extract_video_id(video_url)
    
    if not video_id:
        print("Error: Could not extract Video ID from URL.")
        return None
        
    try:
        # Fetch the transcript list for the video
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all the text blocks into one giant string
        full_transcript = " ".join([segment['text'] for segment in transcript_list])
        
        # Clean up any weird formatting
        full_transcript = full_transcript.replace('\n', ' ')
        
        return full_transcript
        
    except Exception as e:
        print(f"Failed to fetch transcript: {e}")
        return None
