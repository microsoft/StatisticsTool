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
    
    valid_types = ['sequence', 'Body BB', 'objects'] #includes types of both gt logs and algo/golden logs
    valid_sources = ['BODY_DETECTION','BODY_DETEDCTION'] #includes sources of both gt logs and algo/golden logs

    # iterate a full first cycle to infer if 'sequence' annotation is available (if we're parsing gt_log)
    is_sequence_annot_available = False
    prev_line_frame_id = 0
    for line in lines[1:]:
        line = json.loads(line)
        frame_id = line['keys']['frame_id']
        if frame_id > prev_line_frame_id:
            break
        if line['keys']['type'] == 'sequence':
            is_sequence_annot_available = True
        prev_line_frame_id = frame_id

    # parse json lines
    detections_parsed = False
    sequence_parsed = False
    for line in lines[1:]:
        line = json.loads(line)
        frame_id = line['keys']['frame_id']

        if 'type' not in line['keys'] or line['keys']['type'] not in valid_types:
            continue

        if line['keys']['type'] == 'Body BB' or line['keys']['type'] == 'objects':
            sequence = []
            detections = []
            frame_id = line['keys']['frame_id']

            for obj in line['message']['objects']:
                if obj["Source"] not in valid_sources:
                    continue
                bb = obj['BoundingBox']
                detections.append({'detection':True, 'prediction':{'object_id':obj['Id'], 'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height']}})

            if len(detections) == 0:
                detections=[{'detection':False}]

            detections_parsed = True
            dict_line_to_append = {'frame_id': frame_id, 'predictions':detections}
        
        if is_sequence_annot_available and line['keys']['type'] == 'sequence':
            sequence_message = line['message']
            sequence_parsed = True
            dict_line_to_append.update({k + '[sequence]': str(v) if type(v) == list else v for k, v in sequence_message.items()})

        if is_sequence_annot_available and detections_parsed and sequence_parsed:
            records.append(dict_line_to_append)
            detections_parsed = False
            sequence_parsed = False
        elif not(is_sequence_annot_available) and detections_parsed:
            records.append(dict_line_to_append)
            detections_parsed = False
    
    df = pd.DataFrame.from_records(records)

    # adding header
    header = json.loads(lines[0])
    header = header['header']    
    header = {k + '[header]': str(v) if type(v) == list else v for k, v in header.items()}
    metadata_row_df = pd.DataFrame(header, index=[0])
    tmp_df = pd.concat([metadata_row_df]*len(df), ignore_index=True)

    df = pd.concat((df.reset_index(drop=True),
                        tmp_df.reset_index(drop=True)), axis=1)    
       
    
    return df