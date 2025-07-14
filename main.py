# main.py (New file to run the application)
import tkinter as tk
from view.gui import YouTubeDownloaderGUI
from controller.app_controller import AppController

def main():
    """
    Main function to initialize and run the application.
    """
    root = tk.Tk() # Create the main Tkinter window
    app_gui = YouTubeDownloaderGUI(root) # Instantiate the GUI     
    app_controller = AppController(app_gui) # Instantiate the Controller, linking GUI and Model
    root.mainloop() # Start the Tkinter event loop

if __name__ == "__main__":
    main() 