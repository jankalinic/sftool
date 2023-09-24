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


# Quest persons
DRUNKEN_GUY_QUEST_LOCATION = {'x': 536, 'y': 1530}
DRUNKEN_GUY_QUEST_DIMENSIONS = {'left': 465, 'top': 946, 'right': 624, 'bottom': 1154}

PRINCE_CHARMING_QUEST_LOCATION = {'x': 264, 'y': 1122}
PRINCE_CHARMING_QUEST_DIMENSIONS = {'left': 188, 'top': 1050, 'right': 355, 'bottom': 1175}

PRINCES_DIANA_QUEST_LOCATION = {'x': 494, 'y': 974}
PRINCES_DIANA_QUEST_DIMENSIONS = {'left': 406, 'top': 848, 'right': 570, 'bottom': 1010}

ORC_QUEST_LOCATION = {'x': 505, 'y': 995}
ORC_QUEST_DIMENSIONS = {'left': 420, 'top': 940, 'right': 610, 'bottom': 1040}

CONAN_QUEST_LOCATION = {'x': 426, 'y': 935}
CONAN_QUEST_DIMENSIONS = {'left': 338, 'top': 848, 'right': 565, 'bottom': 1000}

ELF_QUEST_LOCATION = {'x': 426, 'y': 935}
ELF_QUEST_DIMENSIONS = {'left': 338, 'top': 848, 'right': 565, 'bottom': 1000}

TAVERN_MASTER_LOCATION = {'x': 822, 'y': 815}
TAVERN_MASTER_DIMENSIONS = {'left': 779, 'top': 764, 'right': 905, 'bottom': 870}

DRINK_BEER_LOCATION = {'x': 624, 'y': 1462}
DRINK_BEER_MUSHROOM_DIMENSIONS = {'left': 578, 'top': 1425, 'right': 672, 'bottom': 1515}

# NUMBERS
GOLD_TEXT_DIMENSIONS = {'left': 136, 'top': 1243, 'right': 316, 'bottom': 1292}
EXP_TEXT_DIMENSIONS = {'left': 136, 'top': 1316, 'right': 316, 'bottom': 1365}
TIME_TEXT_DIMENSIONS = {'left': 136, 'top': 1395, 'right': 316, 'bottom': 1444}

FIRST_QUEST_LOCATION = {'x': 444, 'y': 448}
FIRST_QUEST_DIMENSIONS = {'left': 349, 'top': 407, 'right': 533, 'bottom': 485}

SECOND_QUEST_LOCATION = {'x': 680, 'y': 448}
SECOND_QUEST_DIMENSIONS = {'left': 581, 'top': 407, 'right': 777, 'bottom': 485}

THIRD_QUEST_LOCATION = {'x': 911, 'y': 448}
THIRD_QUEST_DIMENSIONS = {'left': 819, 'top': 407, 'right': 1010, 'bottom': 485}

ACCEPT_QUEST_LOCATION = {'x': 533, 'y': 1450}

SKIP_QUEST_AD_LOCATION = {'x': 900, 'y': 1444}
SKIP_QUEST_AD_DIMENSIONS = {'left': 963, 'top': 1414, 'right': 1050, 'bottom': 480}

# Quest tools
QUEST_DONE_OK_BUTTON_LOCATION = {'x': 536, 'y': 1530}
QUEST_DONE_OK_BUTTON_DIMENSIONS = {'left': 315, 'top': 1444, 'right': 760, 'bottom': 1603}


AD_SUFFIX = "ad"
CLOSE_AD_SUFFIX = "close-ad"
MENU_BUTTON_SUFFIX = "menu-button"
GOLD_NUM_SUFFIX = "gold-number"
EXP_NUM_SUFFIX = "exp-number"
TIME_NUM_SUFFIX = "time-number"
# --------
# Consts and glob
STATE_KEY = "state"
IMAGE_EXTENSION = ".png"
MENU_BUTTON_IMAGE_DIFF_THRESHOLD = 0.1
TV_IMAGE_DIFF_THRESHOLD = 0.12
CLOSE_AD_DIFF_THRESHOLD = 0.5
