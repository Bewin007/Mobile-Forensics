import subprocess

# Execute the adb shell command to reboot the device and capture the output
result = subprocess.run(["adb", "shell", "reboot"], capture_output=True)

# Decode the output to handle it as a string
output = result.stdout.decode()