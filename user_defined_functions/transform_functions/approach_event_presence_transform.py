import pandas as pd
import numpy as np

from user_defined_functions.transform_functions.calc_flicker_metrics import calc_flicker_metrics
from user_defined_functions.transform_functions import  determine_approach_success_mask

def approach_event_presence_transform(comp_data):
    # Inits
    early_wake_flag  = False
    early_wake_flag2 = False

    # Program
    approach_success_mask, multi_seq, pop_up_indication, pop_up_indication2, pop_up_reason_ind, pop_up_reason_ind2 = determine_approach_success_mask(comp_data)

    user_move_type = comp_data['User_Status_gt']
    presence_pred = comp_data['detection']
    presence_pred_at_approach = presence_pred[user_move_type=='Approach_PC']
    approach_ind = np.where(user_move_type=='Approach_PC')[0]
    mask_true_ind = np.where(approach_success_mask==True)[0]
    presence_pred_at_range = presence_pred[mask_true_ind]

    if len(approach_ind)==0: # No approach sequence exists
        print(np.unique(user_move_type))
        return pd.DataFrame()

    if multi_seq == True:
        seperator_app = np.where((np.diff(approach_ind)==1)==False)
        approach_ind2 = approach_ind[(seperator_app[0][0]+1):]
        approach_ind  = approach_ind[0:(seperator_app[0][0]+1)]
        presence_pred_at_approach2 = presence_pred_at_approach[(seperator_app[0][0]+1):]
        presence_pred_at_approach  = presence_pred_at_approach[0:(seperator_app[0][0]+1)]

        seperator_mask = np.where((np.diff(mask_true_ind)==1)==False)
        mask_true_ind2 = mask_true_ind[(seperator_mask[0][0]+1):]
        mask_true_ind  = mask_true_ind[0:(seperator_mask[0][0]+1)]
        presence_pred_at_range2 = presence_pred_at_range[(seperator_mask[0][0]+1):]
        presence_pred_at_range  = presence_pred_at_range[0:(seperator_mask[0][0]+1)]

    # Check valid range
    if sum(presence_pred_at_range)==0:
        temp_success_flag = False
        presence_true_prct_at_range = 0
    else:
        temp_success_flag = True
        presence_true_prct_at_range = sum(presence_pred_at_range)/len(presence_pred_at_range)

    if multi_seq == True:
        if sum(presence_pred_at_range2)==0:
            temp_success_flag2 = False
            presence_true_prct_at_range2 = 0
        else:
            temp_success_flag2 = True
            presence_true_prct_at_range2 = sum(presence_pred_at_range2)/len(presence_pred_at_range2)    


    # Detect first true duration from last approach frame
    first_presence_in_app = np.where(presence_pred_at_approach==True)[0]
    if len(first_presence_in_app) > 0:
        first_presence_in_app = first_presence_in_app[0]
        duration_from_app_end = len(presence_pred_at_approach) - first_presence_in_app
    else:
        first_presence_in_app = np.nan
        duration_from_app_end = -60
    
    if multi_seq == True:
        first_presence_in_app2 = np.where(presence_pred_at_approach2==True)[0]
        if len(first_presence_in_app2) > 0:
            first_presence_in_app2 = first_presence_in_app2[0]
            duration_from_app_end2 = len(presence_pred_at_approach2) - first_presence_in_app2
        else:
            first_presence_in_app2 = np.nan
            duration_from_app_end2 = -60        

    # Check for early Wakes (FP)
    first_range_frame_within_app = np.where(approach_ind==mask_true_ind[0])
    if first_presence_in_app < first_range_frame_within_app[0][0]:
        early_wake_flag = True
    
    if multi_seq == True:
        first_range_frame_within_app2 = np.where(approach_ind2==mask_true_ind2[0])
        if first_presence_in_app2 < first_range_frame_within_app2[0][0]:
            early_wake_flag2 = True

    # Calc flicker metrics
    if len(presence_pred_at_approach)>0:
        seq_num, avg_seq_len, med_seq_len = calc_flicker_metrics(np.array(presence_pred_at_approach))
    else:
        seq_num = avg_seq_len = med_seq_len = 0

    if multi_seq == True:
        if len(presence_pred_at_approach2)>0:
            seq_num2, avg_seq_len2, med_seq_len2 = calc_flicker_metrics(np.array(presence_pred_at_approach2))
        else:
            seq_num2 = avg_seq_len2 = med_seq_len2 = 0        


    # Arrange new_event output format
    new_event = comp_data.iloc[approach_ind[0]].to_dict()
    new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
    new_event['end_frame'] = approach_ind[-1]
    new_event['frame_id']  = approach_ind[0] #start_frame
    new_event['Presence approach flicker sequence num'] = seq_num
    new_event['Presence approach flicker sequence mean length'] = avg_seq_len
    new_event['Presence approach flicker sequence median length'] = med_seq_len

    if multi_seq == True:
        new_event2 = comp_data.iloc[approach_ind2[0]].to_dict()
        new_event2['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
        new_event2['end_frame'] = approach_ind2[-1]
        new_event2['frame_id']  = approach_ind2[0] #start_frame
        new_event2['Presence approach flicker sequence num'] = seq_num2
        new_event2['Presence approach flicker sequence mean length'] = avg_seq_len2
        new_event2['Presence approach flicker sequence median length'] = med_seq_len2       
    

    # Determine output state (FP, TP, FN)
    if temp_success_flag == True:
        new_event['detection'] = True
        new_event['state'] = 1
    else: # Late wake (FN)
        new_event['detection'] = False
        new_event['state'] = 0
    if early_wake_flag == True: # Early wake (FP)
        new_event['detection_gt'] = False
        new_event['detection'] = True
        new_event['state'] = 0

    if multi_seq == True:
        if temp_success_flag2 == True:
            new_event2['detection'] = True
            new_event2['state'] = 1
        else: # Late wake (FN)
            new_event2['detection'] = False
            new_event2['state'] = 0
        if early_wake_flag2 == True: # Early wake (FP)
            new_event2['detection_gt'] = False
            new_event2['detection'] = True
            new_event2['state'] = 0        


    # Add statistics about the event
    new_event['Approach pop up indication'] = pop_up_indication
    new_event['Presence seq duration prior to approach event end'] = duration_from_app_end
    new_event['Approach event presence detected percent'] = presence_true_prct_at_range
    new_event['Approach event number in clip'] = 1
    new_event['Approach event pop up reason index'] = pop_up_reason_ind

    if multi_seq == True:
        new_event2['Approach pop up indication'] = pop_up_indication2
        new_event2['Presence seq duration prior to approach event end'] = duration_from_app_end2
        new_event2['Approach event presence detected percent'] = presence_true_prct_at_range2   
        new_event2['Approach event number in clip'] = 2
        new_event2['Approach event pop up reason index'] = pop_up_reason_ind2


    events = []
    events.append(new_event)
    if multi_seq == True:
        events.append(new_event2)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data