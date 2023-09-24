import threading
import time

from common.custom_logger import logger, DEBUG_LEVEL
from common import common_utils as util
from common import constants as const

CAN_USE_MUSHROOMS_FOR_BEER = bool


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
    return not util.are_images_similar(emulator_device,
                                       const.TAVERN_MASTER[const.PATH_KEY],
                                       util.get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX),
                                       const.NPC_THRESHOLD)


def can_drink_more(emulator_device):
    if True and CAN_USE_MUSHROOMS_FOR_BEER:
        return True


def drink_beer(emulator_device):
    emulator_device.click(const.DRINK_BEER_BUTTON[const.CLICK_LOCATION_KEY])


def click_ok_quest_done(emulator_device):
    emulator_device.click(const.QUEST_DONE_OK_BUTTON[const.DIMENSIONS_KEY])


def open_quest_from_npc(emulator_device):
    for npc in const.QUEST_NPC_LIST:
        util.crop_screenshot(emulator_device, npc[const.DIMENSIONS_KEY], const.NPC_SUFFIX)
        if util.are_images_similar(emulator_device,
                                   util.get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX),
                                   npc[const.PATH_KEY],
                                   const.NPC_THRESHOLD):
            emulator_device.click(npc[const.CLICK_LOCATION_KEY][const.X_KEY], npc[const.CLICK_LOCATION_KEY][const.Y_KEY])
            time.sleep(2)
            break


def crop_first_quest(emulator_device):
    util.crop_screenshot(emulator_device, const.FIRST_QUEST[const.DIMENSIONS_KEY], const.FIRST_QUEST_SUFFIX)


def crop_tavern_master(emulator_device):
    util.crop_screenshot(emulator_device, const.TAVERN_MASTER[const.DIMENSIONS_KEY], const.NPC_SUFFIX)


def is_in_quest_selection(emulator_device):
    return util.are_images_similar(emulator_device,
                                   util.get_cropped_screenshot_path(emulator_device, const.ACCEPT_QUEST_BUTTON[const.NAME_KEY]),
                                   const.ACCEPT_QUEST_BUTTON[const.PATH_KEY],
                                   const.QUEST_DIFF_THRESHOLD)


def is_selected_correct_quest(emulator_device, quest_num):
    util.take_screenshot(emulator_device)
    selected_quest = const.QUEST_LIST[quest_num - 1]
    util.crop_screenshot(emulator_device, selected_quest[const.DIMENSIONS_KEY], selected_quest[const.NAME_KEY])
    return util.are_images_similar(emulator_device,
                               util.get_cropped_screenshot_path(selected_quest[const.NAME_KEY]),
                               selected_quest[const.PATH_KEY],
                               const.QUEST_DIFF_THRESHOLD)


def start_quest(emulator_device, quest_num):
    emulator_device.click(const.QUEST_LIST[quest_num - 1])
    # check if correct quest is selected
    if is_selected_correct_quest(emulator_device, quest_num):
        pass
    else:
        if is_in_quest_selection(emulator_device):
            # Try again
            start_quest(emulator_device, quest_num)
        else:
            # maybe is back in tavern
            pass


def select_best_quest(emulator_device):
    # already selected first quest
    # check stats for first quest
    crop_quest_numbers(emulator_device)

    gold = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.GOLD_NUM_SUFFIX))
    exp = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.EXP_NUM_SUFFIX))
    time = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.TIME_NUM_SUFFIX))

    # TODO: Jirka logic to pick which quest is the best
    pick_quest_num = 1 if gold != 0 else 3

    start_quest(emulator_device, pick_quest_num)


def quest_loop(emulator):
    logger.info(f"Running quest loop for: {emulator}")
    while True:
        if util.is_emulator_attached(emulator):

            util.take_screenshot(emulator)
            util.crop_menu_button(emulator)

            if util.is_in_tavern(emulator):

                crop_tavern_master(emulator)

                if is_enough_thirst(emulator):
                    open_quest_from_npc(emulator)

                    util.take_screenshot(emulator)
                    crop_first_quest(emulator)

                    if is_in_quest_selection(emulator):
                        # decide which to pick
                        select_best_quest(emulator)
                        # check if in quest
                        util.take_screenshot(emulator)
                        # crop_first_quest(emulator)
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