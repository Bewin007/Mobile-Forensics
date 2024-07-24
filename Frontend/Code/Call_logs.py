import subprocess
import csv
import tkinter as tk
from tkinter import filedialog

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode()

def get_call_logs():
    call_logs_command = "adb shell content query --uri content://call_log/calls"
    call_logs_output, call_logs_error = execute_command(call_logs_command)
    if call_logs_error:
        print("Error retrieving call logs:", call_logs_error)
        return None
    else:
        return call_logs_output

def save_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for line in data.splitlines():
            writer.writerow(line.split(','))

# Get call logs
call_logs_data = get_call_logs()

if call_logs_data:
    # Create GUI window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt user to select the file path
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save CSV file")

    if file_path:
        # Save to CSV file if the user selected a file path
        save_to_csv(file_path, call_logs_data)
        print("Call logs saved to", file_path)
    else:
        print("No file selected. Exiting...")
else:
    print("No call logs retrieved. Exiting...")
