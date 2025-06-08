import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import googleapiclient.discovery

def fetch_transcript(video_url: str, save_dir: str = "content") -> str:
    os.makedirs(save_dir, exist_ok=True)

    yt = YouTube(video_url)
    video_id = yt.video_id
    video_title = yt.title.replace("/", "_").replace("\\", "_").replace(" ", "_")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    full_text = "\n".join([line['text'] for line in transcript])
    file_path = os.path.join(save_dir, f"{video_title}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Transcript saved: {file_path}")
    return file_path

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