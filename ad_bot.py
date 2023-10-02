import timeimport threadingfrom common import constants as constfrom common import common_utils as utilfrom common import adb_utils as adbutilfrom common import os_utils as osutilfrom common import image_utils as imgutilfrom common import check_utils as checkfrom common.custom_logger import logger, DEBUG_LEVELdef check_device_loop(emulator):    logger.info(f"Running loop for: {emulator}")    while True:        try:            imgutil.take_screenshot(emulator)            if check.is_ad_present(emulator):                util.watch_ad_and_close_after(emulator)            else:                util.close_ad_if_playing(emulator)        except Exception as e:            logger.error(f"[{emulator.serial}]: emulation failed")            exit(1)if __name__ == '__main__':    logger.setLevel(DEBUG_LEVEL)    logger.info("Started Shakes_AD_Bot")    osutil.check_cli_tools_installed()    osutil.clean_screenshots()    thread_list = []    SKIP_EMULATORS = []    # SKIP_EMULATORS = ["emulator-5562", "emulator-5554", "emulator-5556", "emulator-5558","emulator-5560"]    emulator_device_list = adbutil.filter_emulators(adbutil.get_adb_client().device_list(), SKIP_EMULATORS)    adbutil.check_emulator_list(emulator_device_list)    for device in emulator_device_list:        thread = threading.Thread(target=check_device_loop, args=(device,))        thread.start()        thread_list.append(thread)    for thread in thread_list:        thread.join()