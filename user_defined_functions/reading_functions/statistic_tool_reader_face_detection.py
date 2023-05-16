from cmath import nan
import json
import numpy as np
from turtle import left
import pandas as pd
import os, sys

current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(current_file_directory, '..'))
from utils_reading import transform_bb_size

def statistic_tool_reader_face_detection(path):
    with open(path,'r') as file:
        lines = file.readlines()

    if len(lines) < 1:
        return None
    
    if json.loads(lines[0])['header']['type']=='IO':
        log_field_type = 'FaceDetectionOutput'
        emulation_matrix_str = json.loads(lines[0])['header']['emulation_matrix']
        emulation_matrix_str = emulation_matrix_str .replace('[', '').replace(']', '').replace('\n', '').split()
        emulation_matrix = np.array(emulation_matrix_str, dtype=float).reshape(3, 3)
    elif json.loads(lines[0])['header']['type'][0]=='gt_log':
        log_field_type = 'Face BB'
        emulation_matrix = np.identity(3)

    line = json.loads(lines[1])
    records = []
    
    for line in lines[1:]:
        line = json.loads(line)
        if ('type' in line['keys'] and line['keys']['type'] != log_field_type) or 'objects' not in line['message']:
            continue

        detections = []
        frame_id = line['keys']['frame_id']
       
        for obj in line['message']['objects']:
            if obj["Source"] != "FACE_DETECTION":
                continue
            bb = transform_bb_size(obj['BoundingBox'], emulation_matrix)
            prediction = {'object_id':obj['Id'], 'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height']}
            if 'Score' in obj:
                prediction['Score'] = obj['Score']
            detections.append({'detection':True, 'prediction': prediction})

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df