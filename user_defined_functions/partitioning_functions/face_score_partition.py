import numpy as np
import os, sys
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(current_file_directory, '..'))
from utils_partition import score_partition

def face_score_partition(dataframe, from_file=False, img_width=1280, img_height=720):

    desired_masks = score_partition(dataframe, from_file=from_file, score_ranges=(0.25, 0.5, 0.75))

    return desired_masks
