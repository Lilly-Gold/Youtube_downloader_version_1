#!/usr/bin/env python3
"""
Test script to check if YouTube Shorts URLs are recognized.
"""

from model.downloader import VideoDownloader

def test_shorts_url():
    downloader = VideoDownloader()
    
    # Test YouTube Shorts URLs
    shorts_urls = [
        "https://www.youtube.com/shorts/jrCMnbcRa9s",
        "https://youtube.com/shorts/jrCMnbcRa9s",
        "http://www.youtube.com/shorts/jrCMnbcRa9s",
        "https://m.youtube.com/shorts/jrCMnbcRa9s"
    ]
    
    print("Testing YouTube Shorts URL validation:")
    print("=" * 50)
    
    for url in shorts_urls:
        if downloader.is_valid_url(url):
            print(f"✓ Valid Shorts URL: {url}")
        else:
            print(f"✗ Invalid Shorts URL: {url}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_shorts_url()

