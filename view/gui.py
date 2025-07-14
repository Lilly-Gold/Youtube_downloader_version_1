# view/gui.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json
import os
from datetime import datetime

class YouTubeDownloaderGUI:
    def __init__(self, root):
        """
        Constructor that sets up the GUI layout and widgets.
        :param root: The main Tkinter window object.
        """
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x300") # Increased size for better layout
        self.root.resizable(False, False) # Prevent resizing for now

        self.save_path = tk.StringVar() # To store the chosen save path
        self.save_path.set("downloads") # Default save path

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and places all the widgets on the GUI window.
        """
        # Main frame for better organization
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL Input Section
        url_frame = ttk.LabelFrame(main_frame, text="Video URL", padding="10")
        url_frame.pack(pady=10, fill=tk.X)

        self.url_label = ttk.Label(url_frame, text="Enter YouTube Video URL:")
        self.url_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Save Path Section
        path_frame = ttk.LabelFrame(main_frame, text="Save Location", padding="10")
        path_frame.pack(pady=10, fill=tk.X)

        self.path_entry = ttk.Entry(path_frame, textvariable=self.save_path, width=40, state='readonly')
        self.path_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.browse_button = ttk.Button(path_frame, text="Browse", command=self._select_save_path)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Download Button
        self.download_button = ttk.Button(main_frame, text="Download")
        self.download_button.pack(pady=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Status label for messages
        self.status_label = ttk.Label(main_frame, text="", foreground="blue", wraplength=550)
        self.status_label.pack(pady=5)

    def _select_save_path(self):
        """
        Opens a directory chooser dialog and sets the chosen path.
        """
        path = filedialog.askdirectory(title="Select Save Location")
        if path:
            self.save_path.set(path)

    def get_video_url(self):
        """
        Retrieves the URL entered by the user.
        :return: The URL string.
        """
        return self.url_entry.get()

    def get_save_path(self):
        """
        Retrieves the selected save path.
        :return: The save path string.
        """
        return self.save_path.get()

    def update_status(self, message, color="blue"):
        """
        Updates the status label with a message and a specified color.
        :param message: The message to display.
        :param color: The color of the message text (e.g., "blue", "red", "green").
        """
        self.status_label.config(text=message, foreground=color)

    def update_progress(self, current_bytes, total_bytes):
        """
        Updates the progress bar based on downloaded bytes.
        :param current_bytes: Number of bytes downloaded so far.
        :param total_bytes: Total size of the file in bytes.
        """
        if total_bytes > 0:
            percentage = (current_bytes / total_bytes) * 100
            self.progress_bar['value'] = percentage
            self.root.update_idletasks() # Update GUI immediately

    def reset_progress(self):
        """
        Resets the progress bar to 0.
        """
        self.progress_bar['value'] = 0
        self.root.update_idletasks()

    def set_download_callback(self, callback):
        """
        Connects the download button to a controller method.
        :param callback: The method to be called when the download button is clicked.
        """
        self.download_button.config(command=callback)





