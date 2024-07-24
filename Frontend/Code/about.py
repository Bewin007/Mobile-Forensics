import subprocess
import tkinter as tk
from tkinter import filedialog
import datetime

def run_adb_command(command):
    try:
        process = subprocess.Popen(['adb'] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        if process.returncode == 0:
            return output.decode().strip()
        else:
            print("Error executing adb command:", error.decode())
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def extract_device_info():
    info = {}
    
    # Get device model
    model = run_adb_command(['shell', 'getprop', 'ro.product.model'])
    info['Model'] = model if model else 'Unknown'
    
    # Get manufacturer (brand)
    manufacturer = run_adb_command(['shell', 'getprop', 'ro.product.brand'])
    info['Manufacturer'] = manufacturer if manufacturer else 'Unknown'

    # Get Android version
    android_version = run_adb_command(['shell', 'getprop', 'ro.build.version.release'])
    info['Android Version'] = android_version if android_version else 'Unknown'
    
    # Get OS type (usually "Android")
    info['OS Type'] = 'Android'

     # Get baseband version
    baseband_version = run_adb_command(['shell', 'getprop', 'gsm.version.baseband'])
    info['Baseband Version'] = baseband_version if baseband_version else 'Unknown'

     # Get last Android version update date
    last_update_utc = run_adb_command(['shell', 'getprop', 'ro.build.date.utc'])
    if last_update_utc:
        last_update_timestamp = int(last_update_utc)
        last_update_date = datetime.datetime.utcfromtimestamp(last_update_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
    else:
        last_update_date = 'Unknown'
    
    info['Last Android Update'] = last_update_date
    
    # Get legal information (e.g., build number, security patch level)
    build_number = run_adb_command(['shell', 'getprop', 'ro.build.display.id'])
    security_patch_level = run_adb_command(['shell', 'getprop', 'ro.build.version.security_patch'])
    info['Build Number'] = build_number if build_number else 'Unknown'
    info['Security Patch Level'] = security_patch_level if security_patch_level else 'Unknown'

    # Get device ID
    device_id = run_adb_command(['devices', '-l'])
    info['Device ID'] = device_id.split()[0] if device_id else 'Unknown'

     # Get kernel version
    kernel_version = run_adb_command(['shell', 'uname', '-r'])
    info['Kernel Version'] = kernel_version if kernel_version else 'Unknown'

     # Get hardware version
    hardware_version = run_adb_command(['shell', 'getprop', 'ro.hardware'])
    info['Hardware Version'] = hardware_version if hardware_version else 'Unknown'

     # Get processor
    processor = run_adb_command(['shell', 'getprop', 'ro.product.cpu.abi'])
    info['Processor'] = processor if processor else 'Unknown'
    
    # Get MAC address
    mac_address = run_adb_command(['shell', 'cat', '/sys/class/net/wlan0/address'])
    info['MAC Address'] = mac_address if mac_address else 'Unknown'

    # Get last security update
    security_patch_level = run_adb_command(['shell', 'getprop', 'ro.build.version.security_patch'])
    info['Last Security Update'] = security_patch_level if security_patch_level else 'Unknown'

     # Get battery level (in percentage)
    battery_level = run_adb_command(['shell', 'dumpsys', 'battery'])
    if 'level' in battery_level:
        battery_level = battery_level.split('level: ')[1].split(',')[0]
    else:
        battery_level = 'Unknown'
    info['Battery Level (%)'] = battery_level

     # Get IMEI for SIM slot 1 and SIM slot 2
    imei_slot1 = run_adb_command(['shell', 'service', 'call', 'iphonesubinfo', '1'])
    imei_slot2 = run_adb_command(['shell', 'service', 'call', 'iphonesubinfo', '2'])
    info['IMEI SIM Slot 1'] = imei_slot1.split("'")[1] if imei_slot1 else 'Unknown'
    info['IMEI SIM Slot 2'] = imei_slot2.split("'")[1] if imei_slot2 else 'Unknown'

    # Get serial number
    serial_number = run_adb_command(['shell', 'getprop', 'ro.serialno'])
    info['Serial Number'] = serial_number if serial_number else 'Unknown'
    
    # Get uptime
    uptime = run_adb_command(['shell', 'uptime'])
    info['Uptime'] = uptime if uptime else 'Unknown'
    
    # Get SIM card status
    sim_status = run_adb_command(['shell', 'dumpsys', 'telephony.registry'])
    if 'mDataRegState' in sim_status:
        info['SIM Card Status'] = 'Inserted'
    else:
        info['SIM Card Status'] = 'Not Inserted'
    
     # Get battery capacity (requires root)
    battery_capacity = run_adb_command(['shell', 'cat', '/sys/class/power_supply/battery/capacity'])
    info['Battery Capacity'] = battery_capacity if battery_capacity else 'Unknown'
    
    # Get screen size (resolution)
    screen_size = run_adb_command(['shell', 'wm', 'size'])
    info['Screen Size'] = screen_size.split(':')[1].strip() if screen_size else 'Unknown'
    
    # Get RAM size (total memory)
    ram_size = run_adb_command(['shell', 'cat', '/proc/meminfo'])
    for line in ram_size.split('\n'):
        if 'MemTotal' in line:
            ram_size = line.split()[1]
            break
    info['RAM Size'] = f"{ram_size} KB" if ram_size else 'Unknown'
    
    # Get IP address
    ip_address = run_adb_command(['shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0'])
    if ip_address:
        ip_address = ip_address.split('\n')[1].split()[1].split('/')[0]
    else:
        ip_address = 'Unknown'
    info['IP Address'] = ip_address
    
    # Get device manufacture date
    manufacture_date = run_adb_command(['shell', 'getprop', 'ro.build.date'])
    info['Manufacture Date'] = manufacture_date if manufacture_date else 'Unknown'
    
    # Get battery capacity (requires root)
    battery_capacity = run_adb_command(['shell', 'dumpsys', 'battery'])
    info['Battery Capacity'] = battery_capacity.split('\n')[1].split(':')[1].strip() if battery_capacity else 'Unknown'
    
    # Get screen size (resolution)
    screen_size = run_adb_command(['shell', 'wm', 'size'])
    info['Screen Size'] = screen_size.split(':')[1].strip() if screen_size else 'Unknown'
    
    # Get RAM size (total memory)
    ram_size = run_adb_command(['shell', 'cat', '/proc/meminfo'])
    for line in ram_size.split('\n'):
        if 'MemTotal' in line:
            ram_size = line.split()[1]
            break
    info['RAM Size'] = f"{ram_size} KB" if ram_size else 'Unknown'
    
    # Get camera specifications (front and back megapixels)
    # Note: This is a placeholder. The actual implementation may vary depending on the device and Android version
    camera_info = run_adb_command(['shell', 'dumpsys', 'media.camera'])
    info['Camera Front MP'] = 'Unknown'
    info['Camera Back MP'] = 'Unknown'
    
    # Get device status (e.g., charging, discharging)
    device_status = run_adb_command(['shell', 'dumpsys', 'battery'])
    if 'AC powered: true' in device_status:
        status = 'Charging'
    elif 'USB powered: true' in device_status:
        status = 'USB Powered'
    else:
        status = 'Battery Powered'
    info['Device Status'] = status
    
    return info

def save_to_file(data):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
    if file_path:
        try:
            with open(file_path, 'w') as file:
                for key, value in data.items():
                    file.write(f"{key}: {value}\n")
            print(f"Saved device information to {file_path}")
        except Exception as e:
            print("Error saving to file:", e)

if __name__ == "__main__":
    device_info = extract_device_info()
    if device_info:
        save_to_file(device_info)
