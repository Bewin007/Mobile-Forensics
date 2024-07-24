import subprocess
import tkinter as tk
from tkinter import filedialog

def get_logged_in_emails():
    try:
        adb_output = subprocess.check_output(['adb', 'shell', 'dumpsys', 'account'])
        adb_output = adb_output.decode('utf-8')
        email_lines = [line for line in adb_output.split('\n') if '@' in line]
        return email_lines
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

# Get the logged-in emails
logged_in_emails = get_logged_in_emails()

if logged_in_emails:
    # Create GUI window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt user to select the file path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save Text file")

    if file_path:
        # Save the emails to the selected text file
        with open(file_path, 'w') as file:
            file.writelines(logged_in_emails)
        print("Logged-in Accounts saved to", file_path)
    else:
        print("No file selected. Exiting...")
else:
    print("No logged-in Accounts retrieved. Exiting...")
