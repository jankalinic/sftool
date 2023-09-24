import threading
import time

from common.custom_logger import logger, DEBUG_LEVEL
from common import common_utils as util
from common import constants as const

CAN_USE_MUSHROOMS_FOR_BEER = bool


def crop_accept_button(emulator_device):
    util.crop_screenshot(emulator_device, const.ACCEPT_QUEST_BUTTON[const.DIMENSIONS_KEY], const.ACCEPT_QUEST_BUTTON[const.NAME_KEY])


def crop_gold(emulator_device):
    util.crop_screenshot(emulator_device, const.GOLD_TEXT_DIMENSIONS, const.GOLD_NUM_SUFFIX)


def crop_exp(emulator_device):
    util.crop_screenshot(emulator_device, const.EXP_TEXT_DIMENSIONS, const.EXP_NUM_SUFFIX)


def crop_time(emulator_device):
    util.crop_screenshot(emulator_device, const.TIME_TEXT_DIMENSIONS, const.TIME_NUM_SUFFIX)


def crop_quest_numbers(emulator_device):
    crop_gold(emulator_device)
    crop_exp(emulator_device)
    crop_time(emulator_device)


def crop_beer_mushroom_button(emulator_device):
    util.crop_screenshot(emulator_device,
                         const.DRINK_BEER_MUSHROOM_BUTTON[const.DIMENSIONS_KEY],
                         const.DRINK_BEER_MUSHROOM_BUTTON[const.NAME_KEY])


def is_enough_thirst(emulator_device):
    return not util.are_images_similar(emulator_device,
                                       const.TAVERN_MASTER[const.PATH_KEY],
                                       util.get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX),
                                       const.NPC_THRESHOLD)


def can_drink_more(emulator_device):
    if CAN_USE_MUSHROOMS_FOR_BEER:

        util.take_screenshot(emulator_device)
        crop_beer_mushroom_button(emulator_device)

        if util.are_images_similar(emulator_device,
                                   const.DRINK_BEER_MUSHROOM_BUTTON[const.PATH_KEY],
                                   util.get_cropped_screenshot_path(emulator_device, const.DRINK_BEER_MUSHROOM_BUTTON[const.NAME_KEY]),
                                   const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD):
            return True

    return False


def drink_beer(emulator_device):
    logger.debug(f"[{emulator_device.serial}]: Drink beer")
    emulator_device.click(const.DRINK_BEER_MUSHROOM_BUTTON[const.CLICK_LOCATION_KEY][const.X_KEY], const.DRINK_BEER_MUSHROOM_BUTTON[const.CLICK_LOCATION_KEY][const.Y_KEY])


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
            time.sleep(1)
            break


def crop_first_quest(emulator_device):
    util.crop_screenshot(emulator_device, const.FIRST_QUEST[const.DIMENSIONS_KEY], const.FIRST_QUEST[const.NAME_KEY])


def crop_second_quest(emulator_device):
    util.crop_screenshot(emulator_device, const.SECOND_QUEST[const.DIMENSIONS_KEY], const.SECOND_QUEST[const.NAME_KEY])


def crop_third_quest(emulator_device):
    util.crop_screenshot(emulator_device, const.THIRD_QUEST[const.DIMENSIONS_KEY], const.THIRD_QUEST[const.NAME_KEY])


def crop_tavern_master(emulator_device):
    util.crop_screenshot(emulator_device, const.TAVERN_MASTER[const.DIMENSIONS_KEY], const.NPC_SUFFIX)


def is_selected_correct_quest(emulator_device, quest_num):
    util.take_screenshot(emulator_device)
    selected_quest = const.QUEST_LIST[quest_num]
    util.crop_screenshot(emulator_device, selected_quest[const.DIMENSIONS_KEY], selected_quest[const.NAME_KEY])
    return util.are_images_similar(emulator_device,
                                   util.get_cropped_screenshot_path(emulator_device, selected_quest[const.NAME_KEY]),
                                   selected_quest[const.PATH_KEY],
                                   const.QUEST_DIFF_THRESHOLD)


