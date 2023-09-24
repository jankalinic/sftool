import os

import adbutils
import subprocess
import time
from PIL import Image, ImageEnhance
import pytesseract

from common import constants as const
from common.custom_logger import logger
from common.image_comparator import CompareImage


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
    logger.debug(f"[{emulator_device.serial}] Cropping a screenshot {suffix}")
    start_time = time.time()

    # Image.open(get_screenshot_path(emulator_device)).crop(to_box(dimensions)).save(get_cropped_screenshot_path(emulator_device))
    crop_cmd = f"convert {get_screenshot_path(emulator_device)} -crop {dimensions['right'] - dimensions['left']}x{dimensions['bottom'] - dimensions['top']}+{dimensions['left']}+{dimensions['top']} {get_cropped_screenshot_path(emulator_device, suffix)}"
    subprocess.run(crop_cmd, shell=True, check=True)

    logger.debug(f"[{emulator_device.serial}] Execution of cropping took: {time.time() - start_time:.6f} seconds")


def are_images_similar(emulator_device, first_image, second_image, threshold):
    start_time = time.time()  # Record the start time

    compare_image = CompareImage(first_image, second_image)
    image_difference = compare_image.compare_image()
    logger.debug(f"[{emulator_device.serial}]: Compared ({first_image.split('/')[-1]}) X ({second_image.split('/')[-1]}) difference: {image_difference}")

    logger.debug(f"[{emulator_device.serial}]: Execution of comparing took: {time.time() - start_time:.6f} seconds")

    return image_difference < threshold


def crop_menu_button(emulator_device):
    crop_screenshot(emulator_device, const.MENU_BUTTON_IMAGE_DIMENSIONS, const.MENU_BUTTON_SUFFIX)


def is_in_tavern(emulator_device):
    logger.debug(f"[{emulator_device.serial}]: Looking for menu button")

    if are_images_similar(emulator_device,
                           get_cropped_screenshot_path(emulator_device, const.MENU_BUTTON_SUFFIX),
                           const.ORIGINAL_MENU_BUTTON_NOTIFICATION_IMAGE_PATH,
                           const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD):
        logger.debug(f"[{emulator_device.serial}]: You have a notification")

        return True

    return are_images_similar(emulator_device,
                              get_cropped_screenshot_path(emulator_device, const.MENU_BUTTON_SUFFIX),
                              const.ORIGINAL_MENU_BUTTON_IMAGE_PATH,
                              const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)


def get_npc_image_path(npc_name):
    return os.path.join(const.ORIGINAL_NPC_DIR_PATH, npc_name) + const.IMAGE_EXTENSION


def get_contrasted_image_path(image_path):
    return image_path.split(const.IMAGE_EXTENSION)[0] + "_contrasted" + const.IMAGE_EXTENSION


def enhance_image_contrast(image_path):
    start_time = time.time()
    image = Image.open(image_path)
    im_output = ImageEnhance.Contrast(image).enhance(3)
    im_output.save(get_contrasted_image_path(image_path))
    logger.debug(f"Execution of contrast enhancing: {time.time() - start_time:.6f} seconds")


def get_number_from_image(image_path):

    # enhance_image_contrast(image_path)
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config='--psm 6')
    text = text.replace("\n", "")

    if "," in text:
        numeric_text = text.replace(",", ".")
        return float(numeric_text)

    elif "." in text:
        return float(text)

    elif ":" in text:
        numeric_text = text.split(":")
        return (int(numeric_text[0]) * 60) + int(numeric_text[1])

    else:
        return int(''.join(filter(str.isdigit, text)))


def is_in_quest_selection(emulator_device):
    return are_images_similar(emulator_device,
                              get_cropped_screenshot_path(emulator_device, const.ACCEPT_QUEST_BUTTON[const.NAME_KEY]),
                              const.ACCEPT_QUEST_BUTTON[const.PATH_KEY],
                              const.QUEST_DIFF_THRESHOLD)


def go_to_tavern_using_key(emulator_device):
    logger.debug(f"[{emulator_device.serial}]: Pressing 't' to return to tavern")

    # first leave the tavern to exit without clicking on close and then go back using t
    adm_command = f"adb -s {emulator_device.serial} shell input text 'a'"
    subprocess.run(adm_command, shell=True, check=True)
    time.sleep(1)

    adm_command = f"adb -s {emulator_device.serial} shell input text 't'"
    subprocess.run(adm_command, shell=True, check=True)
    time.sleep(1)

    take_screenshot(emulator_device)
    crop_menu_button(emulator_device)

    if not is_in_tavern(emulator_device) or is_in_quest_selection(emulator_device):
        logger.debug(f"[{emulator_device.serial}]: Pressing 't' did not work")
        go_to_tavern_using_key(emulator_device)


def crop_close_ad(emulator_device):
    crop_screenshot(emulator_device, const.CLOSE_AD_DIMENSIONS, const.CLOSE_AD_SUFFIX)


def is_close_ad_present(emulator_device):
    logger.debug(f"[{emulator_device.serial}]: Looking for AD close button")

    for image in const.ORIGINAL_CLOSE_AD_IMAGES_PATHS:
        if are_images_similar(emulator_device,
                                   get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_SUFFIX),
                                   image,
                                   const.CLOSE_AD_DIFF_THRESHOLD):
            # This is redundant check to make sure it's not the main exit button
            if not are_images_similar(emulator_device,
                                        get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_SUFFIX),
                                        const.ORIGINAL_DONT_CLOSE_ADD_BUTTON_IMAGE_PATH,
                                        const.CLOSE_AD_DIFF_THRESHOLD):
                return True
    return False


def click_exit_ad(emulator_device):
    logger.debug(f"[{emulator_device.serial}]: exiting AD")
    emulator_device.click(const.CLOSE_AD_LOCATION[const.X_KEY], const.CLOSE_AD_LOCATION[const.Y_KEY])


def close_ad_if_playing(emulator_device):
    logger.debug(f"[{emulator_device.serial}]: close ad if playing")
    take_screenshot(emulator_device)
    crop_close_ad(emulator_device)

    if is_close_ad_present(emulator_device):
        logger.debug(f"[{emulator_device.serial}]: closing ad")
        click_exit_ad(emulator_device)
        time.sleep(2)
        close_ad_if_playing(emulator_device)
    else:
        logger.debug(f"[{emulator_device.serial}]: ad is not playing")
        crop_menu_button(emulator_device)
        if is_in_tavern(emulator_device):
            logger.debug(f"[{emulator_device.serial}]: is in tavern")


def clean_directory(directory_path):
    try:
        # List all files and subdirectories in the directory
        items = os.listdir(directory_path)

        # Loop through each item in the directory
        for item in items:
            item_path = os.path.join(directory_path, item)

            # Check if it's a file and delete it
            if os.path.isfile(item_path):
                os.remove(item_path)

            # Check if it's a subdirectory and recursively clean it
            elif os.path.isdir(item_path):
                clean_directory(item_path)

        logger.debug(f"Directory cleaned: {directory_path}")

    except Exception as e:
        logger.error(f"An error occurred while cleaning the directory: {e}")


def clean_screenshots():
    clean_directory(const.SCREENSHOT_DIR_PATH)