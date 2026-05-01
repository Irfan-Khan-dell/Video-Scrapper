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
            # Try English first
            transcript = transcript_list.find_transcript(['en'])
        except:
            try:
                # If that fails, try to find ANY transcript and translate
                transcript = transcript_list.find_manually_created_transcript()
            except:
                # Last resort: just get the first one available
                transcript = transcript_list.find_generated_transcript(['en'])
        
    except Exception as e:
        # CRITICAL: We print the exact error to the server logs so we can read it
        print(f"--- DETAILED YOUTUBE ERROR ---")
        print(str(e))
        print("------------------------------")
        return None
