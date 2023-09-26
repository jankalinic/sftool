import threading
import time

from common.custom_logger import logger, DEBUG_LEVEL
from common import common_utils as util
from common import constants as const

CAN_USE_MUSHROOMS_FOR_BEER = bool


def start_quest(emulator_device, quest_num):
    logger.info(f"[{emulator_device.serial}]: Starting quest [{quest_num}]")
    quest_click_location = const.QUEST_LIST[quest_num][const.CLICK_LOCATION_KEY]
    emulator_device.click(quest_click_location[const.X_KEY], quest_click_location[const.Y_KEY])
    # check if correct quest is selected
    if util.is_selected_correct_quest(emulator_device, quest_num):
        start_quest_location = const.ACCEPT_QUEST_BUTTON[const.CLICK_LOCATION_KEY]
        emulator_device.click(start_quest_location[const.X_KEY], start_quest_location[const.Y_KEY])
        time.sleep(5)
    else:
        if util.is_in_quest_selection(emulator_device):
            logger.info(f"[{emulator_device.serial}]: Failed to start the quest -> try again")
            start_quest(emulator_device, quest_num)
        else:
            # maybe is back in tavern
            logger.debug("idk")


def select_best_quest(emulator_device):
    # check stats for first quest
    gold_list = []
    exp_list = []
    time_list = []

    # already selected first quest
    for quest in const.QUEST_LIST:
        location = quest[const.CLICK_LOCATION_KEY]
        emulator_device.click(location[const.X_KEY], location[const.Y_KEY])

        time.sleep(1)

        util.take_screenshot(emulator_device)
        util.crop_quest_numbers(emulator_device)

        gold = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.GOLD_DATA[const.NAME_KEY]))
        logger.debug(f"[{emulator_device.serial}]: Current gold: {gold}")
        gold_list.append(gold)

        exp = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.EXP_DATA[const.NAME_KEY]))
        logger.debug(f"[{emulator_device.serial}]: Current exp: {exp}")
        exp_list.append(exp)

        time_seconds = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.TIME_DATA[const.NAME_KEY]))
        logger.debug(f"[{emulator_device.serial}]: Current time: {time_seconds}")
        time_list.append(time_seconds)

    # TODO: Jirka logic to pick which quest is the best
    pick_quest_num = exp_list.index(max(exp_list))

    start_quest(emulator_device, pick_quest_num)


def open_tavern_master_menu(emualator_device):
    click_location = const.TAVERN_MASTER[const.CLICK_LOCATION_KEY]
    emualator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
    time.sleep(0.5)


def exit_done_quest(emulator_device):
    click_location = const.QUEST_DONE_OK_BUTTON[const.CLICK_LOCATION_KEY]
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
    time.sleep(0.5)


def quest_loop(emulator):
    logger.info(f"Running quest loop for: {emulator.serial}")
    while True:
        if util.is_emulator_attached(emulator):

            util.take_screenshot(emulator)

            if util.is_in_tavern(emulator):
                logger.info(f"[{emulator.serial}]: is in tavern")
                if util.is_enough_thirst(emulator):
                    util.open_quest_from_npc(emulator)

                    util.take_screenshot(emulator)

                    if util.is_in_quest_selection(emulator):
                        logger.info(f"[{emulator.serial}]: picking quest")
                        select_best_quest(emulator)
                else:
                    logger.info(f"[{emulator.serial}]: Need to drink beer.")
                    open_tavern_master_menu(emulator)

                    util.take_screenshot(emulator)

                    if util.can_drink_more(emulator, CAN_USE_MUSHROOMS_FOR_BEER):
                        util.drink_beer_and_return_to_tavern(emulator)
                    else:
                        logger.error(f"[{emulator.serial}]: cannot do more quest. Terminating bot.")
                        break
            else:
                if util.is_in_quest(emulator):
                    logger.info(f"[{emulator.serial}]: is in quest")
                    if util.is_quest_skipable_with_ad(emulator):
                        logger.info(f"[{emulator.serial}]: quest can be skipped with ad")
                        util.skip_quest_with_ad(emulator)
                    else:
                        if util.is_quest_done(emulator):
                            logger.info(f"[{emulator.serial}]: quest is done")
                            exit_done_quest(emulator)
                        else:
                            logger.info(f"[{emulator.serial}]: is still in quest, lets wait 30s")
                            time.sleep(30)
                            continue
                else:
                    util.close_ad_if_playing(emulator)
                    if util.is_quest_done(emulator):
                        exit_done_quest(emulator)
                    else:
                        if util.is_in_quest_selection(emulator):
                            logger.info(f"[{emulator.serial}]: is in tavern and chosing quest")
                            # util.go_back_using_key(emulator)
                            util.go_to_tavern_using_key(emulator)
                        else:
                            logger.info(f"[{emulator.serial}]: is not in tavern might still be in ad, wait for a 2 seconds")
                            time.sleep(2)

        else:
            logger.error(f"[{emulator.serial}]: is offline")
            break


if __name__ == '__main__':
    CAN_USE_MUSHROOMS_FOR_BEER = True

    logger.setLevel(DEBUG_LEVEL)
    logger.info("Started Shakes_Quest_Bot")

    # check installed adb
    util.check_cli_tools_installed()
    util.clean_screenshots()

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
