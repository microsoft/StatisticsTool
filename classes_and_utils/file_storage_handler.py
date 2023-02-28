import os,sys
import pathlib


sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo

from app_config.constants import constants
from utils.AzureStorageHelper import get_full_blob_path, blob_exists, list_blobs_in_results_path, read_video_file_from_blob, get_blob_from_cache_or_download
from utils.LocalStrageHelper import list_local_dir

def list_files_in_results_path(path, recursive=True):
    if os.path.exists(path):
        dirs = list_local_dir(path, recursive)
    else:
        dirs = list_blobs_in_results_path(path, recursive)

    return dirs
    
def path_exists(path):
    if path.startswith(constants.folder_prefix_for_blob):
        return blob_exists(path)
    else:
        return os.path.exist(path)

def get_local_video_path(path):
    if os.path.exists(path):
        return path
    
    return read_video_file_from_blob(path)

def get_local_or_blob_full_path(path, storeType):
    if os.path.exists(path):
        return path
    return get_full_blob_path(path, storeType)

def calc_log_file_full_path(log_name, video_name, logs_base_path):
    video_base_name = pathlib.Path(video_name).stem
    full_path = None
    if os.path.exists(logs_base_path):
        if log_name: #not null, algo_logs format
            full_path = os.path.join(logs_base_path, video_base_name, log_name)
        else:
            full_path = os.path.join(logs_base_path, video_base_name+'.json')
    else:
        if log_name:
            full_path = os.path.join(logs_base_path, os.path.splitext(video_name)[0],log_name)
        else:
            full_path = os.path.join(logs_base_path, os.path.splitext(video_name)[0]+'.json')
    return full_path

def get_local_or_blob_file(path):
    if os.path.exists(path):
        return path
    
    return get_blob_from_cache_or_download(path)
