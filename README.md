# 🎥 YouTube Transcript RAG System

A powerful **Retrieval-Augmented Generation (RAG)** system that fetches YouTube video transcripts and enables intelligent Q&A using AI. Built with Flask, FAISS, and Transformers for CPU-only operation.

## 🌟 Features

### 🚀 **Enhanced Transcript Fetching (v2.0)**
- **📥 Advanced Fallback System**: Multiple robust methods for YouTube transcript retrieval
- **🔄 Intelligent Retry Logic**: Automatic retries with different languages and methods
- **🌍 Multi-Language Support**: Supports English variants (US, UK, CA, AU) and auto-detection
- **⚡ Smart Error Handling**: Detailed error messages with helpful suggestions
- **🛡️ Graceful Degradation**: Falls back to manual input when automatic fetching fails

### 📝 **Improved Manual Input System**
- **🧹 Automatic Text Cleaning**: Removes timestamps and cleans formatting automatically
- **✅ Input Validation**: Validates transcript quality and provides warnings
- **📊 Content Analysis**: Checks transcript length and word count for quality assurance
- **🔄 Duplicate Detection**: Warns when overwriting existing transcripts

### 🎯 **Smart Web Interface**
- **📋 Playlist Support**: Fetch transcripts from entire YouTube playlists using YouTube API
- **🔍 Vector Search**: Create FAISS vector stores for semantic search
- **🤖 AI Q&A**: Ask questions about video content using Microsoft Phi-2 model
- **🌐 Enhanced Web Interface**: Beautiful, responsive Flask web application
- **💻 CPU Only**: No GPU required - runs on any machine
- **📱 Mobile Friendly**: Responsive design works on all devices

### 🛠️ **Advanced Error Recovery**
- **💡 Contextual Suggestions**: Provides specific suggestions based on error type
- **🔧 Multiple Flash Message Types**: Success, error, warning, and info messages
- **📈 Progress Tracking**: Shows detailed progress for playlist processing
- **🎯 Targeted Help**: Specific guidance for different failure scenarios

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

### 🌐 Web Interface

#### 1. **Enhanced Single Video Fetching**:
   - Enter a YouTube URL in the "Fetch Transcript" section
   - Click "Fetch Transcript" - the system will:
     - Try multiple languages (English variants + auto-detection)
     - Retry failed attempts automatically
     - Show detailed progress and suggestions
     - Automatically create a vector store on success
   - If fetching fails, you'll see:
     - Specific error messages explaining why it failed
     - Helpful suggestions for manual input
     - Available language information (if any)

#### 2. **Improved Manual Transcript Input**:
   - **When to use**: Automatic fetching fails, private videos, restricted content
   - **Features**:
     - Automatic timestamp removal (detects patterns like `00:01:30`)
     - Text quality validation and warnings
     - Duplicate file detection
     - Automatic vector store creation
   - **How to use**:
     - Enter a descriptive video title
     - Paste the transcript text (timestamps will be cleaned automatically)
     - Click "Save Manual Transcript"
     - System provides warnings for quality issues

#### 3. **Smart Playlist Processing**:
   - Enter a YouTube playlist URL
   - The system will:
     - Fetch all videos in the playlist using YouTube API
     - Process each video with enhanced error handling
     - Show detailed progress (success/failure counts)
     - Continue processing even if some videos fail
     - Provide summary of results

#### 4. **Intelligent Q&A System**:
   - Select a transcript from the dropdown (only shows transcripts with vector stores)
   - Type your question in the text area
   - Click "Ask Question" to get AI-powered answers
   - View question history and previous answers

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

4. **Enhanced Transcript Fetching Issues** (v2.0 Improvements):
   - **🔄 Automatic Retry System**: Tries multiple methods, languages, and transcript types
   - **🎯 Smart Error Detection**: Identifies specific issues (disabled transcripts, language mismatches)
   - **💡 Contextual Suggestions**: Provides specific guidance based on the error type
   - **🌍 Language Support**: Attempts English variants (US, UK, CA, AU) and auto-generated transcripts
   - **📝 Manual Input Guidance**: Step-by-step instructions for manual transcript extraction
   - **⚠️ Quality Warnings**: Alerts for short transcripts, timestamp issues, or formatting problems
   
   **Common Error Types & Solutions**:
   - `TranscriptsDisabled`: Video creator disabled transcripts → Use manual input
   - `NoTranscriptFound`: No transcript in requested language → Try different language or manual input
   - `Private/Restricted Video`: Video not accessible → Use manual input with copied transcript
   - `Network Issues`: Connection problems → Check internet and retry
   - `Very Short Transcript`: Quality warning → Verify content completeness

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

## 🆕 What's New in v2.0

### 🚀 **Major Improvements**

#### **Enhanced Transcript Fetching**
- **Multi-Language Retry System**: Automatically tries English variants (US, UK, CA, AU) and auto-detection
- **Intelligent Error Handling**: Specific error detection for disabled transcripts, language issues, etc.
- **Smart Fallback Logic**: Tries manual transcripts, auto-generated transcripts, and different transcript types
- **Detailed Progress Feedback**: Shows exactly what the system is trying and why it failed

#### **Improved Manual Input**
- **Automatic Text Cleaning**: Removes timestamps automatically using pattern detection
- **Quality Validation**: Checks transcript length, word count, and content quality
- **Smart Warnings**: Alerts for potential issues like very short content or excessive timestamp removal
- **Duplicate Detection**: Warns when overwriting existing files

#### **Better User Experience**
- **Enhanced Flash Messages**: Success, error, warning, and info message types with appropriate icons
- **Contextual Help**: Specific suggestions based on the type of error encountered
- **Improved Error Recovery**: Graceful handling of failures with actionable next steps
- **Progress Tracking**: Better feedback during playlist processing

#### **Technical Improvements**
- **Robust Video ID Extraction**: Handles multiple YouTube URL formats
- **Safe Filename Generation**: Proper sanitization of video titles for file system compatibility
- **Better Exception Handling**: More specific error catching and reporting
- **Retry Logic**: Automatic retries with delays for transient failures

### 🔧 **Under the Hood**
- **Pure Python Implementation**: No direct API dependencies for transcript fetching
- **Multiple Fallback Methods**: Uses `youtube-transcript-api` and `pytube` with intelligent switching
- **Enhanced Vector Store Creation**: Automatic creation with better error handling
- **Improved Web Interface**: Better responsive design and user feedback

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
