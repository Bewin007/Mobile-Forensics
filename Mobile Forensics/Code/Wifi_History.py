import subprocess
import os
import tkinter as tk
from tkinter import filedialog

# Function to fetch saved Wi-Fi networks using ADB
def fetch_saved_wifi_networks():
    try:
        # Run ADB command to fetch saved Wi-Fi networks
        result = subprocess.run(['adb', 'shell', 'dumpsys', 'wifi', '|', 'grep', '-E', '"SSID|capabilities"'], 
                                capture_output=True, text=True, check=True)
        # Parse the Wi-Fi network information
        wifi_info = result.stdout.strip().split('\n')
        networks = []
        for line in wifi_info:
            if line.startswith("SSID:"):
                ssid = line.split(":")[1].strip()
                networks.append(ssid)
        return networks
    except subprocess.CalledProcessError as e:
        print("Failed to run ADB command:", e)
        return []

# Function to select the file location and enter filename using Tkinter GUI
def select_file_location_and_filename():
    root = tk.Tk()
    root.withdraw()
    
    # Prompt user to enter filename only if networks are found
    if fetch_saved_wifi_networks():
        # Prompt user to enter filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Wi-Fi Network List"
        )
        return filename
    else:
        print("No saved Wi-Fi networks found.")
        return None

# Select the file location and enter filename using GUI
selected_filename = select_file_location_and_filename()

# Write the list of saved Wi-Fi networks to a text file
if selected_filename:
    try:
        with open(selected_filename, 'w') as f:
            for network in fetch_saved_wifi_networks():
                f.write(network + '\n')

        print("Saved Wi-Fi networks have been saved to:", selected_filename)
    except Exception as e:
        print("An error occurred while writing to file:", e)
else:
    print("No filename selected.")
