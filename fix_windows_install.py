#!/usr/bin/env python3
"""
Windows Installation Fix Script
This script helps resolve common Windows installation issues
"""

import subprocess
import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_package(package_name, pip_name=None):
    """Install a package with error handling"""
    if pip_name is None:
        pip_name = package_name
    
    try:
        # Check if already installed
        importlib.import_module(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"📦 Installing {package_name}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--user", pip_name
            ])
            print(f"✅ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False

def main():
    """Main installation function"""
    print("🔧 YouTube Transcript RAG System - Windows Fix")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Upgrade pip first
    print("\n📦 Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip upgraded successfully")
    except subprocess.CalledProcessError:
        print("⚠️ Warning: Could not upgrade pip, continuing anyway...")
    
    # Install packages in order
    packages = [
        ("flask", "flask>=2.3.0"),
        ("youtube_transcript_api", "youtube-transcript-api>=0.6.0"),
        ("pytube", "pytube>=15.0.0"),
        ("numpy", "numpy>=1.24.0"),
        ("torch", "torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu"),
        ("sentence_transformers", "sentence-transformers>=2.2.0"),
        ("transformers", "transformers>=4.30.0"),
        ("faiss", "faiss-cpu>=1.7.0"),
        ("langchain", "langchain>=0.0.300"),
        ("googleapiclient", "google-api-python-client>=2.100.0"),
    ]
    
    print("\n📦 Installing required packages...")
    failed_packages = []
    
    for package_name, pip_name in packages:
        if not install_package(package_name, pip_name):
            failed_packages.append(package_name)
    
    # Summary
    print("\n" + "=" * 50)
    if failed_packages:
        print("⚠️ Installation completed with some issues:")
        for pkg in failed_packages:
            print(f"   ❌ {pkg}")
        print("\nTry installing failed packages manually:")
        for pkg in failed_packages:
            print(f"   pip install --user {pkg}")
    else:
        print("✅ All packages installed successfully!")
    
    print("\n🚀 Next steps:")
    print("1. Open Command Prompt as Administrator")
    print("2. Navigate to this directory")
    print("3. Run: python app.py")
    print("4. Open browser to http://localhost:12001")
    
    return len(failed_packages) == 0

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)