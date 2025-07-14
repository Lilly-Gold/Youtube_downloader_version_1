#!/usr/bin/env python3
"""
Command-line interface for the YouTube Downloader.
This script allows downloading videos without the GUI.
"""

import sys
import os
from model.downloader import VideoDownloader
import threading
import time

class CLIDownloader:
    def __init__(self):
        self.downloader = VideoDownloader("downloads")
        self.download_complete = False
        self.download_success = False
        self.status_message = ""
        self.progress_info = {"current": 0, "total": 0}
        
        # Set up callbacks
        self.downloader.set_callbacks(
            on_progress=self.progress_callback,
            on_complete=self.completion_callback
        )
    
    def progress_callback(self, bytes_downloaded, total_bytes):
        """Callback for download progress."""
        self.progress_info["current"] = bytes_downloaded
        self.progress_info["total"] = total_bytes
        
        if total_bytes > 0:
            percentage = (bytes_downloaded / total_bytes) * 100
            mb_downloaded = bytes_downloaded / (1024 * 1024)
            mb_total = total_bytes / (1024 * 1024)
            
            # Clear the line and print progress
            print(f"\rProgress: {percentage:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="", flush=True)
    
    def completion_callback(self, message, is_success):
        """Callback for download completion."""
        self.status_message = message
        self.download_success = is_success
        self.download_complete = True
        print()  # New line after progress
        
        if is_success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    def download_video(self, url):
        """Download a video with progress tracking."""
        print(f"🔗 URL: {url}")
        print(f"📁 Download path: {os.path.abspath(self.downloader.save_path)}")
        
        # Validate URL first
        if not self.downloader.is_valid_url(url):
            print("❌ Invalid YouTube URL format.")
            return False
        
        print("🚀 Starting download...")
        
        # Reset flags
        self.download_complete = False
        self.download_success = False
        
        # Start download in a separate thread
        download_thread = threading.Thread(target=self.downloader.download_video, args=(url,))
        download_thread.start()
        
        # Wait for completion
        while not self.download_complete:
            time.sleep(0.1)
        
        download_thread.join()
        return self.download_success

def main():
    """Main function for CLI downloader."""
    if len(sys.argv) != 2:
        print("Usage: python cli_download.py <youtube_url>")
        print("Example: python cli_download.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("YouTube Video Downloader (CLI)")
    print("=" * 50)
    
    # Create downloads directory if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    
    # Initialize downloader
    cli_downloader = CLIDownloader()
    
    # Download the video
    success = cli_downloader.download_video(url)
    
    print("=" * 50)
    if success:
        print("🎉 Download completed successfully!")
        print(f"📂 Check the 'downloads' folder for your video.")
    else:
        print("💔 Download failed. Please check the URL and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

