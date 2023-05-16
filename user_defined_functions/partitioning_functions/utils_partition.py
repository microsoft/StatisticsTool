import numpy as np
import pandas as pd

def bb_size_partition(dataframe, from_file=False, img_w_h=(1920,1080), bb_size_percent=(0.05,0.15,0.25)):
    img_width, img_height = img_w_h
    img_size = img_width*img_height

    bb_size_percent = (-1,) + bb_size_percent + (1,)
    bb_size = tuple([img_size*x for x in bb_size_percent])

    type_ = float
    bb_size_gt = dataframe['width_gt'].values.astype(type_) * dataframe['height_gt'].values.astype(type_)

    bb_size_gt[np.isnan(bb_size_gt)] = 0
    gt_exists = dataframe['detection_gt'].notnull().values.astype('bool')

    poss_part_names = []
    masks_list = []

    for i in range(len(bb_size)-1):
        curr_mask = (bb_size_gt > bb_size[i]) & (bb_size_gt <= bb_size[i+1]) & gt_exists
        masks_list.append(curr_mask)
        poss_part_names.append( str(bb_size_percent[i]) + ' < and <= ' + str(bb_size_percent[i+1]))

    bb_size_dict = {'possible partitions': poss_part_names, 'masks': masks_list}

    check_partition(len(dataframe), masks_list, 'bb_size_partition')

    return bb_size_dict

def score_partition(dataframe, from_file=False, score_ranges=(0.25, 0.5, 0.75)):
    type_ = float if from_file else object
    score = dataframe['Score'].values.astype(type_)

    score_ranges = (dataframe['Score'].min()-1,) + score_ranges + (dataframe['Score'].max()+1,)

    poss_part_names = []
    masks_list = []

    for i in range(len(score_ranges)-1):
        curr_mask = (score > score_ranges[i]) & (score <= score_ranges[i+1])
        masks_list.append(curr_mask)
        poss_part_names.append(str(score_ranges[i]) + ' < and <= ' + str(score_ranges[i+1]))

    curr_mask = dataframe['Score'].isna()
    masks_list.append(curr_mask)
    poss_part_names.append('nan')

    score_dict = {'possible partitions': poss_part_names, 'masks': masks_list}

    check_partition(len(dataframe), masks_list, 'score_partition')

    return score_dict

def check_partition(dataframe_len, masks_list, partition_name):
    all_masks_len = 0
    for mask in masks_list:
        all_masks_len += np.sum(mask)
    if all_masks_len != dataframe_len:
        raise ValueError(['The sum of all partition groups should be equal to total number of samples (length of the dataframe)! Check partion function: ' + partition_name + '!'])
