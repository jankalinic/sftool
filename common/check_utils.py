import os
from common import image_utils as imgutil
from common import constants as const
from common import adb_utils as adbutil
from common.custom_logger import logger
from common import ocr_utils as ocrutil


def is_in_quest(emulator_device):
    imgutil.crop_quest_progress_bar(emulator_device)
    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, const.QUEST_PROGRESS_BAR[const.NAME_KEY]),
                               const.QUEST_PROGRESS_BAR[const.PATH_KEY],
                               const.QUEST_PROGRESS_BAR_DIFF_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: is {'' if is_it else 'NOT'} in quest")
    return is_it


def is_in_tavern(emulator_device):
    # Screen must contain beer + not acceptQuest + not questworm
    imgutil.crop_beer_button(emulator_device)

    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, const.BEER_TAVERN_BUTTON[const.NAME_KEY]),
                               const.BEER_TAVERN_BUTTON[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD) and \
            not is_in_quest_selection(emulator_device) and \
            not is_in_quest(emulator_device)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: is {'' if is_it else 'NOT'} in tavern")
    return is_it



def is_in_game(emulator_device):
    imgutil.crop_wallpaper(emulator_device)
    is_it = not ocrutil.are_images_similar(emulator_device,
                                   imgutil.get_cropped_screenshot_path(emulator_device, const.WALLPAPER_DATA[const.NAME_KEY]),
                                   const.WALLPAPER_DATA[const.PATH_KEY],
                                   const.WALLPAPER_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: is {'' if is_it else 'NOT'} in sfgame")
    return is_it


def is_in_quest_selection(emulator_device):
    imgutil.crop_accept_button(emulator_device)
    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, const.ACCEPT_QUEST_BUTTON[const.NAME_KEY]),
                               const.ACCEPT_QUEST_BUTTON[const.PATH_KEY],
                               const.QUEST_DIFF_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: is {'' if is_it else 'NOT'} in quest select")
    return is_it


def is_dont_close_ad_button_present(emulator_device):
    return ocrutil.are_images_similar(emulator_device,
                       imgutil.get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_BUTTON[const.NAME_KEY]),
                       const.DONT_CLOSE_AD_BUTTON[const.PATH_KEY],
                       const.CLOSE_AD_DIFF_THRESHOLD)


def is_close_ad_text_present(emulator_device, image_path):
    imgutil.enhance_contrast(image_path, imgutil.get_contrasted_image_path(image_path))
    imgutil.enhance_number_image(imgutil.get_contrasted_image_path(image_path), imgutil.get_enhanced_image_path(image_path))
    image_paths = [image_path, imgutil.get_enhanced_image_path(image_path), imgutil.get_contrasted_image_path(image_path)]
    for img_path in image_paths:
        for psm in const.PSM_CONFIG:
            text = ocrutil.get_close_ad_text(img_path, psm)
            for char in const.CLOSE_BUTTON_WHITELIST_STRING:
                if char in text:
                    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: close ad found by char: {char}")
                    return True

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: X in ad not found as a text")
    return False


def is_close_ad_present(emulator_device):
    imgutil.crop_close_ad(emulator_device)
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Looking for AD close button")

    if is_dont_close_ad_button_present(emulator_device):
        logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: there is only DO NOT CLOSE button")
        return False

    is_it = is_close_ad_text_present(emulator_device,
                                     imgutil.get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_BUTTON[const.NAME_KEY]))

    for image in const.LIST_OF_CLOSEBUTTONS:
        if ocrutil.are_images_similar(emulator_device,
                              imgutil.get_cropped_screenshot_path(emulator_device, const.CLOSE_AD_BUTTON[const.NAME_KEY]),
                              os.path.join(const.ORIGINAL_ADS_CLOSE_BUTTONS_DIR_PATH, image),
                              const.CLOSE_AD_DIFF_THRESHOLD):
            logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: close ad found by image")
            return True

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: close ad {'' if is_it else 'NOT'} found by any way")
    return is_it


def is_reversed_close_ad_present(emulator_device):
    imgutil.crop_reversed_close_ad(emulator_device)

    is_it = is_close_ad_text_present(emulator_device,
                             imgutil.get_cropped_screenshot_path(emulator_device, const.REVERSED_CLOSE_AD_BUTTON[const.NAME_KEY]))
    return is_it


def is_google_close_ad_present(emulator_device):
    imgutil.crop_google_close_ad(emulator_device)

    is_it = is_close_ad_text_present(emulator_device,
                             imgutil.get_cropped_screenshot_path(emulator_device, const.GOOGLE_CLOSE_AD_BUTTON[const.NAME_KEY]))
    return is_it



