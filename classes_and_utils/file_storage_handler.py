import os,sys
import pathlib


sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo

from app_config.config import app_config
from utils.LocalStorageFileCache import LocalStorageFileCache
from utils.AzureStorageHelper import AzureStorageHelper
from utils.LocalStrageHelper import list_local_dir


class StoreType():
    Data = 1
    Annotation = 2
    Predictions = 3


local_storage_cache = None
storage_handler = None
def GetStorageHandler():
    global storage_handler
    if storage_handler is not None:
        return storage_handler
    
    storage_handler = AzureStorageHelper(app_config.azure_storage_id, app_config.data_container_name, app_config.storage_connection_string)
    return storage_handler

def GetFilesCache():
    global local_storage_cache

    if local_storage_cache is not None:
        return local_storage_cache

    local_storage_cache = LocalStorageFileCache(GetStorageHandler())

    return local_storage_cache
#create on initialization no race conditions dangare
GetFilesCache()

def list_files_in_path(path, store_type, recursive=True):
    if os.path.exists(path):
        dirs = list_local_dir(path, recursive)
    else:
        full_path = get_path_on_store(path, store_type)
        dirs = GetStorageHandler().ls_files(full_path, recursive)
        dirs = [os.path.join(path, dir) for dir in dirs]
    return dirs

def get_path_on_store(path, store_type:StoreType):
    if store_type == StoreType.Annotation:
        return os.path.join(app_config.annotation_store_blobs_prefix, path)
    if store_type == StoreType.Data:
        return os.path.join(app_config.data_store_blobs_prefix, path)
    if store_type == StoreType.Predictions:
        return os.path.join(app_config.predictions_blobs_prefix, path)
    else:
        return path

def get_file_on_local_storage(path, store_type:StoreType = None):  
    #file is originally from local storage
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path

    #download from data store
    full_path = get_path_on_store(path, store_type)
    
    local_file_path = GetFilesCache().get_file_and_download_if_needed(full_path)
    return local_file_path


def find_in_store_by_video_name(base_path, full_video_name, log_name, path_exists_func, ext = '.json'):
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
    full_file_name = get_path_on_store(file_name, store_type)
    return find_in_store_by_video_name('', full_file_name, log_name, GetStorageHandler().blob_exists, ext)
