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
    # replace nan with zero
    # bb_size_gt = np.nan_to_num(bb_size_gt)
    bb_size_gt[np.isnan(bb_size_gt)] = 0
    gt_exists = dataframe['detection_gt'].notnull().values.astype('bool')

    bb_key_tiny   = (bb_size_gt <= bb_size_tiny ) & gt_exists
    bb_key_small  = (bb_size_gt > bb_size_tiny  ) & (bb_size_gt <= bb_size_small ) & gt_exists
    bb_key_medium = (bb_size_gt > bb_size_small ) & (bb_size_gt <= bb_size_medium) & gt_exists
    bb_key_large  = (bb_size_gt > bb_size_medium) & gt_exists

    # cond_tiny_less   = (bb_size_gt <= bb_size_tiny)
    # cond_tiny_more   = (bb_size_gt >  bb_size_tiny)
    # cond_small_less  = (bb_size_gt <= bb_size_small)
    # cond_small_more  = (bb_size_gt >  bb_size_small)
    # cond_medium_less = (bb_size_gt <= bb_size_medium)
    # cond_medium_more = (bb_size_gt >  bb_size_medium)
    # bb_key_tiny   = cond_tiny_less & gt_exists
    # bb_key_small  = cond_tiny_more & cond_small_less & gt_exists
    # bb_key_medium = cond_small_more & cond_medium_less & gt_exists
    # bb_key_large  = cond_medium_more & gt_exists

    bb_size = {'possible partitions': ['tiny', 'small', 'medium', 'large'], 
               'masks': [bb_key_tiny, bb_key_small, bb_key_medium, bb_key_large]}

    desired_masks = {'Bounding box size': bb_size}

    return desired_masks
