import os

# PATHS
IMAGE_EXTENSION = ".png"

SFTOOL_DIR_PATH = os.path.join(os.path.dirname(__file__), "../")
IMAGES_DIR_PATH = os.path.join(SFTOOL_DIR_PATH, "images")
ORIGINAL_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "original")

ORIGINAL_NPC_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "npc")
ORIGINAL_ADS_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "ads")
ORIGINAL_QUESTS_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "quests")


# original constant images - readonly files
ORIGINAL_TV_IMAGE_PATH = os.path.join(ORIGINAL_ADS_DIR_PATH, "colorTV.png")
ORIGINAL_MENU_BUTTON_IMAGE_PATH = os.path.join(ORIGINAL_ADS_DIR_PATH, "menuButton.png")
DONT_CLOSE_ADD_BUTTON_PATH = os.path.join(ORIGINAL_ADS_DIR_PATH, "dontCloseButton.png")

FIRST_QUEST_IMAGE_PATH = os.path.join(ORIGINAL_QUESTS_DIR_PATH, "firstQuest.png")


# list of close ad buttons as they may vary
ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "closebuttons")
ORIGINAL_CLOSE_AD_IMAGES_PATHS = [os.path.join(ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH, file) for file in os.listdir(ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH)]

# Screenshot dir
SCREENSHOT_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "screenshots")
SCREENSHOT_PATH_PREFIX = os.path.join(SCREENSHOT_DIR_PATH, "screenshot-")
CROPPED_SCREENSHOT_PATH_PREFIX = os.path.join(SCREENSHOT_DIR_PATH, "cropped-")

NAME_KEY = "name"
DIMENSIONS_KEY = "dimensions"
CLICK_LOCATION_KEY = "click_location"
STATE_KEY = "state"


def new_location(x, y):
    return {'x': x, 'y': y}


def new_dimensions(left, top, right, bottom):
    return {'left': left, 'top': top, 'right': right, 'bottom': bottom}

def new_coords(dimensions, location):
    return {
        DIMENSIONS_KEY: dimensions,
        CLICK_LOCATION_KEY: location
    }


def new_npc(name, dimensions, click_location):
    return {
        NAME_KEY: name,
        DIMENSIONS_KEY: dimensions,
        CLICK_LOCATION_KEY: click_location
    }


def new_quest(dimensions, click_location):
    return new_coords(dimensions, click_location)


# ---------------------------
#  ADS

TV_LOCATION = new_location(188, 277)
TV_IMAGE_DIMENSIONS = new_dimensions(110, 180, 275, 360)

CLOSE_AD_LOCATION = new_location(1013, 55)
CLOSE_AD_DIMENSIONS = new_dimensions(980, 30, 1050, 100)

MENU_BUTTON_IMAGE_DIMENSIONS = new_dimensions(65, 1725, 210, 1865)
# ---------------------------
#  QUESTS

TAVERN_MASTER = new_npc("tavern-master", new_dimensions(779, 764, 905, 870), new_location(822, 815))
DRUNKEN_GUY = new_npc("drunken-guy", new_dimensions(465, 946, 624, 1154), new_location(536, 1530))
PRINCE_CHARMING = new_npc("prince-charming", new_dimensions(188, 1050, 355, 1175), new_location(264, 1122))
PRINCESS_DIANA = new_npc("princess-diana", new_dimensions(406, 848, 570, 1010), new_location(494, 974))
ORC = new_npc("orc", new_dimensions(420, 940, 610, 1040), new_location(505, 995))
CONAN = new_npc("conan", new_dimensions(338, 848, 565, 1000), new_location(426, 935))
ELF = new_npc("elf", new_dimensions(338, 848, 565, 1000), new_location(426, 935))
QUEST_NPC_LIST = [DRUNKEN_GUY, PRINCE_CHARMING, PRINCESS_DIANA, ORC, CONAN, ELF]

DRINK_BEER_LOCATION = new_location(624, 1462)
DRINK_BEER_MUSHROOM_DIMENSIONS = new_dimensions(578, 1425, 672, 1515)

# NUMBERS
GOLD_TEXT_DIMENSIONS = new_dimensions(136, 1243, 316, 1292)
EXP_TEXT_DIMENSIONS = new_dimensions(136, 1316, 316, 1365)
TIME_TEXT_DIMENSIONS = new_dimensions(136, 1395, 316, 1444)

FIRST_QUEST = new_quest(new_dimensions(349, 407, 533, 485), new_location(444, 448))
SECOND_QUEST = new_quest(new_dimensions(581, 407, 777, 485), new_location(680, 448))
THIRD_QUEST = new_quest(new_dimensions(819, 407, 1010, 485), new_location(911, 448))

ACCEPT_QUEST_LOCATION = new_location(533, 1450)
SKIP_QUEST_AD = new_coords(new_dimensions(963, 1414, 1050, 480), new_location(900, 1444))

# Quest tools
QUEST_DONE_OK_BUTTON = new_coords(new_dimensions(315, 1444, 760, 1603), new_location(536, 1530))


AD_SUFFIX = "ad"
CLOSE_AD_SUFFIX = "close-ad"
TIERS_SUFFIX = "tiers"
MENU_BUTTON_SUFFIX = "menu-button"
GOLD_NUM_SUFFIX = "gold-number"
EXP_NUM_SUFFIX = "exp-number"
TIME_NUM_SUFFIX = "time-number"
NPC_SUFFIX = "npc"
# Threshold for hist diff
MENU_BUTTON_IMAGE_DIFF_THRESHOLD = 0.1
TV_IMAGE_DIFF_THRESHOLD = 0.12
CLOSE_AD_DIFF_THRESHOLD = 0.5
QUEST_DIFF_THRESHOLD = 0.2
NPC_THRESHOLD = 0.15
