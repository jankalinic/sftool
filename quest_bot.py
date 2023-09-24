import threading
import time

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
    return not util.are_images_similar(emulator_device, util.get_npc_image_path(const.TAVERN_MASTER[const.NAME_KEY]), util.get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX), const.NPC_THRESHOLD)


def can_drink_more(emulator_device):
    if True and CAN_USE_MUSHROOMS_FOR_BEER:
        return True


def drink_beer(emulator_device):
    pass


def click_ok_quest_done(emulator_device):
    emulator_device.click(const.QUEST_DONE_OK_BUTTON_DIMENSIONS)


def click_on_quest_npc(emulator_device):
    for npc in const.QUEST_NPC_LIST:
        util.crop_screenshot(emulator_device, npc[const.DIMENSIONS_KEY], const.NPC_SUFFIX)
        if util.are_images_similar(emulator_device, util.get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX), util.get_npc_image_path(npc[const.NAME_KEY]), const.NPC_THRESHOLD):
            emulator_device.click(npc[const.CLICK_LOCATION_KEY]['x'], npc[const.CLICK_LOCATION_KEY]['y'])
            time.sleep(2)
            break


def crop_quest_tiers(emulator_device):
    util.crop_screenshot(emulator_device, const.FIRST_QUEST_DIMENSIONS, const.TIERS_SUFFIX)


def crop_tavern_master(emulator_device):
    util.crop_screenshot(emulator_device, const.TAVERN_MASTER[const.DIMENSIONS_KEY], const.NPC_SUFFIX)


def is_in_quest_selection(emulator_device):
    return util.are_images_similar(emulator_device,
                                   util.get_cropped_screenshot_path(emulator_device, const.BUTTON_SUFFIX), , const.QUEST_DIFF_THRESHOLD)

def quest_loop(emulator):
    logger.info(f"Running loop for: {emulator}")
    while True:
        # check if its online
        if util.is_emulator_attached(emulator):
            util.take_screenshot(emulator)
            util.crop_menu_button(emulator)
            if util.is_in_tavern(emulator):
                crop_tavern_master(emulator)
                if is_enough_thirst(emulator):
                    click_on_quest_npc(emulator)

                    util.take_screenshot(emulator)
                    crop_accept_quest_button(emulator)

                    if is_in_quest_selection(emulator):
                        # cycle through 3 quests and get numbers
                        crop_quest_numbers(emulator)
                        # decide which to pick

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