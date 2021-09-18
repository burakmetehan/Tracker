from pathlib import Path
import os

#====================================GLOBALS====================================
MAIN_PATH = Path(__file__).parent.absolute()
os.chdir(MAIN_PATH)

CONFIG_FILE_PATH = "./files/config.json"
ACTIVITY_FILE_PATH = "./files/activity.json"
TODAY_ACTIVITY_FILE_PATH = "./files/today_activity.json"
TODOFRAME_ACTIVITY_PATH = "./files/todoframe_activity.json"
#===============================================================================

#===============================TimerFrame Texts================================
POP_UP_WINDOW_TITLE = "Insert Information"
POP_UP_WINDOW_MESSAGE = "Enter a category, subcategory and description"

YES_OR_NO_MESSAGE_BOX_TEXT = "There is not active activity in todo list. Do you want to insert information?\nIf you choose \"No\" the item will be saved without information."
BREAK_DONE_MESSAGE_BOX_TEXT = "Break is done. Next activity will be super."
ACTIVITY_DONE_MESSAGE_BOX_TEXT = "Activity is done. The activity is saved in your activities."
#===============================================================================

#================================ToDoFrame Texts================================
TODO_YES_OR_NO_MESSAGE_BOX_TEXT = "The catergory or/and subcategory or/and description is not inserted properly. Do you want to continue without insert?\nIf you choose \"Yes\" item will be saved without information.\nIf you choose \"No\" item will not be saved"
#===============================================================================
