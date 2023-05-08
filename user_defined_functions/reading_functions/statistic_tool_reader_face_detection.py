from cmath import nan
import json
import numpy as np
from turtle import left
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from classes_and_utils.utils import empty_when_negative_x
import pandas as pd

def statistic_tool_reader_face_detection(path):
    #compare only gt_logs or facedetection logs
    # if not ('GT_logs' in path or 'FaceDetectionOutput' in path):
    #     return None

    with open(path,'r') as file:
        lines = file.readlines()

    if len(lines) < 1:
        return None
    
    if json.loads(lines[0])['header']['type']=='IO':
        log_field_type = 'FaceDetectionOutput'
        scale_factor_x = 1920/232
        scale_factor_y = 1080/132
    elif json.loads(lines[0])['header']['type'][0]=='gt_log':
        log_field_type = 'Face BB'
        scale_factor_x = 1
        scale_factor_y = 1

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
            bb = obj['BoundingBox']
            prediction = {'object_id':obj['Id'], 'x':bb['Left']*scale_factor_x,'y':bb['Top']*scale_factor_y,'width':bb['Width']*scale_factor_x,'height':bb['Height']*scale_factor_y}
            if 'Score' in obj:
                prediction['Score'] = obj['Score']
            detections.append({'detection':True, 'prediction': prediction})

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df