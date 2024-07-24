import subprocess
import tkinter as tk
from tkinter import filedialog

def get_installed_packages():
    try:
        # Execute adb shell dumpsys package packages command and capture output
        output = subprocess.check_output(["adb", "shell", "dumpsys", "package", "packages"], text=True)
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
                                               title="Save Installed Packages As")
    return output_file

if __name__ == "__main__":
    # Get installed packages with permissions
    packages_output = get_installed_packages()

    if packages_output is not None:
        # Ask user to select the output file location
        output_file = select_output_file()

        if output_file:
            # Save the output to the selected text file
            save_to_text_file(packages_output, output_file)
        else:
            print("No file selected. Exiting.")
    else:
        print("Failed to retrieve installed packages.")
