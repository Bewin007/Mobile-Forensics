import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def select_destination_directory():
    root = tk.Tk()
    root.withdraw()
    destination_dir = filedialog.askdirectory(title="Select Destination Directory")
    return destination_dir

def adb_pull_sdcard(destination_dir):
    try:
        process = subprocess.Popen(['adb', 'pull', '/sdcard/', destination_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Extracting files from the device. Please wait...")
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Files pulled successfully.")
            print(stdout.decode('utf-8'))
        else:
            print("Failed to pull files:")
            print(stderr.decode('utf-8'))
    except Exception as e:
        print("An error occurred:", e)

def main():
    destination_dir = select_destination_directory()
    if destination_dir:
        adb_pull_sdcard(destination_dir)
    else:
        print("No destination directory selected.")

if __name__ == "__main__":
    main()
