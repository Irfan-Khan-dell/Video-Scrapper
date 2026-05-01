from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import re

def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch': return parse_qs(query.query).get('v', [None])[0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def get_youtube_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id: return None
        
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Priority 1: Manual English
        # Priority 2: Auto-generated English
        # Priority 3: Translation from any available language
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                # Fallback: Find the first available and translate it to 'en'
                transcript = transcript_list.filter(lambda t: True)[0].translate('en')

        transcript_data = transcript.fetch()
        return " ".join([segment['text'] for segment in transcript_data]).replace('\n', ' ')
        
    except Exception as e:
        print(f"--- DETAILED YOUTUBE ERROR ---\n{str(e)}") # Helpful for logs
        return None
