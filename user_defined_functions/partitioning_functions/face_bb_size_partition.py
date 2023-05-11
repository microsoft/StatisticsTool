import numpy as np
import os, sys
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(current_file_directory, '..'))
from utils_partition import bb_size_partition

def face_bb_size_partition(dataframe, from_file=False):

    desired_masks = bb_size_partition(dataframe, from_file=from_file, img_w_h=(1920,1080), bb_size_t_s_m_l=(0.05,0.15,0.25))

    return desired_masks
