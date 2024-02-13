import os,sys
import shutil
import pathlib
from threading import Lock
import concurrent
from pathlib import Path

from app_config.constants import Constants, StorageHelper
from app_config.config import AppConfig
from experiment_engine.UserDefinedFunctionsHelper import load_class_from_file
from utils.LocalStorageFileCache import LocalStorageFileCache
from utils.AzureStorageHelper import AzureStorageHelper
from utils.LocalStorageHelper import list_local_dir


class StoreType():
    Data = 'Data'
    Annotations = 'Annotation'
    Predictions = 'Prediction'


local_storage_cache = None
external_storage_wrapper = {}
storage_handler_lock = Lock()

def GetStorageHandler(store_type):
    """
    Returns an instance of AzureStorageHelper class that is used to interact with Azure Blob Storage.
    """
    container_name = container_name_from_store_type(store_type)
    
    if container_name in external_storage_wrapper:
        return external_storage_wrapper[container_name]
    with storage_handler_lock:
        if container_name in external_storage_wrapper:
            return external_storage_wrapper[container_name]
        app_config = AppConfig.get_app_config()
        if (app_config.custom_storage_helper):
            try:
                if os.path.exists(app_config.custom_storage_helper):
                    path = app_config.custom_storage_helper
                else:
                    path = os.path.join(app_config.external_lib_path,  Constants.SDK_CUSTOMIZATION_FOLDER, app_config.custom_storage_helper)
                if not Path(path).suffix:
                    path = path+'.py'
                
                external_storage_wrapper[container_name] = load_class_from_file(path)
            except Exception as ex:
                print('\nFatal Error: \nFailed to load external storage helper.')
                print (ex)
                raise ex
        else:        
            external_storage_wrapper[container_name] = AzureStorageHelper()
    
        external_storage_wrapper[container_name].set_storage(app_config.storage_id, container_name, app_config.storage_connection_string)
        return external_storage_wrapper[container_name]

def container_name_from_store_type(store_type):
    app_config = AppConfig.get_app_config()
    if store_type == StoreType.Annotations and app_config.annotation_container_name:
        return app_config.annotation_container_name
    if store_type == StoreType.Predictions and app_config.prediction_container_name:
        return app_config.prediction_container_name
    
    return app_config.data_container_name
           
def GetFilesCache():
    """
    Returns an instance of LocalStorageFileCache class that is used to cache files downloaded from Azure Blob Storage.
    """
    global local_storage_cache

    if local_storage_cache is not None:
        return local_storage_cache
    
    local_storage_cache = LocalStorageFileCache()

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
        dirs = GetStorageHandler(store_type).ls_files(full_path, True)
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
    if store_type == StoreType.Annotations:
        return os.path.join(app_config.annotation_store_blobs_prefix, path)
    if store_type == StoreType.Data:
        return os.path.join(app_config.data_store_blobs_prefix, path)
    if store_type == StoreType.Predictions:
        return os.path.join(app_config.predictions_blobs_prefix, path)
    else:
        return path

def export_list(images_list, report_path, ref_report_path, segmentations_string, statistics_string, is_unique, is_ref, dst_path):
    """Export images_list

    Args:
        images_list (list(str)): list of images
        report_path (str): the path of the main report
        ref_report_path (str): refference report path
        segmentations_string (str): Current segmentations concatenated to string
        statistics_string (str): List statistics category
        is_unique (bool): Is list of unique frames
        is_ref (bool): Is list of ref report
        dst_path (str): Dst path to save output file

    Returns:
        bool: return True not to contiue with default export operation, False will perform default export list operation.
    """
    return False


def get_file_wrapper(vars):
    path, store_type, dst_path = vars
    local_path = ''
    try:
        if dst_path:
             download_file_to_path(path, store_type, dst_path)
        else:
            local_path = get_file_on_local_storage(path, store_type)
    except Exception as ex:
        print(f'Failed to download blob: {path} from store: {store_type} with exception: {ex}')
    return local_path


def parallel_get_files_on_local_storage(paths:dict, dst_paths:list = None):
    """_summary_

    Args:
        paths (dict): dictionary where path on blob is the keys and the values are store_types.

    Returns:
        list: list of local paths
    """
    if dst_paths is None:
        dst_paths = ['']*len(paths)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_file_wrapper, [(path, type, dst) for path, type, dst in zip(paths.keys(), paths.values(), dst_paths)])
        executor.shutdown(wait=True) 
    ret = []
    for result in results:
        ret.append(result)
    return ret

def download_file_to_path(path, store_type, local_path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        shutil.copyfile(path, local_path)
        
    path_on_blob = get_path_on_store(path, store_type)
    GetStorageHandler(store_type).download_blob(path_on_blob, local_path)
    
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
        local_file_path = GetFilesCache().get_folder_and_download_if_needed(full_path, GetStorageHandler(store_type))
    else:
        local_file_path = GetFilesCache().get_file_and_download_if_needed(full_path, GetStorageHandler(store_type))
    return local_file_path


def find_in_store_by_video_name(base_path, full_video_name, log_name, path_exists_func):
    """
    Finds a file in store by video name.

    Args:
        base_path (str): The base path of the file.
        full_video_name (str): The full name of the video.
        log_name (str): The name of the log file.
        path_exists_func (function): A function that checks if a file exists.
        ext (str): The extension of the file.

    Returns:
        The local path of the file.
    """
    
    
    #set gt_file path to be as full path in data store. the log is {video_full_name(path)}.json
    folder = os.path.split(full_video_name)[0]
    video_file_name = os.path.split(full_video_name)[1]
    folder = os.path.normpath(folder)
    gt_local_path = os.path.join(base_path, folder, video_file_name)
    if path_exists_func(gt_local_path):
        return gt_local_path
    
    #set gt_file path to be as full path in data store. full_video_name includes log name and the video name is the base folder
    video_path = os.path.dirname(full_video_name)
    folder, video_name = os.path.split(video_path)
    folder = os.path.normpath(folder)
    gt_local_path = os.path.join(base_path, folder, video_name)
    if path_exists_func(gt_local_path):
        return gt_local_path
    
    video_file_name = pathlib.Path(full_video_name).stem
    
    #if not exists set gt_file to be as algo_logs file format
    gt_local_path = os.path.join(base_path, video_file_name, log_name)
    if path_exists_func(gt_local_path):
        return gt_local_path
    
    return None

def find_in_blob_by_video_name(file_name, log_name, store_type):
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
    return find_in_store_by_video_name('', full_file_name, log_name, GetStorageHandler(store_type).blob_exists)
