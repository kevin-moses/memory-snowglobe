import os
import zipfile
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


data_dir = '../data/photo_data_resized'

# Convert jpg and jpeg to png
# Process jpg/jpeg files one at a time
def convert_jpg_to_png(data_dir):
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.jpg', '.jpeg']:
                jpg_path = os.path.join(root, file)
                png_path = os.path.splitext(jpg_path)[0] + '.png'
                
                try:
                    # Convert single image
                    with Image.open(jpg_path) as img:
                        img.save(png_path, 'PNG')
                    
                    # Remove original after successful conversion
                    os.remove(jpg_path)
                    logger.info(f"Converted {jpg_path} to PNG")
                    
                except Exception as e:
                    logger.error(f"Error converting {jpg_path}: {str(e)}")

def remove_non_512_files(data_dir):
    output_dir = '../data/photo_data_512'
    # os.makedirs(output_dir, exist_ok=True)
    print(data_dir)
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png']:
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        if img.size == (512, 512):
                            output_path = os.path.join(output_dir, os.path.splitext(file)[0] + '.png')
                            img.save(output_path, 'PNG')
                            logger.info(f"Saved 512x512 file to: {output_path}")
                        else:
                            logger.info(f"Skipping non-512x512 file: {file_path}")
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")

remove_non_512_files(data_dir)