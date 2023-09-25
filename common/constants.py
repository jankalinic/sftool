import os

# PATHS
IMAGE_EXTENSION = ".png"
# ------
SFTOOL_DIR_PATH = os.path.join(os.path.dirname(__file__), "../")
IMAGES_DIR_PATH = os.path.join(SFTOOL_DIR_PATH, "images")
ORIGINAL_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "original")
# ------
ORIGINAL_NPC_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "npc")
ORIGINAL_ADS_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "ads")
ORIGINAL_TAVERN_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "tavern")
ORIGINAL_QUESTS_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "quests")
ORIGINAL_BUTTON_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, "buttons")
# ------
SCREENSHOT_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "screenshots")
# ------
OFFLINE = "offline"
NPC_SUFFIX = "npc"
CROPPED_SUFFIX = "cropped"
SCREENSHOT_SUFFIX = "screenshot"
# ------ THRESHOLDS
QUEST_PROGRESS_BAR_DIFF_THRESHOLD = 0.2
MENU_BUTTON_IMAGE_DIFF_THRESHOLD = 0.1
TV_IMAGE_DIFF_THRESHOLD = 0.12
CLOSE_AD_DIFF_THRESHOLD = 0.5
QUEST_DIFF_THRESHOLD = 0.01
NPC_THRESHOLD = 0.01
# ------ DICT KEYS
NAME_KEY = "name"
DIMENSIONS_KEY = "dimensions"
CLICK_LOCATION_KEY = "click_location"
STATE_KEY = "state"
PATH_KEY = "path"
X_KEY = "x"
Y_KEY = "y"
LEFT_KEY = "left"
RIGHT_KEY = "right"
TOP_KEY = "top"
BOTTOM_KEY = "bottom"
# ------


def new_location(x, y):
    return {X_KEY: x, Y_KEY: y}


def new_dimensions(left, top, right, bottom):
    return {LEFT_KEY: left, TOP_KEY: top, RIGHT_KEY: right, BOTTOM_KEY: bottom}


def new_coords(dimensions, location):
    return {DIMENSIONS_KEY: dimensions, CLICK_LOCATION_KEY: location}


def new_quest_data(name, dimensions):
    return {NAME_KEY: name, DIMENSIONS_KEY: dimensions}


def new_npc(name, dimensions, click_location):
    return {NAME_KEY: name, PATH_KEY: os.path.join(ORIGINAL_NPC_DIR_PATH, (name + IMAGE_EXTENSION)), DIMENSIONS_KEY: dimensions, CLICK_LOCATION_KEY: click_location}


def new_quest(name, dimensions, click_location):
    return {NAME_KEY: name, PATH_KEY: os.path.join(ORIGINAL_QUESTS_DIR_PATH, (name + IMAGE_EXTENSION)), DIMENSIONS_KEY: dimensions, CLICK_LOCATION_KEY: click_location}


def new_button(name, dimensions, click_location):
    return {NAME_KEY: name, PATH_KEY: os.path.join(ORIGINAL_BUTTON_DIR_PATH, (name + IMAGE_EXTENSION)), DIMENSIONS_KEY: dimensions, CLICK_LOCATION_KEY: click_location}


# ---------------------------
# BUTTONS
# ----- ADS
AD_BUTTON = new_button("ad", new_dimensions(110, 180, 275, 360), new_location(188, 277))
CLOSE_AD_BUTTON = new_button("close-ad", new_dimensions(980, 0, 1080, 100), new_location(1013, 55))
DONT_CLOSE_AD_BUTTON = new_button("dont-close-button", new_dimensions(980, 0, 1080, 100), new_location(0, 0))
# ----- BEER
DRINK_BEER_MUSHROOM_BUTTON = new_button("beer-mushroom-button", new_dimensions(578, 1425, 672, 1515), new_location(624, 1462))
BEER_TAVERN_BUTTON = new_button("beer-button", new_dimensions(324, 1738, 443, 1858), new_location(324, 1738))
# ----- QUEST
ACCEPT_QUEST_BUTTON = new_button("accept-quest-button", new_dimensions(353, 1420, 728, 1505), new_location(533, 1450))
QUEST_DONE_OK_BUTTON = new_button("quest-done-ok-button", new_dimensions(315, 1444, 760, 1603), new_location(536, 1530))
# ---------------------------------------------
# QUESTS
# ----------- NPCS
TAVERN_MASTER = new_npc("tavern-master", new_dimensions(779, 764, 879, 864), new_location(822, 815))
# ------
DRUNKEN_GUY = new_npc("drunken-guy", new_dimensions(465, 946, 624, 1154), new_location(536, 1530))
PRINCE_CHARMING = new_npc("prince-charming", new_dimensions(188, 1050, 355, 1175), new_location(264, 1122))
PRINCESS_DIANA = new_npc("princess-diana", new_dimensions(406, 848, 570, 1010), new_location(494, 974))
ORC = new_npc("orc", new_dimensions(420, 940, 610, 1040), new_location(505, 995))
CONAN = new_npc("conan", new_dimensions(338, 848, 565, 1000), new_location(426, 935))
ELF = new_npc("elf", new_dimensions(445, 1010, 627, 1100), new_location(545, 1060))
WIZARD = new_npc("wizard", new_dimensions(318, 862, 444, 980), new_location(394, 932))
KK_MEMBER = new_npc("kk-member", new_dimensions(329, 934, 471, 1037), new_location(394, 984))
MAP_GUY = new_npc("map-guy", new_dimensions(431, 696, 536, 840), new_location(484, 826))
FIDGET = new_npc("fidget", new_dimensions(560, 945, 746, 1044), new_location(642, 999))
# ------
QUEST_NPC_LIST = [DRUNKEN_GUY, PRINCE_CHARMING, PRINCESS_DIANA, ORC, CONAN, ELF, WIZARD, KK_MEMBER, MAP_GUY, FIDGET]
# ------ 200x57
GOLD_DATA = new_quest_data("gold-number", new_dimensions(130, 1240, 330, 1297))
EXP_DATA = new_quest_data("exp-number", new_dimensions(130, 1313, 330, 1370))
TIME_DATA = new_quest_data("time-number", new_dimensions(130, 1390, 330, 1447))
# ------
QUEST_AD = new_quest("quest-ad", new_dimensions(767, 1420, 1048, 1494), new_location(888, 1444))
QUEST_AD_WO_HOURGLASS = new_quest("quest-ad-without-hourglass", new_dimensions(591, 1388, 967, 1487), new_location(764, 1419))
QUEST_PROGRESS_BAR = new_quest("quest-progress-bar", new_dimensions(641, 1638, 678, 1654), new_location(0, 0))
# ------
FIRST_QUEST = new_quest("first-quest", new_dimensions(409, 425, 471, 468), new_location(444, 448))
SECOND_QUEST = new_quest("second-quest", new_dimensions(644, 425, 702, 468), new_location(680, 448))
THIRD_QUEST = new_quest("third-quest", new_dimensions(878, 425, 949, 468), new_location(911, 448))
QUEST_LIST = [FIRST_QUEST, SECOND_QUEST, THIRD_QUEST]
