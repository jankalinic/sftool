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


def quest_loop(emulator):
    logger.debug(f"Running quest loop for: {emulator.serial}")
    while True:
        imgutil.take_screenshot(emulator)
        if check.is_in_game(emulator):
            if check.is_in_profile_selection(emulator):
                util.login_and_go_to_tavern(emulator)
            elif check.is_in_tavern(emulator):
                if check.is_enough_thirst(emulator):
                    util.complete_quest(emulator)
                else:
                    util.open_tavern_master_menu_and_drink_if_possible(emulator)
            elif check.is_in_quest_selection(emulator):
                util.select_best_quest(emulator)
            elif check.is_in_quest(emulator):
                util.handle_quest(emulator)
            elif check.is_quest_done(emulator):
                util.exit_done_quest(emulator)
            elif check.is_new_level_accept_present(emulator):
                util.accept_new_level(emulator)
            else:
                logger.debug(f"{adbutil.full_name(emulator)}: is not in tavern and not in quest might still be in ad, wait for a 2s")
                util.close_ad_if_playing(emulator)
                time.sleep(2)
        else:
            logger.error(f"{adbutil.full_name(emulator)}: is not playing the game")
            time.sleep(10)


if __name__ == '__main__':

    logger.setLevel(DEBUG_LEVEL)
    logger.info("Started Shakes_Quest_Bot")
    osutil.check_cli_tools_installed()

    thread_list = []
    SKIP_EMULATORS = list()
    # SKIP_EMULATORS = ["emulator-5554", "emulator-5556"]

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
