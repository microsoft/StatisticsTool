
import os

def list_local_dir(path, recursive = True):
    files = []
    dirs = os.listdir(path)
    for file in dirs:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            if recursive:
                dir_files = list_local_dir(file_path, recursive)
                files = files+ dir_files
        else:
            files.append(file_path)

    return files