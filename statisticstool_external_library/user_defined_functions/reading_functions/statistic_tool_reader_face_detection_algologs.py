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

BAD_MF_TYPES = ['NO_OBJECT', 'OBJECT_NO_DETECTION']

def statistic_tool_reader_face_detection_algologs(path):
    with open(path,'r') as file:
        lines = file.readlines()
        header = lines[0]
        lines = lines[1:]

    if len(lines) < 1:
        return None
    
    emulation_matrix = get_emulation_matrix(json.loads(header))

    log_type = check_log_type(json.loads(header))
    if log_type == LogTypes.IO_LOG:
        log_field_type = 'FaceDetectionOutput'
    elif log_type == LogTypes.GT_LOG:
        log_field_type = 'Face BB'
    elif log_type == LogTypes.ALGO_LOG:
        log_field_type = 'fusion_objects'

    records = []
    
    for line in lines:
        line = json.loads(line)
        if ('type' in line['keys'] and line['keys']['type'] != log_field_type) or 'objects' not in line['message']:
            continue

        detections = []
        frame_id = line['keys']['frame_id']
       
        for obj in line['message']['objects']:
            if ("Source" in obj and obj["Source"] != "FACE_DETECTION") or ("Face" in obj and "MFObjectType" in obj["Face"] and obj["Face"]["MFObjectType"] in BAD_MF_TYPES):
                continue

            if "Face" in obj and "FinalObject" in obj["Face"]:
                face_obj = obj["Face"]["FinalObject"]
                face_obj['Id'] = obj["Face"]["MFObjectID"]
            else:
                face_obj = obj

            bb = transform_bb_to_original_frame_size(face_obj['BoundingBox'], emulation_matrix)
            prediction = {'object_id':face_obj['Id'], 'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height']}
            if 'Score' in face_obj:
                prediction['Score'] = face_obj['Score']
            if 'InRange' in face_obj:
                prediction['InRange'] = face_obj['InRange']
            detections.append({'detection':True, 'prediction': prediction})

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df