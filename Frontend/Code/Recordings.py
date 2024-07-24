import tkinter as tk
from tkinter import filedialog
import subprocess

# Function to check if the device is connected
def is_device_connected():
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        output = result.stdout.strip().split("\n")
        return len(output) > 1  # Check if any devices are listed (excluding the header)
    except subprocess.CalledProcessError as e:
        print("Error checking device connection:", e)
        return False

# Function to handle selecting the output folder using Tkinter GUI
def select_output_folder():
    if not is_device_connected():
        print("Device is not connected. Cannot select output folder.")
        return None
    
    try:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select Folder to Save Call Recordings")
        return folder_path
    except Exception as e:
        print("An error occurred while selecting the folder:", e)
        return None

# Function to fetch call recordings from the device and save them in a folder
def fetch_and_save_call_recordings(output_folder):
    try:
        # Run the adb command to pull the entire directory to the output folder
        adb_command = f'adb pull /sdcard/music/Recordings "{output_folder}"'
        process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stderr:
            print("Error:", stderr)
        else:
            print("Call recordings have been saved to:", output_folder)
    except Exception as e:
        print("An error occurred:", e)

# Main function to orchestrate the process
def main():
    if not is_device_connected():
        print("Device is not connected. Exiting...")
        return
    
    try:
        # Select the output folder using GUI
        output_folder = select_output_folder()

        if output_folder is not None:  # Check if output_folder is not None before proceeding
            if output_folder:
                print("Selected output folder:", output_folder)  # Print the selected output folder for debugging
                # Fetch and save call recordings into the output folder
                fetch_and_save_call_recordings(output_folder)
            else:
                print("No folder selected.")
    except Exception as e:
        print("An error occurred during execution:", e)

if __name__ == "__main__":
    main()
