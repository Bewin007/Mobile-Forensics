import tkinter as tk
from tkinter import filedialog
import subprocess
import os

# Function to check if the device is connected
def is_device_connected():
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        output = result.stdout.strip().split("\n")
        return len(output) > 1  # Check if any devices are listed (excluding the header)
    except subprocess.CalledProcessError as e:
        print("Error checking device connection:", e)
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False

# Function to fetch WhatsApp media files from the device and save them in separate folders based on type
def fetch_and_save_whatsapp_media(output_folder):
    try:
        # Run the adb command to find WhatsApp media files and iterate over each file path
        adb_command = 'adb shell "find /sdcard/android/media/com.whatsapp/whatsapp/media -type f"'
        process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stderr:
            raise Exception(stderr)

        # Iterate over each file path and pull the file to the appropriate folder
        file_paths = stdout.strip().split('\n')
        for file_path in file_paths:
            # Determine the type of media based on file extension
            media_type = get_media_type(file_path)
            if media_type:
                # Create output directory for the media type if not exists
                media_type_dir = os.path.join(output_folder, media_type)
                os.makedirs(media_type_dir, exist_ok=True)
                # Pull the media file from the device and save it into the appropriate folder
                pull_command = f'adb pull "{file_path}" "{media_type_dir}"'
                subprocess.run(pull_command, shell=True)
        print("WhatsApp media files have been saved to:", output_folder)
    except Exception as e:
        print("An error occurred while fetching and saving WhatsApp media:", e)

# Function to determine the type of media based on file extension
def get_media_type(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension in ('.jpg', '.jpeg', '.png', '.gif'):
        return 'Images'
    elif extension in ('.mp4', '.mkv', '.avi'):
        return 'Videos'
    elif extension in ('.mp3', '.m4a', '.aac'):
        return 'Audio'
    else:
        return 'Other'

# Function to handle selecting the output folder using Tkinter GUI
def select_output_folder():
    try:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select Folder to Save WhatsApp Media")
        return folder_path
    except Exception as e:
        print("An error occurred while selecting the output folder:", e)
        return None

# Main function to orchestrate the process
def main():
    try:
        if not is_device_connected():
            print("Device is not connected. Exiting...")
            return

        # Select the output folder using GUI
        output_folder = select_output_folder()

        if output_folder:
            # Fetch and save WhatsApp media files into appropriate folders
            fetch_and_save_whatsapp_media(output_folder)
        else:
            print("No folder selected.")
    except Exception as e:
        print("An error occurred during execution:", e)

if __name__ == "__main__":
    main()
