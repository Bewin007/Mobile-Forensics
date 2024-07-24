import subprocess
import tkinter as tk
from tkinter import filedialog

def is_device_connected():
    try:
        # Run the adb devices command to check if any device is connected
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
        devices_output = result.stdout.strip().split('\n')
        # Check if any device is listed (excluding the header)
        return len(devices_output) > 1
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return False

def extract_logs(package_name):
    try:
        if not is_device_connected():
            print("Device is not connected. Exiting...")
            return

        # Create a Tkinter root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Prompt the user to select the file path using a file dialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")],
                                                  title="Save Log File As")

        # Check if the user canceled the file dialog
        if not file_path:
            print("No file selected. Exiting...")
            return

        # Run the adb logcat command to capture the device logs
        result = subprocess.run(['adb', 'logcat', '-d'], capture_output=True, text=True, encoding='latin1')

        # Check if the command executed successfully
        if result.returncode == 0:
            # Check if any output was captured
            if result.stdout is not None:
                # Split the logcat output by lines
                log_lines = result.stdout.splitlines()

                # Filter logs for the specified package name
                filtered_logs = [line for line in log_lines if package_name in line]

                # Save the filtered logs to the specified file path
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(filtered_logs))

                print("Application logs extracted successfully!")
            else:
                print("No output captured from logcat command.")
        else:
            print("Failed to extract device logs. Error:", result.stderr)

    except FileNotFoundError:
        print("ADB is not installed or not in the system PATH.")
    except Exception as e:
        print("An error occurred:", e)

# Call the function to extract the logs for a specific application
extract_logs("com.whatsapp")  # Replace "com.whatsapp" with the package name of your application
