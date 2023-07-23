
import tempfile
import os,sys
from pathlib import Path
from timeit import default_timer as timer

from utils.LocalStrageHelper import list_local_dir

sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo


ONE_GIGA = 1024 * 1024 * 1024
STATISTICS_TOOL_TEMP_FOLDER_NAME = "statistic-tool-tmp"
FREE_SPACE_FACTOR = 0.1
TEMP_DIR_MAX_SIZE = 3 * ONE_GIGA # 2 GB Default size
MAX_ELAPSED_TIME_TO_VALIDATE_GT = 60 * 60 #one hour in seconds
VERSION_PREFIX = 'version-'

local_storage_cache = None
class LocalStorageFileCache:
    #####
    ## storage_handler - blob storage handler
    ## prefixes_to_validate - list of prefixes in the storage blob to validate for new versions
    ######
    def __init__(self, storage_handler, prefixes_to_validate=[]):
        self.storage_handler = storage_handler
        self.last_check_time = None
        self.prefixes_to_validate = prefixes_to_validate
        self.temp_dir = os.path.join(tempfile.gettempdir(), STATISTICS_TOOL_TEMP_FOLDER_NAME)
        if os.path.exists(self.temp_dir) == False:
            os.makedirs(self.temp_dir)     
    
    def get_path_on_cache(self, file_name):
        name = file_name.replace('/','_').replace('\\','_')
        full_path = os.path.join(self.temp_dir, name) 
        return full_path
        
    def create_or_get_cached_file_full_path(self, file_name, touch_file = True):
        if not self.is_blob_exists_in_cache(file_name):
            self.free_overused_storage()
        
        full_path = self.get_path_on_cache(file_name)

        if touch_file:
            Path(full_path).touch()
        
        return full_path
    
    def is_blob_exists_in_cache(self, file_name):
        full_path = self.get_path_on_cache(file_name)
        
        if os.path.exists(full_path):
            return True

        return False

    def free_overused_storage(self):
        dir_size = self.get_temp_dir_size()
        if dir_size > TEMP_DIR_MAX_SIZE:
            temp_files = list_local_dir(self.temp_dir)
        
            sorted_files = sorted( temp_files,
                                    key =  lambda x: os.stat(x).st_mtime, reverse=False)
            for file in sorted_files:
                size = os.stat(file).st_size
                os.remove(file)
                dir_size -= size
                if dir_size < TEMP_DIR_MAX_SIZE*(1-FREE_SPACE_FACTOR):
                    break

    def get_temp_dir_size(self):
        temp_files = list_local_dir(self.temp_dir)     
        return sum(os.path.getsize(f) for f in temp_files)
    
    def delete_all_file_with_prefix(self, prefix):
        cache_prefix = self.get_path_on_cache(prefix)
        temp_files = list_local_dir(self.temp_dir)
        for file in temp_files:
            if file.startswith(cache_prefix):
                os.remove(file)

    def get_file_and_download_if_needed(self, blob_path):
        self.invalidate_cache_if_needed()

        if self.is_blob_exists_in_cache(blob_path):
            return self.get_path_on_cache(blob_path)

        path_on_cache = self.save_blob_to_cache(blob_path)
        return path_on_cache

    def save_blob_to_cache(self, blob_path):
        self.free_overused_storage()
            
        path_on_cache = self.get_path_on_cache(blob_path)
        
        Path(path_on_cache).touch()
        path_on_cache = self.storage_handler.download_blob(blob_path, path_on_cache)
        return path_on_cache
 
    def invalidate_cache_if_needed(self):
        if self.last_check_time is not None and self.last_check_time - timer() < MAX_ELAPSED_TIME_TO_VALIDATE_GT:
            self.last_check_time = timer()
            return
        self.last_check_time = timer()

        for prefix in self.prefixes_to_validate:
            version_blob_prefix = os.path.join(prefix, VERSION_PREFIX)

            version_files = self.storage_handler.ls_files(version_blob_prefix, specific_name = True)
            if len(version_files) == 0:
                print ('No version file in storage skip invalidate')
                return
            
            version_file = os.path.basename(version_files[0])
            version_blob = os.path.join(prefix, version_file)

            if self.is_blob_exists_in_cache(version_blob):
                return
            self.delete_all_file_with_prefix(prefix)

            self.save_blob_to_cache(version_blob)

