
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/GUI')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/back_end')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/front_end')))


from GUI import gui_utility
from GUI import hd_utility
from GUI import MyGoogleDrive
from MyServer import SFTPClient as Server

# Load Google Drive
try:
    my_drive = MyGoogleDrive.MyGoogleDrive(initilization_json_path = './GUI/google_drive_initialization_data.json')
    print()
except Exception as e:
    print("Google Drive Initialization Exception:", e)

# Load My Server
try:
    credentials_json = hd_utility.HD_Utility.read_json_file('server_initialization_data.json')
    my_server = Server(server_ip= credentials_json["server_ip"],
                        username = credentials_json["username"],
                        port = int(credentials_json["port_number"]) ,
                        private_key_path = credentials_json["public_key_folder_path"],
                        passphrase= credentials_json["pass"])
    print()
except Exception as e:
    print("Server Initialization Exception:", e)



# Load Texts JSON
pdf_texts_json = hd_utility.HD_Utility.read_json_file('pdf_texts.json')

# Load GUI
gui_utility.GUI_Main_Page(my_drive, pdf_texts_json, my_server)
