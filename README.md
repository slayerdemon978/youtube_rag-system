# 🎥 YouTube Transcript RAG System

A powerful **Retrieval-Augmented Generation (RAG)** system that fetches YouTube video transcripts and enables intelligent Q&A using AI. Built with Flask, FAISS, and Transformers for CPU-only operation.

## 🌟 Features

- **📥 Transcript Fetching**: Automatically download transcripts from YouTube videos
- **📋 Playlist Support**: Fetch transcripts from entire YouTube playlists using YouTube API
- **🔍 Vector Search**: Create FAISS vector stores for semantic search
- **🤖 AI Q&A**: Ask questions about video content using Microsoft Phi-2 model
- **🌐 Web Interface**: Beautiful, responsive Flask web application
- **💻 CPU Only**: No GPU required - runs on any machine
- **📱 Mobile Friendly**: Responsive design works on all devices

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

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/slayerdemon978/youtube_rag-system.git
cd youtube_rag-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Web Application

```bash
python app.py
```

The application will be available at `http://localhost:12001`

### 4. Alternative: Use CLI Interface

```bash
python main.py
```

## 📖 Usage Guide

### Web Interface

1. **Fetch Single Video**:
   - Enter a YouTube URL in the "Fetch Transcript" section
   - Click "Fetch Transcript" - this automatically creates a vector store

2. **Fetch Playlist** (YouTube API):
   - Enter a YouTube playlist URL
   - The system will fetch all videos in the playlist

3. **Ask Questions**:
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

### Common Issues

1. **Transcript Not Available**:
   - Some videos don't have transcripts
   - Try videos with auto-generated captions

2. **Model Loading Slow**:
   - First-time model download can take several minutes
   - Models are cached locally after first use

3. **Memory Issues**:
   - Ensure you have at least 4GB RAM available
   - Close other applications if needed

4. **API Errors**:
   - Check internet connection
   - Verify YouTube URLs are valid and public

### Error Messages

- `❌ Error fetching transcript`: Video has no available transcript
- `❌ Error creating vector store`: Issue with text processing or model loading
- `❌ Error generating answer`: Problem with the language model

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
