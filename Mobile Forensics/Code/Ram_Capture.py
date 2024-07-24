import subprocess
import os
import tkinter as tk
from tkinter import filedialog

# Function to check if the device is connected
def is_device_connected():
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        output = result.stdout.strip().split("\n")
        return len(output) > 1  # Check if any devices are listed (excluding the header)
    except subprocess.CalledProcessError as e:
        print("Error checking device connection:", e)
        return False

# Function to capture RAM
def capture_ram():
    if not is_device_connected():
        print("Device is not connected. Cannot capture RAM.")
        return False
    
    try:
        # Prompt the user to select the destination folder and enter the file name using a GUI
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save RAM Dump As")
        if not file_path:
            print("No file selected. Exiting...")
            return False

        # Change the current working directory to the selected folder
        os.chdir(os.path.dirname(file_path))

        # Run ADB command to dump RAM to the selected file path (without root access)
        result = subprocess.run(["adb", "shell", "dumpsys", "meminfo", "--unreachable"], capture_output=True, text=True)
        with open(file_path, "w") as f:
            f.write(result.stdout)

        print("RAM captured and saved successfully to:", file_path)
        return True
    except Exception as e:
        print("Error capturing RAM:", e)
        return False

# Function to analyze RAM artifacts
def analyze_ram():
    try:
        # Pull the RAM dump file from the device to the local machine
        result = subprocess.run(["adb", "pull", "/sdcard/ram_dump.txt"], capture_output=True, text=True)
        if result.returncode == 0:
            print("RAM dump file pulled successfully.")
            
            # Perform analysis on the RAM dump file
            # You can add your analysis code here
            
            # Example: Print the size of the RAM dump file
            file_size = os.path.getsize("ram_dump.txt")
            print("RAM dump file size:", file_size, "bytes")
            
            # Example: Print the first 100 lines of the RAM dump file
            with open("ram_dump.txt", "r") as f:
                first_100_lines = ''.join(f.readlines()[:100])
                print("First 100 lines of the RAM dump file:\n", first_100_lines)
        
    except Exception as e:
        print("Error analyzing RAM:", e)

# Main function
def main():
    # Capture RAM
    if capture_ram():
        # Analyze RAM artifacts
        analyze_ram()

# Call the main function
if __name__ == "__main__":
    main()
