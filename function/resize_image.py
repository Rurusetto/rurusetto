from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import pathlib

"""Code to resize image to make the website performance better. Just out this file in image folder and run."""

# Get current path to the current folder
current_path = pathlib.Path().resolve()
print(f"Current path : {current_path}")

# Get a list of file in the folder
picture_file_list = [f for f in listdir(current_path) if isfile(join(current_path, f))]
# Remove its own
# If you have more file that is not image just add it here.
picture_file_list.remove("resize_image.py")
print(f"Picture list to resize : {picture_file_list}")

print()

converted = 0  # Count the image that converted

# Resize image process
for image in picture_file_list:
    print(f"Start resize {image}")
    file_path = os.path.abspath(image)
    img = Image.open(file_path)
    print(f"Full path : {os.path.abspath(image)}")
    if img.height > 1080 or img.width > 1920:
        img.thumbnail((1920, 1080))
        img.save(file_path)
        print(f"Saved converted picture to {file_path}")
        converted += 1

print()
print(f"Converted {converted} images!")