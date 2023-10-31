from cmath import nan
import json
import numpy as np
from turtle import left
import pandas as pd
import os, sys

current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(current_file_directory, '..'))
from utils.LogsParser import *

def statistic_tool_reader_face_detection_classification(path, **kwargs):
    with open(path,'r') as file:
        lines = file.readlines()
        header = lines[0]
        lines = lines[1:]

    if len(lines) < 1:
        return None
    
    log_type = check_log_type(json.loads(header))
    if log_type == LogTypes.IO_LOG:
        log_field_type = 'FaceDetectionOutput'
    elif log_type == LogTypes.GT_LOG:
        log_field_type = 'Face BB'

    records = []
    prediction = {'frame_id':-1, 'detection':-1}
    for line in lines:
        line = json.loads(line)
        if ('type' in line['keys'] and line['keys']['type'] != log_field_type) or 'objects' not in line['message']:
            continue

        prediction['frame_id'] = line['keys']['frame_id']
        prediction['detection']= True if len(line['message']['objects'])>0 else False
        
        records.append(prediction.copy())
    
    df = pd.DataFrame.from_records(records)  
    
    return df
