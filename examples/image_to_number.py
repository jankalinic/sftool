import os
import time
from PIL import Image, ImageEnhance
import pytesseract
import threading

import common.constants as const


def enhance_image_contrast(image_path):
    start_time = time.time()
    # image brightness enhancer
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)

    factor = 3  # increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save(image_path.split(const.IMAGE_EXTENSION)[0] + "_contrasted" + const.IMAGE_EXTENSION)
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time
    print(f"Execution of contrast enhancing: {execution_time:.6f} seconds")


def get_number_from_image(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Use pytesseract to perform OCR on the image
    text = pytesseract.image_to_string(image, config='--psm 6')

    if "," in text:
        numeric_text = text.replace("\n", "").replace(",", ".")
        return float(numeric_text)

    elif ":" in text:
        numeric_text = text.replace("\n", "").split(":")
        return (int(numeric_text[0]) * 60) + int(numeric_text[1])

    else:
        return int(''.join(filter(str.isdigit, text)))


if __name__ == '__main__':
    IMAGE_PATH = os.path.join(const.SFTOOL_DIR_PATH, "examples", "images", "crop_gold_image_with_number.png")
    # IMAGE_PATH = '/Users/jkalinic-mac/sftool/common/../images/screenshots/cropped-emulator-5556-gold-number_contrasted.png'
    # whole => x:136 y:1243 - x:313 y:1465 = 180x222 left:130 top:1243
    # gold => y = 1243 - 1292 = 180x49 ==== 180x49+136+1243
    # exp => y= 1316 - 1386 = 180x49 ==== 180x49+136+1316
    start_time = time.time()
    number = get_number_from_image(IMAGE_PATH)
    print(f"Extracted number: {number}")
    print(f"Execution of number recognition took: {time.time() - start_time:.6f} seconds")
    # ------------------------

    enhance_image_contrast(IMAGE_PATH)

    start_time = time.time()
    number = get_number_from_image(IMAGE_PATH)
    print(f"Extracted number: {number}")
    print(f"Execution of number recognition took: {time.time() - start_time:.6f} seconds")