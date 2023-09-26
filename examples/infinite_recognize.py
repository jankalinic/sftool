import time
from PIL import Image
import subprocess
import common.common_utils as util
import common.constants as const
import os


if __name__ == '__main__':

    emulator = util.get_adb_client().device("emulator-5554")

    # util.take_screenshot(emulator)
    #
    # util.crop_gold(emulator)
    # util.crop_exp(emulator)
    # util.crop_time(emulator)

    enhanced_dir = os.path.join(const.SCREENSHOT_DIR_PATH, emulator.serial, "enhanced")

    image_name = const.TIME_DATA[const.NAME_KEY]
    input_path = util.get_cropped_screenshot_path(emulator, image_name)
    output_path = os.path.join(enhanced_dir, (image_name + const.IMAGE_EXTENSION))
    output_svg_path = output_path.replace('.png', '.svg')
    sharpened_path = os.path.join(enhanced_dir, ("SHARP-" + image_name + const.IMAGE_EXTENSION))

    number = util.get_number_from_image(output_path)
    #
    # if not os.path.exists(enhanced_dir):
    #     os.makedirs(enhanced_dir)
    #
    #
    # ratio = 2
    # width = int(197 * ratio)
    # height = int(60 * ratio)
    #
    #
    # image = Image.open(input_path)
    # # image = image.resize((width, height), resample=BICUBIC)
    # image = image.convert('L')
    # threshold_value = 100
    # image = image.point(lambda x: 0 if x < threshold_value else 255, '1')
    # image.save(output_path)
    # convert_command = f"potracer {output_path}  -b svg -o {output_svg_path}"
    # subprocess.run(convert_command, shell=True, check=True)
    #
    #
    #
    # # print(f"Recognized number : {number}")
    #
    # time.sleep(5)

