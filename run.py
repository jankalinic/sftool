import adbutils
import threading
import bot


if __name__ == '__main__':
    logger = bot.logger
    logger.info("Started SF_Bot")

    # check installed adb
    bot.check_cli_tools_installed()

    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    emulator_device_list = adb.device_list()
    
    thread_list = []

    if len(emulator_device_list) == 0 or (len(emulator_device_list) == 1 and emulator_device_list[0].info == "offline"):
        logger.error("No running emulators, exiting now.")
        exit(1)

    for device in emulator_device_list:
        thread = threading.Thread(target=bot.check_device_loop, args=(device,))
        thread.start()
        thread_list.append(thread)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.debug("Program status: Ending program.")
        for thread in thread_list:
            thread.join()
