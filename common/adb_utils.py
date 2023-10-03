import adbutils
import subprocess

from common import constants as const
from common.custom_logger import logger


def get_adb_client():
    return adbutils.AdbClient(host="127.0.0.1", port=5037)


def full_name (emulator_device):
    adb_command = f"adb -s {emulator_device.serial} emu avd name"
    result = str(subprocess.run(adb_command, shell=True, capture_output=True).stdout.decode()).split("\n")[0].replace(
        "\r", "")
    return f"[{emulator_device.serial}]-[{result}]"


def check_emulator_list(emulator_device_list):
    if len(emulator_device_list) == 0 or (
            len(emulator_device_list) == 1 and emulator_device_list[0].info[const.STATE_KEY] == const.OFFLINE):
        logger.error("No running emulators, exiting now.")
        exit(1)


def filter_emulators(emulator_list, skip_list):
    output_list = []

    for emulator in emulator_list:
        if emulator.serial not in skip_list:
            output_list.append(emulator)

    return output_list


def get_emulator(emulator_number):
    return get_adb_client().device(f"emulator-{emulator_number}")