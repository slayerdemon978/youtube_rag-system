# 🚀 Quick Windows Fix

## Your Error:
```
ModuleNotFoundError: No module named 'youtube_transcript_api'
```

## 🔧 Immediate Solutions:

### Solution 1: Use Virtual Environment (BEST & RECOMMENDED)
```cmd
# Create virtual environment
python -m venv youtube_rag_env

# Activate it
youtube_rag_env\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install packages
pip install -r requirements.txt

# Run the app
python app.py
```
**Why this works**: Virtual environments avoid all permission and conflict issues!

### Solution 2: Use the Fix Script
```cmd
python fix_windows_install.py
```
This script will automatically install all packages with proper error handling.

### Solution 3: Manual Installation with --user Flag
```cmd
pip install --user youtube-transcript-api
pip install --user pytube
pip install --user flask
pip install --user sentence-transformers
pip install --user faiss-cpu
pip install --user langchain
pip install --user transformers
pip install --user google-api-python-client
```

### Solution 4: Run as Administrator (Last Resort)
1. Right-click Command Prompt → "Run as administrator"
2. Navigate to your project folder
3. Run: `pip install -r requirements.txt`

## 🎯 After Installation:

**If you used virtual environment (Solution 1):**
```cmd
# Make sure virtual environment is activated
youtube_rag_env\Scripts\activate

# Run the app
python app.py
```

**For other solutions:**
```cmd
python app.py
```

Then open: http://localhost:12001

## 🔄 Next Time You Want to Run the App:

**If you used virtual environment:**
```cmd
# Navigate to project folder
cd path\to\youtube_rag-system

# Activate virtual environment
youtube_rag_env\Scripts\activate

# Run the app
python app.py

# When done, deactivate
deactivate
```

## 📋 Files Added for Windows Support:
- `fix_windows_install.py` - Automated installation script
- `install_windows.bat` - Batch file installer
- `WINDOWS_SETUP.md` - Comprehensive Windows guide
- `requirements_minimal.txt` - Minimal requirements list

## 🆘 Still Having Issues?
Check `WINDOWS_SETUP.md` for detailed troubleshooting of all common Windows problems.