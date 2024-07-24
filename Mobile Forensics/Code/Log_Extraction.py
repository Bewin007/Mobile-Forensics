import subprocess
from tkinter import filedialog, Tk

def is_device_connected():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
        output = result.stdout.strip().split('\n')
        return len(output) > 1  # Check if there are any devices listed (excluding the header)
    except subprocess.CalledProcessError as e:
        print("Error checking device connection:", e)
        return False

def extract_logs():
    if not is_device_connected():
        print("Device is not connected. Cannot extract logs.")
        return
    
    try:
        # Run the adb logcat command to capture the device logs
        result = subprocess.run(['adb', 'logcat', '-d'], capture_output=True)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            stdout = result.stdout
            if stdout is not None:
                stdout = stdout.decode('utf-8')  # Decode the binary output using UTF-8 encoding
                
                # Prompt the user to select the file path to save the logs
                root = Tk()
                root.withdraw()  # Hide the main window
                
                file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                          title="Save Device Logs As")
                root.destroy()  # Destroy the root window
                
                # Save the logs to the selected file path
                if file_path:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(stdout)
                    
                    print("Device logs extracted successfully and saved to:", file_path)
                else:
                    print("No file selected. Device logs not saved.")
            else:
                print("No output received. Device logs not saved.")
        else:
            print("Failed to extract device logs.")
    
    except FileNotFoundError:
        print("ADB is not installed or not in the system PATH.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

# Call the function to extract the logs
extract_logs()
