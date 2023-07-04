import numpy as np
import os, sys
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(current_file_directory, '..'))
from utils.utils_partition import bb_size_partition, score_partition, pred_bb_size_partition, inrange_partition

def face_partition(dataframe, from_file=False, img_width=1280, img_height=720, use_pred=False):

    if use_pred:
        bb_size = pred_bb_size_partition(dataframe, from_file=from_file, img_width=1920, bb_size_percent=(0.05, 0.1, 0.15, 0.2, 0.25, 0.30))
    else:
        bb_size = bb_size_partition(dataframe, from_file=from_file, img_w_h=(1920,1080), bb_size_percent=(0.05,0.15,0.25))

    score = score_partition(dataframe, from_file=from_file, score_ranges=(0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.45, 0.5, 0.6))

    inrange = inrange_partition(dataframe, from_file=from_file)
    
    desired_masks = {'Bounding box size': bb_size, 'Score': score, 'Inrange': inrange}

    return desired_masks
