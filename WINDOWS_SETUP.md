# 🪟 Windows Setup Guide

This guide helps you set up the YouTube Transcript RAG System on Windows.

## 🚨 Common Windows Issues & Solutions

### Issue 1: Permission Errors During Installation
```
ERROR: Could not install packages due to an OSError: [WinError 2] The system cannot find the file specified
```

**Solutions:**
1. **Run as Administrator** (Recommended)
   - Right-click Command Prompt → "Run as administrator"
   - Navigate to project folder
   - Run installation commands

2. **Use --user flag**
   ```cmd
   pip install --user -r requirements.txt
   ```

3. **Use virtual environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Issue 2: Module Not Found Errors
```
ModuleNotFoundError: No module named 'youtube_transcript_api'
```

**Solutions:**
1. **Check Python PATH**
   ```cmd
   python -c "import sys; print(sys.path)"
   ```

2. **Install in user directory**
   ```cmd
   pip install --user youtube-transcript-api
   ```

3. **Use the fix script**
   ```cmd
   python fix_windows_install.py
   ```

## 🛠️ Installation Methods

### Method 1: Automated Fix Script (Recommended)
```cmd
python fix_windows_install.py
```

### Method 2: Batch File Installation
```cmd
install_windows.bat
```

### Method 3: Manual Step-by-Step Installation

1. **Upgrade pip first**
   ```cmd
   python -m pip install --upgrade pip
   ```

2. **Install core packages**
   ```cmd
   pip install --user flask>=2.3.0
   pip install --user youtube-transcript-api>=0.6.0
   pip install --user pytube>=15.0.0
   pip install --user numpy>=1.24.0
   ```

3. **Install PyTorch (CPU version)**
   ```cmd
   pip install --user torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu
   ```

4. **Install AI/ML packages**
   ```cmd
   pip install --user sentence-transformers>=2.2.0
   pip install --user transformers>=4.30.0
   pip install --user faiss-cpu>=1.7.0
   ```

5. **Install remaining packages**
   ```cmd
   pip install --user langchain>=0.0.300
   pip install --user google-api-python-client>=2.100.0
   ```

### Method 4: Virtual Environment (Safest)
```cmd
# Create virtual environment
python -m venv youtube_rag_env

# Activate it
youtube_rag_env\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run the app
python app.py
```

## 🚀 Running the Application

1. **Open Command Prompt as Administrator**
2. **Navigate to project directory**
   ```cmd
   cd "C:\path\to\youtube_rag-system"
   ```
3. **Run the application**
   ```cmd
   python app.py
   ```
4. **Open browser to**
   ```
   http://localhost:12001
   ```

## 🔧 Troubleshooting

### Problem: "python is not recognized"
**Solution:** Add Python to PATH
1. Search "Environment Variables" in Windows
2. Edit System Environment Variables
3. Add Python installation directory to PATH

### Problem: SSL Certificate errors
**Solution:** Update certificates
```cmd
pip install --upgrade certifi
```

### Problem: Long path issues
**Solution:** Enable long paths in Windows
1. Run `gpedit.msc` as administrator
2. Navigate to: Computer Configuration → Administrative Templates → System → Filesystem
3. Enable "Enable Win32 long paths"

### Problem: Antivirus blocking installation
**Solution:** Temporarily disable antivirus or add Python to exceptions

## 📋 System Requirements

- **OS:** Windows 10/11
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 2GB free space
- **Internet:** Required for downloading models and fetching videos

## 🆘 Still Having Issues?

1. **Check Python version**
   ```cmd
   python --version
   ```

2. **Check pip version**
   ```cmd
   pip --version
   ```

3. **Clear pip cache**
   ```cmd
   pip cache purge
   ```

4. **Reinstall pip**
   ```cmd
   python -m ensurepip --upgrade
   ```

5. **Use alternative package manager**
   ```cmd
   # Install conda/miniconda first, then:
   conda install pytorch torchvision torchaudio cpuonly -c pytorch
   conda install -c conda-forge sentence-transformers
   pip install youtube-transcript-api pytube flask langchain faiss-cpu
   ```

## 📞 Support

If you're still experiencing issues:
1. Check the main README.md for general troubleshooting
2. Ensure you have the latest Python version
3. Try running in a fresh virtual environment
4. Check Windows Event Viewer for detailed error messages

---

**Made with ❤️ for Windows users**