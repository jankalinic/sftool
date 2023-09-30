import os
import time
import subprocess
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from common import constants as const
from common import common_utils as util

def bw_image(image_path, out_image_path):

    image = Image.open(image_path)
    image = image.resize((image.width * const.RESIZE_RATIO, image.height * const.RESIZE_RATIO))

    # ImageEnhance.Contrast(image.convert('L')).enhance(10).point(lambda x: 0 if x < 200 else 255, '1').show()
    # ImageEnhance.Contrast(image).enhance(10).convert('L').point(lambda x: 0 if x < 100 else 255, '1').show()
    # image.convert('L').point(lambda x: 0 if x < 100 else 255, '1').show()

    image = image.convert('L')
    image = image.filter(ImageFilter.MedianFilter())
    image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Thresholding
    image = image.filter(ImageFilter.MedianFilter())
    image = ImageOps.invert(image)
    # image.show()
    image = image.convert('L').filter(ImageFilter.GaussianBlur(radius=1.5))
    image.save(out_image_path)


def convert_to_svg(input_path, output_path):
    start = time.time()



if __name__ == '__main__':
    img_dir = os.path.join(os.path.dirname(__file__), "images")
    image_path = os.path.join(img_dir, "exp-number.png")
    out_image_path = os.path.join(img_dir, "exp-number-out.png")
    output_path = os.path.join(img_dir, "exp-number-out-DONE.png")


    text = util.get_number_from_image(image_path)

    time.sleep(2)

    #
    # image = Image.open(image_path)
    #
    # image = image.resize((image.width * const.RESIZE_RATIO, image.height * const.RESIZE_RATIO))
    # image = image.convert('L')
    # image = ImageEnhance.Contrast(image).enhance(5)
    # image = image.point(lambda x: 0 if x < threshold else 255, '1')
    # image = image.convert('L').filter(ImageFilter.MedianFilter(size=9))
    # image.save(get_contrasted_image_path(image_path))