def is_selected_correct_quest(emulator_device, quest_num):
    selected_quest = const.QUEST_LIST[quest_num]

    imgutil.take_screenshot(emulator_device)
    imgutil.crop_quest(emulator_device, selected_quest)

    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, selected_quest[const.NAME_KEY]),
                               selected_quest[const.PATH_KEY],
                               const.QUEST_TIERS_DIFF_THRESHOLD)

    logger.debug(
        f"{adbutil.get_emulator_and_adv_name(emulator_device)}: current "
        f"quest:{selected_quest[const.NAME_KEY]} is {'' if is_it else 'in'}correctly selected")
    return is_it


def is_enough_thirst(emulator_device):
    imgutil.crop_tavern_master(emulator_device)
    is_it = not ocrutil.are_images_similar(emulator_device,
                                   const.TAVERN_MASTER[const.PATH_KEY],
                                   imgutil.get_cropped_screenshot_path(emulator_device, const.TAVERN_MASTER[const.NAME_KEY]),
                                   const.NPC_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: {'' if is_it else 'NOT'}enough thirst")
    return is_it


def is_quest_ad_wo_hourglass_present(emulator_device):
    imgutil.crop_quest_ad_wo_hourglass(emulator_device)
    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device,
                                                           const.QUEST_AD_WO_HOURGLASS[const.NAME_KEY]),
                               const.QUEST_AD_WO_HOURGLASS[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Quest ad is with{'out' if is_it else ''} hourglass")
    return is_it


def is_quest_ad_present(emulator_device):
    imgutil.crop_quest_ad(emulator_device)
    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, const.QUEST_AD[const.NAME_KEY]),
                               const.QUEST_AD[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)
    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Quest is {'' if is_it else 'NOT'} skippable with free ad")

    return is_it


def is_quest_skipable_with_ad(emulator_device):
    return is_quest_ad_present(emulator_device) or is_quest_ad_wo_hourglass_present(emulator_device)




def is_quest_done(emulator_device):
    imgutil.crop_quest_done(emulator_device)
    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, const.QUEST_DONE_OK_BUTTON[const.NAME_KEY]),
                               const.QUEST_DONE_OK_BUTTON[const.PATH_KEY],
                               const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Quest is {'already' if is_it else 'not yet'} done")
    return is_it




def is_new_level_accept_present(emulator_device):
    imgutil.crop_new_level(emulator_device)
    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, const.NEW_LEVEL_OK_BUTTON[const.NAME_KEY]),
                               const.NEW_LEVEL_OK_BUTTON[const.PATH_KEY],
                               const.NEW_LEVEL_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: New level button is {'' if is_it else 'not'} present")
    return is_it




def is_in_profile_selection(emulator_device):
    imgutil.crop_profile_selection(emulator_device)
    is_it = ocrutil.are_images_similar(emulator_device,
                               imgutil.get_cropped_screenshot_path(emulator_device, const.PROFILE_BUTTON[const.NAME_KEY]),
                               const.PROFILE_BUTTON[const.PATH_KEY],
                               const.NEW_LEVEL_THRESHOLD)

    logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Is {'' if is_it else 'not'} in profile select")
    return is_it




def is_ad_present(emulator_device):
    imgutil.crop_ad(emulator_device)
    logger.debug(f"[{emulator_device.serial}]: Looking for AD")
    return ocrutil.are_images_similar(emulator_device,
                              imgutil.get_cropped_screenshot_path(emulator_device, const.AD_BUTTON[const.NAME_KEY]),
                              const.AD_BUTTON[const.PATH_KEY],
                              const.AD_IMAGE_THRESHOLD)


def can_drink_more(emulator_device, can_use_mushrooms):
    if can_use_mushrooms:
        imgutil.crop_beer_mushroom_button(emulator_device)

        if ocrutil.are_images_similar(emulator_device,
                              const.DRINK_BEER_MUSHROOM_BUTTON[const.PATH_KEY],
                              imgutil.get_cropped_screenshot_path(emulator_device,
                                                          const.DRINK_BEER_MUSHROOM_BUTTON[const.NAME_KEY]),
                              const.MENU_BUTTON_IMAGE_DIFF_THRESHOLD):
            return True

        logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Not drinking beer, the mushroom button is not present.")
    else:
        logger.debug(f"{adbutil.get_emulator_and_adv_name(emulator_device)}: Not drinking beer, if you want, set CAN_USE_MUSHROOMS to True")

    return False


