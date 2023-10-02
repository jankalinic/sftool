import threading
import time

from common.custom_logger import logger, DEBUG_LEVEL
from common import constants as const
from common import common_utils as util
from common import adb_utils as adbutil
from common import os_utils as osutil
from common import ocr_utils as ocrutil
from common import image_utils as imgutil
from common import check_utils as check

CAN_USE_MUSHROOMS_FOR_BEER = bool


def start_quest(emulator_device, quest_num):
    logger.debug(f"[{emulator_device.serial}]: Starting quest [{quest_num}]")
    quest_click_location = const.QUEST_LIST[quest_num][const.CLICK_LOCATION_KEY]
    emulator_device.click(quest_click_location[const.X_KEY], quest_click_location[const.Y_KEY])
    # check if correct quest is selected
    if check.is_selected_correct_quest(emulator_device, quest_num):
        start_quest_location = const.ACCEPT_QUEST_BUTTON[const.CLICK_LOCATION_KEY]
        emulator_device.click(start_quest_location[const.X_KEY], start_quest_location[const.Y_KEY])
        time.sleep(5)
    else:
        if check.is_in_quest_selection(emulator_device):
            logger.debug(f"[{emulator_device.serial}]: Failed to start the quest -> try again")
            start_quest(emulator_device, quest_num)
        else:
            # maybe is back in tavern
            logger.debug("idk")


def select_best_quest(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Choosing best quest")
    # check stats for first quest
    gold_list = []
    exp_list = []
    time_list = []

    # already selected first quest
    for quest in const.QUEST_LIST:
        location = quest[const.CLICK_LOCATION_KEY]
        emulator_device.click(location[const.X_KEY], location[const.Y_KEY])

        time.sleep(1)

        imgutil.take_screenshot(emulator_device)
        imgutil.crop_quest_numbers(emulator_device)

        gold = ocrutil.get_number_from_image(imgutil.get_cropped_screenshot_path(emulator_device, const.GOLD_DATA[const.NAME_KEY]))
        logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Current gold: {gold}")
        gold_list.append(gold)

        exp = ocrutil.get_number_from_image(imgutil.get_cropped_screenshot_path(emulator_device, const.EXP_DATA[const.NAME_KEY]))
        logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Current exp: {exp}")
        exp_list.append(exp)

        time_seconds = ocrutil.get_number_from_image(imgutil.get_cropped_screenshot_path(emulator_device, const.TIME_DATA[const.NAME_KEY]))
        logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Current time: {time_seconds}")
        time_list.append(time_seconds)

    # TODO: Jirka logic to pick which quest is the best
    pick_quest_num = exp_list.index(max(exp_list))

    start_quest(emulator_device, pick_quest_num)


def open_tavern_master_menu(emulator_device):
    logger.debug(f"[{adbutil.get_emulator_and_adv_name(emulator_device)}]: Open tavern menu")
    click_location = const.TAVERN_MASTER[const.CLICK_LOCATION_KEY]
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
    time.sleep(0.5)


def quest_loop(emulator):
    logger.debug(f"Running quest loop for: {emulator.serial}")
    while True:
        imgutil.take_screenshot(emulator)
        if check.is_in_tavern(emulator):
            if check.is_enough_thirst(emulator):
                util.open_quest_from_npc(emulator)
                imgutil.take_screenshot(emulator)
                if check.is_in_quest_selection(emulator):
                    select_best_quest(emulator)
            else:
                open_tavern_master_menu(emulator)
                imgutil.take_screenshot(emulator)
                if check.can_drink_more(emulator, CAN_USE_MUSHROOMS_FOR_BEER):
                    util.drink_beer_and_return_to_tavern(emulator)
                else:
                    logger.error(
                        f"[{adbutil.get_emulator_and_adv_name(emulator)}]: cannot do more quest. Terminating bot.")
                    break
        elif check.is_in_quest(emulator):
            if check.is_quest_ad_present(emulator):
                util.skip_quest_with_ad(emulator)
            elif check.is_quest_ad_wo_hourglass_present(emulator):
                util.click_on_quest_ad_until_its_available(emulator)
            elif check.is_quest_done(emulator):
                util.exit_done_quest(emulator)
            elif check.is_ad_present(emulator):
                util.watch_ad_and_close_after(emulator)
            else:
                logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator)}: is still in quest, cannot skip, waiting")
                time.sleep(20)
                continue
        elif check.is_new_level_accept_present(emulator):
            util.accept_new_level(emulator)
        elif check.is_quest_done(emulator):
            util.exit_done_quest(emulator)
        elif check.is_in_quest_selection(emulator):
            util.go_to_tavern_using_key(emulator)
        elif check.is_dont_close_ad_button_present(emulator):
            util.go_to_tavern_using_key(emulator)
        else:
            logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator)}: is not in tavern and not in quest might still be in ad, wait for a 2s")
            util.close_ad_if_playing(emulator)
            time.sleep(2)


if __name__ == '__main__':
    CAN_USE_MUSHROOMS_FOR_BEER = True

    logger.setLevel(DEBUG_LEVEL)
    logger.info("Started Shakes_Quest_Bot")

    # check installed adb
    osutil.check_cli_tools_installed()
    thread_list = []
    SKIP_EMULATORS = []
    # SKIP_EMULATORS = ["emulator-5562", "emulator-5554", "emulator-5556", "emulator-5558","emulator-5560"]

    emulator_device_list = adbutil.filter_emulators(adbutil.get_adb_client().device_list(), SKIP_EMULATORS)
    adbutil.check_emulator_list(emulator_device_list)
    osutil.clean_screenshots()

    for device in emulator_device_list:
        if device.serial not in SKIP_EMULATORS:
            thread = threading.Thread(target=quest_loop, args=(device,))
            thread.start()
            thread_list.append(thread)

    for thread in thread_list:
        thread.join()
