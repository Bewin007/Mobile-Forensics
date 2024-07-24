import tkinter as tk
from tkinter import filedialog
import subprocess
import csv

# Function to execute adb shell command
def run_adb_command(command):
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error executing ADB command:", e)
        return None

# Function to save data to CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line in data.splitlines():
            writer.writerow(line.split(','))

# Function to check if mobile device is connected
def is_device_connected():
    try:
        result = subprocess.run("adb devices", capture_output=True, text=True, check=True)
        output = result.stdout.strip().split('\n')
        # Check if there are any devices listed (excluding the header)
        return len(output) > 1
    except subprocess.CalledProcessError as e:
        print("Error checking device connection:", e)
        return False

# Function to handle selecting the output folder and getting filename using Tkinter GUI
def select_output_folder_and_filename():
    root = tk.Tk()
    root.withdraw()
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save CSV File"
    )
    
    if filename:
        return filename
    else:
        return None

# Main function to orchestrate the process
def main():
    if not is_device_connected():
        print("Error: Mobile device is not connected.")
        return
    
    filename = select_output_folder_and_filename()

    if filename:
        print("Filename selected:", filename)

        adb_command = "adb shell content query --uri content://com.android.calendar/events"
        output = run_adb_command(adb_command)
        if output:
            save_to_csv(output, filename)
            print("Data saved to", filename)
        else:
            print("No data retrieved.")
    else:
        print("Filename not selected.")

if __name__ == "__main__":
    main()
