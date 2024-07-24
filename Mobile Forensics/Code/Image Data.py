import os
from tkinter import Tk, filedialog
from PIL import Image
import json

def select_image_file():
    root = Tk()
    root.withdraw()
    image_file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    return image_file_path

def select_output_directory():
    root = Tk()
    root.withdraw()
    output_directory = filedialog.askdirectory(title="Select Output Directory")
    return output_directory

def decode_location(location_bytes):
    try:
        # Strip null bytes from the end of the byte string
        location_bytes = location_bytes.rstrip(b'\x00')
        
        # Decode the location bytes to string
        location_string = location_bytes.decode("utf-8")
        
        # Parse the JSON-like string
        location_json = json.loads(location_string)
        
        # Extract relevant information
        night_flag = location_json.get("nightFlag", "Unknown")
        night_mode = location_json.get("nightMode", "Unknown")
        iso = location_json.get("iso", "Unknown")
        exp_time = location_json.get("expTime", "Unknown")
        feature_type = location_json.get("featuretype", "Unknown")
        hdr_scope = location_json.get("hdrscope", "Unknown")
        ai_deblur = location_json.get("aiDeblur", "Unknown")
        
        # Construct the location details string
        location_details = f"Night Flag: {night_flag}, Night Mode: {night_mode}, ISO: {iso}, Exposure Time: {exp_time}, Feature Type: {feature_type}, HDR Scope: {hdr_scope}, AI Deblur: {ai_deblur}"
        
        return location_details
    except Exception:
        return "Unknown"

def save_image_details_to_file(image_file_path, output_directory):
    try:
        # Open the image
        image = Image.open(image_file_path)
        
        # Get image details
        width, height = image.size
        format = image.format
        mode = image.mode
        dpi = image.info.get("dpi", "Unknown")
        
        # Check if EXIF data is available
        exif_data = image._getexif()
        device = "Unknown"
        location = "Unknown"
        taken_time = "Unknown"
        if exif_data:
            device = exif_data.get(0x0110, "Unknown")  # Device make
            location_bytes = exif_data.get(0x927C, b"Unknown")  # GPS location
            location = decode_location(location_bytes)
            
            # Extract photo taken time (if available)
            taken_time_tag = exif_data.get(0x9003)
            if taken_time_tag:
                taken_time = taken_time_tag
        
        # Prepare image details
        details = []
        details.append(f"File: {os.path.basename(image_file_path)}")
        details.append(f"Location: {location}")
        details.append(f"Device: {device}")
        details.append(f"Photo Taken Time: {taken_time}")
        details.append(f"Dimensions: {width}x{height} pixels")
        details.append(f"Format: {format}")
        details.append(f"Mode: {mode}")
        details.append(f"DPI: {dpi}")
        
        # Write image details to file
        output_file_path = os.path.join(output_directory, "image_details.txt")
        with open(output_file_path, "w") as file:
            for detail in details:
                file.write(detail + "\n")
        
        print(f"Image details saved to {output_file_path}")
        
        # Print raw location data
        print("Raw Location Data:", location_bytes)
        
    except Exception as e:
        print(f"Failed to open image: {e}")

def main():
    image_file_path = select_image_file()
    if image_file_path:
        output_directory = select_output_directory()
        if output_directory:
            save_image_details_to_file(image_file_path, output_directory)

if __name__ == "__main__":
    main()
