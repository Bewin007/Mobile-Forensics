import subprocess
import tkinter as tk
from tkinter import filedialog

def run_adb_command(command):
    try:
        # Execute the ADB command and capture its output
        output = subprocess.check_output(command, shell=True, text=True)
        return output.strip()  # Strip any leading/trailing whitespace
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def save_to_text_file(data, output_file):
    try:
        with open(output_file, "w") as file:
            file.write(data)
        print("Output saved to:", output_file)
    except Exception as e:
        print("Error:", e)

def select_output_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    output_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                                               title="Save Bluetooth Manager Info As")
    return output_file

if __name__ == "__main__":
    # Run adb shell command to fetch Bluetooth manager information
    adb_command = "adb shell dumpsys bluetooth_manager"
    output = run_adb_command(adb_command)

    if output is not None:
        # Ask user to select the output file location
        output_file = select_output_file()

        if output_file:
            # Save the output to the selected text file
            save_to_text_file(output, output_file)
        else:
            print("No file selected. Exiting.")
    else:
        print("Failed to retrieve Bluetooth manager information.")
