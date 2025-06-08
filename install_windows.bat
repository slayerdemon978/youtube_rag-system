@echo off
echo Installing YouTube Transcript RAG System on Windows...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Proceeding with installation...
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install packages one by one to avoid conflicts
echo.
echo Installing core dependencies...
python -m pip install --user flask>=2.3.0
python -m pip install --user youtube-transcript-api>=0.6.0
python -m pip install --user pytube>=15.0.0
python -m pip install --user numpy>=1.24.0

echo.
echo Installing AI/ML dependencies...
python -m pip install --user torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install --user sentence-transformers>=2.2.0
python -m pip install --user transformers>=4.30.0
python -m pip install --user faiss-cpu>=1.7.0

echo.
echo Installing LangChain dependencies...
python -m pip install --user langchain>=0.0.300

echo.
echo Installing Google API client...
python -m pip install --user google-api-python-client>=2.100.0

echo.
echo Installation complete!
echo.
echo To run the application:
echo 1. Open Command Prompt as Administrator (recommended)
echo 2. Navigate to this directory
echo 3. Run: python app.py
echo 4. Open browser to http://localhost:12001
echo.
pause