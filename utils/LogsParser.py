
import os, sys
sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo
import json
from app_config.constants import constants
import enum
import numpy as np

class LogTypes(enum.IntEnum):
    ALGO_LOG = 0
    GT_LOG = 1
    IO_LOG = 2

def check_log_type(header):
    log_type=header['header']['type']
    if log_type == 'ALGO':
        return LogTypes.ALGO_LOG
    if log_type == 'gt_log':
        return LogTypes.GT_LOG
    if log_type == 'IO':
        return LogTypes.IO_LOG

def is_gt_log(header):
    return check_log_type(header) == LogTypes.GT_LOG

def is_golden_log(header):
    return check_log_type(header) == LogTypes.ALGO_LOG

def transform_bb_to_original_frame_size(bb, header):
    if 'emulated_resolution' in header['header'].keys():
        if header['header']['emulated_resolution']:
            emulation_matrix=string2array(header['header']['emulation_matrix'])
            width_scale=emulation_matrix[0,0]
            height_scale=emulation_matrix[1,1]
            bb['Left'] = bb['Left']*width_scale
            bb['Top'] = bb['Top']*height_scale
            bb['Width'] = bb['Width']*width_scale
            bb['Height'] = bb['Height']*height_scale
    return bb

def string2array(array_string):
    # remove starting and ending brackets and newline charactes
    array_string = array_string.replace('[','').replace(']','').replace('\n','')
    # make a list of floats 
    array_data = [float(x) for x in array_string.split()]
    # reshape it back as numpy array
    array = np.array(array_data).reshape((3,3))
    return array

def get_fps(header):
    if 'fps_original_video' in header['header'].keys():
        return header['header']['fps_original_video']
    else:
        return 30 #TODO: change to acceptable option, need to add fps to gtlog
    
def parse_video_name_from_pred_file(file_path):
    local_path = None
    with open(file_path, "r") as file:
        header = file.readline()
        header = json.loads(header)
        video_name = header[constants.log_header_token][constants.log_header_video_name_token]
        if constants.log_header_video_path_token in header[constants.log_header_token] and header[constants.log_header_token][constants.log_header_video_path_token].startswith(constants.blob_path_startwidth_token):
            local_path = header[constants.log_header_token][constants.log_header_video_path_token]
    return video_name, local_path
   