import json
import os
import sys
import numpy as np
from turtle import left
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes_and_utils.utils import empty_when_negative_x
import pandas as pd

"""
Reading Function instructions:
------------------------------

Input:
a. Accept as input a path to the data file (any type that the user preffered)

A reading function should:
1. Read the input file (The type of the file is defined by the user according to user prefference)
2. Convert the input data to panda's data frame format. The data frame should have at least the following columns:
    a. frame_id
    b. Bounding box columns, using the following names:
        i.   'x' is the minimal x coordinate
        ii.  'y' is the minimal y coordinate
        iii. 'width' is the width of the bounding box (column name will be 'width')
        iv.  'height' is the height of the bounding box (column name will be 'height')

4. Define a function that identify empty frames in GT data (frames with no labels):
    a. returns True if the row loaded from the data is an empty frame, false otherwise
    b. could be None (optional function)

Returns:
pandas dataframe, empty frame function (or None)
"""



def statistic_tool_reader_presence_algo_logs(path):
    with open(path,'r') as file:
        lines = file.readlines()
    
    line = json.loads(lines[1])
    
    df = pd.DataFrame(columns=['frame_id','x','y','width','height']) 
    for line in lines[1:]:
        line = json.loads(line)
        if line['keys']['type'] == 'system_state':
            continue
        if not line['message']['objects']:
           continue
        frame_id = line['keys']['frame_id']
        for obj in line['message']['objects']:
            if obj["Source"] != "BODY_DETECTION":
                continue
            bb = obj['BoundingBox']
            data={'frame_id':frame_id,'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height']}
            df=df.append(data,ignore_index=True)

    df = df.astype({'frame_id': np.int})
    return df, None


def statistic_tool_reader_zvi(path):
    # the user should define a function that reads his input data as pandas dataframe for example from csv to pandas:
    df = pd.read_csv(path)
    # changing the name of the current frame number column name to the statistics tool accepted name - 'frame_id'
    old_frame_column_name = "frame_number"
    new_frame_column_name = 'frame_id'
    df.rename(columns={old_frame_column_name: new_frame_column_name}, inplace=True)
    return df

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

if __name__ =="__main__":
    a,b=statistic_tool_reader_presence_algo_logs("C:/Users/v-nrosenberg/Documents/Sources/DataScienceSIL/Subsystem/Sensors/presence_sensing/camera/prod/golden_simulation/logger/logs/24_07_2022_10_52_36/presence_log.json")
    b=statistic_tool_reader_zvi("C:/Users/v-nrosenberg/Documents/Sources/DataScienceSIL/Tools/StatisticsTool/running example/Detections_DNN_FACE_HD_0001.csv")
    print(a)
    print(b)
