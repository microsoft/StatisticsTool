import numpy as np

from Tools.StatisticsTool.user_defined_functions.PartitioningFunctions import size_horizontal_vertical

"""
Partitioning Function instructions:
------------------------------
Input:
a. prdediction dataframe (after the modifications of the Reading function)
b. label dataframe (after the modifications of the Reading function)
c. from_file, boolean that indicates weather the dataframe was loaded (to manage type of variable)

A Reading function:

1. The high-level dictionary returned should be of the form:
{'Partition Name': Partition Dictionary}

2. The lower level "Partition Dictionary" should be of the form:
{'possible partitions': ['option 1', 'option 2', ..., 'option n'],
 'prediction masks': [predictions boolean mask for option 1, predictions boolean mask for option 2, ..., predictions boolean mask for option n],
 'labels masks': [labels boolean mask for option 1, labels boolean mask for option 2, ..., labels boolean mask for option n]}
 
Notice: the predictions boolean masks should match the boolean data frame (same for labels)
 
Notice 2: its not allowed to use the same option name for different partitions:
    for example a 'Partitions Name' = 'Time of day' will have the 'possible partitions': 'night' and 'day'
    if we use another 'Partitions Name', for example 'vehicle',
    we cant use 'night' or 'day' as 'possible partitions' this will mess up the software
    to make sure it doesnt happen an assertion was added to the examples bellow.
 
Returns:
The high-level dictionary which contains at least one Partition Dictionary
"""

def size_horizontal_vertical_and_bb_area(dataframe, from_file=False, img_width=1920, img_height=1080):

    desired_masks = size_horizontal_vertical(dataframe, from_file=from_file, img_width=img_width, img_height=img_height)
    # return desired_masks
    type_ = float if from_file else object
    prd_width = dataframe['width'].values.astype(type_)
    prd_height = dataframe['height'].values.astype(type_)
    label_width = dataframe['width_gt'].values.astype(type_)
    label_height = dataframe['height_gt'].values.astype(type_)

    size_bb_threshold_small = 8000
    size_bb_threshold_mid = 20000
    # masking by the area of the bounding box (pixels)
    prd_bb_erea = prd_height*prd_width
    label_bb_erea = label_height*label_width

    prd_large_mask = prd_bb_erea > size_bb_threshold_mid
    prd_medium_mask = (size_bb_threshold_mid >= prd_bb_erea) & (prd_bb_erea > size_bb_threshold_small)
    prd_small_mask = np.logical_not(prd_large_mask | prd_medium_mask)

    label_large_mask = label_bb_erea > size_bb_threshold_mid
    label_medium_mask = (size_bb_threshold_mid >= label_bb_erea) & (label_bb_erea > size_bb_threshold_small)
    label_small_mask = np.logical_not(label_large_mask | label_medium_mask)

    large_mask = prd_large_mask | (label_large_mask & dataframe['x'].isnull())
    medium_mask = prd_medium_mask | (label_medium_mask & dataframe['x'].isnull())
    small_mask = prd_small_mask | (label_small_mask & dataframe['x'].isnull())

    size_bb = {'possible partitions': ['large_area', 'medium_area', 'small_area'], 'masks': [large_mask, medium_mask, small_mask]}

    desired_masks['size_bb'] = size_bb


    confidence_high = 0.95
    confidence_mid_high = 0.9
    confidence_mid_low = 0.8
    # masking by the confidence score of the prediction
    prd_confidence = dataframe['confidence'].values.astype(type_)

    prd_confidence_high = prd_confidence > confidence_high
    prd_confidence_mid_high = (prd_confidence <= confidence_high) & (prd_confidence > confidence_mid_high)
    prd_confidence_mid_low = (prd_confidence <= confidence_mid_high) & (prd_confidence > confidence_mid_low)
    prd_confidence_low = np.logical_not(prd_confidence_high | prd_confidence_mid_high | prd_confidence_mid_low) & (~dataframe['confidence'].isnull())
    prd_confidence_none = dataframe['confidence'].isnull()

    prediction_scores = {'possible partitions': [f'confidence_high[>{confidence_high}]', f'confidence_mid_high[>{confidence_mid_high}]', \
        f'confidence_mid_low[>{confidence_mid_low}]', f'confidence_low[<={confidence_mid_low}]', f'confidence_none[no-detection]'], \
        'masks': [prd_confidence_high, prd_confidence_mid_high, prd_confidence_mid_low, prd_confidence_low, prd_confidence_none]}

    desired_masks['prediction_confidence_score'] = prediction_scores


    confidence_gt_high = 0.90
    confidence_gt_mid_high = 0.8
    confidence_gt_mid_low = 0.7
    confidence_gt_low = 0.6
    # confidence_gt_mid_low = 0.6
    # confidence_gt_mid_low = 0.5
    # masking by the confidence score of the prediction
    label_confidence = dataframe['confidence_gt'].values.astype(type_)  # in this case label_confidence == fusion_confidence

    prd_confidence_gt_high = label_confidence > confidence_gt_high
    prd_confidence_gt_mid_high = (label_confidence <= confidence_gt_high) & (label_confidence > confidence_gt_mid_high)
    prd_confidence_gt_mid_low = (label_confidence <= confidence_gt_mid_high) & (label_confidence > confidence_gt_mid_low)
    prd_confidence_gt_low = (label_confidence <= confidence_gt_mid_low) & (label_confidence > confidence_gt_low)
    prd_confidence_gt_very_low = np.logical_not(prd_confidence_gt_high | prd_confidence_gt_mid_high | prd_confidence_gt_mid_low | prd_confidence_gt_low) & (~dataframe['confidence_gt'].isnull())
    prd_confidence_gt_none = dataframe['confidence_gt'].isnull()

    prediction_scores = {'possible partitions': [f'fusion_confidence_high[>{confidence_gt_high}]', f'fusion_confidence_mid_high[>{confidence_gt_mid_high}]', \
        f'fusion_confidence_mid_low[>{confidence_gt_mid_low}]', f'fusion_confidence_low[>{confidence_gt_low}]', f'fusion_confidence_very_low[<={confidence_gt_low}]', f'fusion_confidence_none[below_fusion_threshold]'], \
        'masks': [prd_confidence_gt_high, prd_confidence_gt_mid_high, prd_confidence_gt_mid_low, prd_confidence_gt_low, prd_confidence_gt_very_low, prd_confidence_gt_none]}

    desired_masks['fusion_confidence_score'] = prediction_scores
    ########################


    all_the_options = []
    for key in desired_masks:
        for option_list in desired_masks[key]['possible partitions']:
            all_the_options.append(option_list)
    assert len(all_the_options) == len(np.unique(all_the_options)), 'two partition options cant have the same name'

    return desired_masks