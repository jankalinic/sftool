import adbutils
import subprocess
import time

import constants as const
from custom_logger import logger
from image_comparator import CompareImage


def check_cli_tools_installed():
    try:
        adb_command = "adb --version"
        result = subprocess.run(adb_command, shell=True, capture_output=True)
        if "Android Debug Bridge" in str(result.stdout):
            logger.debug("ADB is installed.")
        else:
            raise Exception
    except Exception:
        logger.warning("ADB is not installed. Please use: brew install android-platform-tools")
        exit(1)

    try:
        convert_command = "convert --version"
        result = subprocess.run(convert_command, shell=True, capture_output=True)
        if "Version: ImageMagick" in str(result.stdout):
            logger.debug("Convert is installed.")
        else:
            raise Exception
    except Exception:
        logger.warning("Convert is not installed. Please install")
        exit(1)


def is_emulator_attached(emulator_device):
    if emulator_device.info[const.STATE_KEY] == "device":
        logger.debug(f"[{emulator_device.serial}] is attached")
        return True
    else:
        logger.error(f"[{emulator_device.serial}] IS OFFLINE")
        exit(1)


def get_adb_client():
    return adbutils.AdbClient(host="127.0.0.1", port=5037)


def to_box(dimensions):
    return dimensions['left'], dimensions['top'], dimensions['right'], dimensions['bottom']


def get_screenshot_path(emulator_device):
    return const.SCREENSHOT_PATH_PREFIX + emulator_device.serial + const.IMAGE_EXTENSION


def get_cropped_screenshot_path(emulator_device, suffix=""):
    suffix = "-" + suffix if suffix != "" else ""
    return const.CROPPED_SCREENSHOT_PATH_PREFIX + emulator_device.serial + suffix + const.IMAGE_EXTENSION


def take_screenshot(emulator_device):
    logger.info(f"[{emulator_device.serial}] Taking a screenshot")

    start_time = time.time()

    adb_command = f"adb -s {emulator_device.serial} exec-out screencap -p > {get_screenshot_path(emulator_device)}"
    subprocess.run(adb_command, shell=True, check=True)

    logger.debug(f"[{emulator_device.serial}] Execution of sceenshot took: {time.time() - start_time:.6f} seconds")


def crop_screenshot(emulator_device, dimensions, suffix):
    logger.debug(f"[{emulator_device.serial}] Cropping a screenshot")
    start_time = time.time()

    # Image.open(get_screenshot_path(emulator_device)).crop(to_box(dimensions)).save(get_cropped_screenshot_path(emulator_device))
    crop_cmd = f"convert {get_screenshot_path(emulator_device)} -crop {dimensions['right'] - dimensions['left']}x{dimensions['bottom'] - dimensions['top']}+{dimensions['left']}+{dimensions['top']} {get_cropped_screenshot_path(emulator_device, suffix)}"
    subprocess.run(crop_cmd, shell=True, check=True)

    logger.debug(f"[{emulator_device.serial}] Execution of cropping took: {time.time() - start_time:.6f} seconds")


def are_images_similar(emulator_device, first_image, second_image, threshhold):
    start_time = time.time()  # Record the start time

    compare_image = CompareImage(first_image, second_image)
    image_difference = compare_image.compare_image()
    logger.debug(f"[{emulator_device.serial}]: Compared ({first_image.split('/')[-1]}) X ({second_image.split('/')[-1]}) difference: {image_difference}")

    logger.debug(f"[{emulator_device.serial}]: Execution of comparing took: {time.time() - start_time:.6f} seconds")

    return image_difference < threshhold
