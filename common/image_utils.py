import os
import subprocess
import time
import cv2
from PIL import Image, ImageFilter, ImageEnhance, ImageOps


from common import constants as const
from common.custom_logger import logger
from common import adb_utils as adbutil
from common import os_utils as osutil


# ----------------------
# Image paths
def get_npc_image_path(npc_name):
    return os.path.join(const.ORIGINAL_NPC_DIR_PATH, npc_name) + const.IMAGE_EXTENSION


def get_contrasted_image_path(image_path):
    return image_path.split(const.IMAGE_EXTENSION)[0] + "_contrasted" + const.IMAGE_EXTENSION


def get_enhanced_image_path(image_path):
    return image_path.split(const.IMAGE_EXTENSION)[0] + "_enhanced" + const.IMAGE_EXTENSION


def get_screenshot_path(emulator_device):
    return os.path.join(const.SCREENSHOT_DIR_PATH, emulator_device.serial,
                        (const.SCREENSHOT_SUFFIX + const.IMAGE_EXTENSION))


def get_cropped_screenshot_path(emulator_device, suffix=""):
    suffix = const.CROPPED_SUFFIX if suffix == "" else suffix
    return os.path.join(const.SCREENSHOT_DIR_PATH, emulator_device.serial,
                        const.CROPPED_SUFFIX, (suffix + const.IMAGE_EXTENSION))


def take_screenshot(emulator_device):
    osutil.check_if_path_exist_or_create(os.path.dirname(get_screenshot_path(emulator_device)))
    logger.debug(f"{adbutil.full_name(emulator_device)} Taking a screenshot")
    adb_command = f"adb -s {emulator_device.serial} exec-out screencap -p > {get_screenshot_path(emulator_device)}"
    subprocess.run(adb_command, shell=True, check=True)
    time.sleep(0.05 * const.TIME_DELAY)


def crop_screenshot(emulator_device, dimensions, suffix):
    osutil.check_if_path_exist_or_create(os.path.dirname(get_cropped_screenshot_path(emulator_device, suffix)))
    logger.debug(f"{adbutil.full_name(emulator_device)} Cropping a screenshot {suffix}")
    crop_image(get_screenshot_path(emulator_device), get_cropped_screenshot_path(emulator_device, suffix), dimensions)


def crop_image(input_path, output_path, dimensions):
    crop_cmd = f"convert {input_path} -crop {dimensions['right'] - dimensions['left']}x{dimensions['bottom'] - dimensions['top']}+{dimensions['left']}+{dimensions['top']} {output_path}"
    subprocess.run(crop_cmd, shell=True, check=True)


def crop_ad(emulator_device):
    crop_screenshot(emulator_device,
                    const.AD_BUTTON[const.DIMENSIONS_KEY],
                    const.AD_BUTTON[const.NAME_KEY])


def crop_quest_ad(emulator_device):
    crop_screenshot(emulator_device,
                    const.QUEST_AD[const.DIMENSIONS_KEY],
                    const.QUEST_AD[const.NAME_KEY])


def crop_quest_ad_wo_hourglass(emulator_device):
    crop_screenshot(emulator_device,
                    const.QUEST_AD_WO_HOURGLASS[const.DIMENSIONS_KEY],
                    const.QUEST_AD_WO_HOURGLASS[const.NAME_KEY])


def crop_tavern_master(emulator_device):
    crop_screenshot(emulator_device,
                    const.TAVERN_MASTER[const.DIMENSIONS_KEY],
                    const.TAVERN_MASTER[const.NAME_KEY])


def crop_quest(emulator_device, selected_quest):
    crop_screenshot(emulator_device,
                    selected_quest[const.DIMENSIONS_KEY],
                    selected_quest[const.NAME_KEY])


def crop_close_ad(emulator_device):
    crop_screenshot(emulator_device,
                    const.CLOSE_AD_BUTTON[const.DIMENSIONS_KEY],
                    const.CLOSE_AD_BUTTON[const.NAME_KEY])


def crop_reversed_close_ad(emulator_device):
    crop_screenshot(emulator_device,
                    const.REVERSED_CLOSE_AD_BUTTON[const.DIMENSIONS_KEY],
                    const.REVERSED_CLOSE_AD_BUTTON[const.NAME_KEY])


def crop_google_close_ad(emulator_device):
    crop_screenshot(emulator_device,
                    const.GOOGLE_CLOSE_AD_BUTTON[const.DIMENSIONS_KEY],
                    const.GOOGLE_CLOSE_AD_BUTTON[const.NAME_KEY])

def crop_accept_button(emulator_device):
    crop_screenshot(emulator_device,
                    const.ACCEPT_QUEST_BUTTON[const.DIMENSIONS_KEY],
                    const.ACCEPT_QUEST_BUTTON[const.NAME_KEY])

def crop_beer_count(emulator_device):
    crop_screenshot(emulator_device,
                    const.BEER_COUNT_IMAGE[const.DIMENSIONS_KEY],
                    const.BEER_COUNT_IMAGE[const.NAME_KEY])


def crop_wallpaper(emulator_device):
    crop_screenshot(emulator_device,
                    const.WALLPAPER_DATA[const.DIMENSIONS_KEY],
                    const.WALLPAPER_DATA[const.NAME_KEY])


def crop_beer_button(emulator_device):
    crop_screenshot(emulator_device,
                    const.BEER_TAVERN_BUTTON[const.DIMENSIONS_KEY],
                    const.BEER_TAVERN_BUTTON[const.NAME_KEY])


