from cmath import nan
import json
import numpy as np
from turtle import left
import sys
import os
root_dir = os.path.join(os.path.abspath(__file__).split('StatisticsTool')[0], 'StatisticsTool')
sys.path.append(root_dir)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from classes_and_utils.utils import empty_when_negative_x
import pandas as pd
from utils.LogsParser import is_golden_log, transform_bb_to_original_frame_size, get_fps
def statistic_tool_reader_body_detection_manual_vs_auto_gt(path):
    with open(path,'r') as file:
        lines = file.readlines()

    if len(lines) < 1:
        return None

    header = json.loads(lines[0])
    # log_is_algo = is_golden_log(header)
    line = json.loads(lines[1])
    records = []

    if 'manual_annotated' in path:
        valid_types = ['sequence', 'objects', 'Body BB - manual']
        valid_sources= ['Manual']   #includes sources of both gt logs and algo/golden logs
    else:
        valid_types = ['sequence', 'objects', 'Body BB']
        valid_sources= ['BODY_DETECTION']   #includes sources of both gt logs and algo/golden logs    

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
            # if  log_is_algo:
            #     bb = transform_bb_to_original_frame_size(bb, header)
            detection_dict = {'detection':True, 'prediction':{'object_id':obj['Id'], 'x':bb['Left'],'y':bb['Top'],'width':bb['Width'],'height':bb['Height'],'fps_original_video':get_fps(header)}}
            if 'BB_Body_Orientation' in obj.keys():
                detection_dict['prediction']['BB_Body_Orientation'] = obj['BB_Body_Orientation']
            if 'BB_Identity' in obj.keys():
                detection_dict['prediction']['BB_Identity'] = obj['BB_Identity']
            if 'BB_Occluded' in obj.keys():
                detection_dict['prediction']['BB_Occluded'] = obj['BB_Occluded']
            if 'BB_Body_InFrame' in obj.keys():
                detection_dict['prediction']['BB_Body_InFrame'] = obj['BB_Body_InFrame']
            detections.append(detection_dict)

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df

if __name__ == '__main__':

    data_root = fr'C:\Users\v-galgozes\Documents\annotation_logs\Experiments\WOALOLTestSetP0_manual_annotated'
    files = os.listdir(data_root)
    files = [f for f in files if f.endswith('.json')]
    import shutil

    for file in files:
        file_path = os.path.join(data_root, file)

        with open(file_path,'r') as file:
            lines = file.readlines()

        is_manual = False
        is_auto = False
        dst = file_path.replace(r"WOALOLTestSetP0_manual_annotated", r"WOALOLTestSetP0_manual_annotated_missing")
        for line in lines[1:]:
            line = json.loads(line)
            if line['keys']['type'] in ['Body BB - manual']:
                is_manual = True
            if line['keys']['type'] in ['Body BB']:
                is_auto = True
            if is_manual and is_auto:
                dst = file_path.replace(r"WOALOLTestSetP0_manual_annotated", r"\\WOALOLTestSetP0_manual_annotated_filtered")
                break
        else:
            print(f'{file_path} not found')
        shutil.copyfile(file_path, dst)
        

        # df = statistic_tool_reader_presence_algo_logs(path)
        # print(df.head())


    auto_root = data_root.replace(r"WOALOLTestSetP0_manual_annotated", r"WOALOLTestSetP0_gt_logs_filtered")
    manual_root = data_root.replace(r"WOALOLTestSetP0_manual_annotated", r"WOALOLTestSetP0_manual_annotated_filtered")
    file_name = 'ApproachLeave_2b220_User33_EmptyStaticBackground_Lighted_Sunny_110_2023-01-12_16-11-28'
    path_gt = fr'{manual_root}\{file_name}.json'
    df_gt = statistic_tool_reader_body_detection_manual_vs_auto_gt(path_gt)
    path_pred = fr'{auto_root}\{file_name}.json'
    df_pred = statistic_tool_reader_body_detection_manual_vs_auto_gt(path_pred)
    
    print(df_gt.head())
    print(df_pred.head())