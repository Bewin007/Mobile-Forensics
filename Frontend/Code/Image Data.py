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
        taken_time = "Unknown"
        if exif_data:
            device = exif_data.get(0x0110, "Unknown")  # Device make
            
            # Extract photo taken time (if available)
            taken_time_tag = exif_data.get(0x9003)
            if taken_time_tag:
                taken_time = taken_time_tag
        
        # Prepare image details
        details = []
        details.append(f"File: {os.path.basename(image_file_path)}")
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
