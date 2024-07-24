import subprocess
import tkinter as tk
from tkinter import filedialog

def run_adb_command(command):
    try:
        process = subprocess.Popen(['adb'] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            return output.decode().strip()
        else:
            print(f"Error executing adb command ({' '.join(command)}):\n{error.decode()}")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def get_installed_apps():
    try:
        # Execute adb command to list installed packages
        packages = run_adb_command(['shell', 'pm', 'list', 'packages', '-3'])  # '-3' filters out system apps

        if packages:
            # Extract package names from the output
            package_names = [line.split(":")[1] for line in packages.splitlines() if line.startswith("package:")]

            # Get app names by querying their application label
            app_names = []
            for package in package_names:
                app_name_cmd = ['shell', 'dumpsys', 'package', package.strip(), '|', 'grep', 'Application-label:']
                app_name = run_adb_command(app_name_cmd)
                if app_name:
                    app_name = app_name.split(":")[1].strip()
                    app_names.append(app_name)

            return app_names
        else:
            print("No installed apps found.")
            return []
    except Exception as e:
        print("An error occurred:", e)
        return []

def save_to_file(app_names, filename="installed_apps.txt"):
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            with open(file_path, 'w') as file:
                for app_name in app_names:
                    file.write(f"{app_name}\n")
            print(f"Saved {len(app_names)} installed apps to {file_path}")
    except Exception as e:
        print("Error saving to file:", e)

if __name__ == "__main__":
    installed_apps = get_installed_apps()
    if installed_apps:
        save_to_file(installed_apps)
