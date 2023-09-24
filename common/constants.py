import os

# PATHS
SFTOOL_DIR_PATH = os.path.join(os.path.dirname(__file__), "../")
IMAGES_DIR_PATH = os.path.join(SFTOOL_DIR_PATH, "images")
ORIGINAL_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "original")
# original constant images - readonly files
ORIGINAL_TV_IMAGE_PATH = os.path.join(ORIGINAL_DIR_PATH, "colorTV.png")
# Tavern homebutton
ORIGINAL_MENU_BUTTON_IMAGE_PATH = os.path.join(IMAGES_DIR_PATH, "original", "menuButton.png")
DONT_CLOSE_ADD_BUTTON_PATH = os.path.join(IMAGES_DIR_PATH, "original", "dontCloseButton.png")

# list of close ad buttons as they may vary
ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "closebuttons")
ORIGINAL_CLOSE_AD_IMAGES_PATHS = [os.path.join(ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH, file) for file in os.listdir(ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH)]

# Screenshot dir
SCREENSHOT_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "screenshots")
SCREENSHOT_PATH_PREFIX = os.path.join(SCREENSHOT_DIR_PATH, "screenshot-")
CROPPED_SCREENSHOT_PATH_PREFIX = os.path.join(SCREENSHOT_DIR_PATH, "cropped-")
# --------
# Vars
# Open AD
TV_LOCATION = {'x': 188, 'y': 277}
TV_IMAGE_DIMENSIONS = {'left': 110, 'top': 180, 'right': 275, 'bottom': 360}
# Close AD
CLOSE_AD_LOCATION = {'x': 1013, 'y': 55}
CLOSE_AD_DIMENSIONS = {'left': 980, 'top': 30, 'right': 1050, 'bottom': 100}

MENU_BUTTON_IMAGE_DIMENSIONS = {'left': 65, 'top': 1725, 'right': 210, 'bottom': 1865}

AD_SUFFIX = "ad"
CLOSE_AD_SUFFIX = "close-ad"
MENU_BUTTON_SUFFIX = "menu-button"
# --------
# Consts and glob
SERIAL_KEY = "serialno"
STATE_KEY = "state"
IMAGE_EXTENSION = ".png"
MENU_BUTTON_IMAGE_DIFF_THRESHOLD = 0.1
TV_IMAGE_DIFF_THRESHOLD = 0.12
CLOSE_AD_DIFF_THRESHOLD = 0.5
