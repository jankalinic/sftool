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
# ------
ORIGINAL_TV_IMAGE_PATH = os.path.join(ORIGINAL_TAVERN_DIR_PATH, "colorTV.png")
ORIGINAL_MENU_BUTTON_IMAGE_PATH = os.path.join(ORIGINAL_TAVERN_DIR_PATH, "menuButton.png")
ORIGINAL_MENU_BUTTON_NOTIFICATION_IMAGE_PATH = os.path.join(ORIGINAL_TAVERN_DIR_PATH, "menuButtonNotification.png")
ORIGINAL_DONT_CLOSE_ADD_BUTTON_IMAGE_PATH = os.path.join(ORIGINAL_TAVERN_DIR_PATH, "dontCloseButton.png")
ORIGINAL_BEER_BUTTON_IMAGE_PATH = os.path.join(ORIGINAL_TAVERN_DIR_PATH, "beerMushroomButton.png")

FIRST_QUEST_IMAGE_PATH = os.path.join(ORIGINAL_QUESTS_DIR_PATH, "firstQuest.png")
SECOND_QUEST_IMAGE_PATH = os.path.join(ORIGINAL_QUESTS_DIR_PATH, "secondQuest.png")
THIRD_QUEST_IMAGE_PATH = os.path.join(ORIGINAL_QUESTS_DIR_PATH, "thirdQuest.png")
QUEST_PROGRESS_BAR_IMAGE_PATH = os.path.join(ORIGINAL_QUESTS_DIR_PATH, "questProgressBar.png")
QUEST_AD_IMAGE_PATH = os.path.join(ORIGINAL_QUESTS_DIR_PATH, "questAd.png")
ACCEPT_QUEST_BUTTON_IMAGE_PATH = os.path.join(ORIGINAL_QUESTS_DIR_PATH, "acceptQuestButton.png")

TAVERN_MASTER_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "tavernMaster.png")
DRUNKEN_GUY_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "drunkenGuy.png")
PRINCE_CHARMING_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "princeCharming.png")
PRINCESS_DIANA_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "princesDiana.png")
ORC_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "orc.png")
CONAN_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "conan.png")
ELF_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "elf.png")
WIZARD_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "wizard.png")
KK_MEMBER_IMAGE_PATH = os.path.join(ORIGINAL_NPC_DIR_PATH, "kkMember.png")
# ------
# list of close ad buttons as they may vary
ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH = os.path.join(ORIGINAL_ADS_DIR_PATH, "closebuttons")
ORIGINAL_CLOSE_AD_IMAGES_PATHS = [os.path.join(ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH, file) for file in os.listdir(ORIGINAL_CLOSE_AD_IMAGES_DIR_PATH)]
# ------
SCREENSHOT_DIR_PATH = os.path.join(IMAGES_DIR_PATH, "screenshots")
SCREENSHOT_PATH_PREFIX = os.path.join(SCREENSHOT_DIR_PATH, "screenshot-")
CROPPED_SCREENSHOT_PATH_PREFIX = os.path.join(SCREENSHOT_DIR_PATH, "cropped-")
# ------
OFFLINE = "offline"
AD_SUFFIX = "ad"
CLOSE_AD_SUFFIX = "close-ad"
TIERS_SUFFIX = "tiers"
FIRST_QUEST_SUFFIX = "first-quest"
MENU_BUTTON_SUFFIX = "menu-button"
GOLD_NUM_SUFFIX = "gold-number"
EXP_NUM_SUFFIX = "exp-number"
TIME_NUM_SUFFIX = "time-number"
NPC_SUFFIX = "npc"
# ------
# Thresholds
MENU_BUTTON_IMAGE_DIFF_THRESHOLD = 0.1
TV_IMAGE_DIFF_THRESHOLD = 0.12
CLOSE_AD_DIFF_THRESHOLD = 0.5
QUEST_DIFF_THRESHOLD = 0.09
NPC_THRESHOLD = 0.15
# ------
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


def new_npc(name, path, dimensions, click_location):
    return {NAME_KEY: name, PATH_KEY: path, DIMENSIONS_KEY: dimensions, CLICK_LOCATION_KEY: click_location}


def new_quest(name, path, dimensions, click_location):
    return {NAME_KEY: name, PATH_KEY: path, DIMENSIONS_KEY: dimensions, CLICK_LOCATION_KEY: click_location}


