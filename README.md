# 🎥 YouTube Transcript RAG System

A powerful **Retrieval-Augmented Generation (RAG)** system that fetches YouTube video transcripts and enables intelligent Q&A using AI. Built with Flask, FAISS, and Transformers for CPU-only operation.

## 🌟 Features

- **📥 Robust Transcript Fetching**: Multiple fallback methods for YouTube transcript retrieval
- **📝 Manual Transcript Input**: Add transcripts manually when automatic fetching fails
- **📋 Playlist Support**: Fetch transcripts from entire YouTube playlists using YouTube API
- **🔍 Vector Search**: Create FAISS vector stores for semantic search
- **🤖 AI Q&A**: Ask questions about video content using Microsoft Phi-2 model
- **🌐 Enhanced Web Interface**: Beautiful, responsive Flask web application with error handling
- **💻 CPU Only**: No GPU required - runs on any machine
- **📱 Mobile Friendly**: Responsive design works on all devices
- **🛡️ Error Recovery**: Graceful handling of transcript failures with manual input option
- **🌍 Multi-Language Support**: Automatic detection and fallback for different transcript languages

## 🏗️ Project Structure

```
youtube_rag-system/
├── main.py                 # CLI interface
├── app.py                  # Flask web application
├── backend/
│   ├── transcript_fetcher.py  # YouTube transcript fetching
│   ├── vector_store.py        # FAISS vector database
│   └── rag_engine.py          # RAG question-answering
├── content/                   # Stores transcript files (.txt)
├── vector_db/                 # FAISS vector databases
├── static/
│   └── style.css             # Web interface styling
├── templates/
│   └── index.html            # Web interface template
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🚀 Quick Start (Recommended: Virtual Environment)

### 1. Clone the Repository

```bash
git clone https://github.com/slayerdemon978/youtube_rag-system.git
cd youtube_rag-system
```

### 2. Create and Activate Virtual Environment

**For Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv youtube_rag_env

# Activate virtual environment
source youtube_rag_env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

**For Windows:**
```cmd
# Create virtual environment
python -m venv youtube_rag_env

# Activate virtual environment
youtube_rag_env\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Note:** The first installation may take 5-10 minutes as it downloads AI models and dependencies.

### 4. Run the Web Application

```bash
python app.py
```

The application will be available at `http://localhost:12001`

### 5. Alternative: Use CLI Interface

```bash
python main.py
```

### 6. Deactivate Virtual Environment (When Done)

```bash
deactivate
```

## 🔄 Alternative Installation Methods

### Option 1: System-wide Installation (Not Recommended)

**For Linux/Mac:**
```bash
pip install -r requirements.txt
```

**For Windows:**
```cmd
# Use the automated fix script
python fix_windows_install.py

# Or manual installation with --user flag
pip install --user -r requirements.txt
```

### Option 2: Windows-Specific Tools

