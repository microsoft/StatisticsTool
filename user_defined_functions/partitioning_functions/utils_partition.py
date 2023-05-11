import numpy as np
import pandas as pd

def bb_size_partition(dataframe, from_file=False, img_w_h=(1920,1080), bb_size_t_s_m_l=(0.05,0.15,0.25)):
    img_width, img_height = img_w_h
    img_size = img_width*img_height

    bb_size_tiny   = bb_size_t_s_m_l[0] * img_size
    bb_size_small  = bb_size_t_s_m_l[1] * img_size
    bb_size_medium = bb_size_t_s_m_l[2] * img_size

    type_ = float
    bb_size_gt = dataframe['width_gt'].values.astype(type_) * dataframe['height_gt'].values.astype(type_)

    bb_size_gt[np.isnan(bb_size_gt)] = 0
    gt_exists = dataframe['detection_gt'].notnull().values.astype('bool')

    bb_key_tiny   = (bb_size_gt <= bb_size_tiny ) & gt_exists
    bb_key_small  = (bb_size_gt > bb_size_tiny  ) & (bb_size_gt <= bb_size_small ) & gt_exists
    bb_key_medium = (bb_size_gt > bb_size_small ) & (bb_size_gt <= bb_size_medium) & gt_exists
    bb_key_large  = (bb_size_gt > bb_size_medium) & gt_exists

    bb_size = {'possible partitions': ['tiny', 'small', 'medium', 'large'], 
               'masks': [bb_key_tiny, bb_key_small, bb_key_medium, bb_key_large]}

    desired_masks = {'Bounding box size': bb_size}

    return desired_masks

def score_partition(dataframe, from_file=False, score_ranges=(0.25, 0.5, 0.75)):
    type_ = float if from_file else object
    score = dataframe['Score'].values.astype(type_)

    score_ranges = (0,) + score_ranges + (1,)

    poss_part_names = []
    masks_list = []

    for i in range(len(score_ranges)-1):
        curr_mask = (score > score_ranges[i]) & (score <= score_ranges[i+1])
        masks_list.append(curr_mask)
        poss_part_names.append('>' + str(score_ranges[i]) + ' and <=' + str(score_ranges[i+1]))

    score = {'possible partitions': poss_part_names, 'masks': masks_list}

    desired_masks = {'Score': score}

    return desired_masks
