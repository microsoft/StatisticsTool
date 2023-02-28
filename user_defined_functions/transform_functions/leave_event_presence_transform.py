import pandas as pd
import numpy as np

from user_defined_functions.transform_functions.calc_flicker_metrics import calc_flicker_metrics

def leave_event_presence_transform(comp_data):
    frame_num_to_remove_at_leave_seq_start = 15 # should be omitted after introducing distance>1.3m
    ten_sec_in_frames = 10*30 + frame_num_to_remove_at_leave_seq_start
    success_range_start = 4*30
    success_range_end   = 6*30

    key = 'User_Status_gt'
    user_move_type = comp_data[key]
    leave_event_locs = np.where(user_move_type=='Leaving_PC')[0]
    if len(leave_event_locs)==0: # No leave sequence exists
        return pd.DataFrame()

    leave_event_start = leave_event_locs[0] + frame_num_to_remove_at_leave_seq_start
    leave_event_end = min(leave_event_start+ten_sec_in_frames, user_move_type[-1:].index.start)

    new_event = comp_data.iloc[leave_event_start].to_dict()
    new_event['Event length'] = leave_event_end - leave_event_start
    new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
    new_event['end_frame'] = leave_event_end
    new_event['frame_id']  = leave_event_start #start_frame

 
    presence_pred = comp_data['detection']
    presence_pred_at_leave = np.array(presence_pred[(leave_event_start-frame_num_to_remove_at_leave_seq_start):leave_event_end])
    if len(presence_pred_at_leave)>0:
        seq_num, avg_seq_len, med_seq_len = calc_flicker_metrics(presence_pred_at_leave)
    else:
        seq_num = avg_seq_len = med_seq_len = 0
    new_event['Presence leave flicker sequence num'] = seq_num
    new_event['Presence leave flicker sequence mean length'] = avg_seq_len
    new_event['Presence leave flicker sequence median length'] = med_seq_len

    presence_pred_false_loc = np.where(presence_pred_at_leave==False)[0]
    presence_pred_true_loc  = np.where(presence_pred_at_leave==True)[0]
    if len(presence_pred_false_loc)==0:  # no presence_pred=false (assuming at least one true prediction)
        last_true_pred = ten_sec_in_frames + 1
        new_event['Presence leave event true/false ratio'] = 1
    else:
        if len(presence_pred_true_loc)>0:
            last_true_pred = presence_pred_true_loc[-1]
        else:
            last_true_pred = 0
        new_event['Presence leave event true/false ratio'] = len(presence_pred_true_loc) / len(presence_pred_false_loc)

    if (last_true_pred>success_range_start) and (last_true_pred<success_range_end):
        new_event['detection'] = True
        new_event['state'] = 1
    else:
        new_event['detection'] = False
        new_event['state'] = 0
    if (last_true_pred<=success_range_start):
        new_event['detection_gt'] = False
        new_event['detection'] = True
        new_event['state'] = 0


    new_event['Presence last True before False till end of leave event'] = last_true_pred - frame_num_to_remove_at_leave_seq_start

    events = []
    events.append(new_event)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data

