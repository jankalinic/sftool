import os
import adbutils
import subprocess
import time
import re
from PIL import Image

from common import constants as const
from common.custom_logger import logger
from common.image_comparator import CompareImage


# -----------------------
# ADB UTILS
def is_emulator_attached(emulator_device):
    if emulator_device.info[const.STATE_KEY] == "device":
        logger.debug(f"[{get_emulator_name(emulator_device.serial)}] is attached")
        return True
    else:
        logger.error(f"[{get_emulator_name(emulator_device.serial)}] IS OFFLINE")
        exit(1)


def get_adb_client():
    return adbutils.AdbClient(host="127.0.0.1", port=5037)


# END ADB UTILS
# -----------------------


# ---------------------------
# OS UTILS
def clean_directory(directory_path):
    try:
        rmrf_command = f"rm -rf {directory_path}/*"
        subprocess.run(rmrf_command, shell=True, check=True)
    except Exception as e:
        logger.error(f"An error occurred while cleaning the directory: {e}")


def clean_screenshots():
    clean_directory(const.SCREENSHOT_DIR_PATH)


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


# END OS UTILS
# ---------------


# ----------------------
# Picture UTILS
def get_screenshot_path(emulator_device):
    return os.path.join(const.SCREENSHOT_DIR_PATH, emulator_device.serial,
                        (const.SCREENSHOT_SUFFIX + const.IMAGE_EXTENSION))


def get_cropped_screenshot_path(emulator_device, suffix=""):
    suffix = const.CROPPED_SUFFIX if suffix == "" else suffix
    return os.path.join(const.SCREENSHOT_DIR_PATH, emulator_device.serial, const.CROPPED_SUFFIX,
                        (suffix + const.IMAGE_EXTENSION))


def check_if_path_exist_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)


def take_screenshot(emulator_device):
    check_if_path_exist_or_create(os.path.dirname(get_screenshot_path(emulator_device)))

    logger.info(f"[{get_emulator_name(emulator_device.serial)}] Taking a screenshot")

    adb_command = f"adb -s {emulator_device.serial} exec-out screencap -p > {get_screenshot_path(emulator_device)}"
    subprocess.run(adb_command, shell=True, check=True)

    time.sleep(0.05)


def crop_screenshot(emulator_device, dimensions, suffix):
    check_if_path_exist_or_create(os.path.dirname(get_cropped_screenshot_path(emulator_device, suffix)))

    logger.debug(f"[{get_emulator_name(emulator_device.serial)}] Cropping a screenshot {suffix}")

    # Image.open(get_screenshot_path(emulator_device)).crop(to_box(dimensions)).save(get_cropped_screenshot_path(emulator_device))
    crop_cmd = f"convert {get_screenshot_path(emulator_device)} -crop {dimensions['right'] - dimensions['left']}x{dimensions['bottom'] - dimensions['top']}+{dimensions['left']}+{dimensions['top']} {get_cropped_screenshot_path(emulator_device, suffix)}"
    subprocess.run(crop_cmd, shell=True, check=True)


# --------------------------
# Compare images
def are_images_similar(emulator_device, first_image, second_image, threshold):
    compare_image = CompareImage(first_image, second_image)
    image_difference = compare_image.compare_image()
    logger.debug(
        f"[{get_emulator_name(emulator_device.serial)}]: Compared "
        f"({first_image.split('/')[-1]}) X ({second_image.split('/')[-1]}) difference: {image_difference}")
    return image_difference < threshold


# END Compare images
# --------------------------


# --------------------------
# OCR UTILS
def get_text_from_image(image_path, config="--psm 8"):
    tesseract_command = f"tesseract {image_path} stdout {config}"
    result = str(subprocess.run(tesseract_command, shell=True, capture_output=True).stdout.decode())

    if result == "":
        logger.debug(f"No text found in {image_path}")

    return result.replace("\n", "").replace("\t", "").replace(" ", "").replace(",", ".")


def text_to_seconds(number_with_doubledot):
    numbers = number_with_doubledot.split(":")
    return (int(numbers[0]) * 60) + int(numbers[1])


