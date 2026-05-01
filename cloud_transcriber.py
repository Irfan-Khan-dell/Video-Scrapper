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
    
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def get_youtube_transcript(video_url):
    """
    Fetches the transcript directly from YouTube.
    Includes logic to handle auto-generated and foreign language captions.
    """
    video_id = extract_video_id(video_url)
    
    if not video_id:
        print("Error: Could not extract Video ID from URL.")
        return None
        
    try:
        # Pull the list of available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            # Step 1: Try to find ANY English transcript (manual or auto-generated)
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except:
            # Step 2: If no English, grab the first available transcript (e.g., Hindi)
            transcript = transcript_list.filter(lambda t: True)[0]
            # Translate it to English
            if transcript.language_code != 'en':
                transcript = transcript.translate('en')

        # Fetch the actual text
        transcript_data = transcript.fetch()
        full_transcript = " ".join([segment['text'] for segment in transcript_data])
        full_transcript = full_transcript.replace('\n', ' ')
        
        return full_transcript
        
    except Exception as e:
        # CRITICAL: We print the exact error to the server logs so we can read it
        print(f"--- DETAILED YOUTUBE ERROR ---")
        print(str(e))
        print("------------------------------")
        return None
