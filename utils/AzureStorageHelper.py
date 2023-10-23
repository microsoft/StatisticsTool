import os, sys
from azure.storage.blob import BlobServiceClient
from colorama import Fore
sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo


class AzureStorageHelper():
    '''
    A helper class for interacting with Azure Blob Storage
    '''

    def __init__(self, storage_id, container_name, connection_string):
        '''
        Initializes the AzureStorageHelper object with the given storage ID, container name, and connection string

        Args:
            storage_id (str): The ID of the Azure Blob Storage account
            container_name (str): The name of the container to interact with
            connection_string (str): The connection string for the Azure Blob Storage account
        '''
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
        '''
        Uploads a file to Azure Blob Storage with the given destination name

        Args:
            source (str): The path to the local file to upload
            dest (str): The name of the blob to create in Azure Blob Storage
        '''
        with open(source, 'rb') as data:
            self.container_client_obj.upload_blob(name=dest, data=data, overwrite=True)

    def blob_exists(self, blob_path):
        '''
        Checks if a blob exists in Azure Blob Storage with the given path

        Args:
            blob_path (str): The path to the blob to check

        Returns:
            bool: True if the blob exists, False otherwise
        '''
        return self.container_client_obj.get_blob_client(blob_path).exists()

    def ls_files(self, path, recursive=False, specific_name = False):
        '''
        Lists files under a path in Azure Blob Storage, optionally recursively

        Args:
            path (str): The path to list files under
            recursive (bool): Whether to list files recursively or not (default: False)
            specific_name (bool): Whether to list files with a specific name or not (default: False)

        Returns:
            List[str]: A list of file names under the given path
        '''
        if specific_name == False and not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.container_client_obj.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = blob.name.removeprefix(path)
            relative_path = relative_path.removeprefix('/')
            if relative_path and (recursive or not '/' in relative_path):
                files.append(relative_path)
        return files

    def download_blob(self, blob_path, dst_file_path):
        '''
        Downloads a blob from Azure Blob Storage to the given local file path

        Args:
            blob_path (str): The path to the blob to download
            dst_file_path (str): The path to the local file to create

        Returns:
            str: The path to the downloaded file
        '''
        print (f'{Fore.YELLOW}Start download blob{Fore.RESET} {blob_path} to local path {dst_file_path}')
        
        blob_data = self.container_client_obj.get_blob_client(blob_path).download_blob().readall()
        with open(dst_file_path, "wb") as file:
            file.write(blob_data)
        
        print (f'{Fore.YELLOW}Finished download{Fore.RESET}')
        
        return dst_file_path

  