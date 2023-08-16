import os
import datetime
import paramiko # pip install paramiko

class SFTPClient:



    def __init__(self, server_ip, username, port, private_key_path, passphrase = None):
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
        self.port = port
        self.username = username
        self.private_key_path = private_key_path
        self.transport = paramiko.Transport((server_ip, port))
        self.current_directory = f'/var/www/ilsf/images'

        # Load the private key
        mykey = paramiko.RSAKey(filename=self.private_key_path, password=passphrase)

        # print(f"Username: {self.username} | Pass: {passphrase} | Port: {self.port} | IP: {self.server_ip}")

        self.transport.connect(username=self.username, pkey=mykey)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def create_directory(self):
        dir_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.current_directory = f'/var/www/ilsf/images/{dir_name}'  # adjust this based on where you want to create the directories
        print("[Create Directory]: Current Directory: ")
        self.sftp.mkdir(self.current_directory)
        return self.current_directory

    def upload_file(self, local_path):
        # remote_path = os.path.join(self.current_directory, os.path.basename(local_path))
        remote_path = self.current_directory + "/" + os.path.basename(local_path)
        self.sftp.put(local_path, remote_path)
        return remote_path

    def get_url(self, remote_path):
        # Assuming the server hosts files at URLs matching their paths
        return f'http://{self.server_ip}:{self.port}{remote_path}'

    def close_connection(self):
        self.sftp.close()
        self.transport.close()

    def upload_new_document(self, path_to_file):

        # Create New Directory On Server
        # remote_directory_path_url = self.create_directory()
        # print(f"Created: {remote_directory_path_url}")

        # Upload The File on Server
        remote_file_path = self.upload_file(path_to_file)
        print("Uploaded to local path: ", remote_file_path)

        # Get Full Path To File
        # full_path_url = self.get_url(remote_file_path)
        full_path_url = "https://ilsf.duckdns.org/?image=" + path_to_file
        print("Received Full Path: ", full_path_url)


        # Close Connection
        #self.close_connection()

        return full_path_url