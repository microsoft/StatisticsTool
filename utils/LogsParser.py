
import os, sys
import pathlib
sys.path.append(os.path.join(__file__, '..',).split('StatisticsTool')[0])  # this is the root of the repo
import json
from app_config.constants import Constants
import enum
import numpy as np

class LogTypes(enum.IntEnum):
    ALGO_LOG = 0
    GT_LOG = 1
    IO_LOG = 2

def check_log_type(header): 
    log_type = header['header']['type']
    if (log_type == 'ALGO') | (log_type[0] == 'ALGO'):
        return LogTypes.ALGO_LOG
    if (log_type == 'gt_log') | (log_type[0] == 'gt_log'):
        return LogTypes.GT_LOG
    if (log_type == 'IO') | (log_type[0] == 'IO'):
        return LogTypes.IO_LOG

def is_gt_log(header):
    return check_log_type(header) == LogTypes.GT_LOG

def is_golden_log(header):
    return check_log_type(header) == LogTypes.ALGO_LOG

def get_emulation_matrix(header):
    if 'emulated_resolution' in header['header'].keys():
        if header['header']['emulated_resolution']:
            emulation_matrix=string2array(header['header']['emulation_matrix'])
    else:
        emulation_matrix = np.identity(3)
    return emulation_matrix

def transform_bb_to_original_frame_size(bb_object, emulation_matrix):
    '''
    Transforms the bounding box size according to the emulation matrix
    :param bb_object: dictionary with the bounding box information, fields: 'Left', 'Top', 'Width', 'Height'
    :param emulation_matrix: 3x3 matrix
    :return: transformed bb_object
    '''
    # if emulation matrix is a unit matrix, then no transformation is needed
    if np.array_equal(emulation_matrix, np.identity(3)):
        return bb_object
    else:
        cord = np.array([bb_object['Left'], bb_object['Top'], 1])
        cord = emulation_matrix.dot(cord)
        width_hight = np.array([bb_object['Width'], bb_object['Height'], 0])
        width_hight = emulation_matrix.dot(width_hight)
        return {'Left':cord[0],'Top':cord[1],'Width':width_hight[0],'Height':width_hight[1]}


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
    
def get_video_name_from_pred_file(pred_file, pred_name, pred_dir):
    try:
        with open(pred_file, "r") as file:
            header = file.readline()
            header = json.loads(header)
            video_name = header[Constants.log_header_token][Constants.log_header_video_name_token]
    except:
        video_name = os.path.relpath(pred_name, pred_dir)
    
    # Convert path to Unix style
    video_name = video_name.replace('\\', '/')
    
    return video_name
