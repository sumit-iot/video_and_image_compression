import json
import os
from PIL import Image

#loading data from config.json
with open("config.json", "r") as f:
    config = json.load(f)

print(config['new_size_ratio'])


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_img(image_name, new_size_ratio=config['new_size_ratio'], quality=config['quality'], width=config['width'], height=config['height'], to_jpg=True):
    print(new_size_ratio,quality,width,height)
    # load the image to memory
    img = Image.open(image_name)
    # print the original image shape
    print("[*] Image shape:", img.size)
    # get the original image size in bytes
    image_size = os.path.getsize(image_name)
    # print the size before compression/resizing
    print("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio == 1.0:
        # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    elif width and height:
        # if width and height are set, resize with them instead
        img = img.resize((width, height), Image.ANTIALIAS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name

    new_filename ='a_compress.jpg' 
    a=config['output_file_image'] + new_filename
    # save the image with the corresponding quality and optimize set to True
    img.save(f"{config['output_file_image']}/a.jpg", quality=quality, optimize=True)
    print("[+] New file saved:", new_filename)
# calling the function
compress_img(config['input_file_image'])