from cmath import nan
import json
import numpy as np
from turtle import left
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from classes_and_utils.utils import empty_when_negative_x
import pandas as pd


def statistic_tool_reader_activity(path, **kwargs):
    if 'body_detection_log.json' in path:
        return None

    with open(path,'r') as file:
        lines = file.readlines()

    if len(lines) < 1:
        return None

    line = json.loads(lines[1])
    records = []
    
    valid_types = ['sequence', 'presence'] #includes types of both gt logs and algo/golden logs

    # parse json lines
    for line in lines[1:]:
        line = json.loads(line)
        frame_id = line['keys']['frame_id']

        if 'type' not in line['keys'] or line['keys']['type'] not in valid_types:
            continue

        detections = []
        frame_id = line['keys']['frame_id']

        # parse golden sim log
        if line['keys']['type'] == 'presence':
            if line['message']["Activity State"] == "ACTIVITY_DETECTED":
                detections.append({'detection':True, 'prediction':{'activity':1.0}})
            else:
                detections.append({'detection':False, 'prediction':{'activity':0.0}})
            dict_line_to_append = {'frame_id': frame_id, 'predictions':detections}            

        # parse gt log
        elif line['keys']['type'] == 'sequence':
            sequence_message = line['message']
            # add gt detection separately
            if "Activity_ROI" in sequence_message.keys() and sequence_message["Activity_ROI"] == "True":
                detections.append({'detection':True, 'prediction':{'activity':1.0}})
            else:
                detections.append({'detection':False, 'prediction':{'activity':0.0}})
            dict_line_to_append = {'frame_id': frame_id, 'predictions':detections}            
            dict_line_to_append.update({k + '[sequence]': str(v) if type(v) == list else v for k, v in sequence_message.items()})

        records.append(dict_line_to_append)

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