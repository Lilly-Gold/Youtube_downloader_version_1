#!/usr/bin/env python3
"""
Alternative YouTube downloader using yt-dlp instead of pytube.
yt-dlp is generally more reliable and up-to-date.
"""

import sys
import os
import yt_dlp
from pathlib import Path

class YtDlpDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
    def progress_hook(self, d):
        """Progress callback for yt-dlp."""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = d.get('downloaded_bytes', 0) / d['total_bytes'] * 100
                mb_downloaded = d.get('downloaded_bytes', 0) / (1024 * 1024)
                mb_total = d['total_bytes'] / (1024 * 1024)
                print(f"\rProgress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="", flush=True)
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                percent = d.get('downloaded_bytes', 0) / d['total_bytes_estimate'] * 100
                mb_downloaded = d.get('downloaded_bytes', 0) / (1024 * 1024)
                mb_total = d['total_bytes_estimate'] / (1024 * 1024)
                print(f"\rProgress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB~)", end="", flush=True)
        elif d['status'] == 'finished':
            print(f"\n✅ Download completed: {d['filename']}")
    
    def download_video(self, url):
        """Download video using yt-dlp."""
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                'format': 'best[height<=1080]/best',  # Best quality up to 1080p
                'progress_hooks': [self.progress_hook],
                'ignoreerrors': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("🔍 Extracting video information...")
                
                # Extract info first to get title
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                
                print(f"📹 Title: {title}")
                print(f"👤 Uploader: {uploader}")
                if duration:
                    mins, secs = divmod(duration, 60)
                    print(f"⏱️  Duration: {mins:02d}:{secs:02d}")
                
                print("🚀 Starting download...")
                
                # Download the video
                ydl.download([url])
                
                return True
                
        except yt_dlp.DownloadError as e:
            print(f"\n❌ Download error: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False

def main():
    """Main function for yt-dlp downloader."""
    if len(sys.argv) != 2:
        print("Usage: python yt_dlp_downloader.py <youtube_url>")
        print("Example: python yt_dlp_downloader.py 'https://www.youtube.com/shorts/jrCMnbcRa9s'")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("YouTube Video Downloader (yt-dlp)")
    print("=" * 50)
    print(f"🔗 URL: {url}")
    
    # Create downloads directory
    download_path = Path("downloads")
    download_path.mkdir(exist_ok=True)
    print(f"📁 Download path: {download_path.absolute()}")
    
    # Initialize downloader
    downloader = YtDlpDownloader("downloads")
    
    # Download the video
    success = downloader.download_video(url)
    
    print("=" * 50)
    if success:
        print("🎉 Download completed successfully!")
        print(f"📂 Check the 'downloads' folder for your video.")
    else:
        print("💔 Download failed. Please check the URL and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

