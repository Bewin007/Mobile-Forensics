import subprocess
import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import os

def run_adb_command(command):
    try:
        process = subprocess.Popen(['adb'] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        if process.returncode == 0:
            return output.decode().strip()
        else:
            print("Error executing adb command:", error.decode())
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def extract_profile_details():
    profile_details = {}

    # Create shared_prefs directory if it doesn't exist
    if not os.path.exists('shared_prefs'):
        os.makedirs('shared_prefs')

    # Pull the shared preferences folder to local
    run_adb_command(['pull', '/data/data/com.example.app/shared_prefs', 'shared_prefs'])

    prefs_files = [f for f in os.listdir('shared_prefs') if f.endswith('.xml')]

    for prefs_file in prefs_files:
        try:
            tree = ET.parse(os.path.join('shared_prefs', prefs_file))
            root = tree.getroot()

            for child in root:
                if child.tag == 'string' and child.attrib.get('name') in ['display_name', 'email', 'phone_number']:
                    profile_details[child.attrib['name'].replace('_', ' ').title()] = child.text

        except Exception as e:
            print(f"Error parsing {prefs_file}: {e}")

    return profile_details

def save_profile_details():
    profile_details = extract_profile_details()

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if file_path:
        with open(file_path, 'w') as file:
            for key, value in profile_details.items():
                file.write(f"{key}: {value}\n")
        print(f"Saved profile details to {file_path}")

if __name__ == "__main__":
    save_profile_details()
