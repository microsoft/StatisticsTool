import os, sys
from azure.storage.blob import BlobServiceClient
from colorama import Fore
sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo


class AzureStorageHelper():
    def __init__(self, storage_id, container_name, connection_string):
        self.account_url = f"https://{storage_id}.blob.core.windows.net"
        self.container_client_obj = None
        self.blob_service_client_obj = None

        print(f"Try create client for container: {container_name}")
        if not connection_string:
            print("******************** ERROR ************")
            print("No connection string, work only with local files\n\n")
        else:
            # Create the BlobServiceClient object
            self.blob_service_client_obj = BlobServiceClient.from_connection_string(connection_string)
            self.container_client_obj = self.blob_service_client_obj.get_container_client(container_name)
        
        return

        

    def upload_file(self, source, dest):
        with open(source, 'rb') as data:
            self.container_client_obj.upload_blob(name=dest, data=data, overwrite=True)

    def blob_exists(self, blob_path):
        return self.container_client_obj.get_blob_client(blob_path).exists()

    def ls_files(self, path, recursive=False, specific_name = False):
        '''
        List files under a path, optionally recursively
        '''
        if specific_name == False and not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.container_client_obj.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or not '/' in relative_path:
                files.append(relative_path)
        return files

    def download_blob(self, blob_path, dst_file_path):
        print (f'{Fore.YELLOW}Start download blob{Fore.RESET} {blob_path} to local path {dst_file_path}')
        
        blob_data = self.container_client_obj.get_blob_client(blob_path).download_blob().readall()
        with open(dst_file_path, "wb") as file:
            file.write(blob_data)
        
        print (f'{Fore.YELLOW}Finished download{Fore.RESET}')
        
        return dst_file_path

  