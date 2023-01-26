from cmath import nan
import json
import os
import sys
import numpy as np
from turtle import left
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes_and_utils.utils import empty_when_negative_x
import pandas as pd

"""
Reading Function instructions:
------------------------------

Input:
a. Accept as input a path to the data file (any type that the user preffered)

A reading function should:
1. Read the input file (The type of the file is defined by the user according to user prefference)
2. Convert the input data to panda's data frame format. The data frame should have at least the following columns:
    a. frame_id
    b. predictions (1 or more) - array with predictions results for the current frame:
        each element in the array should be dictionary with at least the following keys:
            a. detection (mandatory) - True/False : For TP/FP calculation.
            b. predictioon (not mandatory) - prediction dictionary for comparing between gt/prediction

        If the  prediction is bounding box in the format below, it can be shown as rectangles on frame view:
        - Bounding box columns, using the following names:
                        i.   'x' is the minimal x coordinate
                        ii.  'y' is the minimal y coordinate
                        iii. 'width' is the width of the bounding box (column name will be 'width')
                        iv.  'height' is the height of the bounding box (column name will be 'height')
        
        exmaples for output rows in the dataframe:

            classification example:           
            {'frame_id':frame_id, 'predictions': [{'detection':True, 'prediction':{'classification':'Active'}}]}
            {'frame_id':frame_id, 'predictions': [{'detection':False, 'prediction':{'classification':'Not_Active'}}]}
           
            detection example:
            {'frame_id': frame_id, 'predictions' [{'detection':True, 'prediction':{'object_id':1, 'x':10,'y':20,'width':10,'height':10}}]}
            {'frame_id': frame_id, 'predictions' [{'detection':False}]}



Returns:
pandas dataframe
"""

def statistic_tool_reader_activity_calssification(path):
    with open(path,'r') as file:
        lines = file.readlines()
        
        line = json.loads(lines[1])
        records = []

        # Add header information to all frames
        header_line = json.loads(lines[0])
        if 'Location' in header_line['header']:
            clip_loc = header_line['header']['Location']
        else:
            clip_loc = 'NA'
        if 'General_Background_People' in header_line['header']:
            clip_bg_people = header_line['header']['General_Background_People']
        else:
            clip_bg_people = 'NA'
        if 'User_Gender' in header_line['header']:
            clip_user_gender = header_line['header']['User_Gender']
        else:
            clip_user_gender = 'NA'
        if 'User_Complexion' in header_line['header']:
            clip_user_complexion = header_line['header']['User_Complexion']
        else:
            clip_user_complexion = 'NA'
        if 'Enviroment' in header_line['header']:
            clip_enviroment = header_line['header']['Enviroment']
        else:
            clip_enviroment = 'NA'
        if 'General_Natural_Light' in header_line['header']:
            clip_general_natural_light = header_line['header']['General_Natural_Light']
        else:
            clip_general_natural_light = 'NA'
        if 'General_Artificial_Light' in header_line['header']:
            clip_artificial_light = header_line['header']['General_Artificial_Light']
        else:
            clip_artificial_light = 'NA'
        if 'Device_Posture' in header_line['header']:
            clip_device_posture = header_line['header']['Device_Posture']
        else:
            clip_device_posture = 'NA'
        if 'External_Monitor' in header_line['header']:
            clip_external_monitor = header_line['header']['External_Monitor']
        else:
            clip_external_monitor = 'NA'
        if 'Clip_Duration [MIN]' in header_line['header']:
            clip_duration = header_line['header']['Clip_Duration [MIN]']
        else:
            clip_duration = 'NA'
        
        for line in lines[1:]:
            line = json.loads(line)
            if 'type' not in line['keys'] or line['keys']['type'] != 'presence':
                continue
            
            frame_id = line['keys']['frame_id']
            if int(line['message']['activity'])>0:
                data={'frame_id':frame_id, 'predictions': [{'detection':True, 'prediction':{'activity':1.0}}]}
            else:
                data={'frame_id':frame_id, 'predictions': [{'detection':False, 'prediction':{'activity':0.0}}]}

            data['predictions'][0]['Location']                  = clip_loc
            data['predictions'][0]['General_Background_People'] = clip_bg_people
            data['predictions'][0]['User_Gender']               = clip_user_gender
            data['predictions'][0]['User_Complexion']           = clip_user_complexion
            data['predictions'][0]['Enviroment']                = clip_enviroment
            data['predictions'][0]['General_Natural_Light']     = clip_general_natural_light
            data['predictions'][0]['General_Artificial_Light']  = clip_artificial_light
            data['predictions'][0]['Device_Posture']            = clip_device_posture
            data['predictions'][0]['External_Monitor']          = clip_external_monitor
            data['predictions'][0]['Clip_Duration [MIN]']       = clip_duration

            if 'static' in line['message']:
                data['predictions'][0]['static'] = line['message']['static']
                data['predictions'][0]['relevant'] = line['message']['relevant']
                data['predictions'][0]['Multiple People'] = line['message']['Multiple People']
            if 'User_Physical_Status' in line['message']:
                data['predictions'][0]['User_Physical_Status'] = line['message']['User_Physical_Status']
                data['predictions'][0]['User_Movement_Type'] = line['message']['User_Movement_Type']
            if 'People_Outside_ROI_Only' in line['message']:
                data['predictions'][0]['People_Outside_ROI_Only'] = line['message']['People_Outside_ROI_Only']
            if 'Approach event activity detected length' in line['message']:
                data['predictions'][0]['Approach event activity detected length']         = line['message']['Approach event activity detected length']
                data['predictions'][0]['Approach event activity detected percent']        = line['message']['Approach event activity detected percent']
                data['predictions'][0]['Active seq duration prior to approach event end'] = line['message']['Active seq duration prior to approach event end']
                data['predictions'][0]['Active seq duration from approach event start']   = line['message']['Active seq duration from approach event start']
            if 'Separate FN sequence length' in line['message']:
                data['predictions'][0]['Separate FN sequence length'] = line['message']['Separate FN sequence length']
                data['predictions'][0]['Separate FN sequence count']  = line['message']['Separate FN sequence count']
            if 'Separate FP sequence length' in line['message']:
                data['predictions'][0]['Separate FP sequence length'] = line['message']['Separate FP sequence length']
                data['predictions'][0]['Separate FP sequence count']  = line['message']['Separate FP sequence count']


            records.append(data)

    df = pd.DataFrame.from_records(records)
    return df   
    