def get_number_from_image(image_path, config="--psm {} -c tessedit_char_whitelist=0123456789.,:", psm=8):
    enhance_image_bw(image_path)
    text = get_text_from_image(get_contrasted_image_path(image_path), config.format(psm))

    if "." in text:
        return float(re.match(r'(?P<decimal>\d+\.\d+)', text).group('decimal'))
    elif ":" in text:
        return text_to_seconds(text)
    else:
        if is_number(text):
            return int(''.join(filter(str.isdigit, text)))
        else:
            logger.error(f"[{image_path}] did not have numbers in it with config {config}")
            if psm > 6:
                return get_number_from_image(image_path, config=config, psm=psm - 1)
            exit(1)


def get_close_ad_text(emulator_device, config_psm=6):
    text = get_text_from_image(
        get_contrasted_image_path(get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_BUTTON[const.NAME_KEY])),
        f"--psm {config_psm}")
    if text == "" and config_psm < 10:
        return get_close_ad_text(emulator_device, config_psm=config_psm + 1)
    return text


# END OCR UTILS
# --------------------------


# --------------------------
# QUEST DECISIONS
def crop_quest_progress_bar(emulator_device):
    crop_screenshot(emulator_device, const.QUEST_PROGRESS_BAR[const.DIMENSIONS_KEY],
                    const.QUEST_PROGRESS_BAR[const.NAME_KEY])


def is_in_quest(emulator_device):
    crop_quest_progress_bar(emulator_device)
    is_it = are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device, const.QUEST_PROGRESS_BAR[const.NAME_KEY]),
                               const.QUEST_PROGRESS_BAR[const.PATH_KEY],
                               const.QUEST_PROGRESS_BAR_DIFF_THRESHOLD)

    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: is {'' if is_it else 'NOT'} in quest")
    return is_it


def crop_beer_button(emulator_device):
    crop_screenshot(emulator_device, const.BEER_TAVERN_BUTTON[const.DIMENSIONS_KEY],
                    const.BEER_TAVERN_BUTTON[const.NAME_KEY])


def is_in_tavern(emulator_device):
    # Screen must contain beer + not acceptQuest + not questworm
    crop_beer_button(emulator_device)

    is_it = are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device, const.BEER_TAVERN_BUTTON[const.NAME_KEY]),
                               const.BEER_TAVERN_BUTTON[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD) and \
            not is_in_quest_selection(emulator_device) and \
            not is_in_quest(emulator_device)

    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: is {'' if is_it else 'NOT'} in tavern")
    return is_it


def crop_wallpaper(emulator_device):
    crop_screenshot(emulator_device, const.WALLPAPER_DATA[const.DIMENSIONS_KEY], const.WALLPAPER_DATA[const.NAME_KEY])


def is_in_game(emulator_device):
    crop_wallpaper(emulator_device)
    is_it = not are_images_similar(emulator_device,
                                   get_cropped_screenshot_path(emulator_device, const.WALLPAPER_DATA[const.NAME_KEY]),
                                   const.WALLPAPER_DATA[const.PATH_KEY],
                                   const.WALLPAPER_THRESHOLD)

    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: is {'NOT' if is_it else ''} in sfgame")
    return is_it


def crop_accept_button(emulator_device):
    crop_screenshot(emulator_device, const.ACCEPT_QUEST_BUTTON[const.DIMENSIONS_KEY],
                    const.ACCEPT_QUEST_BUTTON[const.NAME_KEY])


def is_in_quest_selection(emulator_device):
    crop_accept_button(emulator_device)
    is_it = are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device, const.ACCEPT_QUEST_BUTTON[const.NAME_KEY]),
                               const.ACCEPT_QUEST_BUTTON[const.PATH_KEY],
                               const.QUEST_DIFF_THRESHOLD)

    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: is {'' if is_it else 'NOT'} in quest select")
    return is_it


def crop_close_ad(emulator_device):
    crop_screenshot(emulator_device, const.CLOSE_AD_BUTTON[const.DIMENSIONS_KEY], const.CLOSE_AD_BUTTON[const.NAME_KEY])


