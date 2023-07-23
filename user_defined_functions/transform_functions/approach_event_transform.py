import pandas as pd
import numpy as np

def approach_event_transform(comp_data, **kwargs):
    minimal_active_seq_len = 3
    key = 'User_Movement_Type_gt'
    user_move_type = comp_data[key]
    move_type_mask_approach = np.full(np.shape(user_move_type), False)
    move_type_mask_approach[user_move_type=='Approach_PC']   = True

    activity_pred = comp_data['activity']
    activity_pred_at_approach = activity_pred[move_type_mask_approach==True] #assuming that approach labeling is in a single sequence of consecutive frames

    seq_str_for_search = "1. "*minimal_active_seq_len
    seq_embeded_count = str(np.array(activity_pred_at_approach)).count(seq_str_for_search[:-1])

    # Arrange new_event output format
    approach_indices = np.where(move_type_mask_approach==True)
    if len(approach_indices[0])==0: # No approach sequence exists
        return pd.DataFrame()
    
    new_event = comp_data.iloc[approach_indices[0][0]].to_dict()
    new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
    new_event['end_frame'] = approach_indices[0][-1]
    new_event['frame_id']  = approach_indices[0][0] #start_frame
    
    if seq_embeded_count>0:
        new_event['detection'] = True
        new_event['state'] = 1
    else:
        new_event['detection'] = False
        new_event['state'] = 0

    # Add statistics about the event
    # Length of the activity sequence out of the entire approach event
    new_event['Approach event activity detected percent'] = len(np.where(np.array(activity_pred_at_approach)==1)[0])/len(np.array(activity_pred_at_approach))
    # Length of the sequence of activity=1 within the approach event
    if np.all(np.diff(np.where(np.array(activity_pred_at_approach)==1)[0])):
        new_event['Approach event activity detected length'] = len(np.where(np.array(activity_pred_at_approach)==1)[0]) - (minimal_active_seq_len-1)
    else:
        new_event['Approach event activity detected length'] = len(np.where(np.array(activity_pred_at_approach)==1)[0]) - (minimal_active_seq_len-1)*3
    # Length (in frames) from the first detected sequence to the end of the approach event
    new_event['Active seq duration prior to approach event end'] = np.where(np.array(activity_pred_at_approach)==1)[0][-1]-np.where(np.array(activity_pred_at_approach)==1)[0][0]-(minimal_active_seq_len-1)
    new_event['Active seq duration from approach event start'] = np.where(np.array(activity_pred_at_approach)==1)[0][0] + 1


    events = []
    events.append(new_event)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data

