from cmath import nan
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
    b. detection:
        one of the following:
        - Bounding box columns, using the following names:
                        i.   'x' is the minimal x coordinate
                        ii.  'y' is the minimal y coordinate
                        iii. 'width' is the width of the bounding box (column name will be 'width')
                        iv.  'height' is the height of the bounding box (column name will be 'height')
        - classification:
                    class name
    
        

4. Define a function that identify empty frames in GT data (frames with no labels):
    a. returns True if the row loaded from the data is an empty frame, false otherwise
    b. could be None (optional function)

Returns:
pandas dataframe, empty frame function (or None)
"""

def statistic_tool_reader_presence_calssification(path):
    with open(path,'r') as file:
        lines = file.readlines()
        
        line = json.loads(lines[1])
        records = []
        
        for line in lines[1:]:
            line = json.loads(line)
            if 'type' not in line['keys'] or line['keys']['type'] != 'presence':
                continue
            
            frame_id = line['keys']['frame_id']
            if int(line['message']['HumanPresence'])>0:
                
                data={'frame_id':frame_id, 'prediction': True}
            else:
                data={'frame_id':frame_id, 'prediction': False}
            records.append(data)

    df = pd.DataFrame.from_records(records)
    return df   

def statistic_tool_reader_presence_algo_logs(path):
    with open(path,'r') as file:
        lines = file.readlines()
    
    line = json.loads(lines[1])
    records = []
    
    for line in lines[1:]:
        line = json.loads(line)
        if 'type' not in line['keys'] or line['keys']['type'] != 'objects' or 'objects' not in line['message']:
            continue

        detections = []
        frame_id = line['keys']['frame_id']
        for obj in line['message']['objects']:
            if obj["Source"] != "BODY_DETECTION":
                continue
            bb = obj['BoundingBox']
            detections.append({'object_id':obj['Id'], 'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height']})
            
        records.append({'frame_id': frame_id, 'prediction':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df



if __name__ =="__main__":
    a,b=statistic_tool_reader_presence_algo_logs("C:/Users/v-nrosenberg/Documents/Sources/DataScienceSIL/Subsystem/Sensors/presence_sensing/camera/prod/golden_simulation/logger/logs/24_07_2022_10_52_36/presence_log.json")
    
    print(a)
