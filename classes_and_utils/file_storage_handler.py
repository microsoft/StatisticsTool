import os,sys


sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo


from StatisticsTool.app_config.config import AppConfig
from StatisticsTool.app_config.constants import constants
from StatisticsTool.utils.AzureStorageHelper import blob_exists, list_blobs_in_results_path, read_video_file_from_blob, get_blob_from_cache_or_download
from StatisticsTool.utils.LocalStrageHelper import list_local_dir


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

def get_local_or_blob_file(path):
    if os.path.exists(path):
        return path
    
    return get_blob_from_cache_or_download(path)
