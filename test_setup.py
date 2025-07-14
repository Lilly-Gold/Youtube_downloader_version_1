#!/usr/bin/env python3
"""
Test script to verify that all components of the YouTube Downloader are working correctly.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import tkinter: {e}")
        return False
    
    try:
        import pytube
        print("✓ pytube imported successfully")
        print(f"  pytube version: {pytube.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import pytube: {e}")
        return False
    
    try:
        from view.gui import YouTubeDownloaderGUI
        print("✓ YouTubeDownloaderGUI imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import YouTubeDownloaderGUI: {e}")
        return False
    
    try:
        from controller.app_controller import AppController
        print("✓ AppController imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AppController: {e}")
        return False
    
    try:
        from model.downloader import VideoDownloader
        print("✓ VideoDownloader imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import VideoDownloader: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without actually downloading."""
    print("\nTesting basic functionality...")
    
    try:
        from model.downloader import VideoDownloader
        downloader = VideoDownloader()
        
        # Test URL validation
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "http://youtube.com/watch?v=dQw4w9WgXcQ"
        ]
        
        invalid_urls = [
            "https://www.google.com",
            "not_a_url",
            "https://vimeo.com/123456"
        ]
        
        for url in valid_urls:
            if downloader.is_valid_url(url):
                print(f"✓ Valid URL recognized: {url}")
            else:
                print(f"✗ Valid URL not recognized: {url}")
                return False
        
        for url in invalid_urls:
            if not downloader.is_valid_url(url):
                print(f"✓ Invalid URL rejected: {url}")
            else:
                print(f"✗ Invalid URL not rejected: {url}")
                return False
        
        print("✓ URL validation working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Error during basic functionality test: {e}")
        return False

def test_directories():
    """Test that required directories exist or can be created."""
    print("\nTesting directory structure...")
    
    required_dirs = ["view", "model", "controller"]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"✓ Directory exists: {dir_name}")
        else:
            print(f"✗ Directory missing: {dir_name}")
            return False
    
    # Test downloads directory creation
    try:
        from model.downloader import VideoDownloader
        downloader = VideoDownloader("test_downloads")
        if os.path.exists("test_downloads"):
            print("✓ Downloads directory creation working")
            os.rmdir("test_downloads")  # Clean up
        else:
            print("✗ Downloads directory not created")
            return False
    except Exception as e:
        print(f"✗ Error testing directory creation: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("YouTube Downloader Setup Test")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_directories()
    all_tests_passed &= test_basic_functionality()
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("🎉 All tests passed! The application is ready to use.")
        print("\nTo run the application:")
        print("1. Make sure the virtual environment is activated")
        print("2. Run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