**Windows Users:** If you encounter permission errors, see [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed troubleshooting and additional installation methods.

## 📖 Usage Guide

### Web Interface

1. **Fetch Single Video**:
   - Enter a YouTube URL in the "Fetch Transcript" section
   - Click "Fetch Transcript" - this automatically creates a vector store
   - If fetching fails, you'll see an error message with manual input suggestion

2. **Manual Transcript Input** (New Feature):
   - Use this when automatic fetching fails
   - Enter the video title and paste the transcript text
   - Click "Save Manual Transcript" - automatically creates a vector store
   - Perfect for private videos, restricted content, or when API limits are reached

3. **Fetch Playlist** (YouTube API):
   - Enter a YouTube playlist URL
   - The system will fetch all videos in the playlist
   - Failed videos are logged, successful ones are processed

4. **Ask Questions**:
   - Select a transcript from the dropdown
   - Type your question in the text area
   - Click "Ask Question" to get AI-powered answers

### CLI Interface

The CLI provides a menu-driven interface for:
- Fetching transcripts from URLs
- Creating vector stores manually
- Querying transcripts
- Listing available data

## 🔧 Configuration

### YouTube API Setup

The system includes YouTube API integration for playlist fetching. The API key is already configured in the code:

```python
YOUTUBE_API_KEY = "AIzaSyCm25gJyd8DIolApx9o0lYWzZb4uE2vIb4"
```

### Model Configuration

The system uses these models by default:
- **Embeddings**: `all-MiniLM-L6-v2` (SentenceTransformers)
- **Language Model**: `microsoft/phi-2` (Transformers)

## 🛠️ Technical Details

### How It Works

1. **Transcript Extraction**: Uses `youtube-transcript-api` and `pytube` to fetch video transcripts
2. **Text Chunking**: Splits transcripts into 500-character chunks with 50-character overlap
3. **Vector Embeddings**: Creates semantic embeddings using SentenceTransformers
4. **Vector Storage**: Stores embeddings in FAISS for fast similarity search
5. **Question Answering**: Uses retrieved context with Phi-2 model for answer generation

### Key Components

- **Flask Web App**: Modern, responsive web interface
- **FAISS Vector DB**: Fast similarity search for relevant transcript chunks
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate answers
- **YouTube API**: Automated playlist processing

## 📋 Requirements

### System Requirements
- Python 3.8+
- 4GB+ RAM (for model loading)
- Internet connection (for downloading models and fetching videos)

### Python Dependencies
- Flask 2.3.3
- youtube-transcript-api 0.6.1
- pytube 15.0.0
- sentence-transformers 2.2.2
- faiss-cpu 1.7.4
- langchain 0.0.350
- transformers 4.35.2
- torch 2.1.1
- google-api-python-client 2.108.0

## 🛡️ Why Use Virtual Environment?

**Virtual environments are strongly recommended because they:**

- ✅ **Isolate Dependencies**: Prevent conflicts with other Python projects
- ✅ **Easy Cleanup**: Simply delete the folder to remove everything
- ✅ **Reproducible**: Ensure consistent behavior across different machines
- ✅ **Safe Installation**: No risk of breaking system Python packages
- ✅ **Version Control**: Lock specific package versions for stability

**Virtual Environment Commands Quick Reference:**

```bash
# Create (one time only)
python -m venv youtube_rag_env

# Activate (every time you work on the project)
source youtube_rag_env/bin/activate  # Linux/Mac
youtube_rag_env\Scripts\activate     # Windows

# Install packages (after activation)
pip install -r requirements.txt

# Run the application (after activation)
python app.py

# Deactivate (when done working)
deactivate
```

## 🎯 Use Cases

- **Educational Content**: Ask questions about lecture videos
- **Tutorial Analysis**: Get specific information from how-to videos
- **Research**: Extract insights from documentary content
- **Content Creation**: Analyze competitor videos for ideas
- **Accessibility**: Make video content searchable and accessible

## 🔍 Example Queries

Once you have transcripts loaded, you can ask questions like:

- "What are the main points discussed in this video?"
- "How does the speaker explain [specific concept]?"
- "What examples are given for [topic]?"
- "What is the conclusion of this presentation?"
- "Can you summarize the key takeaways?"

## 🚨 Troubleshooting

> **💡 Important**: If you used a virtual environment for installation, make sure to activate it before running any commands:
> ```bash
> source youtube_rag_env/bin/activate  # Linux/Mac
> youtube_rag_env\Scripts\activate     # Windows
> ```

### Common Issues

1. **Module Not Found Errors** (Most Common):
   ```bash
   # SOLUTION: Use virtual environment (recommended)
   python -m venv youtube_rag_env
   source youtube_rag_env/bin/activate  # Linux/Mac
   youtube_rag_env\Scripts\activate     # Windows
   pip install -r requirements.txt
   python app.py
   ```

2. **Windows Installation Errors**:
   - **First try**: Use virtual environment (solution above)
   - **Alternative**: Use `python fix_windows_install.py` for automated fixes
   - **Last resort**: Run Command Prompt as Administrator
   - **Detailed help**: See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for comprehensive solutions

3. **Permission Errors**:
   ```bash
   # SOLUTION: Virtual environment avoids permission issues
   python -m venv youtube_rag_env
   # Then activate and install as shown above
   
   # Alternative: Use --user flag (not recommended)
   pip install --user package_name
   ```

4. **Transcript Fetching Issues** (Enhanced Error Handling):
   - **Automatic Retry**: System tries multiple methods and languages
   - **Manual Input**: Use the "Manual Transcript Input" section when automatic fetching fails
   - **Common Causes**: Private videos, disabled captions, region restrictions
   - **Solution**: Copy transcript manually from YouTube and paste into the manual input form
   - **Tip**: Look for the "Show transcript" button on YouTube videos

5. **Model Loading Slow**:
   - First-time model download can take several minutes
   - Models are cached locally after first use

6. **Memory Issues**:
   - Ensure you have at least 4GB RAM available
   - Close other applications if needed

7. **API Errors**:
   - Check internet connection
   - Verify YouTube URLs are valid and public

### Error Messages

- `❌ Error fetching transcript`: Video has no available transcript
- `❌ Error creating vector store`: Issue with text processing or model loading
- `❌ Error generating answer`: Problem with the language model

## 📋 How to Get Transcripts Manually from YouTube

When automatic transcript fetching fails, you can manually extract transcripts:

### Method 1: YouTube Web Interface
1. **Open the video** on YouTube
2. **Click the "..." menu** below the video
3. **Select "Show transcript"** from the dropdown
4. **Copy the transcript text** (you can click the toggle to remove timestamps)
5. **Paste into the "Manual Transcript Input"** section in the web app

### Method 2: YouTube Mobile App
1. **Open the video** in the YouTube mobile app
2. **Tap the video description** to expand it
3. **Look for "Show transcript"** option
4. **Copy the text** and paste into the web app

### Method 3: Browser Extensions
- Use browser extensions like "YouTube Transcript" for easier copying
- These extensions can format transcripts automatically

### Tips for Manual Input:
- ✅ **Remove timestamps** if present (the system handles plain text better)
- ✅ **Use descriptive titles** for easy identification
- ✅ **Include speaker names** if it's a multi-person discussion
- ✅ **Clean up obvious transcription errors** if you notice them

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **YouTube Transcript API**: For transcript extraction
- **Hugging Face**: For transformer models and embeddings
- **FAISS**: For efficient vector similarity search
- **Flask**: For the web framework
- **Google**: For YouTube API access

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Review the code documentation

---

**Made with ❤️ for the AI and education community**
