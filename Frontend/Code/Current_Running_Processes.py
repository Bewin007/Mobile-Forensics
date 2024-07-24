import subprocess
import tkinter as tk
from tkinter import filedialog

def get_running_processes():
    try:
        # Execute adb shell ps command and capture output
        output = subprocess.check_output(["adb", "shell", "ps"], text=True)
        return output
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def save_to_text_file(data, output_file):
    try:
        with open(output_file, "w") as file:
            file.write(data)
        print("Data saved to:", output_file)
    except Exception as e:
        print("Error:", e)

def select_output_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    output_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                                               title="Save Running Processes As")
    return output_file

if __name__ == "__main__":
    # Get running processes
    processes_output = get_running_processes()

    if processes_output is not None:
        # Ask user to select the output file location
        output_file = select_output_file()

        if output_file:
            # Save the output to the selected text file
            save_to_text_file(processes_output, output_file)
        else:
            print("No file selected. Exiting.")
    else:
        print("Failed to retrieve running processes.")
