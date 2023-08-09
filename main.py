
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/GUI'))) 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/back_end')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/front_end')))


from GUI import gui_utility
from GUI import hd_utility
from GUI import MyGoogleDrive

# Load Google Drive
try:
    my_drive = MyGoogleDrive.MyGoogleDrive(initilization_json_path = './GUI/google_drive_initialization_data.json')
    print()
except Exception as e:
    print("Exception:", e)



# Load Texts JSON
pdf_texts_json = hd_utility.HD_Utility.read_json_file('pdf_texts.json')

# Load GUI
gui_utility.GUI_Main_Page(my_drive, pdf_texts_json)
