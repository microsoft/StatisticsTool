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
            bb = obj['BoundingBox']
            cord = np.array([bb['Left'], bb['Top'], 1])
            cord = emulation_matrix.dot(cord)
            width_hight = np.array([bb['Width'], bb['Height'], 0])
            width_hight = emulation_matrix.dot(width_hight)
            prediction = {'object_id':obj['Id'], 'x':cord[0],'y':cord[1],'width':width_hight[0],'height':width_hight[1]}
            if 'Score' in obj:
                prediction['Score'] = obj['Score']
            detections.append({'detection':True, 'prediction': prediction})

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df