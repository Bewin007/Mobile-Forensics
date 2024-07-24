import os
import re
import hashlib
import subprocess
import tkinter as tk
from tkinter import filedialog

# Constants
SUPPORTED_TYPES = ['PDF', 'DOCX', 'AVI', 'GIF', 'PNG', 'JPG', 'JPG_FFDB', 'BMP', 'MPEG']

# Function to search for media files on connected Android devices using ADB
def search_media_files():
    try:
        # Run ADB command to list files on the device
        result = subprocess.run(['adb', 'shell', 'find', '/sdcard/', '-type', 'f'], capture_output=True, text=True, errors='ignore')
        if result.returncode == 0:
            # Parse file paths from ADB output
            if result.stdout:
                file_paths = result.stdout.split('\n')
                return file_paths
            else:
                print("No files found on the device.")
                return []
        else:
            print("Failed to run ADB command:", result.stderr)
            return []
    except Exception as e:
        print("An error occurred:", e)
        return []

# Function to read file bytes from Android device using ADB
def read_file_from_device(file_path, dest):
    try:
        # Run ADB command to pull file from the device
        result = subprocess.run(['adb', 'pull', file_path, dest], capture_output=True)
        if result.returncode == 0:
            return os.path.join(dest, os.path.basename(file_path))
        else:
            print(f"Failed to pull file {file_path} from device:", result.stderr)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Function to write recovered bytes to file
def write_bytes(file_path, filename):
    try:
        with open(file_path, 'rb') as source_file:
            bytes_data = source_file.read()
            with open(filename, 'wb') as dest_file:
                dest_file.write(bytes_data)
        print(f"Recovered: {filename}")
    except Exception as e:
        print("An error occurred:", e)

# Function to create a directory for recovered files
def create_recovery_directory():
    root = tk.Tk()
    root.withdraw() 
    
    # Ask the user to select a directory
    directory_path = filedialog.askdirectory(initialdir="/", title="Select Directory")
    
    return directory_path

# Function to handle recovery for a specific file type
def handle_recovery(file_paths, recovered_dir):
    for file_path in file_paths:
        file_extension = os.path.splitext(file_path)[1].strip('.').upper()
        if file_extension in SUPPORTED_TYPES:
            recovered_file_path = read_file_from_device(file_path, recovered_dir)
            if recovered_file_path:
                write_bytes(recovered_file_path, os.path.join(recovered_dir, os.path.basename(file_path)))

# Main function
def main():
    media_files = search_media_files()
    if media_files:
        recovered_dir = create_recovery_directory()
        handle_recovery(media_files, recovered_dir)
    else:
        print("No media files found on connected Android device.")

# Entry point of the script
if __name__ == "__main__":
    main()
