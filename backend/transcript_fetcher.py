import os
import re
import requests
import time
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from pytube import YouTube
import googleapiclient.discovery
from urllib.parse import urlparse, parse_qs
import json

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
    methods_tried = []
    
    # Method 1: Try pytube with retry
    for attempt in range(2):
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            title = yt.title
            if title and title.strip():
                print(f"✅ Title fetched via pytube: {title}")
                return title.strip()
        except Exception as e:
            methods_tried.append(f"Pytube attempt {attempt + 1}: {str(e)}")
            if attempt == 0:
                time.sleep(1)  # Brief pause before retry
    
    # Method 2: Try direct web scraping with multiple patterns
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}", 
                              headers=headers, timeout=15)
        
        # Try multiple title extraction patterns
        title_patterns = [
            r'<title>(.+?) - YouTube</title>',
            r'"title":"([^"]+)"',
            r'<meta property="og:title" content="([^"]+)"',
            r'<meta name="title" content="([^"]+)"'
        ]
        
        for pattern in title_patterns:
            title_match = re.search(pattern, response.text)
            if title_match:
                title = title_match.group(1)
                # Clean up HTML entities
                title = title.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                if title and title.strip():
                    print(f"✅ Title fetched via web scraping: {title}")
                    return title.strip()
                    
    except Exception as e:
        methods_tried.append(f"Web scraping: {str(e)}")
    
    # Method 3: Try extracting from JSON-LD data
    try:
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}", 
                              headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        
        # Look for JSON-LD structured data
        json_ld_match = re.search(r'<script type="application/ld\+json">(.+?)</script>', response.text, re.DOTALL)
        if json_ld_match:
            json_data = json.loads(json_ld_match.group(1))
            if isinstance(json_data, list):
                for item in json_data:
                    if item.get('@type') == 'VideoObject' and 'name' in item:
                        title = item['name']
                        if title and title.strip():
                            print(f"✅ Title fetched via JSON-LD: {title}")
                            return title.strip()
            elif json_data.get('@type') == 'VideoObject' and 'name' in json_data:
                title = json_data['name']
                if title and title.strip():
                    print(f"✅ Title fetched via JSON-LD: {title}")
                    return title.strip()
                    
    except Exception as e:
        methods_tried.append(f"JSON-LD extraction: {str(e)}")
    
    # Method 4: Fallback to video ID with warning
    print(f"⚠️ All title extraction methods failed: {'; '.join(methods_tried)}")
    return f"Video_{video_id}"

