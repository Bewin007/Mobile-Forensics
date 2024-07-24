import subprocess
import csv
import tkinter as tk
from tkinter import filedialog

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode()

def get_contact_data():
    contact_command = "adb shell content query --uri content://contacts/phones/ --projection display_name:number"
    contact_output, contact_error = execute_command(contact_command)
    if contact_error:
        print("Error retrieving contact data:", contact_error)
        return None
    else:
        return contact_output

def save_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for line in data.splitlines():
            writer.writerow(line.split(','))

# Get contact data
contact_data = get_contact_data()

if contact_data:
    # Create GUI window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt user to select the file path
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save CSV file")

    if file_path:
        # Save to CSV file if the user selected a file path
        save_to_csv(file_path, contact_data)
        print("Contacts saved to", file_path)
    else:
        print("No file selected. Exiting...")
else:
    print("No contact data retrieved. Exiting...")
