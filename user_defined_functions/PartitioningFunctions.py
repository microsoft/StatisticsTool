import numpy as np

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





def size_horizontal_vertical(prd_dataframe, label_dataframe, from_file=False):
    type_ = float if from_file else object
    prd_width = prd_dataframe['width'].values.astype(type_)
    prd_height = prd_dataframe['height'].values.astype(type_)
    label_width = label_dataframe['width'].values.astype(type_)
    label_height = label_dataframe['height'].values.astype(type_)
    prd_x = prd_dataframe['x'].values.astype(type_)
    label_x = label_dataframe['x'].values.astype(type_)
    prd_y = prd_dataframe['y'].values.astype(type_)
    label_y = label_dataframe['y'].values.astype(type_)

    prd_y_center = (2*prd_y + prd_height)/2
    label_y_center = (2*label_y + label_height)/2
    prd_x_center = (2*prd_x + prd_width)/2
    label_x_center = (2*label_x + label_width)/2


    # masking by the area of the bounding box
    prd_large_mask = prd_width * prd_height > 0.1
    prd_small_mask = np.logical_not(prd_large_mask)
    label_large_mask = label_width * label_height > 0.1
    label_small_mask = np.logical_not(label_large_mask)
    size = {'possible partitions': ['large', 'small'], 'prediction masks': [prd_large_mask, prd_small_mask], 'labels masks': [label_large_mask, label_small_mask]}

    # masking by x value
    prd_left_x = prd_x_center < 0.5
    label_left_x = label_x_center < 0.5
    prd_right_x = np.logical_not(prd_left_x)
    label_right_x = np.logical_not(label_left_x)

    x_position = {'possible partitions': ['right', 'left'], 'prediction masks': [prd_right_x, prd_left_x], 'labels masks': [label_right_x, label_left_x]}

    # masking by y value
    prd_upper_y = prd_y_center < 0.5  # upper because of how matplotlib shows the image - the y axis origin is at the top so the upper part has lower values
    label_upper_y = label_y_center < 0.5
    prd_lower_y = np.logical_not(prd_upper_y)
    label_lower_y = np.logical_not(label_upper_y)
    y_position = {'possible partitions': ['up', 'down'], 'prediction masks': [prd_upper_y, prd_lower_y], 'labels masks': [label_upper_y, label_lower_y]}

    desired_masks = {'size': size, 'x position': x_position, 'y position': y_position}

    # making sure there is no same 'possible partitions' for different partitions
    all_the_options = []
    for key in desired_masks:
        for option_list in desired_masks[key]['possible partitions']:
            all_the_options.append(option_list)
    assert len(all_the_options) == len(np.unique(all_the_options)), 'two partition options cant have the same name'

    return desired_masks