def start_quest(emulator_device, quest_num):
    quest_click_location = const.QUEST_LIST[quest_num][const.CLICK_LOCATION_KEY]
    emulator_device.click(quest_click_location[const.X_KEY], quest_click_location[const.Y_KEY])
    # check if correct quest is selected
    if is_selected_correct_quest(emulator_device, quest_num):
        start_quest_location = const.ACCEPT_QUEST_BUTTON[const.CLICK_LOCATION_KEY]
        emulator_device.click(start_quest_location[const.X_KEY], start_quest_location[const.Y_KEY])
        time.sleep(0.5)
    else:
        if util.is_in_quest_selection(emulator_device):
            logger.debug("Try again")
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
        crop_quest_numbers(emulator_device)

        gold_list.append(util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.GOLD_NUM_SUFFIX)))
        exp_list.append(util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.EXP_NUM_SUFFIX)))
        time_list.append(util.get_number_from_image(util.get_cropped_screenshot_path(emulator_device, const.TIME_NUM_SUFFIX)))

        time.sleep(0.1)


    # TODO: Jirka logic to pick which quest is the best
    pick_quest_num = exp_list.index(max(exp_list))

    start_quest(emulator_device, pick_quest_num)


def is_in_quest(emulator_device):
    return util.are_images_similar(emulator_device,
                                   util.get_cropped_screenshot_path(emulator_device, const.QUEST_PROGRESS_BAR[const.NAME_KEY]),
                                   const.QUEST_PROGRESS_BAR[const.PATH_KEY],
                                   const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)


def crop_quest_progress_bar(emulator_device):
    util.crop_screenshot(emulator_device, const.QUEST_PROGRESS_BAR[const.DIMENSIONS_KEY], const.QUEST_PROGRESS_BAR[const.NAME_KEY])


def crop_quest_ad(emulator_device):
    util.crop_screenshot(emulator_device, const.QUEST_AD[const.DIMENSIONS_KEY], const.QUEST_AD[const.NAME_KEY])


def drink_beer_and_return_to_tavern(emulator_device):
    drink_beer(emulator_device)
    util.go_to_tavern_using_key(emulator_device)


def is_quest_skipable_with_ad(emulator_device):
    return util.are_images_similar(emulator_device,
                                   util.get_cropped_screenshot_path(emulator_device, const.QUEST_AD[const.NAME_KEY]),
                                   const.QUEST_AD[const.PATH_KEY],
                                   const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)


def skip_quest_with_ad(emulator_device):
    ad_location = const.QUEST_AD[const.CLICK_LOCATION_KEY]
    emulator_device.click(ad_location[const.X_KEY], ad_location[const.Y_KEY])


def quest_loop(emulator):
    logger.info(f"Running quest loop for: {emulator.serial}")
    while True:
        if util.is_emulator_attached(emulator):

            util.take_screenshot(emulator)

            util.crop_menu_button(emulator)
            crop_accept_button(emulator)
            crop_quest_progress_bar(emulator)

            # there is need for a better check for being in tavern
            if util.is_in_tavern(emulator) and not util.is_in_quest_selection(emulator) and not is_in_quest(emulator):

                crop_tavern_master(emulator)

                if is_enough_thirst(emulator):
                    open_quest_from_npc(emulator)

                    util.take_screenshot(emulator)
                    crop_accept_button(emulator)

                    if util.is_in_quest_selection(emulator):
                        # decide which to pick
                        select_best_quest(emulator)

                        util.take_screenshot(emulator)
                        crop_quest_ad(emulator)

                        if is_quest_skipable_with_ad(emulator):
                            skip_quest_with_ad(emulator)
                            util.close_ad_if_playing(emulator)
                        else:
                            continue
                else:
                    logger.debug(f"[{emulator.serial}]: Need to drink beer.")
                    emulator.click(const.TAVERN_MASTER[const.CLICK_LOCATION_KEY][const.X_KEY], const.TAVERN_MASTER[const.CLICK_LOCATION_KEY][const.Y_KEY])
                    if can_drink_more(emulator):
                        drink_beer_and_return_to_tavern(emulator)
                    else:
                        logger.error(f"[{emulator.serial}]: cannot do more quest. Terminating bot.")
                        break
            else:
                crop_quest_progress_bar(emulator)
                if is_in_quest(emulator):
                    logger.debug(f"[{emulator.serial}]: is in quest, lets wait 15s")
                    time.sleep(15)
                else:
                    logger.debug(f"[{emulator.serial}]: is not in tavern")
                    util.go_to_tavern_using_key(emulator)
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