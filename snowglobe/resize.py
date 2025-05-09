from PIL import Image, ImageOps
import os

input_dir = "../data/photo_data"
output_dir = "../data/photo_data_resized"
os.makedirs(output_dir, exist_ok=True)

def resize_with_crop(img, target_size):
    # Get current dimensions
    width, height = img.size
    
    # Calculate aspect ratios
    aspect = width / height
    target_aspect = target_size[0] / target_size[1]
    
    # Determine dimensions to scale to
    if aspect > target_aspect:
        # Image is wider than target
        new_height = target_size[1]
        new_width = int(new_height * aspect)
    else:
        # Image is taller than target
        new_width = target_size[0]
        new_height = int(new_width / aspect)
    
    # Resize while maintaining aspect ratio
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Calculate cropping box
    left = (new_width - target_size[0]) // 2
    top = (new_height - target_size[1]) // 2
    right = left + target_size[0]
    bottom = top + target_size[1]
    
    # Crop to target size
    return img_resized.crop((left, top, right, bottom))

# Main loop
for img_name in os.listdir(input_dir):
    img_path = os.path.join(input_dir, img_name)
    with Image.open(img_path) as img:
        img = ImageOps.exif_transpose(img)
        img_resized = resize_with_crop(img, (512, 512))
        # Check if resized image is 512x512
        if img_resized.size != (512, 512):
            continue
        output_path = os.path.join(output_dir, os.path.splitext(img_name)[0] + '.png')
        img_resized.save(output_path, format='PNG')