# controller/app_controller.py
import tkinter as tk
from model.downloader import VideoDownloader
import threading
import os

class AppController:
    def __init__(self, view):
        """
        Controller constructor: connects the View (GUI) and the Model (Downloader).
        :param view: Instance of the GUI class (YouTubeDownloaderGUI)
        """
        self.view = view
        self.downloader = VideoDownloader(save_path=self.view.get_save_path()) # Initialize with default path from GUI

        # Connect the GUI's Download button to this controller's method
        self.view.set_download_callback(self.handle_download)

        # Set up downloader callbacks
        self.downloader.set_callbacks(
            on_progress=self.update_progress_ui,
            on_complete=self.on_download_complete
        )

        # Link the save path variable in GUI to downloader's save path
        self.view.save_path.trace_add("write", self._on_save_path_change)

    def _on_save_path_change(self, *args):
        """
        Callback for when the save path in the GUI changes.
        Updates the downloader's save path.
        """
        new_path = self.view.get_save_path()
        if new_path:
            try:
                self.downloader.save_path = new_path
                self.view.update_status(f"Download path set to: {new_path}", color="grey")
            except IOError as e:
                self.view.update_status(f"Error setting path: {e}", color="red")


    def handle_download(self):
        """
        This method is triggered when the user clicks the 'Download' button.
        It retrieves the URL from the GUI and starts the download in a new thread.
        """
        url = self.view.get_video_url()
        save_path = self.view.get_save_path()

        if not url:
            self.view.update_status("Please enter a YouTube video URL.", color="orange")
            return

        self.view.update_status("Initiating download...", color="blue")
        self.view.reset_progress() # Reset progress bar for new download

        # Run the download in a separate thread to prevent GUI freeze
        download_thread = threading.Thread(target=self._run_download_in_thread, args=(url,))
        download_thread.start()

    def _run_download_in_thread(self, url):
        """
        Internal method to be run in a separate thread.
        Calls the model's download method.
        """
        self.downloader.download_video(url)

    def update_progress_ui(self, bytes_downloaded, total_bytes):
        """
        Callback from the downloader model to update the GUI progress bar.
        Schedules the update to run on the main Tkinter thread.
        """
        # Ensure GUI updates happen on the main thread
        self.view.root.after(0, self.view.update_progress, bytes_downloaded, total_bytes)

    def on_download_complete(self, message, is_success):
        """
        Callback from the downloader model when a download is complete (success or failure).
        Schedules the status update to run on the main Tkinter thread.
        """
        color = "green" if is_success else "red"
        # Ensure GUI updates happen on the main thread
        self.view.root.after(0, self.view.update_status, message, color)
        # Also reset progress bar on completion
        self.view.root.after(0, self.view.reset_progress)