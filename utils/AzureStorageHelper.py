import os, sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo

from StatisticsTool.utils.LocalStorageFileCache import  GetFileCache
from StatisticsTool.app_config.config import app_config

from azure.identity import DefaultAzureCredential


class StoreType():
    Data = 1
    Annotation = 2
    Predictions = 3


account_url = f"https://{app_config.azure_storage_id}.blob.core.windows.net"
default_credential = DefaultAzureCredential()
container_client_obj = None
blob_service_client_obj = None

def container_client():
    global blob_service_client_obj,  container_client_obj
    if blob_service_client_obj is None or container_client_obj is None:
        print(f"Try create client for container: {app_config.data_container_name}")
        if not app_config.storage_connection_string:
            print("No connection string")
            raise Exception("No connection string in configuration file, exit!!!")
        # Create the BlobServiceClient object
        blob_service_client_obj = BlobServiceClient.from_connection_string(app_config.storage_connection_string)
        container_client_obj = blob_service_client_obj.get_container_client(app_config.data_container_name)
    
    return container_client_obj

def upload_file(source, dest, verbose=False):
    '''
    Upload a single file to a path inside the container
    '''
    with open(source, 'rb') as data:
        container_client().upload_blob(name=dest, data=data, overwrite=True)

def get_full_blob_path(blob, storeType:StoreType):
    if storeType == StoreType.Annotation:
        return os.path.join(app_config.annotation_store_blobs_prefix, blob)
    if storeType == StoreType.Data:
        return os.path.join(app_config.data_store_blobs_prefix, blob)
    if storeType == StoreType.Predictions:
        return os.path.join(app_config.predictions_blobs_prefix, blob)


def get_video_path_from_name(video_name):
    video_path = os.path.join(app_config.data_store_blobs_prefix, video_name)
    return video_path

def read_video_file_from_blob(blob_path):
    video_path = get_video_path_from_name(blob_path)
 
    file_path = get_blob_from_cache_or_download(video_path)

    return file_path


def read_gt_file_from_blob(video_name):
    annotation_blob_path = os.path.join(app_config.annotation_store_blobs_prefix, video_name)
    annotation_blob_path = os.path.splitext(annotation_blob_path)[0]+".json"
    
    annotation_local_path = get_blob_from_cache_or_download(annotation_blob_path)
    return annotation_local_path

def get_blob_from_cache_or_download(blob):
        
    if blob_exists(blob) == False:
        return None

    if GetFileCache().is_file_exists_in_cache(blob):
       return GetFileCache().create_or_get_cached_file_full_path(blob)

    local_path = save_blob_to_cache(blob)
    return local_path

def save_blob_to_cache(blob_path):
    file_path = GetFileCache().create_or_get_cached_file_full_path(blob_path)
    
    print (f'Start download blob {blob_path} to local path {file_path}')
    
    blob_data = container_client().get_blob_client(blob_path).download_blob().readall()
    with open(file_path, "wb") as file:
        file.write(blob_data)
    
    print (f'Finished download blob {blob_path} to local path {file_path}')
    
    return file_path


def blob_exists(blob_path):
  return container_client().get_blob_client(blob_path).exists()

def ls_files(path, recursive=False):
    '''
    List files under a path, optionally recursively
    '''
    if not path == '' and not path.endswith('/'):
        path += '/'

    blob_iter = container_client().list_blobs(name_starts_with=path)
    files = []
    for blob in blob_iter:
        relative_path = os.path.relpath(blob.name, path)
        if recursive or not '/' in relative_path:
            files.append(relative_path)
    return files

   
def list_blobs_in_results_path(path, recursive=False):
    '''
    List directories under a path, optionally recursively
    '''
    if not path == '' and not path.endswith('/'):
        path += '/'
    cur_path =  f"{app_config.predictions_blobs_prefix}{path}"
    blob_iter = container_client().list_blobs(name_starts_with=cur_path)
    dirs = []
    for blob in blob_iter:
        dirs.append(blob.name)

    return dirs

