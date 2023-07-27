from cmath import nan
import json
import numpy as np
from turtle import left
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from classes_and_utils.utils import empty_when_negative_x
import pandas as pd
from utils.LogsParser import is_golden_log, transform_bb_to_original_frame_size, get_fps

def statistic_tool_reader_fusion_detection_logs(path, threshold_score=0.5, **kwargs):
    with open(path,'r') as file:
        lines = file.readlines()
    
    line = json.loads(lines[1])
    header= json.loads(lines[0])
    log_is_algo = is_golden_log(header)
    records = []
    
    for line in lines[1:]:
        line = json.loads(line)
        if 'type' not in line['keys'] or line['keys']['type'] != 'face detection' or 'objects' not in line['message']:
            continue

        detections = []
        frame_id = line['keys']['frame']
        # frame_id = line['keys']['frame_id']  # just to note that in previous version frame called frame_id
        if 'bb' not in line['keys']['type'] and 'detection' not in line['keys']['type']:
            continue  # skip landmarks. this is only for bb for now
        #TODO update conditions to match appropriate fields in the latest GT logs
        
        for single_bb_id in line['message']['objects']:
            bb = line['message']['objects'][single_bb_id]
            x = bb['Left']
            y = bb['Top']
            width = bb['Width']
            height = bb['Height']
            if 'confidence' in bb:
                score = bb['confidence']
            else:
                score = bb['Confidence']
            
            if score >= threshold_score:
                detections.append({'detection':True, 'prediction':{'confidence': score, 'x': x,'y': y,'width': width,'height': height}})
                #TODO: Add Correction to BB from emulation

            #TODO: Add FPS to detections

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df
    
