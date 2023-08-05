
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/GUI')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/back_end')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/front_end')))


from GUI import gui_utility
from GUI import hd_utility
from GUI import MyGoogleDrive

# Load Google Drive
try:
    my_drive = MyGoogleDrive.MyGoogleDrive(initilization_json_path = './GUI/google_drive_initialization_data.json')
except Exception as e:
    print("Exception:", e)

# Load GUI
gui_utility.GUI_Main_Page(my_drive)
