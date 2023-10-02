import subprocess
import os

from common.custom_logger import logger
from common import constants as const


def clean_directory(directory_path):
    files = os.listdir(directory_path)

    # Iterate through the files and delete them
    for file in files:
        file_path = os.path.join(directory_path, file)
        try:
            if os.path.isfile(file_path):
                if ".gitkeep" not in file_path:
                    os.remove(file_path)
                    logger.debug(f"Deleted: {file_path}")
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
                logger.debug(f"Deleted directory: {file_path}")
        except Exception as e:
            logger.debug(f"Error deleting {file_path}: {str(e)}")


def clean_screenshots():
    clean_directory(os.path.join(const.SCREENSHOT_DIR_PATH))


def check_cli_tools_installed():
    try:
        adb_command = "adb --version"
        result = subprocess.run(adb_command, shell=True, capture_output=True)
        if "Android Debug Bridge" in str(result.stdout):
            logger.debug("ADB is installed.")
        else:
            raise Exception
    except Exception:
        logger.warning("ADB is not installed. Please run: brew install android-platform-tools")
        exit(1)

    try:
        convert_command = "convert --version"
        result = subprocess.run(convert_command, shell=True, capture_output=True)
        if "Version: ImageMagick" in str(result.stdout):
            logger.debug("Convert is installed.")
        else:
            raise Exception
    except Exception:
        logger.warning("Convert is not installed. Please run: brew install imagemagick")
        exit(1)

    try:
        convert_command = "cairosvg --version"
        result = subprocess.run(convert_command, shell=True, capture_output=True)
        if "2." in str(result.stdout):
            logger.debug("cairosvg is installed.")
        else:
            raise Exception
    except Exception:
        logger.warning("cairosvg is not installed. Please run: pip3 install cairosvg")
        exit(1)

    try:
        convert_command = "potracer --version"
        result = subprocess.run(convert_command, shell=True, capture_output=True)
        if "Potrace" in str(result.stdout):
            logger.debug("Potracer is installed.")
        else:
            raise Exception
    except Exception:
        logger.warning("Potracer is not installed. Please run: pip3 install potracer")
        exit(1)


def check_if_path_exist_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)
