import subprocess
import tkinter as tk
from tkinter import filedialog

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

def extract_instagram_data():
    data = {}
    
    # Path to Instagram data (this is just an example, actual path may vary)
    path = '/data/data/com.instagram.android/databases/'
    
    # List files in Instagram data directory
    files_list = run_adb_command(['shell', 'ls', path])
    
    if files_list:
        # You would typically look for specific database files or other data files here
        data['Files in Instagram data directory'] = files_list
    
    return data

def save_to_file(data, filename="instagram_data.txt"):
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        if file_path:
            with open(file_path, 'w') as file:
                for key, value in data.items():
                    file.write(f"{key}:\n{value}\n")
            print(f"Saved Instagram data to {file_path}")
    except Exception as e:
        print("Error saving to file:", e)

if __name__ == "__main__":
    instagram_data = extract_instagram_data()
    if instagram_data:
        save_to_file(instagram_data)
