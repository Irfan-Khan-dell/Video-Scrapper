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
    Includes fallback logic for manual, auto-generated, and foreign language captions.
    """
    video_id = extract_video_id(video_url)
    
    if not video_id:
        print("Error: Could not extract Video ID from URL.")
        return None
        
    try:
        # Step 1: Get the list of all available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            # Step 2: Try to find a standard English transcript
            transcript = transcript_list.find_transcript(['en'])
        except:
            try:
                # Step 3: Try to find a manually created transcript in ANY language and translate to English
                transcript = transcript_list.find_manually_created_transcript().translate('en')
            except:
                # Step 4: Final fallback to auto-generated English captions
                transcript = transcript_list.find_generated_transcript(['en'])

        # Step 5: Fetch and join the text
        transcript_data = transcript.fetch()
        full_transcript = " ".join([segment['text'] for segment in transcript_data])
        return full_transcript.replace('\n', ' ')
        
    except Exception as e:
        print(f"--- DETAILED YOUTUBE ERROR ---")
        print(str(e))
        print("------------------------------")
        return None
        print("------------------------------")
        return None
