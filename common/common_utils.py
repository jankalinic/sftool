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
def go_to_tavern_using_key(emulator_device, must_be_in_tavern=True):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Pressing 'a and t' to return to tavern")

    # first leave the tavern to exit without clicking on close and then go back using t
    adm_command = f"adb -s {emulator_device.serial} shell input text 'a'"
    subprocess.run(adm_command, shell=True, check=True)
    time.sleep(1)

    adm_command = f"adb -s {emulator_device.serial} shell input text 't'"
    subprocess.run(adm_command, shell=True, check=True)
    time.sleep(1)

    imgutil.take_screenshot(emulator_device)

    if not check.is_in_tavern(emulator_device) and must_be_in_tavern:
        logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Pressing 't' did not work")
        go_to_tavern_using_key(emulator_device)


def close_ad(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: closing ad")
    click_exit_ad(emulator_device, const.CLOSE_AD_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(1)


def close_reversed_ad(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: closing reversed ad")
    click_exit_ad(emulator_device, const.REVERSED_CLOSE_AD_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(1)


def close_google_ad(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: closing google ad")
    click_exit_ad(emulator_device, const.GOOGLE_CLOSE_AD_BUTTON[const.CLICK_LOCATION_KEY])
    time.sleep(1)


def close_ad_if_playing(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: close ad if playing")
    imgutil.take_screenshot(emulator_device)

    if check.is_google_close_ad_present(emulator_device):
        close_google_ad(emulator_device)
        return

    if check.is_close_ad_present(emulator_device):
        close_ad(emulator_device)
        return

    if check.is_reversed_close_ad_present(emulator_device):
        close_reversed_ad(emulator_device)
        return

def drink_beer(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Drinking beer")
    emulator_device.click(const.DRINK_BEER_MUSHROOM_BUTTON[const.CLICK_LOCATION_KEY][const.X_KEY],
                          const.DRINK_BEER_MUSHROOM_BUTTON[const.CLICK_LOCATION_KEY][const.Y_KEY])
    time.sleep(0.5)


def drink_beer_and_return_to_tavern(emulator_device):
    for times in range(6):
        drink_beer(emulator_device)
    go_to_tavern_using_key(emulator_device)


def open_quest_from_npc(emulator_device):
    for npc in const.QUEST_NPC_LIST:
        imgutil.crop_screenshot(emulator_device, npc[const.DIMENSIONS_KEY], const.NPC_SUFFIX)
        if ocrutil.are_images_similar(emulator_device,
                              imgutil.get_cropped_screenshot_path(emulator_device, const.NPC_SUFFIX),
                              npc[const.PATH_KEY],
                              const.NPC_THRESHOLD):
            logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: NPC found its {npc[const.NAME_KEY]}")
            click_location = npc[const.CLICK_LOCATION_KEY]
            emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
            time.sleep(0.2)
            break


def skip_quest_with_ad(emulator_device):
    logger.error(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Skipping quest using Ad.")
    click_on_quest_ad(emulator_device)
    time.sleep(5)
    close_ad_if_playing(emulator_device)


def click_exit_ad(emulator_device, exit_ad_location):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: exiting AD")
    emulator_device.click(exit_ad_location[const.X_KEY], exit_ad_location[const.Y_KEY])


def click_on_quest_ad(emulator_device):
    ad_location = const.QUEST_AD[const.CLICK_LOCATION_KEY]
    emulator_device.click(ad_location[const.X_KEY], ad_location[const.Y_KEY])


def click_on_quest_ad_until_its_available(emulator_device, tries=50):
    for x in range(tries):
        logger.error(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Clicking quest ad times:{x}.")
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
    ad_click_location = const.AD_BUTTON[const.CLICK_LOCATION_KEY]
    emulator_device.click(ad_click_location[const.X_KEY], ad_click_location[const.Y_KEY])


def exit_done_quest(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: exiting done quest with OK button")
    click_location = const.QUEST_DONE_OK_BUTTON[const.CLICK_LOCATION_KEY]
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])
    time.sleep(0.5)


def accept_new_level(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: accepting new level")
    click_location = const.NEW_LEVEL_OK_BUTTON[const.CLICK_LOCATION_KEY]
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])


def login_and_go_to_tavern(emulator_device):
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: logining in and going to tavern")
    time.sleep(1)

    click_location = const.PROFILE_BUTTON[const.CLICK_LOCATION_KEY]
    emulator_device.click(click_location[const.X_KEY], click_location[const.Y_KEY])

    time.sleep(3)
    go_to_tavern_using_key(emulator_device, must_be_in_tavern=False)


def watch_ad_and_close_after(emulator_device):
    click_on_ad(emulator_device)
    time.sleep(10)
    close_ad_if_playing(emulator_device)

# END GAME ACTIONS
# ----------------------


# -----------------
# OTHER UTILS
def to_box(dimensions):
    return dimensions['left'], dimensions['top'], dimensions['right'], dimensions['bottom']


