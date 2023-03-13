
import os, sys
sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo


import json
from app_config.constants import constants

def parse_video_name_from_pred_file(file_path):
    local_path = None
    with open(file_path, "r") as file:
        header = file.readline()
        header = json.loads(header)
        video_name = header[constants.log_header_token][constants.log_header_video_name_token]
        if constants.log_header_video_path_token in header[constants.log_header_token] and header[constants.log_header_token][constants.log_header_video_path_token].startswith(constants.blob_path_startwidth_token):
            local_path = header[constants.log_header_token][constants.log_header_video_path_token]
    return video_name, local_path
   