def is_close_ad_present(emulator_device):
    crop_close_ad(emulator_device)
    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: Looking for AD close button")

    # Check corner image if its SF close button
    if are_images_similar(emulator_device,
                          get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_BUTTON[const.NAME_KEY]),
                          const.DONT_CLOSE_AD_BUTTON[const.PATH_KEY],
                          const.CLOSE_AD_DIFF_THRESHOLD):
        logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: there is only DO NOT CLOSE button")
        return False

    # Continue searching corner using text => ad close should contain X text
    enhance_image_bw(get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_BUTTON[const.NAME_KEY]))
    text = get_close_ad_text(emulator_device)

    # Search for chars that are acceptable as detected X
    for char in const.CLOSE_BUTTON_WHITELIST_STRING:
        if char in text:
            logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: close ad found by char: {char}")
            return True

    logger.debug(
        f"[{get_emulator_name(emulator_device.serial)}]: X in ad not found as a text, checking for saved images of close ad buttons")

    for image in const.LIST_OF_CLOSEBUTTONS:
        if are_images_similar(emulator_device,
                              get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_BUTTON[const.NAME_KEY]),
                              os.path.join(const.ORIGINAL_ADS_CLOSE_BUTTONS_DIR_PATH, image),
                              const.CLOSE_AD_DIFF_THRESHOLD):
            logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: close ad found by image")
            return True

    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: close ad not found by any way")
    return False


def crop_quest(emulator_device, selected_quest):
    crop_screenshot(emulator_device, selected_quest[const.DIMENSIONS_KEY], selected_quest[const.NAME_KEY])


def is_selected_correct_quest(emulator_device, quest_num):
    selected_quest = const.QUEST_LIST[quest_num]

    take_screenshot(emulator_device)
    crop_quest(emulator_device, selected_quest)

    is_it = are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device, selected_quest[const.NAME_KEY]),
                               selected_quest[const.PATH_KEY],
                               const.QUEST_TIERS_DIFF_THRESHOLD)

    logger.debug(
        f"[{get_emulator_name(emulator_device.serial)}]: current "
        f"quest:{selected_quest[const.NAME_KEY]} is {'' if is_it else 'in'}correctly selected")
    return is_it


def crop_tavern_master(emulator_device):
    crop_screenshot(emulator_device, const.TAVERN_MASTER[const.DIMENSIONS_KEY], const.TAVERN_MASTER[const.NAME_KEY])


def is_enough_thirst(emulator_device):
    crop_tavern_master(emulator_device)
    is_it = not are_images_similar(emulator_device,
                                   const.TAVERN_MASTER[const.PATH_KEY],
                                   get_cropped_screenshot_path(emulator_device, const.TAVERN_MASTER[const.NAME_KEY]),
                                   const.NPC_THRESHOLD)

    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: {'' if is_it else 'NOT'}enough thirst")
    return is_it


def crop_quest_ad(emulator_device):
    crop_screenshot(emulator_device, const.QUEST_AD[const.DIMENSIONS_KEY], const.QUEST_AD[const.NAME_KEY])
    crop_screenshot(emulator_device, const.QUEST_AD_WO_HOURGLASS[const.DIMENSIONS_KEY],
                    const.QUEST_AD_WO_HOURGLASS[const.NAME_KEY])


def is_quest_skipable_with_ad(emulator_device):
    crop_quest_ad(emulator_device)

    is_it = are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device, const.QUEST_AD[const.NAME_KEY]),
                               const.QUEST_AD[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD) or \
            are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device,
                                                           const.QUEST_AD_WO_HOURGLASS[const.NAME_KEY]),
                               const.QUEST_AD_WO_HOURGLASS[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)

    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: Quest is {'' if is_it else 'NOT'} skippable with free ad")
    return is_it


def crop_quest_done(emulator_device):
    crop_screenshot(emulator_device, const.QUEST_DONE_OK_BUTTON[const.DIMENSIONS_KEY],
                    const.QUEST_DONE_OK_BUTTON[const.NAME_KEY])


def is_quest_done(emulator_device):
    crop_quest_done(emulator_device)
    is_it = are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device, const.QUEST_DONE_OK_BUTTON[const.NAME_KEY]),
                               const.QUEST_DONE_OK_BUTTON[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)

    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: Quest is {'already' if is_it else 'not yet'} done")
    return is_it


