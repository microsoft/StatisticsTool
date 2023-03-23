from cmath import nan
import json
import numpy as np
from turtle import left
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from classes_and_utils.utils import empty_when_negative_x
import pandas as pd

def statistic_tool_reader_presence_algo_logs(path):
    with open(path,'r') as file:
        lines = file.readlines()

    if len(lines) < 1:
        return None

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
            detections.append({'detection':True, 'prediction':{'object_id':obj['Id'], 'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height']}})

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df