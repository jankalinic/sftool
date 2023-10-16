import subprocess
import time

from common import constants as const
from common.custom_logger import logger
from common import adb_utils as adbutil
from common import image_utils as imgutil
from common import ocr_utils as ocrutil
from common import check_utils as check


# ----------------
# GAME ACTIONS
def wait_until_in_tavern(emulator_device):
    while True:
        imgutil.take_screenshot(emulator_device)
        imgutil.crop_beer_button(emulator_device)
        go_to_tavern_using_key(emulator_device)

        time.sleep(4 * const.TIME_DELAY)

        if check.is_in_tavern(emulator_device):
            break

        logger.debug(f"{adbutil.full_name(emulator_device)}: Return to tavern did not work")


def go_to_tavern_using_key(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: Returning to tavern")
    press_key(emulator_device, 'r')
    press_key(emulator_device, 't')


def press_key(emulator_device, key):
    logger.debug(f"{adbutil.full_name(emulator_device)}: Pressing {key}")
    # first leave the tavern to exit without clicking on close and then go back using t
    adm_command = f"adb -s {emulator_device.serial} shell input text '{key}'"
    subprocess.run(adm_command, shell=True, check=True)
    time.sleep(2 * const.TIME_DELAY)


def close_ad(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: closing ad")
    click_exit_ad(emulator_device, const.CLOSE_AD_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(1)


def close_reversed_ad(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: closing reversed ad")
    click_exit_ad(emulator_device, const.REVERSED_CLOSE_AD_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(1)


def close_google_ad(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: closing google ad")
    click_exit_ad(emulator_device, const.GOOGLE_CLOSE_AD_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(1)


def close_ad_if_playing(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: close ad if playing")
    imgutil.take_screenshot(emulator_device)

    if check.is_dont_close_ad_button_present(emulator_device):
        logger.debug(f"{adbutil.full_name(emulator_device)}: there is only DO NOT CLOSE button")
    # elif check.is_google_close_ad_present(emulator_device):
    #     close_google_ad(emulator_device)
    elif check.is_close_ad_present(emulator_device):
        close_ad(emulator_device)
    # elif check.is_reversed_close_ad_present(emulator_device):
    #     close_reversed_ad(emulator_device)


def drink_beer(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: Drinking beer")
    click(emulator_device, const.DRINK_BEER_MUSHROOM_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(0.5 * const.TIME_DELAY)


def get_how_many_times_can_drink(emulator_device):
    imgutil.crop_screenshot(emulator_device, const.BEER_COUNT_IMAGE[const.DIMENSIONS_KEY], const.BEER_COUNT_IMAGE[const.NAME_KEY])
    times = ocrutil.get_raw_text_from_image(imgutil.get_cropped_screenshot_path(emulator_device, const.BEER_COUNT_IMAGE[const.NAME_KEY]),
                                           allowed_chars="-c tessedit_char_whitelist=0123456789/")
    if times != "":
        return int(times.split("/")[0])

    return 0


def drink_beer_and_return_to_tavern(emulator_device):
    can_drink_times = 10 - get_how_many_times_can_drink(emulator_device)
    logger.debug(f"{adbutil.full_name(emulator_device)}: can drink {can_drink_times}")
    # can drink max 5 beers at one time
    for times in range(min(6, can_drink_times + 1)):
        drink_beer(emulator_device)

    wait_until_in_tavern(emulator_device)


def complete_quest(emulator_device):
    open_quest_from_npc(emulator_device)
    imgutil.take_screenshot(emulator_device)
    if check.is_in_quest_selection(emulator_device):
        select_best_quest(emulator_device)


def open_quest_from_npc(emulator_device):
    for npc in const.QUEST_NPC_LIST:
        imgutil.crop_screenshot(emulator_device, npc[const.DIMENSIONS_KEY], const.NPC_SUFFIX)
        if ocrutil.are_images_similar(emulator_device,
                              imgutil.get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX),
                              npc[const.PATH_KEY],
                              const.NPC_THRESHOLD):
            logger.debug(f"{adbutil.full_name(emulator_device)}: NPC found its {npc[const.NAME_KEY]}")
            click(emulator_device, npc[const.CLICK_LOCATION_KEY])
            break


def skip_quest_with_ad(emulator_device):
    logger.error(f"{adbutil.full_name(emulator_device)}: Skipping quest using Ad.")
    click_on_quest_ad(emulator_device)
    time.sleep(8 * const.TIME_DELAY)
    close_ad_if_playing(emulator_device)


def click_exit_ad(emulator_device, exit_ad_location):
    logger.debug(f"{adbutil.full_name(emulator_device)}: exiting AD")
    click(emulator_device, exit_ad_location)


def click_on_quest_ad(emulator_device):
    click(emulator_device, const.QUEST_AD[const.CLICK_LOCATION_KEY])


def click_on_quest_ad_until_its_available(emulator_device, tries=50):
    for x in range(tries):
        logger.error(f"{adbutil.full_name(emulator_device)}: Clicking quest ad times:{x}.")
        click_on_quest_ad(emulator_device)
        time.sleep(0.05)

        imgutil.take_screenshot(emulator_device)
        imgutil.crop_quest_ad(emulator_device)

        if check.is_quest_ad_present(emulator_device):
            skip_quest_with_ad(emulator_device)
            break
        elif x > tries:
            break


def click_on_ad(emulator_device):
    logger.debug(f"[{emulator_device.serial}]: clicking AD")
    click(emulator_device, const.AD_BUTTON[const.CLICK_LOCATION_KEY])


def exit_done_quest(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: exiting done quest with OK button")
    click(emulator_device, const.QUEST_DONE_OK_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(0.5 * const.TIME_DELAY)


def accept_new_level(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: accepting new level")
    click(emulator_device, const.NEW_LEVEL_OK_BUTTON[const.CLICK_LOCATION_KEY])


def login_and_go_to_tavern(emulator_device):
    logger.debug(f"{adbutil.full_name(emulator_device)}: Logging in")
    click(emulator_device, const.PROFILE_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(3 * const.TIME_DELAY)
    go_to_tavern_using_key(emulator_device)


def watch_ad_and_close_after(emulator_device):
    click_on_ad(emulator_device)
    time.sleep(8 * const.TIME_DELAY)
    close_ad_if_playing(emulator_device)


def open_tavern_master_menu_and_drink_if_possible(emulator_device):
    open_tavern_master_menu(emulator_device)
    imgutil.take_screenshot(emulator_device)

    if check.can_drink_more(emulator_device):
        drink_beer_and_return_to_tavern(emulator_device)
    else:
        logger.error(
            f"[{adbutil.full_name(emulator_device)}]: cannot do more quest. Terminating bot.")
        exit(0)



def wait_till_in_tavern_master_menu(emulator_device):
    while True:
        open_tavern_master_menu(emulator_device)


def open_tavern_master_menu(emulator_device):
    logger.debug(f"[{adbutil.full_name(emulator_device)}]: Open tavern menu")
    click(emulator_device, const.TAVERN_MASTER[const.CLICK_LOCATION_KEY])


def click(emulator_device, click_location):
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
    time.sleep(0.5 * const.TIME_DELAY)


def open_game(emulator_device):
    logger.debug(f"[{adbutil.full_name(emulator_device)}]: Open tavern menu")
    click(emulator_device, const.GAME[const.CLICK_LOCATION_KEY])
    time.sleep(10)



# END GAME ACTIONS
# ----------------------
def start_quest(emulator_device, quest_num):
    logger.debug(f"[{emulator_device.serial}]: Starting quest [{quest_num}]")
    click(emulator_device, const.QUEST_LIST[quest_num][const.CLICK_LOCATION_KEY])

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
    logger.debug(f"{adbutil.full_name(emulator_device)}: Choosing best quest")

    gold_list = []
    exp_list = []
    time_list = []

    indexer = 0
    selected_quest = dict

    # already selected first quest
    for quest in const.QUEST_LIST:
        click(emulator_device, quest[const.CLICK_LOCATION_KEY])

        time.sleep(1 * const.TIME_DELAY)

        imgutil.take_screenshot(emulator_device)
        imgutil.crop_quest_numbers(emulator_device)

        # gold = ocrutil.get_number_from_image(imgutil.get_cropped_screenshot_path(emulator_device, const.GOLD_DATA[const.NAME_KEY]))
        # logger.debug(f"{adbutil.full_name(emulator_device)}: Current gold: {gold}")
        # gold_list.append(gold)

        exp = ocrutil.get_number_from_image(imgutil.get_cropped_screenshot_path(emulator_device, const.EXP_DATA[const.NAME_KEY]))
        logger.debug(f"{adbutil.full_name(emulator_device)}: Current exp: {exp}")
        exp_list.append(exp)

        time_seconds = ocrutil.get_number_from_image(imgutil.get_cropped_screenshot_path(emulator_device, const.TIME_DATA[const.NAME_KEY]))
        logger.debug(f"{adbutil.full_name(emulator_device)}: Current time: {time_seconds}")
        time_list.append(time_seconds)

        tmp_indexer = (exp / time_seconds)

        if tmp_indexer > indexer:
            indexer = tmp_indexer
            selected_quest = quest

    # TODO: Jirka logic to pick which quest is the best
    # pick_quest_num = exp_list.index(max(exp_list))
    pick_quest_num = const.QUEST_LIST.index(selected_quest)

    start_quest(emulator_device, pick_quest_num)


def handle_quest(emulator_device):
    if check.is_quest_ad_present(emulator_device):
        skip_quest_with_ad(emulator_device)
    elif check.is_quest_ad_wo_hourglass_present(emulator_device):
        click_on_quest_ad_until_its_available(emulator_device)
    elif check.is_quest_done(emulator_device):
        exit_done_quest(emulator_device)
    elif check.is_ad_present(emulator_device):
        watch_ad_and_close_after(emulator_device)
    else:
        logger.debug(f"{adbutil.full_name(emulator_device)}: is still in quest, cannot skip, waiting")
        time.sleep(20)
# -----------------
# OTHER UTILS
def to_box(dimensions):
    return dimensions['left'], dimensions['top'], dimensions['right'], dimensions['bottom']


