import os,sys
import pathlib
import importlib.util

from app_config.constants import StorageHelper

sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo

from app_config.config import AppConfig
from utils.LocalStorageFileCache import LocalStorageFileCache
from utils.AzureStorageHelper import AzureStorageHelper
from utils.LocalStorageHelper import list_local_dir



class StoreType():
    Data = 1
    Annotation = 2
    Predictions = 3


local_storage_cache = None
storage_handler = None
def GetStorageHandler():
    """
    Returns an instance of AzureStorageHelper class that is used to interact with Azure Blob Storage.
    """
    global storage_handler
    if storage_handler is not None:
        return storage_handler
    
    app_config = AppConfig.get_app_config()
    if (app_config.custom_storage_helper):
        spec = importlib.util.spec_from_file_location(StorageHelper.CUSTOM_CLASS_NAME, app_config.custom_storage_helper)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module) 
        Class = getattr(module, StorageHelper.CUSTOM_CLASS_NAME)
        storage_handler = Class()
    else:        
        storage_handler = AzureStorageHelper()
    
    storage_handler.set_storage(app_config.storage_id, app_config.data_container_name, app_config.storage_connection_string)
    return storage_handler

def GetFilesCache():
    """
    Returns an instance of LocalStorageFileCache class that is used to cache files downloaded from Azure Blob Storage.
    """
    global local_storage_cache

    if local_storage_cache is not None:
        return local_storage_cache

    local_storage_cache = LocalStorageFileCache(GetStorageHandler())

    return local_storage_cache
#create on initialization no race conditions dangare
GetFilesCache()

def list_files_in_path(path, store_type):
    """
    Lists all files in the given path. If the path exists locally, it lists all files in the directory. If the path does not exist locally, it lists all files in the corresponding directory in Azure Blob Storage.

    Args:
        path (str): The path to list files from.
        store_type (StoreType): The type of store to list files from.

    Returns:
        A list of file paths.
    """
    if os.path.exists(path):
        dirs = list_local_dir(path, True)
    else:
        full_path = get_path_on_store(path, store_type)
        dirs = GetStorageHandler().ls_files(full_path, True)
        dirs = [path+'/'+dir for dir in dirs]
    return dirs

def list_files_parent_dirs(files):
    """
    Groups files by their parent directory.

    Args:
        files (list): A list of file paths.

    Returns:
        A dictionary where the keys are parent directories and the values are lists of files in that directory.
    """
    parent_dirs = {}
    for file in files:
        parent_dir = os.path.dirname(file)
        if parent_dir not in parent_dirs:
            parent_dirs[parent_dir]=[]
        parent_dirs[parent_dir].append(file)
    
    return parent_dirs

def get_path_on_store(path, store_type:StoreType):
    """
    Returns the full path of a file in Azure Blob Storage.

    Args:
        path (str): The path of the file.
        store_type (StoreType): The type of store the file is in.

    Returns:
        The full path of the file in Azure Blob Storage.
    """
    app_config = AppConfig.get_app_config()
    if store_type == StoreType.Annotation:
        return os.path.join(app_config.annotation_store_blobs_prefix, path)
    if store_type == StoreType.Data:
        return os.path.join(app_config.data_store_blobs_prefix, path)
    if store_type == StoreType.Predictions:
        return os.path.join(app_config.predictions_blobs_prefix, path)
    else:
        return path

def get_file_on_local_storage(path, store_type:StoreType = None, get_folder = False):  
    """
    Returns the local path of a file. If the file exists locally, it returns the local path. If the file does not exist locally, it downloads the file from Azure Blob Storage and returns the local path.

    Args:
        path (str): The path of the file.
        store_type (StoreType): The type of store the file is in.
        get_folder (bool): If True, returns the local path of the folder containing the file.

    Returns:
        The local path of the file.
    """
    #file is originally from local storage
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path

    #download from data store
    full_path = get_path_on_store(path, store_type)
    
    if get_folder:
        local_file_path = GetFilesCache().get_folder_and_download_if_needed(full_path)
    else:
        local_file_path = GetFilesCache().get_file_and_download_if_needed(full_path)
    return local_file_path



def find_in_store_by_video_name(base_path, full_video_name, log_name, path_exists_func, ext = '.json'):
    """
    Finds a file in Azure Blob Storage by video name.

    Args:
        base_path (str): The base path of the file.
        full_video_name (str): The full name of the video.
        log_name (str): The name of the log file.
        path_exists_func (function): A function that checks if a file exists.
        ext (str): The extension of the file.

    Returns:
        The local path of the file.
    """
    if not ext: #if ext is empty string so full_video_name is a folder and the folder will be video name
        return full_video_name
    
    video_file_name = pathlib.Path(full_video_name).stem
    
    #set gt_file path to be as full path in data store. the log is {video_full_name(path)}.json
    folder = os.path.split(full_video_name)[0]
    folder = os.path.normpath(folder)
    gt_local_path = os.path.join(base_path, folder, video_file_name+ext)
    if path_exists_func(gt_local_path):
        return gt_local_path
    
    #set gt_file path to be as full path in data store. full_video_name includes log name and the video name is the base folder
    video_path = os.path.dirname(full_video_name)
    folder, video_name = os.path.split(video_path)
    folder = os.path.normpath(folder)
    gt_local_path = os.path.join(base_path, folder, video_name+ext)
    if path_exists_func(gt_local_path):
        return gt_local_path
    
    #if not exists set gt_file to be as algo_logs file format
    gt_local_path = os.path.join(base_path, video_file_name, log_name)
    if path_exists_func(gt_local_path):
        return gt_local_path
    
    return None

def find_in_blob_by_video_name(file_name, log_name, store_type, ext = '.json'):
    """
    Finds a file in Azure Blob Storage by video name.

    Args:
        file_name (str): The name of the file.
        log_name (str): The name of the log file.
        store_type (StoreType): The type of store the file is in.
        ext (str): The extension of the file.

    Returns:
        The local path of the file.
    """
    full_file_name = get_path_on_store(file_name, store_type)
    return find_in_store_by_video_name('', full_file_name, log_name, GetStorageHandler().blob_exists, ext)
