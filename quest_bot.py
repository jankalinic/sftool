import threading

from common.custom_logger import logger, DEBUG_LEVEL
from common import common_utils as util
from common import constants as const


def crop_gold(emulator_device):
    util.crop_screenshot(emulator_device, const.GOLD_TEXT_DIMENSIONS, const.GOLD_NUM_SUFFIX)


def crop_exp(emulator_device):
    util.crop_screenshot(emulator_device, const.GOLD_TEXT_DIMENSIONS, const.EXP_NUM_SUFFIX)


def crop_time(emulator_device):
    util.crop_screenshot(emulator_device, const.GOLD_TEXT_DIMENSIONS, const.GOLD_NUM_SUFFIX)


def crop_quest_numbers(emulator_device):
    crop_gold(emulator_device)
    crop_exp(emulator_device)
    crop_time(emulator_device)


def is_enough_thirst(emulator_device):
    return True


def can_drink_more(emulator_device):
    if True and CAN_USE_MUSHROOMS_FOR_BEER:
        return True


def drink_beer(emulator_device):
    pass


def click_ok_quest_done(emulator_device)
    emulator_device.click(QUEST_DONE_OK_BUTTON_DIMENSIONS)


def quest_loop(emulator):
    logger.info(f"Running loop for: {emulator}")
    while True:
        # check if its online
        if util.is_emulator_attached(emulator):
            if is_in_tavern(emulator):
                util.take_screenshot(emulator)
                crop_thirst_bar()
                if is_enough_thirst(emulator):

                    crop_quest_numbers(emulator)
                    # choose_best_quest()
                else:
                    if can_drink_more(emulator):
                        drink_beer(emulator)
                    else:
                        logger.error(f"[{emulator.serial}]: cannot do more quest. Terminating bot.")
                        break
            else:
                logger.debug(f"[{emulator.serial}]: is not in tavern")
        else:
            logger.error(f"[{emulator.serial}]: is offline")
            break


if __name__ == '__main__':
    CAN_USE_MUSHROOMS_FOR_BEER = False

    logger.setLevel(DEBUG_LEVEL)
    logger.info("Started Shakes_Quest_Bot")

    # check installed adb
    util.check_cli_tools_installed()

    adb = util.get_adb_client()
    emulator_device_list = adb.device_list()

    thread_list = []

    if len(emulator_device_list) == 0 or (len(emulator_device_list) == 1 and emulator_device_list[0].info == "offline"):
        logger.error("No running emulators, exiting now.")
        exit(1)

    for device in emulator_device_list:
        thread = threading.Thread(target=quest_loop, args=(device,))
        thread.start()
        thread_list.append(thread)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.debug("Program status: Ending program.")
        for thread in thread_list:
            thread.join()