#!/usr/bin/env python3
"""
Test script to verify the updated downloader works with GUI callbacks.
"""

import sys
import time
from model.downloader import VideoDownloader

class MockGUI:
    """Mock GUI to test callbacks."""
    
    def __init__(self):
        self.progress_updates = []
        self.completion_message = ""
        self.completion_success = False
        
    def mock_progress_callback(self, bytes_downloaded, total_bytes):
        """Mock progress callback."""
        if total_bytes > 0:
            percentage = (bytes_downloaded / total_bytes) * 100
            self.progress_updates.append(percentage)
            print(f"Progress: {percentage:.1f}%", end='\r')
    
    def mock_completion_callback(self, message, is_success):
        """Mock completion callback."""
        self.completion_message = message
        self.completion_success = is_success
        print(f"\nCompletion: {message} (Success: {is_success})")

def test_downloader_integration():
    """Test the downloader with mock GUI callbacks."""
    print("Testing VideoDownloader with yt-dlp integration...")
    print("=" * 60)
    
    # Create mock GUI
    mock_gui = MockGUI()
    
    # Create downloader
    downloader = VideoDownloader("test_downloads")
    
    # Set callbacks
    downloader.set_callbacks(
        on_progress=mock_gui.mock_progress_callback,
        on_complete=mock_gui.mock_completion_callback
    )
    
    # Test URL
    test_url = "https://www.youtube.com/shorts/jrCMnbcRa9s"
    
    print(f"Testing download: {test_url}")
    print("Starting download...")
    
    # Download video
    downloader.download_video(test_url)
    
    # Wait a bit for async operations
    time.sleep(1)
    
    print("=" * 60)
    print(f"Final status: {mock_gui.completion_message}")
    print(f"Success: {mock_gui.completion_success}")
    print(f"Progress updates received: {len(mock_gui.progress_updates)}")
    
    # Clean up test directory
    import os
    import shutil
    if os.path.exists("test_downloads"):
        shutil.rmtree("test_downloads")
        print("Cleaned up test downloads directory")

if __name__ == "__main__":
    test_downloader_integration()

