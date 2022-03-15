from classes_and_utils.utils import empty_when_negative_x
import pandas as pd

"""
Reading Function instructions:
------------------------------

Input:
a. Accept as input a path to a data file

A reading function should:
1. Read the raw prediction/labels files as a pandas dataframe
2. Change the name of the frame column name into "frame_id"
3. Make sure the bounding box format is in a x,y,w,h format when:
    a. x is the minimal x coordinate
    b. y is the minimal y coordinate
    c. w is the width of the bounding box (column name will be 'width')
    d. h is the height of the bounding box (column name will be 'height')
4. Define a function that identify empty frames in GT data (frames with no labels):
    a. returns True if the row loaded from the data is an empty frame, false otherwise
    b. could be None (optional function)

Returns:
pandas dataframe, empty frame function (or None)
"""




def statistic_tool_reader_zvi(path):
    # the user should define a function that reads his input data as pandas dataframe for example from csv to pandas:
    df = pd.read_csv(path)
    # changing the name of the current frame number column name to the statistics tool accepted name - 'frame_id'
    old_frame_column_name = "frame_number"
    new_frame_column_name = 'frame_id'
    df.rename(columns={old_frame_column_name: new_frame_column_name}, inplace=True)

def statistics_tool_reader_ben(path):
    # the user should define a function that reads his input data as pandas dataframe for example from csv to pandas:
    df = pd.read_csv(path)
    # changing the name of the current frame number column name to the statistics tool accepted name - 'frame_id'
    old_frame_column_name = "frame_number"
    new_frame_column_name = 'frame_id'
    df.rename(columns={old_frame_column_name: new_frame_column_name}, inplace=True)
    df.rename(columns={'xmin': 'x', 'ymin': 'y'}, inplace=True)
    df['width'] = df['xmax'] - df['x']
    df['height'] = df['ymax'] - df['y']
    # df.drop('xmax', inplace=False, axis=1)
    # df.drop('ymax', inplace=False, axis=1)



###########################################################################################################
# changing the format of the of the bounding box position variables to be x, y, width, height

# EXAMPLE:
# if the variables in the original data set are for example xmin, ymin, xmax, ymax the user needs to change that by:

#     in the standard form 'x' and 'y' are the names for the minimal x coordinate and minimal y coordinate
#     therefore they should be replaced accordingly
#     df.rename(columns={'xmin': 'x', 'ymin': 'y'}, inplace=True)

#     # the width and height column should be calculated from the current variables and added to the dataframe:
#     df['width'] = df[‘xmax’] - df[‘xmin’]
#     df['height'] = df[‘ymax’] - df[‘ymin’]

# in this case (current data) the names are already x, y, width, height therefore no change is needed
###########################################################################################################

    # defining a function that recognize an empty ground truth row - meaning a ground truth with no labels on it
    # could be None if not needed
    empty_GT_frame_func = empty_when_negative_x

    return df, empty_GT_frame_func