def crop_new_level(emulator_device):
    crop_screenshot(emulator_device, const.NEW_LEVEL_OK_BUTTON[const.DIMENSIONS_KEY],
                    const.NEW_LEVEL_OK_BUTTON[const.NAME_KEY])


def is_new_level_accept_present(emulator_device):
    crop_new_level(emulator_device)
    is_it = are_images_similar(emulator_device,
                               get_cropped_screenshot_path(emulator_device, const.NEW_LEVEL_OK_BUTTON[const.NAME_KEY]),
                               const.NEW_LEVEL_OK_BUTTON[const.PATH_KEY],
                               const.NEW_LEVEL_THRESHOLD)

    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: New level button is {'' if is_it else 'not'} present")
    return is_it


def crop_beer_mushroom_button(emulator_device):
    crop_screenshot(emulator_device,
                    const.DRINK_BEER_MUSHROOM_BUTTON[const.DIMENSIONS_KEY],
                    const.DRINK_BEER_MUSHROOM_BUTTON[const.NAME_KEY])


def can_drink_more(emulator_device, can_use_mushrooms):
    if can_use_mushrooms:
        crop_beer_mushroom_button(emulator_device)

        if are_images_similar(emulator_device,
                              const.DRINK_BEER_MUSHROOM_BUTTON[const.PATH_KEY],
                              get_cropped_screenshot_path(emulator_device,
                                                          const.DRINK_BEER_MUSHROOM_BUTTON[const.NAME_KEY]),
                              const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD):
            return True

        logger.info(f"[{get_emulator_name(emulator_device.serial)}]: Not drinking beer, the mushroom button is not present.")
    else:
        logger.info(f"[{get_emulator_name(emulator_device.serial)}]: Not drinking beer, if you want, set CAN_USE_MUSHROOMS to True")

    return False


# END QUEST DECISIONS
# ------------------


# ------------------
# Crop quest data
def crop_gold(emulator_device):
    crop_screenshot(emulator_device, const.GOLD_DATA[const.DIMENSIONS_KEY], const.GOLD_DATA[const.NAME_KEY])


def crop_exp(emulator_device):
    crop_screenshot(emulator_device, const.EXP_DATA[const.DIMENSIONS_KEY], const.EXP_DATA[const.NAME_KEY])


def crop_time(emulator_device):
    crop_screenshot(emulator_device, const.TIME_DATA[const.DIMENSIONS_KEY], const.TIME_DATA[const.NAME_KEY])


def crop_quest_numbers(emulator_device):
    crop_gold(emulator_device)
    crop_exp(emulator_device)
    crop_time(emulator_device)


def crop_first_quest(emulator_device):
    crop_screenshot(emulator_device, const.FIRST_QUEST[const.DIMENSIONS_KEY], const.FIRST_QUEST[const.NAME_KEY])


def crop_second_quest(emulator_device):
    crop_screenshot(emulator_device, const.SECOND_QUEST[const.DIMENSIONS_KEY], const.SECOND_QUEST[const.NAME_KEY])


def crop_third_quest(emulator_device):
    crop_screenshot(emulator_device, const.THIRD_QUEST[const.DIMENSIONS_KEY], const.THIRD_QUEST[const.NAME_KEY])


# END Crop quest data
# ----------------------


# ----------------------
# Image paths
def get_npc_image_path(npc_name):
    return os.path.join(const.ORIGINAL_NPC_DIR_PATH, npc_name) + const.IMAGE_EXTENSION


def get_contrasted_image_path(image_path):
    return image_path.split(const.IMAGE_EXTENSION)[0] + "_contrasted" + const.IMAGE_EXTENSION


# END Image paths
# ----------------------


# ----------------------
# Enhance images
def enhance_image_bw(image_path, threshold=const.POLARIZE_THRESHOLD):
    image = Image.open(image_path)
    image = image.convert('L')
    image = image.point(lambda x: 0 if x < threshold else 255, '1')
    image.save(get_contrasted_image_path(image_path))
    time.sleep(0.5)


