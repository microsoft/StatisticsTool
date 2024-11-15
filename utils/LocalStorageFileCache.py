
import tempfile
import os,sys
from pathlib import Path
from timeit import default_timer as timer


from utils.LocalStorageHelper import list_local_dir


ONE_GIGA = 1024 * 1024 * 1024
STATISTICS_TOOL_TEMP_FOLDER_NAME = "statistic-tool-tmp"
FREE_SPACE_FACTOR = 0.1
TEMP_DIR_MAX_SIZE = 3 * ONE_GIGA # 2 GB Default size
MAX_ELAPSED_TIME_TO_VALIDATE_GT = 60 * 60 #one hour in seconds
VERSION_PREFIX = 'version-'

local_storage_cache = None
import os
import tempfile
from pathlib import Path
from timeit import default_timer as timer

class LocalStorageFileCache:
    """
    A class for caching files in local storage.

    Args:
        storage_handler: blob storage handler
        prefixes_to_validate: list of prefixes in the storage blob to validate for new versions

    Attributes:
        last_check_time: the last time the cache was checked
        prefixes_to_validate: list of prefixes in the storage blob to validate for new versions
        temp_dir: the temporary directory where the cached files are stored

    Methods:
        get_path_on_cache: returns the full path of a file in the cache
        create_or_get_cached_file_full_path: creates or gets the full path of a file in the cache
        is_blob_exists_in_cache: checks if a blob exists in the cache
        free_overused_storage: frees up space in the cache if it exceeds the maximum size
        get_temp_dir_size: returns the size of the temporary directory
        delete_all_file_with_prefix: deletes all files with a given prefix from the cache
        get_file_and_download_if_needed: gets a file from the cache or downloads it if needed
        save_blob_to_cache: saves a blob to the cache
        invalidate_cache_if_needed: invalidates the cache if needed
    """

    def __init__(self, prefixes_to_validate=[]):
        self.last_check_time = None
        self.prefixes_to_validate = prefixes_to_validate
        self.temp_dir = os.path.join(tempfile.gettempdir(), STATISTICS_TOOL_TEMP_FOLDER_NAME)
        if os.path.exists(self.temp_dir) == False:
            os.makedirs(self.temp_dir)     
    
    def get_path_on_cache(self, file_name,storage_handler, blob_name = None):
        """
        Returns the full path of a file in the cache.

        Args:
            file_name: the name of the file

        Returns:
            The full path of the file in the cache.
        """
        name = file_name.replace('/','_').replace('\\','_')
        storage_name = storage_handler.get_container_name()
        
        full_path = os.path.join(self.temp_dir, storage_name, name)
        
        if blob_name:
            full_path = os.path.join(full_path, blob_name) 
        
        return full_path
        
    def create_or_get_cached_file_full_path(self, file_name, storage_handler, touch_file=True):
        """
        Creates or gets the full path of a file in the cache.

        Args:
            file_name: the name of the file
            touch_file: whether to touch the file or not

        Returns:
            The full path of the file in the cache.
        """
        if not self.is_blob_exists_in_cache(file_name):
            self.free_overused_storage()
        
        full_path = self.get_path_on_cache(file_name, storage_handler)
        
        Path(os.path.split(full_path)[0]).mkdir(parents=True, exist_ok=True)
        if touch_file:
            Path(full_path).touch()
        
        return full_path
    
    def is_blob_exists_in_cache(self, file_name, storage_handler, blob_name=None):
        """
        Checks if a blob exists in the cache.

        Args:
            file_name: the name of the file

        Returns:
            True if the blob exists in the cache, False otherwise.
        """
        full_path = self.get_path_on_cache(file_name, storage_handler, blob_name)
        
        if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
            return True

        return False

    def free_overused_storage(self):
        """
        Frees up space in the cache if it exceeds the maximum size.
        """
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
        """
        Returns the size of the temporary directory.

        Returns:
            The size of the temporary directory.
        """
        temp_files = list_local_dir(self.temp_dir)     
        return sum(os.path.getsize(f) for f in temp_files)
    
    def delete_all_file_with_prefix(self, prefix, storage_handler):
        """
        Deletes all files with a given prefix from the cache.

        Args:
            prefix: the prefix of the files to delete
        """
        cache_prefix = self.get_path_on_cache(prefix, storage_handler)
        temp_files = list_local_dir(self.temp_dir)
        for file in temp_files:
            if file.startswith(cache_prefix):
                os.remove(file)
   
    def get_folder_and_download_if_needed(self, blob_base_path, storage_handler):
        
        path_on_cache =  self.get_path_on_cache(blob_base_path, storage_handler)
        
        if not os.path.exists(path_on_cache):
            os.makedirs(path_on_cache)

        ret_path = storage_handler.download_folder(blob_base_path, path_on_cache)
            
        return ret_path
    
    def get_file_and_download_if_needed(self, blob_base_path, storage_handler, blob_name=None):
            """
            Gets a file from the cache or downloads it if needed.

            Args:
                blob_base_path (str): The base path of the blob.
                blob_name (str, optional): The name of the blob. If None blob_base_path is a blob.

            Returns:
                str: The full path of the file in the cache.
            """
            self.invalidate_cache_if_needed(storage_handler)

            if self.is_blob_exists_in_cache(blob_base_path, storage_handler, blob_name):
                return self.get_path_on_cache(blob_base_path, storage_handler, blob_name)

            path_on_cache = self.save_blob_to_cache(blob_base_path, storage_handler, blob_name)
            
            return path_on_cache

    def save_blob_to_cache(self, blob_path, storage_handler, blob_name=None):
            """
            Saves a blob to the cache.

            Args:
                blob_path (str): The path of the blob, if blob_name is None blob_path is a blob.
                blob_name (str, optional): The name of the blob. Defaults to None.

            Returns:
                str: The full path of the file in the cache.
            """
            self.free_overused_storage()
                
            path_on_cache = self.get_path_on_cache(blob_path, storage_handler, blob_name)
            
            Path(os.path.split(path_on_cache)[0]).mkdir(parents=True, exist_ok=True)
            Path(path_on_cache).touch()
            if blob_name:
                blob_path = blob_path + '/' + blob_name
            path_on_cache = storage_handler.download_blob(blob_path, path_on_cache)
            return path_on_cache
 
    def invalidate_cache_if_needed(self, storage_handler):
        """
        Invalidates the cache if needed.
        """
        if self.last_check_time is not None and self.last_check_time - timer() < MAX_ELAPSED_TIME_TO_VALIDATE_GT:
            self.last_check_time = timer()
            return
        self.last_check_time = timer()

        for prefix in self.prefixes_to_validate:
            version_blob_prefix = os.path.join(prefix, VERSION_PREFIX)

            version_files = storage_handler.ls_files(version_blob_prefix, specific_name=True)
            if len(version_files) == 0:
                print ('No version file in storage skip invalidate')
                return
            
            version_file = os.path.basename(version_files[0])
            version_blob = os.path.join(prefix, version_file)

            if self.is_blob_exists_in_cache(version_blob, storage_handler):
                return
            self.delete_all_file_with_prefix(prefix, storage_handler)

            self.save_blob_to_cache(version_blob, storage_handler)

