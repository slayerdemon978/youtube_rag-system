#!/usr/bin/env python3
"""
Local YouTube Transcript RAG System
Main script for processing YouTube videos and creating vector stores
"""

import os
import sys
from backend.transcript_fetcher import fetch_transcript
from backend.vector_store import create_vector_store
from backend.rag_engine import RAGEngine

def main():
    print("🎥 YouTube Transcript RAG System")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Fetch transcript from YouTube URL")
        print("2. Create vector store from transcript")
        print("3. Query existing transcript")
        print("4. List available transcripts")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            url = input("Enter YouTube URL: ").strip()
            try:
                file_path = fetch_transcript(url)
                print(f"Transcript saved to: {file_path}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            content_dir = "content"
            if not os.path.exists(content_dir):
                print("No content directory found. Please fetch some transcripts first.")
                continue
            
            files = [f for f in os.listdir(content_dir) if f.endswith('.txt')]
            if not files:
                print("No transcript files found. Please fetch some transcripts first.")
                continue
            
            print("\nAvailable transcript files:")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
            
            try:
                file_idx = int(input("Select file number: ")) - 1
                if 0 <= file_idx < len(files):
                    file_path = os.path.join(content_dir, files[file_idx])
                    base_name = create_vector_store(file_path)
                    print(f"Vector store created for: {base_name}")
                else:
                    print("Invalid file number.")
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            vector_dir = "vector_db"
            if not os.path.exists(vector_dir):
                print("No vector database found. Please create vector stores first.")
                continue
            
            index_files = [f for f in os.listdir(vector_dir) if f.endswith('.index')]
            if not index_files:
                print("No vector stores found. Please create vector stores first.")
                continue
            
            print("\nAvailable vector stores:")
            base_names = [f[:-6] for f in index_files]  # Remove .index extension
            for i, name in enumerate(base_names, 1):
                print(f"{i}. {name}")
            
            try:
                store_idx = int(input("Select vector store number: ")) - 1
                if 0 <= store_idx < len(base_names):
                    base_name = base_names[store_idx]
                    
                    print(f"\nLoading RAG engine for: {base_name}")
                    rag = RAGEngine("vector_db")
                    
                    while True:
                        query = input(f"\nAsk a question about '{base_name}' (or 'back' to return): ").strip()
                        if query.lower() == 'back':
                            break
                        
                        if query:
                            try:
                                answer = rag.generate_answer(query, base_name)
                                print(f"\nAnswer: {answer}")
                            except Exception as e:
                                print(f"Error generating answer: {e}")
                else:
                    print("Invalid store number.")
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            content_dir = "content"
            vector_dir = "vector_db"
            
            print("\n📁 Available Transcripts:")
            if os.path.exists(content_dir):
                files = [f for f in os.listdir(content_dir) if f.endswith('.txt')]
                if files:
                    for file in files:
                        print(f"  - {file}")
                else:
                    print("  No transcript files found.")
            else:
                print("  No content directory found.")
            
            print("\n🗃️ Available Vector Stores:")
            if os.path.exists(vector_dir):
                index_files = [f for f in os.listdir(vector_dir) if f.endswith('.index')]
                if index_files:
                    for file in index_files:
                        print(f"  - {file[:-6]}")  # Remove .index extension
                else:
                    print("  No vector stores found.")
            else:
                print("  No vector database directory found.")
        
        elif choice == "5":
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()