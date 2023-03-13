import pandas as pd
import numpy as np

from user_defined_functions.transform_functions.calc_flicker_metrics import calc_flicker_metrics

def approach_event_presence_transform(comp_data):
    minimal_presence_seq_len = 1
    roi_in_sec = 1
    oo_roi_in_sec = 2
    key = 'User_Status_gt'
    user_move_type = comp_data[key]
    move_type_mask_approach = np.full(np.shape(user_move_type), False)
    move_type_mask_approach[user_move_type=='Approach_PC']   = True

    presence_pred = comp_data['detection']
    presence_pred_at_approach = presence_pred[move_type_mask_approach==True] #assuming that approach labeling is in a single sequence of consecutive frames
    approach_length = len(presence_pred_at_approach)
    R0_first_frame = min(approach_length, roi_in_sec*30)
    if approach_length<roi_in_sec*30:
        pop_up_indication = True
    else:
        pop_up_indication = False
    R1_first_frame = min(approach_length, oo_roi_in_sec*30)
    presence_pred_at_approach_R0 = presence_pred_at_approach[approach_length-R0_first_frame:-1]
    presence_pred_at_approach_R1 = presence_pred_at_approach[approach_length-R1_first_frame:approach_length-R0_first_frame]
    presence_pred_at_approach_R2 = presence_pred_at_approach[0:approach_length-R1_first_frame]
    if len(presence_pred_at_approach)>0:
        seq_num, avg_seq_len, med_seq_len = calc_flicker_metrics(np.array(presence_pred_at_approach))
    else:
        seq_num = avg_seq_len = med_seq_len = 0

    seq_str_for_search = "True  "*minimal_presence_seq_len
    seq_embeded_count = str(np.array(presence_pred_at_approach)).count(seq_str_for_search[:-1])

    # Arrange new_event output format
    approach_indices = np.where(move_type_mask_approach==True)
    if len(approach_indices[0])==0: # No approach sequence exists
        return pd.DataFrame()
    
    new_event = comp_data.iloc[approach_indices[0][0]].to_dict()
    new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
    new_event['end_frame'] = approach_indices[0][-1]
    new_event['frame_id']  = approach_indices[0][0] #start_frame
    new_event['Presence approach flicker sequence num'] = seq_num
    new_event['Presence approach flicker sequence mean length'] = avg_seq_len
    new_event['Presence approach flicker sequence median length'] = med_seq_len
    
    if sum(presence_pred_at_approach)==0:  # no presence indication at all
        duration_from_app_end = -30
    else:
        duration_from_app_end = np.where(np.array(presence_pred_at_approach)==1)[0][-1]-np.where(np.array(presence_pred_at_approach)==1)[0][0]-(minimal_presence_seq_len-1)

    if seq_embeded_count>0 and ((duration_from_app_end/30 >= roi_in_sec) and (duration_from_app_end/30 < oo_roi_in_sec)):
        new_event['detection'] = True
        new_event['state'] = 1
    else:
        new_event['detection'] = False
        new_event['state'] = 0
    if (duration_from_app_end/30 >= oo_roi_in_sec):
        new_event['detection_gt'] = False
        new_event['detection'] = True
        new_event['state'] = 0


    # Add statistics about the event
    new_event['Approach pop up indication'] = pop_up_indication
    new_event['Presence detection at R0 first frame'] = presence_pred_at_approach_R0.values[0]
    if len(presence_pred_at_approach_R0)==0:
        new_event['Approach event presence detected percent at R0'] = 0
    else:
        new_event['Approach event presence detected percent at R0'] = sum(presence_pred_at_approach_R0)/len(presence_pred_at_approach_R0)    
    if len(presence_pred_at_approach_R1)==0:
        new_event['Approach event presence detected percent at R1'] = 0
    else:
        new_event['Approach event presence detected percent at R1'] = sum(presence_pred_at_approach_R1)/len(presence_pred_at_approach_R1)    
    if len(presence_pred_at_approach_R2)==0:
        new_event['Approach event presence detected percent at R2'] = 0
    else:
        new_event['Approach event presence detected percent at R2'] = sum(presence_pred_at_approach_R2)/len(presence_pred_at_approach_R2)    
    # Length of the presence sequence out of the entire approach event
    if sum(presence_pred_at_approach)==0:
        new_event['Approach event presence detected percent'] = 0
        new_event['Approach event presence detected length'] = 0
    else:
        new_event['Approach event presence detected percent'] = len(np.where(np.array(presence_pred_at_approach)==1)[0])/len(np.array(presence_pred_at_approach))
        # Length of the sequence of presence=1 within the approach event
        if np.all(np.diff(np.where(np.array(presence_pred_at_approach)==1)[0])):
            new_event['Approach event presence detected length'] = len(np.where(np.array(presence_pred_at_approach)==1)[0]) - (minimal_presence_seq_len-1)
        else:
            new_event['Approach event presence detected length'] = len(np.where(np.array(presence_pred_at_approach)==1)[0]) - (minimal_presence_seq_len-1)*3        

    # Length (in frames) from the first detected sequence to the end of the approach event
    new_event['Presence seq duration prior to approach event end'] = duration_from_app_end
    if sum(presence_pred_at_approach)==0:
        new_event['Presence seq duration from approach event start'] = 100
    else:
        new_event['Presence seq duration from approach event start'] = np.where(np.array(presence_pred_at_approach)==1)[0][0] + 1


    events = []
    events.append(new_event)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data