def new_button(name, path, dimensions, click_location):
    return {NAME_KEY: name, PATH_KEY: path, DIMENSIONS_KEY: dimensions, CLICK_LOCATION_KEY: click_location}


# ---------------------------
#  ADS
TV_LOCATION = new_location(188, 277)
TV_IMAGE_DIMENSIONS = new_dimensions(110, 180, 275, 360)
# ------
CLOSE_AD_LOCATION = new_location(1013, 55)
CLOSE_AD_DIMENSIONS = new_dimensions(980, 30, 1050, 100)
# ------
MENU_BUTTON_IMAGE_DIMENSIONS = new_dimensions(65, 1725, 210, 1865)
# ---------------------------
#  QUESTS
TAVERN_MASTER = new_npc("tavern-master", TAVERN_MASTER_IMAGE_PATH, new_dimensions(779, 764, 879, 864), new_location(822, 815))
# ------
DRUNKEN_GUY = new_npc("drunken-guy", DRUNKEN_GUY_IMAGE_PATH, new_dimensions(465, 946, 624, 1154), new_location(536, 1530))
PRINCE_CHARMING = new_npc("prince-charming", PRINCE_CHARMING_IMAGE_PATH,new_dimensions(188, 1050, 355, 1175), new_location(264, 1122))
PRINCESS_DIANA = new_npc("princess-diana", PRINCESS_DIANA_IMAGE_PATH,new_dimensions(406, 848, 570, 1010), new_location(494, 974))
ORC = new_npc("orc", ORC_IMAGE_PATH,new_dimensions(420, 940, 610, 1040), new_location(505, 995))
CONAN = new_npc("conan", CONAN_IMAGE_PATH, new_dimensions(338, 848, 565, 1000), new_location(426, 935))
ELF = new_npc("elf", ELF_IMAGE_PATH, new_dimensions(338, 848, 565, 1000), new_location(426, 935))
WIZARD = new_npc("wizard", WIZARD_IMAGE_PATH, new_dimensions(318, 862, 444, 980), new_location(394, 932))
KK_MEMBER = new_npc("kk-member", KK_MEMBER_IMAGE_PATH, new_dimensions(329, 934, 471, 1037), new_location(394, 984))
# -------
QUEST_NPC_LIST = [DRUNKEN_GUY, PRINCE_CHARMING, PRINCESS_DIANA, ORC, CONAN, ELF, WIZARD, KK_MEMBER]
# ------
DRINK_BEER_MUSHROOM_BUTTON = new_button("mushroom-button", ORIGINAL_BEER_BUTTON_IMAGE_PATH,new_dimensions(578, 1425, 672, 1515), new_location(624, 1462))
# ------
GOLD_TEXT_DIMENSIONS = new_dimensions(136, 1243, 316, 1292)
EXP_TEXT_DIMENSIONS = new_dimensions(136, 1316, 316, 1365)
TIME_TEXT_DIMENSIONS = new_dimensions(136, 1395, 316, 1444)
# ------
QUEST_AD = new_quest("quest-ad", QUEST_AD_IMAGE_PATH, new_dimensions(767, 1420, 1048, 1494), new_location(888, 1444))
QUEST_PROGRESS_BAR = new_quest("quest-progress-bar", QUEST_PROGRESS_BAR_IMAGE_PATH, new_dimensions(641, 1638, 678, 1654), new_location(0, 0))
FIRST_QUEST = new_quest("first-quest", FIRST_QUEST_IMAGE_PATH, new_dimensions(409, 425, 471, 468), new_location(444, 448))
SECOND_QUEST = new_quest("second-quest", SECOND_QUEST_IMAGE_PATH, new_dimensions(644, 425, 702, 468), new_location(680, 448))
THIRD_QUEST = new_quest("third-quest", THIRD_QUEST_IMAGE_PATH, new_dimensions(878, 425, 949, 468), new_location(911, 448))
QUEST_LIST = [FIRST_QUEST, SECOND_QUEST, THIRD_QUEST]
# ------
ACCEPT_QUEST_BUTTON = new_button("accept-quest", ACCEPT_QUEST_BUTTON_IMAGE_PATH, new_dimensions(353, 1420, 728, 1505), new_location(533, 1450))
# ------
QUEST_DONE_OK_BUTTON = new_coords(new_dimensions(315, 1444, 760, 1603), new_location(536, 1530))

