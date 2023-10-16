import subprocess
import re

from common.custom_logger import logger
from common.image_comparator import CompareImage
from common import adb_utils as adbutil
from common import image_utils as imgutil
from common import constants as const


def are_images_similar(emulator_device, first_image, second_image, threshold):
    image_difference = CompareImage(first_image, second_image).compare_image()
    logger.debug(
        f"{adbutil.full_name(emulator_device)}: Compared "
        f"({first_image.split('/')[-1]}) X ({second_image.split('/')[-1]}) difference: {image_difference}")
    return image_difference < threshold


def get_text_from_image(image_path, config="--psm 8"):
    tesseract_command = f"tesseract {image_path} stdout {config}"
    result = subprocess.run(tesseract_command, shell=True, capture_output=True)\
        .stdout\
        .decode()\
        .replace("\n", "")\
        .replace("\t", "")\
        .replace(" ", "")\
        .replace(",", ".")

    if result == "":
        logger.debug(f"No text found in {image_path}")

    return result


def doubledot_number_to_seconds(number_with_doubledot):
    return (int(number_with_doubledot.split(":")[0]) * 60) + int(number_with_doubledot.split(":")[1])


def get_number_from_image(image_path):
    imgutil.enhance_contrast(image_path, imgutil.get_contrasted_image_path(image_path))
    imgutil.enhance_number_image(imgutil.get_contrasted_image_path(image_path), imgutil.get_enhanced_image_path(image_path))

    image_paths = [imgutil.get_enhanced_image_path(image_path), imgutil.get_contrasted_image_path(image_path), image_path]
    for image_pth in image_paths:
        for psm_try in const.PSM_CONFIG:
            text = get_text_from_image(image_pth, f"--psm {psm_try} -c tessedit_char_whitelist=0123456789,qQ:")
            logger.debug(f"{image_path} IS {text}")
            # sometimes text contains dot at the end
            if text != "" and len(text) > 1:
                if text[-1] == "." or text[-1] == ":":
                    text = text[:-1]

                for number4 in ["q", "Q"]:
                    if number4 in text:
                        return text.replace(number4, "4")

                if "." in text:
                    return float(re.match(r'(?P<decimal>\d+\.\d+)', text).group('decimal'))
                if ":" in text:
                    return doubledot_number_to_seconds(text)
                if is_number(text):
                    return int(''.join(filter(str.isdigit, text)))
                else:
                    logger.debug(f"Failed parse number {text}")
                    exit(1)

        exit(1)


def get_raw_text_from_image(image_path, allowed_chars="-c tessedit_char_whitelist=0123456789,:"):
    imgutil.enhance_contrast(image_path, imgutil.get_contrasted_image_path(image_path))
    imgutil.enhance_number_image(imgutil.get_contrasted_image_path(image_path), imgutil.get_enhanced_image_path(image_path))

    text = ""

    image_paths = [imgutil.get_enhanced_image_path(image_path), imgutil.get_contrasted_image_path(image_path)]
    for image_pth in image_paths:
        for psm_try in const.PSM_CONFIG:
            text = get_text_from_image(image_pth, f"--psm {psm_try} {allowed_chars}")
            if text != "" and len(text) > 1:
                return text

    return text


def get_close_ad_text(image_path, config_psm):
    return get_text_from_image(image_path, f"--psm {config_psm}")


def is_number(s):
    try:
        float(s)  # Attempt to convert the string to a float
        return True
    except ValueError:
        return False