def fetch_transcript(video_url: str, save_dir: str = "content") -> dict:
    """
    Fetch transcript from YouTube video with multiple fallback methods
    Returns: dict with 'success', 'file_path', 'title', 'error', 'suggestions' keys
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
        
        # Check if transcript already exists
        if os.path.exists(file_path):
            print(f"ℹ️ Transcript already exists: {file_path}")
            return {
                'success': True,
                'file_path': file_path,
                'title': video_title,
                'video_id': video_id,
                'error': None,
                'suggestions': []
            }
        
        # Try to get transcript with multiple methods
        transcript_text = None
        error_messages = []
        suggestions = []
        
        # Method 1: Try youtube-transcript-api with different language codes and retry
        language_codes = ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU', 'auto']
        for lang in language_codes:
            for attempt in range(2):  # Retry each language
                try:
                    if lang == 'auto':
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    else:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                    
                    transcript_text = "\n".join([line['text'] for line in transcript])
                    print(f"✅ Transcript fetched using language: {lang} (attempt {attempt + 1})")
                    break
                except TranscriptsDisabled:
                    error_messages.append(f"Transcripts are disabled for this video")
                    suggestions.append("This video has transcripts disabled by the creator")
                    break
                except NoTranscriptFound:
                    error_messages.append(f"No transcript found for language {lang}")
                    continue
                except Exception as e:
                    error_messages.append(f"Language {lang} attempt {attempt + 1}: {str(e)}")
                    if attempt == 0:
                        time.sleep(1)  # Brief pause before retry
                    continue
            
            if transcript_text:
                break
        
        # Method 2: Try getting any available transcript with detailed language detection
        if not transcript_text:
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                available_languages = []
                
                for transcript in transcript_list:
                    available_languages.append(f"{transcript.language} ({transcript.language_code})")
                    try:
                        transcript_data = transcript.fetch()
                        transcript_text = "\n".join([line['text'] for line in transcript_data])
                        print(f"✅ Transcript fetched using available language: {transcript.language}")
                        break
                    except Exception as e:
                        error_messages.append(f"Available transcript {transcript.language}: {str(e)}")
                        continue
                
                if available_languages:
                    suggestions.append(f"Available languages: {', '.join(available_languages)}")
                    
            except TranscriptsDisabled:
                error_messages.append("Transcripts are disabled for this video")
                suggestions.append("The video creator has disabled transcripts for this video")
            except Exception as e:
                error_messages.append(f"List transcripts: {str(e)}")
        
        # Method 3: Try alternative transcript extraction methods
        if not transcript_text:
            try:
                # Try with different transcript types (manual, auto-generated)
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                for transcript in transcript_list:
                    if transcript.is_generated:
                        try:
                            transcript_data = transcript.fetch()
                            transcript_text = "\n".join([line['text'] for line in transcript_data])
                            print(f"✅ Auto-generated transcript fetched: {transcript.language}")
                            suggestions.append("Used auto-generated transcript (may have lower accuracy)")
                            break
                        except Exception as e:
                            error_messages.append(f"Auto-generated transcript: {str(e)}")
                            continue
            except Exception as e:
                error_messages.append(f"Alternative methods: {str(e)}")
        
        if transcript_text:
            # Clean and validate transcript
            transcript_text = transcript_text.strip()
            if len(transcript_text) < 50:  # Very short transcript might be invalid
                suggestions.append("Transcript seems very short - please verify content quality")
            
            # Save transcript
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)
            
            print(f"✅ Transcript saved: {file_path}")
            return {
                'success': True,
                'file_path': file_path,
                'title': video_title,
                'video_id': video_id,
                'error': None,
                'suggestions': suggestions
            }
        else:
            # Provide helpful suggestions for manual input
            suggestions.extend([
                "Try using the 'Manual Transcript Input' section below",
                "Check if the video has captions enabled on YouTube",
                "Look for the 'Show transcript' option in the video description on YouTube",
                "Some videos may have transcripts in languages other than English"
            ])
            
            error_msg = "No transcript available. " + "; ".join(error_messages[:3])  # Limit error message length
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'file_path': None,
                'title': video_title,
                'video_id': video_id,
                'error': error_msg,
                'suggestions': suggestions
            }
            
    except Exception as e:
        error_msg = f"Failed to process video: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            'success': False,
            'file_path': None,
            'title': None,
            'video_id': None,
            'error': error_msg,
            'suggestions': [
                "Check if the YouTube URL is valid and accessible",
                "Try using the 'Manual Transcript Input' section",
                "Ensure you have a stable internet connection"
            ]
        }

def save_manual_transcript(title: str, transcript_text: str, save_dir: str = "content") -> dict:
    """
    Save manually provided transcript with validation and cleaning
    Returns: dict with 'success', 'file_path', 'title', 'error', 'warnings' keys
    """
    try:
        os.makedirs(save_dir, exist_ok=True)
        
        # Validate inputs
        if not title or not title.strip():
            return {
                'success': False,
                'file_path': None,
                'title': title,
                'video_id': None,
                'error': "Title cannot be empty",
                'warnings': []
            }
        
        if not transcript_text or not transcript_text.strip():
            return {
                'success': False,
                'file_path': None,
                'title': title,
                'video_id': None,
                'error': "Transcript text cannot be empty",
                'warnings': []
            }
        
        # Clean and validate transcript text
        cleaned_text = transcript_text.strip()
        warnings = []
        
        # Remove common timestamp patterns if present
        timestamp_patterns = [
            r'\d{1,2}:\d{2}:\d{2}',  # HH:MM:SS
            r'\d{1,2}:\d{2}',        # MM:SS
            r'\[\d{1,2}:\d{2}:\d{2}\]',  # [HH:MM:SS]
            r'\(\d{1,2}:\d{2}:\d{2}\)',  # (HH:MM:SS)
        ]
        
        original_length = len(cleaned_text)
        for pattern in timestamp_patterns:
            cleaned_text = re.sub(pattern, '', cleaned_text)
        
        if len(cleaned_text) < original_length * 0.8:
            warnings.append("Removed many timestamps - please verify transcript quality")
        
        # Clean up extra whitespace
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)  # Multiple newlines to double
        cleaned_text = re.sub(r' +', ' ', cleaned_text)  # Multiple spaces to single
        cleaned_text = cleaned_text.strip()
        
        # Validate final content
        if len(cleaned_text) < 50:
            warnings.append("Transcript seems very short - please verify content")
        
        if len(cleaned_text.split()) < 10:
            warnings.append("Transcript has very few words - please verify content")
        
        # Sanitize title for filename
        safe_title = sanitize_filename(title.strip())
        file_path = os.path.join(save_dir, f"{safe_title}.txt")
        
        # Check if file already exists
        if os.path.exists(file_path):
            warnings.append(f"File already exists and will be overwritten: {safe_title}.txt")
        
        # Save transcript
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        
        print(f"✅ Manual transcript saved: {file_path}")
        if warnings:
            print(f"⚠️ Warnings: {'; '.join(warnings)}")
        
        return {
            'success': True,
            'file_path': file_path,
            'title': title.strip(),
            'video_id': None,
            'error': None,
            'warnings': warnings
        }
        
    except Exception as e:
        error_msg = f"Failed to save manual transcript: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            'success': False,
            'file_path': None,
            'title': title,
            'video_id': None,
            'error': error_msg,
            'warnings': []
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