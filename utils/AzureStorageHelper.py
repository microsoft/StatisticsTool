import os
from azure.storage.blob import BlobServiceClient
from colorama import Fore
from azure.identity import DefaultAzureCredential, AzureCliCredential
import concurrent


class AzureStorageHelper():
    '''
    A helper class for interacting with Azure Blob Storage
    '''
    def set_storage(self, storage_id, container_name, connection_string):
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
        self.container_name = container_name

        print(f"Try create client for container: {container_name}")
        if not connection_string:
            print("******************** ERROR ************")
            print("No connection string, work only with local files\n\n")
        else:
            # Create the BlobServiceClient object
            #self.blob_service_client_obj = AzureStorageHelper._get_blob_service_client_using_connection_string(connection_string)
            self.blob_service_client_obj = AzureStorageHelper._get_blob_service_client_using_credential(self.account_url, AzureStorageHelper._get_token_credential())
            self.container_client_obj = self.blob_service_client_obj.get_container_client(container_name)
        
        return

    def get_container_name(self):
        return self.container_name      

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
    
    @staticmethod
    def handle_file_wrapper(vars):
        path, name, dst_folder_path, self = vars
        blob = path+'/'+name
        dst_folder_path = path+'/'+name
        return self.download_blob(blob, dst_folder_path)
    
    def download_folder(self, blob_base_path, dst_folder_path):
        files_in_folder = self.storage_handler.ls_files(blob_base_path)
       
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(AzureStorageHelper.handle_file_wrapper, [(blob_base_path, file, dst_folder_path, self) for file in files_in_folder])
            executor.shutdown(wait=True) 
        
        return dst_folder_path
            
    def download_blob(self, blob_path, dst_file_path):
        '''
        Downloads a blob from Azure Blob Storage to the given local file path

        Args:
            blob_path (str): The path to the blob to download
            dst_file_path (str): The path to the local file to create

        Returns:
            str: The path to the downloaded file
        '''
        blob_path = blob_path.replace("\\", "/")
        print (f'{Fore.YELLOW}Start download blob{Fore.RESET} {blob_path} to local path {dst_file_path}')
        
        blob_data = self.container_client_obj.get_blob_client(blob_path).download_blob().readall()
        with open(dst_file_path, "wb") as file:
            file.write(blob_data)
        
        print (f'{Fore.YELLOW}Finished download{Fore.RESET}. locl path: {dst_file_path}')
        
        return dst_file_path

    def _get_token_credential():
        ''' Retrieve the token credential '''
        token_credential = None

        try:        
            token_credential = DefaultAzureCredential()
        except Exception as e:
            print(f"AzureWrapper::__init__: DefaultAzureCredential failed with: {e}. Trying AzureCliCredential.")
            token_credential = None

        if token_credential is None:        
            try:
                token_credential = AzureCliCredential()
            except Exception as e:
                print(f"AzureWrapper::__init__: AzureCliCredential failed with: {e}. Sorry, no Credential were found. Try on the terminal: az login --use-device-code")
                token_credential = None
        
        return token_credential
      
    def _get_blob_service_client_using_credential(account_url, token_credential):
        '''
        Initializes the AzureStorageHelper object with the given storage ID, container name, and connection string

        Args:
            connection_string (str): The connection string for the Azure Blob Storage account
        '''
        blob_service_client_obj = BlobServiceClient(account_url=account_url, credential=token_credential)
        return blob_service_client_obj
    
    
    def _get_blob_service_client_using_connection_string(connection_string):
        '''
        Initializes the AzureStorageHelper object with the given storage ID, container name, and connection string

        Args:
            connection_string (str): The connection string for the Azure Blob Storage account
        '''
        blob_service_client_obj = BlobServiceClient.from_connection_string(connection_string)
        return blob_service_client_obj