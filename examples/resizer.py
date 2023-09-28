import cv2
import os
import subprocess
from common import constants as const
from common import common_utils as util

if __name__ == '__main__':

    # Load the image
    in_image_path = os.path.join(os.path.dirname(__file__), "images", "full.png")
    out_image_path = os.path.join(os.path.dirname(__file__), "images", "out.png")

    util.enhance_number_image(in_image_path)
    result = util.get_number_from_image(util.get_contrasted_image_path(in_image_path))

    print(f"text = {result}")