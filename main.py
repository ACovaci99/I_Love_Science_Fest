
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/GUI')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/back_end')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/front_end')))


from GUI import gui_utility
from GUI import hd_utility
from GUI import MyGoogleDrive

# Load Google Drive
my_drive = MyGoogleDrive.MyGoogleDrive(initilization_json_path = 'D:/github/I_Love_Science_Fest/GUI/google_drive_initialization_data.json')

# Load GUI
gui_utility.GUI_Main_Page(my_drive)
