from cmath import nan
import json
import numpy as np
from turtle import left
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from classes_and_utils.utils import empty_when_negative_x
import pandas as pd
from utils.LogsParser import get_fps

def statistic_tool_reader_presence_calssification(path):
    with open(path,'r') as file:
        lines = file.readlines()
        
        header = json.loads(lines[0])
        line = json.loads(lines[1])
        records = []
        
        fps = get_fps(header)

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

        # Add new label tag from existing label keys
        # Set presence GT = false from begining of approach event till last 3 seconds of any approach event
        # To be replaced by distance
        # + split approach to 3 area: ROI, Transition, out of ROI and change GT accordingly
        enable_approach_split = False # False = use sec_num_to_mask, True = use approach_trans_in_frames (split aprroach to 3 areas)
        presence_time_mask = np.full(np.shape(lines[1:]), True)
        approach_index_from_end = np.zeros(np.shape(lines[1:]))
        approach_roi_mask    = np.full(np.shape(lines[1:]), False)
        approach_trans_mask  = np.full(np.shape(lines[1:]), False)
        approach_oo_roi_mask = np.full(np.shape(lines[1:]), False)
        sec_num_to_mask = 3 * fps
        prev_user_status = 'NoUser'
        during_approach_seq = False
        post_app_frame_num = 7 * fps #TODO: Change to time * fps?
        approach_roi_in_frames   = 1 * fps
        approach_trans_in_frames = 1.5 * fps
        
        for ind,line in enumerate(lines[1:]):
            line = json.loads(line)
            if 'type' not in line['keys'] or (line['keys']['type'] != 'sequence' and line['keys']['type'] != 'presence'):
                continue

            if 'User_Status' in line['message']: # GT logs
                curr_user_status = line['message']['User_Status']
                if curr_user_status=='Approach_PC' and during_approach_seq == False:
                    first_approach_ind = ind
                    during_approach_seq = True

                if prev_user_status=='Approach_PC' and curr_user_status!='Approach_PC':
                    # Mark frames from approach start to last 3 second before last approach frame with presence_time_mask = False
                    last_ind_to_mask = int(max(first_approach_ind,ind-sec_num_to_mask))
                    presence_time_mask[first_approach_ind:last_ind_to_mask] = False
                    approach_duration = ind - first_approach_ind
                    #print(-approach_duration+1)
                    approach_index_from_end[first_approach_ind:ind] = np.arange(-approach_duration+1,1)
                    approach_index_from_end[ind-1:ind+(int(min(post_app_frame_num,len(approach_index_from_end)-ind)))-1] = np.arange(0,(int(min(post_app_frame_num,len(approach_index_from_end)-ind))))
                    #if first_approach_ind!=last_ind_to_mask:
                    #    print('found')
                    
                    first_approach_roi_ind   = int(max(ind-approach_roi_in_frames,first_approach_ind))
                    first_approach_trans_ind = int(max(ind-approach_trans_in_frames,first_approach_ind))
                    approach_roi_mask[first_approach_roi_ind:ind]                        = True
                    approach_trans_mask[first_approach_trans_ind:first_approach_roi_ind] = True
                    approach_oo_roi_mask[first_approach_ind:first_approach_trans_ind]    = True
                    during_approach_seq = False
                prev_user_status = curr_user_status

                

        for ind,line in enumerate(lines[1:]):
            line = json.loads(line)
            if 'type' not in line['keys'] or (line['keys']['type'] != 'sequence' and line['keys']['type'] != 'presence'):
                continue
            
            frame_id = line['keys']['frame_id']
            if 'System State' in line['message']: # Prediction logs
                if line['message']['System State']=="SCREEN_ON":
                    data={'frame_id':frame_id, 'predictions': [{'detection':True, 'prediction':{'classification':1.0}}]}
                else:
                    data={'frame_id':frame_id, 'predictions': [{'detection':False, 'prediction':{'classification':0.0}}]}
            else: #GT logs
                if enable_approach_split==False:
                    #If HumanPresence Annotation is true, but the frames are within the first "sec_num_to_mask" (3 seconds) frames of the approach event, 
                    # then HumanPresence Annotation is switched to false
                    if line['message']['HumanPresence'] == 'True' and presence_time_mask[ind]==True:
                        data={'frame_id':frame_id, 'predictions': [{'detection':True, 'prediction':{'classification':1.0}}]}
                    else:
                        data={'frame_id':frame_id, 'predictions': [{'detection':False, 'prediction':{'classification':0.0}}]}
                else:
                    #If HumanPresence Annotation is true, but the frames are within the first "approach_trans_in_frames" (1.5 seconds) frames of the approach event, 
                    # then HumanPresence Annotation is switched to false
                    if line['message']['HumanPresence'] == 'True' and approach_oo_roi_mask[ind]==False:
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

            data['predictions'][0]['Approach_index_from_event_end'] = approach_index_from_end[ind]
            data['predictions'][0]['Approach_split_roi']    = approach_roi_mask[ind]
            data['predictions'][0]['Approach_split_trans']  = approach_trans_mask[ind]
            data['predictions'][0]['Approach_split_oo_roi'] = approach_oo_roi_mask[ind]
            data['predictions'][0]['enable_approach_split'] = enable_approach_split

            if 'Background_People' in line['message']:
                data['predictions'][0]['Background_People'] = line['message']['Background_People']
            if 'Background_Dynamic_Objects' in line['message']:
                data['predictions'][0]['Background_Dynamic_Objects'] = line['message']['Background_Dynamic_Objects']
            if 'Background_People_Activity' in line['message']:
                data['predictions'][0]['Background_People_Activity'] = line['message']['Background_People_Activity']
            if 'User_Status' in line['message']:
                data['predictions'][0]['User_Status'] = line['message']['User_Status']
            if 'System_Context' in line['message']:
                data['predictions'][0]['System_Context'] = line['message']['System_Context']
            if 'Is_Wake_event' in line['message']:
                data['predictions'][0]['Is_Wake_event'] = line['message']['Is_Wake_event']
            if 'Is_Lock_event' in line['message']:
                data['predictions'][0]['Is_Lock_event'] = line['message']['Is_Lock_event']
            if 'Activity_ROI' in line['message']:
                data['predictions'][0]['Activity_ROI'] = line['message']['Activity_ROI']
            if 'Presence_ROI' in line['message']:
                data['predictions'][0]['Presence_ROI'] = line['message']['Presence_ROI']
            


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