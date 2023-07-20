from cmath import nan
import json
import numpy as np
from turtle import left
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from classes_and_utils.utils import empty_when_negative_x
import pandas as pd
from utils.LogsParser import is_golden_log, transform_bb_to_original_frame_size, get_fps, get_emulation_matrix

def statistic_tool_reader_presence_algo_logs(path, **kwargs):
    with open(path,'r') as file:
        lines = file.readlines()

    if len(lines) < 1:
        return None

    header = json.loads(lines[0])
    log_is_algo = is_golden_log(header)
    line = json.loads(lines[1])
    records = []
    valid_types = ['Body BB', 'objects'] #includes types of both gt logs and algo/golden logs
    valid_sources= ['BODY_DETECTION','BODY_DETEDCTION']   #includes sources of both gt logs and algo/golden logs

    emulation_matrix = get_emulation_matrix(header)

    for line in lines[1:]:
        line = json.loads(line)
        if 'type' not in line['keys'] or line['keys']['type'] not in  valid_types or 'objects' not in line['message']:
            continue
          
        detections = []
        frame_id = line['keys']['frame_id']

        for obj in line['message']['objects']:
            if obj["Source"] not in valid_sources:
                continue
            bb = obj['BoundingBox']

            # Add Bounding box to predictions
            if  log_is_algo:
                bb = transform_bb_to_original_frame_size(bb, emulation_matrix)
            
            detections.append({'detection':True, 'prediction':{'object_id':obj['Id'], 'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height'],'fps_original_video':get_fps(header)}})

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df