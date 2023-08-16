# I_Love_Science_Fest
Instant Ubran Climate modelling

## Project Navigation

### Existing Files
- `pdf_texts.json`: This file should contain the texts that are going to be shown to the user at the end of the PDF file.
- `GUI/Scales.json`: Contains the scales of the cities that are ought to be shown to the user in the GUI while loading the app.
- `main.py`: Run this module to run the whole app, including the GUI.
- `GUI/gui_utility.py`: Contains the main GUI code for the app. The whole window is created here.
- `hd_utility.py`: The utility class, consisted of the required methods.

### Hidden Files
Due to security reasons, there are some files that are also included in the `.gitignore` that needs to be added by the user.
- `client_secrets.json`: This file contains some information about the Google Drive API. In order to obtain it, you have to download such a file from your Google Cloud by following the instructions given in the `MyGoogeDrive.py` module.
- `server_initialization_data.json`: File containing the information for connecting to our server in the following format:
    ```
    {
    "private_key_folder_path":"Your Path to Local Private Key File",
    "username":"Your Username on the Server",
    "server_ip":"Your Server IP",
    "port_number": "The Port on Your Server",
    "pass":"Your Private Key Password for decrypting it"
    }
    ```
- `GUI/google_drive_initialization_data.json`: File containing the folder id, in which the output of out file is going to be saved. The format of this file is as follows:
  ```
  {
    "folder_id": "Folder ID. Can be found in the URL of the folder in your Google Drive"
  }
  ```
