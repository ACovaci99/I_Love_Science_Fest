from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from hd_utility import HD_Utility
from datetime import datetime
import json
# Before Using this module, you should setup a Google Drive API. Use these two links as instruction to do so:
# 1. https://developers.google.com/drive/api/quickstart/python
# 2. https://www.projectpro.io/recipes/upload-files-to-google-drive-using-python
# 3. https://developers.google.com/workspace/guides/create-credentials#choose_the_access_credential_that_is_right_for_you
# After setting the API, copy the client_secrets.json file (which you should download from the API page) and paste it next to main.py in the same directory.


import os
# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

class MyGoogleDrive:
    def __init__(self, initilization_json_path = None):
        self.creds = self.sign_in()
        if(initilization_json_path):
            self.google_drive_json = HD_Utility.read_json_file(initilization_json_path)
            self.folder_id = self.google_drive_json["folder_id"]
            self.make_folder_public(self.folder_id)



    def sign_in(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def upload_image(self, file_path, file_name, folder_id):
        drive_service = build('drive', 'v3', credentials=self.creds)
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='image/jpeg')
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))
        return file.get('id')

    def make_folder_public(self, folder_id):
        drive_service = build('drive', 'v3', credentials=self.creds)
        batch = drive_service.new_batch_http_request()
        user_permission = {
            'type': 'anyone',
            'role': 'reader',
        }
        batch.add(drive_service.permissions().create(
            fileId=folder_id,
            body=user_permission,
            fields='id',
        ))
        batch.execute()

    def get_file_url(self, file_id):
        drive_service = build('drive', 'v3', credentials=self.creds)
        result = drive_service.files().get(fileId=file_id, fields='webViewLink').execute()
        print('Shareable link: %s' % result.get('webViewLink'))
        return result.get('webViewLink')

if __name__ == '__main__':
    # my_drive = MyGoogleDrive()
    # name = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # file_id = my_drive.upload_image('1.png', f'My Photo - {name}', '1CXVI1h_wzcwPIeqaS3mMvgQZlL0s14DH')
    # my_drive.make_folder_public('1CXVI1h_wzcwPIeqaS3mMvgQZlL0s14DH')
    # url = my_drive.get_file_url(file_id)
    # print(url)
    print("finished")
