#!/usr/bin/env python3
"""
Flask Web Application for YouTube Transcript RAG System
"""

import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from backend.transcript_fetcher import fetch_transcript, save_manual_transcript
from backend.vector_store import create_vector_store
from backend.rag_engine import RAGEngine
import googleapiclient.discovery
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyCm25gJyd8DIolApx9o0lYWzZb4uE2vIb4"

def get_available_transcripts():
    """Get list of available transcript files"""
    content_dir = "content"
    if not os.path.exists(content_dir):
        return []
    
    transcripts = []
    for filename in os.listdir(content_dir):
        if filename.endswith('.txt'):
            # Use filename without extension as the display name
            display_name = filename[:-4].replace("_", " ")
            transcripts.append({
                'filename': filename[:-4],  # Remove .txt extension
                'display_name': display_name
            })
    
    return transcripts

def get_available_vector_stores():
    """Get list of available vector stores"""
    vector_dir = "vector_db"
    if not os.path.exists(vector_dir):
        return []
    
    stores = []
    for filename in os.listdir(vector_dir):
        if filename.endswith('.index'):
            base_name = filename[:-6]  # Remove .index extension
            pkl_path = os.path.join(vector_dir, f"{base_name}.pkl")
            if os.path.exists(pkl_path):
                stores.append(base_name)
    
    return stores

def fetch_playlist_videos(playlist_url: str) -> list:
    """Fetch video information from a YouTube playlist using API"""
    try:
        # Extract playlist ID
        playlist_id_match = re.search(r'list=([^&]+)', playlist_url)
        if not playlist_id_match:
            raise ValueError("Invalid playlist URL")
        
        playlist_id = playlist_id_match.group(1)
        
        # Initialize YouTube API client
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
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

@app.route('/')
def index():
    """Main page"""
    transcripts = get_available_transcripts()
    vector_stores = get_available_vector_stores()
    return render_template('index.html', transcripts=transcripts, vector_stores=vector_stores)

@app.route('/fetch_transcript', methods=['POST'])
def fetch_transcript_route():
    """Fetch transcript from YouTube URL"""
    try:
        video_url = request.form.get('video_url', '').strip()
        if not video_url:
            flash('Please provide a YouTube URL', 'error')
            return redirect(url_for('index'))
        
        # Fetch transcript with improved error handling
        result = fetch_transcript(video_url)
        
        if result['success']:
            # Create vector store automatically
            base_name = create_vector_store(result['file_path'])
            flash(f'✅ Transcript fetched and vector store created for: {result["title"]}', 'success')
        else:
            # Show error with option for manual input
            error_msg = f'❌ Failed to fetch transcript for "{result["title"] or "video"}": {result["error"]}'
            flash(error_msg, 'error')
            flash('💡 You can manually add the transcript using the "Manual Input" section below.', 'info')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'❌ Error processing video: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/fetch_playlist', methods=['POST'])
def fetch_playlist_route():
    """Fetch videos from YouTube playlist"""
    try:
        playlist_url = request.form.get('playlist_url', '').strip()
        if not playlist_url:
            flash('Please provide a YouTube playlist URL', 'error')
            return redirect(url_for('index'))
        
        # Fetch playlist videos
        videos = fetch_playlist_videos(playlist_url)
        
        success_count = 0
        error_count = 0
        
        for video in videos:
            try:
                # Fetch transcript for each video with improved error handling
                result = fetch_transcript(video['url'])
                if result['success']:
                    # Create vector store
                    create_vector_store(result['file_path'])
                    success_count += 1
                else:
                    print(f"Failed to fetch transcript for {video['title']}: {result['error']}")
                    error_count += 1
            except Exception as e:
                print(f"Error processing video {video['title']}: {e}")
                error_count += 1
                continue
        
        flash(f'Processed {success_count} videos successfully. {error_count} errors.', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error fetching playlist: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/create_vector_store', methods=['POST'])
def create_vector_store_route():
    """Create vector store from existing transcript"""
    try:
        filename = request.form.get('filename', '').strip()
        if not filename:
            flash('Please select a transcript file', 'error')
            return redirect(url_for('index'))
        
        file_path = os.path.join('content', f'{filename}.txt')
        if not os.path.exists(file_path):
            flash('Transcript file not found', 'error')
            return redirect(url_for('index'))
        
        base_name = create_vector_store(file_path)
        flash(f'Vector store created for: {base_name}', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error creating vector store: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/manual_transcript', methods=['POST'])
def manual_transcript_route():
    """Save manually provided transcript"""
    try:
        title = request.form.get('title', '').strip()
        transcript_text = request.form.get('transcript_text', '').strip()
        
        if not title or not transcript_text:
            flash('Please provide both title and transcript text', 'error')
            return redirect(url_for('index'))
        
        # Save manual transcript
        result = save_manual_transcript(title, transcript_text)
        
        if result['success']:
            # Create vector store automatically
            base_name = create_vector_store(result['file_path'])
            flash(f'✅ Manual transcript saved and vector store created for: {result["title"]}', 'success')
        else:
            flash(f'❌ Failed to save manual transcript: {result["error"]}', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'❌ Error saving manual transcript: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/ask_question', methods=['POST'])
def ask_question():
    """Ask a question about a transcript"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        selected_transcript = data.get('transcript', '').strip()
        
        if not question or not selected_transcript:
            return jsonify({'error': 'Please provide both question and transcript selection'}), 400
        
        # Check if vector store exists
        vector_stores = get_available_vector_stores()
        if selected_transcript not in vector_stores:
            return jsonify({'error': 'Vector store not found for selected transcript'}), 400
        
        # Initialize RAG engine and get answer
        rag = RAGEngine("vector_db")
        answer = rag.generate_answer(question, selected_transcript)
        
        return jsonify({
            'answer': answer,
            'transcript': selected_transcript,
            'question': question
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating answer: {str(e)}'}), 500

@app.route('/get_transcripts')
def get_transcripts():
    """API endpoint to get available transcripts"""
    transcripts = get_available_transcripts()
    vector_stores = get_available_vector_stores()
    
    # Only return transcripts that have vector stores
    available_transcripts = [t for t in transcripts if t['filename'] in vector_stores]
    
    return jsonify(available_transcripts)

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('content', exist_ok=True)
    os.makedirs('vector_db', exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=12001, debug=True)