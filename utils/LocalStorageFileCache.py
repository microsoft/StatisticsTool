
import tempfile
import os,sys
from pathlib import Path

sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo

from StatisticsTool.utils.LocalStrageHelper import list_local_dir


STATISTICS_TOOL_TEMP_FOLDER_NAME = "statistic-tool-tmp"

TEMP_DIR_MAX_SIZE = 2 * 1024 * 1024 * 1024 # 2 GB Default size
local_storage_cache = None
class LocalStorageFileCache:
    def __init__(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), STATISTICS_TOOL_TEMP_FOLDER_NAME)
        if os.path.exists(self.temp_dir) == False:
            os.makedirs(self.temp_dir)
        #self.temp_dir.cleanup()
    

    def get_normlized_file_name(self, file_name):
        name = file_name.replace('/','_').replace('\\','_')
        full_path = os.path.join(self.temp_dir, name) 
        return full_path
        

    def create_or_get_cached_file_full_path(self, file_name, touch_file = True):
        if not self.is_file_exists_in_cache(file_name):
            self.free_overused_storage()
        
        full_path = self.get_normlized_file_name(file_name)

        if touch_file:
            Path(full_path).touch()
        
        return full_path
    

    def is_file_exists_in_cache(self, file_name):
        full_path = self.get_normlized_file_name(file_name)
        
        if os.path.exists(full_path):
            return True

        return False

    def free_overused_storage(self):
        dir_size = self.get_temp_dir_size()
        if dir_size > TEMP_DIR_MAX_SIZE:
            temp_files = list_local_dir(self.temp_dir)
        
            sorted_files = sorted( temp_files,
                                    key =  lambda x: os.stat(x).st_mtime, reverse=True)
            for file in sorted_files:
                size = os.stat(file).st_size
                os.remove(file)
                dir_size -= size
                if dir_size < TEMP_DIR_MAX_SIZE:
                    break

    def get_temp_dir_size(self):
        temp_files = list_local_dir(self.temp_dir)     
        return sum(os.path.getsize(f) for f in temp_files)
    
    def delete_all_file_with_prefix(self, prefix):
        cache_prefix = self.get_normlized_file_name(prefix)
        temp_files = list_local_dir(self.temp_dir)
        for file in temp_files:
            if file.startswith(cache_prefix):
                os.remove(file)

def GetFileCache():
    global local_storage_cache

    if local_storage_cache is not None:
        return local_storage_cache

    local_storage_cache = LocalStorageFileCache()

    return local_storage_cache
