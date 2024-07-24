import subprocess
import tkinter as tk
from tkinter import filedialog

# Function to execute a shell command
def execute_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output.decode(), error.decode()
    except Exception as e:
        print("Error executing command:", e)
        return None, str(e)

# Function to retrieve SMS logs from the device
def get_sms_logs():
    try:
        sms_logs_command = "adb shell content query --uri content://sms/inbox --projection date,address,body"
        sms_logs_output, error = execute_command(sms_logs_command)
        if error:
            raise Exception(error)
        return sms_logs_output
    except Exception as e:
        print("Error retrieving SMS logs:", e)
        return None

# Function to save data to a text file
def save_to_text(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as text_file:
            text_file.write(data)
        print("SMS logs saved to", filename)
    except Exception as e:
        print("Error saving SMS logs to file:", e)

# Function to check if the device is connected
def is_device_connected():
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        output = result.stdout.strip().split("\n")
        return len(output) > 1  # Check if any devices are listed (excluding the header)
    except subprocess.CalledProcessError as e:
        print("Error checking device connection:", e)
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False

# Main function
def main():
    try:
        if not is_device_connected():
            print("Device is not connected. Exiting...")
            return

        # Get SMS logs
        sms_logs_data = get_sms_logs()

        if sms_logs_data:
            # Create GUI window
            root = tk.Tk()
            root.withdraw()  # Hide the main window

            # Prompt user to select the file path
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save Text file")

            if file_path:
                # Save to text file if the user selected a file path
                save_to_text(file_path, sms_logs_data)
            else:
                print("No file selected. Exiting...")
        else:
            print("Failed to retrieve SMS logs. Exiting...")
    except Exception as e:
        print("An error occurred during execution:", e)

if __name__ == "__main__":
    main()
