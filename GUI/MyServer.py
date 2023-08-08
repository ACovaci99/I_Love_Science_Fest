import os
import datetime
import paramiko # pip install paramiko

class SFTPClient:
    def __init__(self, server_ip, username, private_key_path):
        '''
        Example Usage:
        sftp = SFTPClient('your_server_ip', 'your_username', 'path_to_your_private_key')
        sftp.create_directory()
        pdf_url = sftp.get_url(sftp.upload_file('local_path_to_your_pdf.pdf'))
        jpg_url = sftp.get_url(sftp.upload_file('local_path_to_your_image.jpg'))
        sftp.close_connection()

        print(f"PDF URL: {pdf_url}")
        print(f"Image URL: {jpg_url}")
        '''

        self.server_ip = server_ip
        self.username = username
        self.private_key = paramiko.RSAKey(filename=private_key_path)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(server_ip, username=username, pkey=self.private_key)
        self.sftp = self.client.open_sftp()

    def create_directory(self):
        dir_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.current_directory = f'/var/www/{dir_name}'  # adjust this based on where you want to create the directories
        self.sftp.mkdir(self.current_directory)
        return self.current_directory

    def upload_file(self, local_path):
        remote_path = os.path.join(self.current_directory, os.path.basename(local_path))
        self.sftp.put(local_path, remote_path)
        return remote_path

    def get_url(self, remote_path):
        # you will need to adjust the base URL below to match your server's configuration
        return f'http://{self.server_ip}/{remote_path}'

    def close_connection(self):
        self.sftp.close()
        self.client.close()
