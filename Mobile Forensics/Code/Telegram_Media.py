import tkinter as tk
from tkinter import filedialog
import subprocess

# Function to handle selecting the output folder using Tkinter GUI
def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder to Save Telegram Media")
    return folder_path

# Function to pull files from Android device and save them to the specified directory
def adb_pull_and_save(output_folder):
    # ADB command to pull files
    adb_command = "adb pull /sdcard/Android/data/org.telegram.messenger/ {}".format(output_folder)
    
    try:
        # Execute the adb command
        subprocess.run(adb_command, shell=True, check=True)
        print("Files pulled and saved successfully!")
    except subprocess.CalledProcessError:
        print("Failed to pull files.")

# Main function to orchestrate the process
def main():
    # Select the output folder using GUI
    output_folder = select_output_folder()

    if output_folder:
        adb_pull_and_save(output_folder)
    else:
        print("No folder selected.")

if __name__ == "__main__":
    main()