def statistic_tool_reader_presence_calssification(path):
    with open(path,'r') as file:
        lines = file.readlines()
        
        line = json.loads(lines[1])
        records = []

        # Add header information to all frames
        header_line = json.loads(lines[0])
        if 'Location' in header_line['header']:
            clip_loc = header_line['header']['Location']
        else:
            clip_loc = 'NA'
        if 'General_Background_People' in header_line['header']:
            clip_bg_people = header_line['header']['General_Background_People']
        else:
            clip_bg_people = 'NA'
        if 'User_Gender' in header_line['header']:
            clip_user_gender = header_line['header']['User_Gender']
        else:
            clip_user_gender = 'NA'
        if 'User_Complexion' in header_line['header']:
            clip_user_complexion = header_line['header']['User_Complexion']
        else:
            clip_user_complexion = 'NA'
        if 'Enviroment' in header_line['header']:
            clip_enviroment = header_line['header']['Enviroment']
        else:
            clip_enviroment = 'NA'
        if 'General_Natural_Light' in header_line['header']:
            clip_general_natural_light = header_line['header']['General_Natural_Light']
        else:
            clip_general_natural_light = 'NA'
        if 'General_Artificial_Light' in header_line['header']:
            clip_artificial_light = header_line['header']['General_Artificial_Light']
        else:
            clip_artificial_light = 'NA'
        if 'Device_Posture' in header_line['header']:
            clip_device_posture = header_line['header']['Device_Posture']
        else:
            clip_device_posture = 'NA'
        if 'External_Monitor' in header_line['header']:
            clip_external_monitor = header_line['header']['External_Monitor']
        else:
            clip_external_monitor = 'NA'
        if 'Clip_Duration [MIN]' in header_line['header']:
            clip_duration = header_line['header']['Clip_Duration [MIN]']
        else:
            clip_duration = 'NA'

        
        for line in lines[1:]:
            line = json.loads(line)
            if 'type' not in line['keys'] or (line['keys']['type'] != 'sequence' and line['keys']['type'] != 'presence'):
                continue
            
            frame_id = line['keys']['frame_id']
            if 'System State' in line['message']:
                if line['message']['System State']=="SCREEN_ON":
                    data={'frame_id':frame_id, 'predictions': [{'detection':True, 'prediction':{'classification':1.0}}]}
                else:
                    data={'frame_id':frame_id, 'predictions': [{'detection':False, 'prediction':{'classification':0.0}}]}
            else:
                if line['message']['HumanPresence'] == 'True':
                    data={'frame_id':frame_id, 'predictions': [{'detection':True, 'prediction':{'classification':1.0}}]}
                else:
                    data={'frame_id':frame_id, 'predictions': [{'detection':False, 'prediction':{'classification':0.0}}]}

            data['predictions'][0]['Location']                  = clip_loc
            data['predictions'][0]['General_Background_People'] = clip_bg_people
            data['predictions'][0]['User_Gender']               = clip_user_gender
            data['predictions'][0]['User_Complexion']           = clip_user_complexion
            data['predictions'][0]['Enviroment']                = clip_enviroment
            data['predictions'][0]['General_Natural_Light']     = clip_general_natural_light
            data['predictions'][0]['General_Artificial_Light']  = clip_artificial_light
            data['predictions'][0]['Device_Posture']            = clip_device_posture
            data['predictions'][0]['External_Monitor']          = clip_external_monitor
            data['predictions'][0]['Clip_Duration [MIN]']       = clip_duration

            if 'Background_People' in line['message']:
                data['predictions'][0]['Background_People'] = line['message']['Background_People']
            if 'Background_Dynamic_Objects' in line['message']:
                data['predictions'][0]['Background_Dynamic_Objects'] = line['message']['Background_Dynamic_Objects']
            if 'Background_People_Activity' in line['message']:
                data['predictions'][0]['Background_People_Activity'] = line['message']['Background_People_Activity']
            if 'User_Status' in line['message']:
                data['predictions'][0]['User_Status'] = line['message']['User_Status']


            if 'static' in line['message']:
                data['predictions'][0]['static'] = line['message']['static']
                data['predictions'][0]['relevant'] = line['message']['relevant']
                data['predictions'][0]['Multiple People'] = line['message']['Multiple People']
            if 'User_Physical_Status' in line['message']:
                data['predictions'][0]['User_Physical_Status'] = line['message']['User_Physical_Status']
                data['predictions'][0]['User_Movement_Type'] = line['message']['User_Movement_Type']
            if 'People_Outside_ROI_Only' in line['message']:
                data['predictions'][0]['People_Outside_ROI_Only'] = line['message']['People_Outside_ROI_Only']
            if 'Approach event presence detected length' in line['message']:
                data['predictions'][0]['Approach event presence detected length']         = line['message']['Approach event presence detected length']
                data['predictions'][0]['Approach event presence detected percent']        = line['message']['Approach event presence detected percent']
                data['predictions'][0]['Presence seq duration prior to approach event end'] = line['message']['Presence seq duration prior to approach event end']
                data['predictions'][0]['Presence seq duration from approach event start']   = line['message']['Presence seq duration from approach event start']
            records.append(data)

    df = pd.DataFrame.from_records(records)
    return df   

def statistic_tool_reader_presence_algo_logs(path):
    with open(path,'r') as file:
        lines = file.readlines()
    
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


def statistic_tool_reader_fusion_detection_logs(path, threshold_score=0.5):
    with open(path,'r') as file:
        lines = file.readlines()
    
    line = json.loads(lines[1])
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

        if len(detections) == 0:
            detections=[{'detection':False}]

        records.append({'frame_id': frame_id, 'predictions':detections})
    
    df = pd.DataFrame.from_records(records)  
    
    return df
    

if __name__ =="__main__":
    a,b=statistic_tool_reader_presence_algo_logs("C:/Users/v-nrosenberg/Documents/Sources/DataScienceSIL/Subsystem/Sensors/presence_sensing/camera/prod/golden_simulation/logger/logs/24_07_2022_10_52_36/presence_log.json")
    
    print(a)
