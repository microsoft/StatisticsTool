import numpy as np
import pandas as pd

def bb_size_partition(dataframe, from_file=False, img_w_h=(1920,1080), bb_size_percent=(0.05,0.15,0.25)):
    '''
    This function partitions the data according to the bounding box size
    :param dataframe: pandas dataframe than contains info of the gt bb size and the detection occurance (detection_gt, width_gt, height_gt)
    :param ing_w_h: tuple of the image width and height that gt bb was calculated on
    :param bb_size_percent: tuple of the bounding box size percentiles borders, for example: <5%, 5-15%, 15-25%, >25%
    :return: dictionary with the possible partitions names and the corresponding masks
    '''
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


def pred_bb_size_partition(dataframe, from_file=False, img_width=1920, bb_size_percent=(0.05,0.15,0.25)):
    '''
    This function partitions the data according to the bounding box size
    :param dataframe: pandas dataframe than contains info of the gt bb size and the detection occurance (detection_gt, width_gt, height_gt)
    :param ing_w_h: tuple of the image width and height that gt bb was calculated on
    :param bb_size_percent: tuple of the bounding box size percentiles borders, for example: <5%, 5-15%, 15-25%, >25%
    :return: dictionary with the possible partitions names and the corresponding masks
    '''
    img_size = img_width

    bb_size_percent = (-1,) + bb_size_percent + (1,)
    bb_size = tuple([img_size*x for x in bb_size_percent])

    type_ = float
    bb_size_pred = dataframe['width'].values.astype(type_)

    bb_size_pred[np.isnan(bb_size_pred)] = 0

    poss_part_names = []
    masks_list = []

    for i in range(len(bb_size)-1):
        curr_mask = (bb_size_pred > bb_size[i]) & (bb_size_pred <= bb_size[i+1])
        masks_list.append(curr_mask)
        poss_part_names.append(str(bb_size_percent[i]) + ' < bb_w <= ' + str(bb_size_percent[i+1]))

    bb_size_dict = {'possible partitions': poss_part_names, 'masks': masks_list}

    check_partition(len(dataframe), masks_list, 'bb_size_partition')

    return bb_size_dict

def score_partition(dataframe, from_file=False, score_ranges=(0.25, 0.5, 0.75)):
    '''
    This function partitions the data according to the score
    :param dataframe: pandas dataframe than contains info of the score ('Score' column)
    :param score_ranges: tuple of the score ranges, for example: <0.25, 0.25-0.5, 0.5-0.75, >0.75
    :return: dictionary with the possible partitions names and the corresponding masks
    '''
    type_ = float if from_file else object
    score = dataframe['Score'].values.astype(type_)

    score_ranges = (dataframe['Score'].min()-1,) + score_ranges + (dataframe['Score'].max()+1,)

    poss_part_names = []
    masks_list = []

    for i in range(len(score_ranges)-1):
        curr_mask = (score > score_ranges[i]) & (score <= score_ranges[i+1])
        masks_list.append(curr_mask)
        poss_part_names.append(str(score_ranges[i]) + ' < bb_score <= ' + str(score_ranges[i+1]))

    curr_mask = dataframe['Score'].isna()
    masks_list.append(curr_mask)
    poss_part_names.append('nan')

    score_dict = {'possible partitions': poss_part_names, 'masks': masks_list}

    check_partition(len(dataframe), masks_list, 'score_partition')

    return score_dict

def inrange_partition(dataframe, from_file=False):
    '''
    This function partitions the data according to whether the detection is in range or not
    :param dataframe: pandas dataframe than contains info of the inRange ('InRange' column)
    :return: dictionary with the possible partitions names and the corresponding masks
    '''
    type_ = float if from_file else object
    inrange = dataframe['InRange'].values.astype(type_)

    poss_part_names = []
    masks_list = []

    curr_mask = (inrange == 1)
    masks_list.append(curr_mask)
    poss_part_names.append('inRange')

    curr_mask = (inrange == 0)
    masks_list.append(curr_mask)
    poss_part_names.append('not inRange')

    curr_mask = dataframe['InRange'].isna()
    masks_list.append(curr_mask)
    poss_part_names.append('nan')

    inrange_dict = {'possible partitions': poss_part_names, 'masks': masks_list}

    check_partition(len(dataframe), masks_list, 'inrange_partition')

    return inrange_dict

# TODO
# def bb_ratio_partition(dataframe, from_file=False, img_w_h=(1920,1080), bb_ratio_percent=(0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2)):
#     '''
#     '''
#     img_w, img_h = img_w_h
#     img_ratio = img_w / img_h

#     bb_ratio_percent = (-1,) + bb_ratio_percent + (1,)
#     bb_ratio = tuple([img_ratio*x for x in bb_ratio_percent])
    
#     type_ = float
#     bb_ratio_pred = dataframe['width'].values.astype(type_) / dataframe['height'].values.astype(type_) if dataframe['height'].values.astype(type_) > 0 else 0

#     bb_ratio_pred[np.isnan(bb_ratio_pred)] = 0

#     poss_part_names = []
#     masks_list = []

#     bb_ratio_percent = (-1,) + bb_ratio_percent + (1,)

#     for i in range(len(bb_ratio)-1):
#         curr_mask = (bb_size_gt > bb_size[i]) & (bb_size_gt <= bb_size[i+1]) & gt_exists
#         masks_list.append(curr_mask)
#         poss_part_names.append( str(bb_size_percent[i]) + ' < and <= ' + str(bb_size_percent[i+1]))

#     curr_mask = dataframe['Score'].isna()
#     masks_list.append(curr_mask)
#     poss_part_names.append('nan')

#     score_dict = {'possible partitions': poss_part_names, 'masks': masks_list}

#     check_partition(len(dataframe), masks_list, 'score_partition')



def check_partition(dataframe_len, masks_list, partition_name):
    '''
    This function checks that the sum of all partition groups is equal to the total number of samples (length of the dataframe).
    In case the partition is not correct, it raises an error.
    :param dataframe_len: length of the dataframe, corresponds to the total number of samples
    :param masks_list: list of all the masks of the partition
    :param partition_name: name of the partition to be used in case of error
    :return: None
    '''
    all_masks_len = 0
    for mask in masks_list:
        all_masks_len += np.sum(mask)
    if all_masks_len != dataframe_len:
        raise ValueError(['The sum of all partition groups should be equal to total number of samples (length of the dataframe)! Check partion function: ' + partition_name + '!'])
