import os
import time

import common.common_utils as util
import common.constants as const


class Emul:
    serial: str = ""

    def __init__(self, serial):
        self.serial = serial


if __name__ == '__main__':
    emulator = Emul("")
    IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images", "emulator-5554", const.EXP_DATA[const.NAME_KEY] + const.IMAGE_EXTENSION)
    start_time = time.time()
    number = util.get_number_from_image(IMAGE_PATH, config="--psm 5 -c tessedit_char_whitelist=0123456789.,:")
    print(f"Extracted number: {number}")
    print(f"Execution of number recognition took: {time.time() - start_time:.6f} seconds")