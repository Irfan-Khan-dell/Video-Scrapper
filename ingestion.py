import os
import yt_dlp

def download_audio(youtube_url, output_folder="audio_files"):
    """
    Downloads the audio from a YouTube video and saves it as an MP3.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

   # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'extract_flat': False,
        
        # --- CLOUD DEPLOYMENT FIX ---
        # Force YouTube to treat this as a mobile app request, which bypasses 
        # most 403 Forbidden blocks on datacenter IPs.
        'extractor_args': {
            'youtube': ['player_client=android']
        }
    }

    try:
        print(f"Starting download for: {youtube_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            title = info_dict.get('title', 'video')
            print(f"Successfully downloaded audio for: {title}")
            
            # Return the expected file path
            expected_path = os.path.join(output_folder, f"{title}.mp3")
            return expected_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Test the script ---
if __name__ == "__main__":
    # Test with a short video first!
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" # First YT video ever (18 seconds)
    saved_file_path = download_audio(test_url)
    print(f"File should be saved at: {saved_file_path}")
