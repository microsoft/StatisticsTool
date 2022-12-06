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



def no_partitioning(dataframe, from_file=False):
    return {}

def activity_partition(dataframe, from_file=False):
    multiple = dataframe['Multiple People_gt'].values.astype(object)
    relevant = dataframe['relevant_gt'].values.astype(object)
    static = dataframe['static_gt'].values.astype(object)
    activity = dataframe['activity_gt'].values.astype(object)

    multiple_mask = multiple > 0
    relevant_mask = relevant > 0
    static_mask = static > 0
    activity_mask = activity > 0

    mult_dict = {'possible partitions': ['one person', 'multiple persons'], 'masks': [np.logical_not( multiple_mask), multiple_mask]}
    relevant_dict = {'possible partitions': ['non relevant', 'relevant'], 'masks': [np.logical_not(relevant_mask), relevant_mask]}
    static_dict = {'possible partitions': ['not static', 'ken static'], 'masks': [np.logical_not(static_mask), static_mask]}
    activity_dict = {'possible partitions': ['no activity', 'has activity'], 'masks': [np.logical_not(activity_mask), activity_mask]}
    desired_masks = {'Multiple': mult_dict, "Relevant":relevant_dict, "Static":static_dict, "Has Person":activity_dict}

    return desired_masks

def size_horizontal_vertical(dataframe, from_file=False):

    img_width = 1280
    img_height = 720

    type_ = float if from_file else object
    prd_width = dataframe['width'].values.astype(type_)
    prd_height = dataframe['height'].values.astype(type_)
    label_width = dataframe['width_gt'].values.astype(type_)
    label_height = dataframe['height_gt'].values.astype(type_)
    prd_x = dataframe['x'].values.astype(type_)
    label_x = dataframe['x_gt'].values.astype(type_)
    prd_y = dataframe['y'].values.astype(type_)
    label_y = dataframe['y_gt'].values.astype(type_)

    prd_y_center = (2*prd_y + prd_height)/2
    label_y_center = (2*label_y + label_height)/2
    prd_x_center = (2*prd_x + prd_width)/2
    label_x_center = (2*label_x + label_width)/2


    # masking by the area of the bounding box
    prd_large_mask = prd_width + prd_height > (img_width + img_height)/2
    prd_medium_mask = (prd_width + prd_height < (img_width + img_height)/1.3) & (prd_width + prd_height > (img_width + img_height)/3)
    prd_small_mask = np.logical_not(prd_large_mask | prd_medium_mask)

    label_large_mask = label_width + label_height > (img_width + img_height)/1.3
    label_medium_mask = (label_width + label_height < (img_width + img_height)/1.3) & (label_width + label_height > (img_width + img_height)/3)
    label_small_mask = np.logical_not(label_large_mask | label_medium_mask)

    large_mask = prd_large_mask | (label_large_mask & dataframe['x'].isnull())
    small_mask = prd_small_mask | (label_small_mask & dataframe['x'].isnull())
    medium_mask = prd_medium_mask | (label_medium_mask & dataframe['x'].isnull())


    size = {'possible partitions': ['large', 'small','medium'], 'masks': [large_mask, small_mask, medium_mask]}

    # masking by x value
    prd_left_x = prd_x_center < img_width/2
    label_left_x = label_x_center < img_width/2
    prd_right_x = np.logical_not(prd_left_x)
    label_right_x = np.logical_not(label_left_x)
    right_mask = prd_right_x | (label_right_x & dataframe['x'].isnull())
    left_mask = prd_left_x | (label_left_x & dataframe['x'].isnull())
    x_position = {'possible partitions': ['right', 'left'], 'masks': [right_mask, left_mask]}

    # masking by y value
    prd_upper_y = prd_y_center < img_height/2  # upper because of how matplotlib shows the image - the y axis origin is at the top so the upper part has lower values
    label_upper_y = label_y_center < img_height/2
    prd_lower_y = np.logical_not(prd_upper_y)
    label_lower_y = np.logical_not(label_upper_y)
    lower_mask = prd_lower_y | (label_lower_y & dataframe['x'].isnull())
    upper_mask = prd_upper_y | (label_upper_y & dataframe['x'].isnull())
    y_position = {'possible partitions': ['up', 'down'], 'masks': [upper_mask, lower_mask]}

    desired_masks = {'size': size, 'x position': x_position, 'y position': y_position}

    # making sure there is no same 'possible partitions' for different partitions
    all_the_options = []
    for key in desired_masks:
        for option_list in desired_masks[key]['possible partitions']:
            all_the_options.append(option_list)
    assert len(all_the_options) == len(np.unique(all_the_options)), 'two partition options cant have the same name'

    return desired_masks