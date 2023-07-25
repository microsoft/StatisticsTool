import pandas as pd
import numpy as np

def leave_event_transform(comp_data, **kwargs):
    key = 'User_Movement_Type_gt'
    user_move_type = comp_data[key]
    move_type_mask_leave = np.full(np.shape(user_move_type), False)
    move_type_mask_leave[user_move_type=='Leaving_PC']   = True

    activity_pred = comp_data['activity']
    activity_pred_at_leave = activity_pred[move_type_mask_leave==True] #assuming that leaveing labeling is in a single sequence of consecutive frames

    # Arrange new_event output format
    leave_indices = np.where(move_type_mask_leave==True)
    if len(leave_indices[0])==0: # No approach sequence exists
        return pd.DataFrame()
    
    new_event = comp_data.iloc[leave_indices[0][0]].to_dict()
    new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
    new_event['end_frame'] = leave_indices[0][-1]
    new_event['frame_id']  = leave_indices[0][0] #start_frame
    # Currently set all sequences at TP. Once we'll get distance we can add more accurate metrics
    new_event['detection'] = True

    events = []
    events.append(new_event)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data

