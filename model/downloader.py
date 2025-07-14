# model/downloader.py
import yt_dlp
import os
import re
import threading # Used for progress callback
from pathlib import Path

class VideoDownloader:
    def __init__(self, save_path="downloads"):
        """
        Initialize the downloader with a default save path.
        """
        self._save_path = save_path # Private attribute for internal use
        self._on_progress_callback = None
        self._on_complete_callback = None

        self._ensure_save_path_exists()

    def _ensure_save_path_exists(self):
        """
        Ensures the save directory exists. Creates it if it doesn't.
        """
        if not os.path.exists(self._save_path):
            try:
                os.makedirs(self._save_path)
            except OSError as e:
                raise IOError(f"Could not create save directory {self._save_path}: {e}")

    @property
    def save_path(self):
        """Getter for save_path."""
        return self._save_path

    @save_path.setter
    def save_path(self, path):
        """Setter for save_path, ensures directory exists on change."""
        self._save_path = path
        self._ensure_save_path_exists()

    def set_callbacks(self, on_progress=None, on_complete=None):
        """
        Sets the progress and completion callback functions.
        :param on_progress: A function to call during download progress.
                            Signature: (stream, chunk, bytes_remaining)
        :param on_complete: A function to call when download is complete.
                            Signature: (status_message, is_success)
        """
        self._on_progress_callback = on_progress
        self._on_complete_callback = on_complete


    def is_valid_url(self, url):
        """
        Simple URL validator for YouTube links.
        This provides a preliminary check; pytube will do a more robust one.
        Supports regular videos, shorts, and various YouTube URL formats.
        """
        # Updated regex to support YouTube Shorts and other formats
        patterns = [
            # Standard YouTube URLs
            r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|m\.youtube\.com)/(watch\?v=|embed/|v/)([a-zA-Z0-9_-]{11})(.*)?$",
            # YouTube Shorts URLs
            r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|m\.youtube\.com)/shorts/([a-zA-Z0-9_-]{11})(.*)?$",
            # youtu.be short URLs
            r"^(https?://)?(www\.)?youtu\.be/([a-zA-Z0-9_-]{11})(.*)?$"
        ]
        
        return any(re.match(pattern, url) for pattern in patterns)

    def _yt_dlp_progress_callback(self, d):
        """
        Progress callback for yt-dlp.
        """
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                bytes_downloaded = d.get('downloaded_bytes', 0)
                total_bytes = d['total_bytes']
                
                if self._on_progress_callback:
                    self._on_progress_callback(bytes_downloaded, total_bytes)
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                bytes_downloaded = d.get('downloaded_bytes', 0)
                total_bytes = d['total_bytes_estimate']

                if self._on_progress_callback:
                    self._on_progress_callback(bytes_downloaded, total_bytes)
        elif d['status'] == 'finished':
            # Here we can use the filename for confirmation, printing or logging purposes
            print(f"\n✅ Download completed: {d['filename']}")

    def download_video(self, url):
        """
        Downloads the video from the provided URL using yt-dlp.
        :param url: YouTube video link
        :return: None (result is communicated via callbacks)
        """
        if not self.is_valid_url(url):
            if self._on_complete_callback:
                self._on_complete_callback("Invalid YouTube URL format.", False)
            return

        try:
            ydl_opts = {
                'format': 'best[height<=1080]/best',  # Best quality up to 1080p
                'outtmpl': str(Path(self._save_path) / '%(title)s.%(ext)s'),
                'progress_hooks': [self._yt_dlp_progress_callback]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', 'Unknown')
                ydl.download([url])

                if self._on_complete_callback:
                    self._on_complete_callback(f"Successfully downloaded: \"{video_title}\"", True)

        except yt_dlp.DownloadError as e:
            if self._on_complete_callback:
                self._on_complete_callback(f"Error: Download failed - {str(e)}", False)
        except Exception as e:
            if self._on_complete_callback:
                self._on_complete_callback(f"An unexpected error occurred: {str(e)}", False)
