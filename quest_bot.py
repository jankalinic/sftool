from common.custom_logger import logger, DEBUG_LEVEL

if __name__ == '__main__':
    logger.setLevel(DEBUG_LEVEL)
    logger.info("Started Shakes_AD_Bot")

    # check installed adb
    check_cli_tools_installed()

    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    emulator_device_list = adb.device_list()

    thread_list = []

    if len(emulator_device_list) == 0 or (len(emulator_device_list) == 1 and emulator_device_list[0].info == "offline"):
        logger.error("No running emulators, exiting now.")
        exit(1)

    for device in emulator_device_list:
        thread = threading.Thread(target=check_device_loop, args=(device,))
        thread.start()
        thread_list.append(thread)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.debug("Program status: Ending program.")
        for thread in thread_list:
            thread.join()