def crop_quest_progress_bar(emulator_device):
    crop_screenshot(emulator_device,
                    const.QUEST_PROGRESS_BAR[const.DIMENSIONS_KEY],
                    const.QUEST_PROGRESS_BAR[const.NAME_KEY])


def crop_beer_mushroom_button(emulator_device):
    crop_screenshot(emulator_device,
                    const.DRINK_BEER_MUSHROOM_BUTTON[const.DIMENSIONS_KEY],
                    const.DRINK_BEER_MUSHROOM_BUTTON[const.NAME_KEY])


def crop_quest_done(emulator_device):
    crop_screenshot(emulator_device,
                    const.QUEST_DONE_OK_BUTTON[const.DIMENSIONS_KEY],
                    const.QUEST_DONE_OK_BUTTON[const.NAME_KEY])


def crop_profile_selection(emulator_device):
    crop_screenshot(emulator_device,
                    const.PROFILE_BUTTON[const.DIMENSIONS_KEY],
                    const.PROFILE_BUTTON[const.NAME_KEY])


def crop_new_level(emulator_device):
    crop_screenshot(emulator_device,
                    const.NEW_LEVEL_OK_BUTTON[const.DIMENSIONS_KEY],
                    const.NEW_LEVEL_OK_BUTTON[const.NAME_KEY])


def crop_gold(emulator_device):
    crop_screenshot(emulator_device,
                    const.GOLD_DATA[const.DIMENSIONS_KEY],
                    const.GOLD_DATA[const.NAME_KEY])


def crop_exp(emulator_device):
    crop_screenshot(emulator_device,
                    const.EXP_DATA[const.DIMENSIONS_KEY],
                    const.EXP_DATA[const.NAME_KEY])


def crop_time(emulator_device):
    crop_screenshot(emulator_device,
                    const.TIME_DATA[const.DIMENSIONS_KEY],
                    const.TIME_DATA[const.NAME_KEY])


def crop_quest_numbers(emulator_device):
    crop_gold(emulator_device)
    crop_exp(emulator_device)
    crop_time(emulator_device)


def crop_first_quest(emulator_device):
    crop_screenshot(emulator_device,
                    const.FIRST_QUEST[const.DIMENSIONS_KEY],
                    const.FIRST_QUEST[const.NAME_KEY])


def crop_second_quest(emulator_device):
    crop_screenshot(emulator_device,
                    const.SECOND_QUEST[const.DIMENSIONS_KEY],
                    const.SECOND_QUEST[const.NAME_KEY])


def crop_third_quest(emulator_device):
    crop_screenshot(emulator_device,
                    const.THIRD_QUEST[const.DIMENSIONS_KEY],
                    const.THIRD_QUEST[const.NAME_KEY])


def crop_number_image(in_image_path):
    image = cv2.imread(get_contrasted_image_path(in_image_path))
    edges = cv2.Canny(image, threshold1=30, threshold2=100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_x_list = []
    min_y_list = []

    max_x_list = []
    max_y_list = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        min_x_list.append(x)
        min_y_list.append(y)
        max_x_list.append(x + w)
        max_y_list.append(y + h)

    min_x = min(min_x_list)
    max_x = max(max_x_list)

    min_y = min(min_y_list)
    max_y = max(max_y_list)

    pic_width = image.shape[1]
    pic_height = image.shape[0]

    margin_x = 20
    margin_y = margin_x

    new_size = const.new_dimensions((min_x - margin_x) if (min_x - margin_x) > 1 else 0,
                                    (min_y - margin_y) if (min_y - margin_y) > 1 else 0,
                                    (max_x + margin_x) if (max_x + margin_x) < pic_width else pic_width,
                                    (max_y + margin_y) if (max_y + margin_y) < pic_height else pic_height)

    crop_image(get_contrasted_image_path(in_image_path), get_enhanced_image_path(in_image_path), new_size)


# ----------------------
# Enhance images

def enhance_grayscale(input_path, output_path):
    image = Image.open(input_path)

    image = image.resize((image.width * const.RESIZE_RATIO, image.height * const.RESIZE_RATIO))
    image = image.convert('L')
    image.save(output_path)
    time.sleep(0.5 * const.TIME_DELAY)


def enhance_contrast(input_path, output_path, threshold=const.POLARIZE_THRESHOLD, enhance_contrast=5):
    image = Image.open(input_path)

    image = image.resize((image.width * const.RESIZE_RATIO, image.height * const.RESIZE_RATIO))
    image = ImageEnhance.Contrast(image.convert('L'))\
                        .enhance(enhance_contrast)\
                        .point(lambda x: 0 if x < threshold else 255, '1')\
                        .convert('L')\
                        .filter(ImageFilter.MedianFilter(size=3))

    image = ImageOps.invert(image)
    image.save(output_path)
    time.sleep(0.5 * const.TIME_DELAY)


def enhance_number_image(input_path, output_path):
    pnm_path = input_path.split(const.IMAGE_EXTENSION)[0] + ".pnm"
    svg_path = input_path.split(const.IMAGE_EXTENSION)[0] + ".svg"
    # first convert png to pnm
    convert_pnm_command = f"convert {input_path} {pnm_path}"
    subprocess.run(convert_pnm_command, shell=True, check=True)

    time.sleep(0.2 * const.TIME_DELAY)

    convert_sv_command = f"potracer {pnm_path} -b svg -o {svg_path}"
    subprocess.run(convert_sv_command, shell=True, check=True)

    time.sleep(0.2 * const.TIME_DELAY)

    convert_png_command = f"cairosvg {svg_path} -o {output_path}"
    subprocess.run(convert_png_command, shell=True, check=True)

    time.sleep(0.2 * const.TIME_DELAY)