# END Enhance images
# ----------------------


# ----------------------
# GAME ACTIONS
def go_to_tavern_using_key(emulator_device):
    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: Pressing 'a and t' to return to tavern")

    # first leave the tavern to exit without clicking on close and then go back using t
    adm_command = f"adb -s {emulator_device.serial} shell input text 'a'"
    subprocess.run(adm_command, shell=True, check=True)
    time.sleep(0.3)

    adm_command = f"adb -s {emulator_device.serial} shell input text 't'"
    subprocess.run(adm_command, shell=True, check=True)
    time.sleep(0.3)

    take_screenshot(emulator_device)

    if not is_in_tavern(emulator_device):
        logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: Pressing 't' did not work")
        go_to_tavern_using_key(emulator_device)


def click_exit_ad(emulator_device):
    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: exiting AD")
    exit_ad_location = const.CLOSE_AD_BUTTON[const.CLICK_LOCATION_KEY]
    emulator_device.click(exit_ad_location[const.X_KEY], exit_ad_location[const.Y_KEY])


def close_ad(emulator_device):
    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: closing ad")
    click_exit_ad(emulator_device)
    time.sleep(2)


def close_ad_if_playing(emulator_device):
    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: close ad if playing")
    take_screenshot(emulator_device)
    crop_close_ad(emulator_device)

    if is_close_ad_present(emulator_device):
        close_ad(emulator_device)
        close_ad_if_playing(emulator_device)
    else:
        if is_in_tavern(emulator_device):
            logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: is in tavern")


def drink_beer(emulator_device):
    logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: Drink beer")
    emulator_device.click(const.DRINK_BEER_MUSHROOM_BUTTON[const.CLICK_LOCATION_KEY][const.X_KEY],
                          const.DRINK_BEER_MUSHROOM_BUTTON[const.CLICK_LOCATION_KEY][const.Y_KEY])


def drink_beer_and_return_to_tavern(emulator_device):
    drink_beer(emulator_device)
    go_to_tavern_using_key(emulator_device)


def open_quest_from_npc(emulator_device):
    for npc in const.QUEST_NPC_LIST:
        crop_screenshot(emulator_device, npc[const.DIMENSIONS_KEY], const.NPC_SUFFIX)
        if are_images_similar(emulator_device,
                              get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX),
                              npc[const.PATH_KEY],
                              const.NPC_THRESHOLD):
            logger.debug(f"[{get_emulator_name(emulator_device.serial)}]: NPC found its {npc[const.NAME_KEY]}")
            click_location = npc[const.CLICK_LOCATION_KEY]
            emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
            time.sleep(0.2)
            break


def skip_quest_with_ad(emulator_device):
    logger.error(f"[{get_emulator_name(emulator_device.serial)}]: Skipping quest using Ad.")
    ad_location = const.QUEST_AD[const.CLICK_LOCATION_KEY]
    emulator_device.click(ad_location[const.X_KEY], ad_location[const.Y_KEY])
    time.sleep(5)
    close_ad_if_playing(emulator_device)


def exit_done_quest(emulator_device):
    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: exiting done quest with OK button")
    click_location = const.QUEST_DONE_OK_BUTTON[const.CLICK_LOCATION_KEY]
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
    time.sleep(0.5)


def accept_new_level(emulator_device):
    logger.info(f"[{get_emulator_name(emulator_device.serial)}]: accepting new level")
    emulator_device.click(const.NEW_LEVEL_OK_BUTTON[const.CLICK_LOCATION_KEY])


# END GAME ACTIONS
# ----------------------


# -----------------
# OTHER UTILS
def to_box(dimensions):
    return dimensions['left'], dimensions['top'], dimensions['right'], dimensions['bottom']


def is_number(s):
    try:
        float(s)  # Attempt to convert the string to a float
        return True
    except ValueError:
        return False


def get_emulator_name(emulator_device):
    adb_command = f"adb -s {emulator_device.serial} emu avd name"
    result = str(subprocess.run(adb_command, shell=True, capture_output=True).stdout.decode()).split("\n")[0].replace(
        "\r", "")
    return result

# END OTHER UTILS
# ----------------------
