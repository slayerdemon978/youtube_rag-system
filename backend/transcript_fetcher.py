import os
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import googleapiclient.discovery

def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If no pattern matches, assume the input is already a video ID
    if len(url) == 11 and url.isalnum():
        return url
    
    raise ValueError(f"Could not extract video ID from URL: {url}")

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system storage"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and replace with underscores
    filename = re.sub(r'\s+', '_', filename)
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename

def get_video_title_fallback(video_id: str) -> str:
    """Get video title using multiple fallback methods"""
    try:
        # Method 1: Try pytube
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        return yt.title
    except Exception as e:
        print(f"⚠️ Pytube failed: {e}")
    
    try:
        # Method 2: Try direct web scraping
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}", timeout=10)
        title_match = re.search(r'<title>(.+?) - YouTube</title>', response.text)
        if title_match:
            return title_match.group(1)
    except Exception as e:
        print(f"⚠️ Web scraping failed: {e}")
    
    # Method 3: Fallback to video ID
    return f"Video_{video_id}"

def fetch_transcript(video_url: str, save_dir: str = "content") -> dict:
    """
    Fetch transcript from YouTube video with multiple fallback methods
    Returns: dict with 'success', 'file_path', 'title', 'error' keys
    """
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        # Extract video ID
        video_id = extract_video_id(video_url)
        print(f"📹 Video ID: {video_id}")
        
        # Get video title with fallbacks
        video_title = get_video_title_fallback(video_id)
        print(f"📝 Video Title: {video_title}")
        
        # Sanitize title for filename
        safe_title = sanitize_filename(video_title)
        file_path = os.path.join(save_dir, f"{safe_title}.txt")
        
        # Try to get transcript with multiple methods
        transcript_text = None
        error_messages = []
        
        # Method 1: Try youtube-transcript-api with different language codes
        language_codes = ['en', 'en-US', 'en-GB', 'auto']
        for lang in language_codes:
            try:
                if lang == 'auto':
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                else:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                
                transcript_text = "\n".join([line['text'] for line in transcript])
                print(f"✅ Transcript fetched using language: {lang}")
                break
            except Exception as e:
                error_messages.append(f"Language {lang}: {str(e)}")
                continue
        
        # Method 2: Try getting any available transcript
        if not transcript_text:
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                for transcript in transcript_list:
                    try:
                        transcript_data = transcript.fetch()
                        transcript_text = "\n".join([line['text'] for line in transcript_data])
                        print(f"✅ Transcript fetched using available language: {transcript.language}")
                        break
                    except Exception as e:
                        error_messages.append(f"Available transcript: {str(e)}")
                        continue
            except Exception as e:
                error_messages.append(f"List transcripts: {str(e)}")
        
        if transcript_text:
            # Save transcript
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)
            
            print(f"✅ Transcript saved: {file_path}")
            return {
                'success': True,
                'file_path': file_path,
                'title': video_title,
                'video_id': video_id,
                'error': None
            }
        else:
            error_msg = "No transcript available. " + "; ".join(error_messages)
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'file_path': None,
                'title': video_title,
                'video_id': video_id,
                'error': error_msg
            }
            
    except Exception as e:
        error_msg = f"Failed to process video: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            'success': False,
            'file_path': None,
            'title': None,
            'video_id': None,
            'error': error_msg
        }

def save_manual_transcript(title: str, transcript_text: str, save_dir: str = "content") -> dict:
    """
    Save manually provided transcript
    Returns: dict with 'success', 'file_path', 'title', 'error' keys
    """
    try:
        os.makedirs(save_dir, exist_ok=True)
        
        # Sanitize title for filename
        safe_title = sanitize_filename(title)
        file_path = os.path.join(save_dir, f"{safe_title}.txt")
        
        # Save transcript
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        
        print(f"✅ Manual transcript saved: {file_path}")
        return {
            'success': True,
            'file_path': file_path,
            'title': title,
            'video_id': None,
            'error': None
        }
        
    except Exception as e:
        error_msg = f"Failed to save manual transcript: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            'success': False,
            'file_path': None,
            'title': title,
            'video_id': None,
            'error': error_msg
        }

def fetch_playlist_videos(playlist_url: str, api_key: str) -> list:
    """Fetch video information from a YouTube playlist using API"""
    try:
        # Extract playlist ID
        playlist_id_match = re.search(r'list=([^&]+)', playlist_url)
        if not playlist_id_match:
            raise ValueError("Invalid playlist URL")
        
        playlist_id = playlist_id_match.group(1)
        
        # Initialize YouTube API client
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
        
        videos = []
        next_page_token = None
        
        while True:
            # Get playlist items
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                video_info = {
                    'video_id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
                }
                videos.append(video_info)
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos
        
    except Exception as e:
        print(f"❌ Error fetching playlist: {str(e)}")
        raise

def get_available_transcripts() -> list:
    """Get list of available transcript files"""
    content_dir = "content"
    if not os.path.exists(content_dir):
        return []
    
    transcripts = []
    for filename in os.listdir(content_dir):
        if filename.endswith('.txt'):
            display_name = filename[:-4].replace("_", " ")
            transcripts.append({
                'filename': filename[:-4],  # Remove .txt extension
                'display_name': display_name
            })
    
    return transcripts