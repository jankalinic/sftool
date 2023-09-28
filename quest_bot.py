import threading
import time

from common.custom_logger import logger, DEBUG_LEVEL
from common import common_utils as util
from common import constants as const

CAN_USE_MUSHROOMS_FOR_BEER = bool


def start_quest(emulator_device, quest_num):
    logger.debug(f"[{emulator_device.serial}]: Starting quest [{quest_num}]")
    quest_click_location = const.QUEST_LIST[quest_num][const.CLICK_LOCATION_KEY]
    emulator_device.click(quest_click_location[const.X_KEY], quest_click_location[const.Y_KEY])
    # check if correct quest is selected
    if util.is_selected_correct_quest(emulator_device, quest_num):
        start_quest_location = const.ACCEPT_QUEST_BUTTON[const.CLICK_LOCATION_KEY]
        emulator_device.click(start_quest_location[const.X_KEY], start_quest_location[const.Y_KEY])
        time.sleep(5)
    else:
        if util.is_in_quest_selection(emulator_device):
            logger.debug(f"[{emulator_device.serial}]: Failed to start the quest -> try again")
            start_quest(emulator_device, quest_num)
        else:
            # maybe is back in tavern
            logger.debug("idk")


def select_best_quest(emulator_device):
    logger.debug(f"[{util.get_emulator_and_adv_name(emulator_device)}]: Choosing best quest")
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
        logger.debug(f"[{util.get_emulator_and_adv_name(emulator_device)}]: Current gold: {gold}")
        gold_list.append(gold)

        exp = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.EXP_DATA[const.NAME_KEY]))
        logger.debug(f"[{util.get_emulator_and_adv_name(emulator_device)}]: Current exp: {exp}")
        exp_list.append(exp)

        time_seconds = util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.TIME_DATA[const.NAME_KEY]))
        logger.debug(f"[{util.get_emulator_and_adv_name(emulator_device)}]: Current time: {time_seconds}")
        time_list.append(time_seconds)

    # TODO: Jirka logic to pick which quest is the best
    pick_quest_num = exp_list.index(max(exp_list))

    start_quest(emulator_device, pick_quest_num)


def open_tavern_master_menu(emulator_device):
    logger.debug(f"[{util.get_emulator_and_adv_name(emulator_device)}]: Open tavern menu")
    click_location = const.TAVERN_MASTER[const.CLICK_LOCATION_KEY]
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
    time.sleep(0.5)


def quest_loop(emulator):
    logger.debug(f"Running quest loop for: {emulator.serial}")
    while True:
        if util.is_emulator_attached(emulator):
            util.take_screenshot(emulator)
            if util.is_in_game(emulator):
                if util.is_in_profile_selection(emulator):
                    util.login_and_go_to_tavern(emulator)
                else:
                    if util.is_in_tavern(emulator):
                        if util.is_enough_thirst(emulator):
                            util.open_quest_from_npc(emulator)
                            util.take_screenshot(emulator)
                            if util.is_in_quest_selection(emulator):
                                select_best_quest(emulator)
                        else:
                            open_tavern_master_menu(emulator)
                            util.take_screenshot(emulator)
                            if util.can_drink_more(emulator, CAN_USE_MUSHROOMS_FOR_BEER):
                                util.drink_beer_and_return_to_tavern(emulator)
                            else:
                                logger.error(f"[{util.get_emulator_and_adv_name(emulator)}]: cannot do more quest. Terminating bot.")
                                break
                    elif util.is_in_quest(emulator):
                        if util.is_quest_skipable_with_ad(emulator):
                            util.skip_quest_with_ad(emulator)
                        elif util.is_quest_done(emulator):
                            util.exit_done_quest(emulator)
                        else:
                            logger.debug(f"{util.get_emulator_and_adv_name(emulator)}: is still in quest, cannot skip, lets wait 20s")
                            time.sleep(20)
                            continue
                    elif util.is_close_ad_present(emulator):
                        util.close_ad(emulator)
                    elif util.is_new_level_accept_present(emulator):
                        util.accept_new_level(emulator)
                    elif util.is_quest_done(emulator):
                        util.exit_done_quest(emulator)
                    elif util.is_in_quest_selection(emulator):
                        util.go_to_tavern_using_key(emulator)
                    elif util.is_dont_close_ad_button_present(emulator):
                        util.go_to_tavern_using_key(emulator)
                    else:
                        logger.debug(f"{util.get_emulator_and_adv_name(emulator)}: is not in tavern and not in quest might still be in ad, wait for a 2s")
                        time.sleep(2)
            else:
                logger.error(f"[{util.get_emulator_and_adv_name(emulator)}]: is not playing sf")
                exit(1)
        else:
            logger.error(f"[{util.get_emulator_and_adv_name(emulator)}]: is offline")
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

    if len(emulator_device_list) == 0 or (len(emulator_device_list) == 1 and emulator_device_list[0].debug == "offline"):
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
