import pandas as pd
import numpy as np
def naive_event_transform(comp_data):
    key = 'detection'
    in_event = False
    prediction = comp_data[key]
    label = comp_data[key+'_gt']
    frames = comp_data['frame_id']
    events = []
    new_event = {}
    last_frame=-1
    last_event = None
    for ind, (pred, gt) in enumerate(zip(prediction, label)):
        if pred or gt:
            event = True
        else:
            event = False
        
        if last_event != event:
            last_event = event
            if new_event:
                new_event['end_frame'] = last_frame
                events.append(new_event)
            new_event = comp_data.iloc[ind].to_dict()
            new_event[key]=False
            new_event[key+"_gt"]=False
            
        if pred:
            new_event[key]=True
        if gt:
            new_event[key+'_gt']=True

          
        last_frame = frames[ind]

    new_event['end_frame'] = last_frame
    events.append(new_event)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data

def separate_FN_sequence_transform(comp_data):
    sep_seq_param_len_between_adj      = 5
    sep_seq_param_len_for_single_count = 10
    key = 'detection'
    in_seq_fn = False
    fn_seq_count = 0
    prediction = comp_data[key]
    label = comp_data[key+'_gt']
    frames = comp_data['frame_id']
    events = []
    events_temp = []
    new_event = {}
    for ind, (pred, gt) in enumerate(zip(prediction, label)):
        if pred == False and gt == True: # FN seq
            if in_seq_fn == False: # save seq start
                in_seq_fn = True
                new_event = comp_data.iloc[ind].to_dict()
                new_event[key+'_gt'] = False
                new_event[key]       = True
                new_event['frame_id']  = frames[ind] #start_frame

            fn_seq_count = fn_seq_count + 1
        else: # save seq end
            if in_seq_fn == True:
                in_seq_fn = False
                new_event['end_frame'] = frames[ind]
                new_event['Separate FN sequence length'] = fn_seq_count
                fn_seq_count = 0
                events_temp.append(new_event)

        if ind==(len(prediction)-1) and in_seq_fn==True:
            new_event['end_frame'] = frames[ind]
            new_event['Separate FN sequence length'] = fn_seq_count
            fn_seq_count = 0
            events_temp.append(new_event)

    # Merge of sequences + add count
    event_temp_len = len(events_temp)
    if event_temp_len==0:
        return pd.DataFrame()

    merged_event_point = 0
    merge_on_last_index = False
    if event_temp_len > 1:
        for index in np.arange(event_temp_len): #np.arange(1,event_temp_len)
            if index==0:
                #events.append(events_temp[0])
                s = 4
            else:
                if (events_temp[index]['frame_id'] - events_temp[merged_event_point]['end_frame'])<=sep_seq_param_len_between_adj:
                    # Merge close sequences
                    events_temp[merged_event_point]['end_frame'] = events_temp[index]['end_frame']
                    events_temp[merged_event_point]['Separate FN sequence length'] = events_temp[index]['end_frame']-events_temp[merged_event_point]['frame_id']
                    if (event_temp_len-index)==1:
                        merge_on_last_index = True                    
                else:
                    events.append(events_temp[merged_event_point])
                    merged_event_point = merged_event_point + 1
        if merge_on_last_index:
            events.append(events_temp[merged_event_point])
        else:
            events.append(events_temp[-1])
    else:
        events = events_temp

    for index in np.arange(len(events)):
        events[index]['Separate FN sequence count'] = np.ceil(events[index]['Separate FN sequence length']/sep_seq_param_len_for_single_count)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data

def separate_FP_sequence_transform(comp_data):
    sep_seq_param_len_between_adj      = 5
    sep_seq_param_len_for_single_count = 15
    key = 'detection'
    in_seq_fp = False
    fp_seq_count = 0
    prediction = comp_data[key]
    label = comp_data[key+'_gt']
    frames = comp_data['frame_id']
    events = []
    events_temp = []
    new_event = {}
    for ind, (pred, gt) in enumerate(zip(prediction, label)):
        if pred == True and gt == False: # FP seq
            if in_seq_fp == False: # save seq start
                in_seq_fp = True
                new_event = comp_data.iloc[ind].to_dict()
                new_event[key+'_gt'] = False
                new_event[key]       = True
                new_event['frame_id']  = frames[ind] #start_frame

            fp_seq_count = fp_seq_count + 1
        else: # save seq end
            if in_seq_fp == True:
                in_seq_fp = False
                new_event['end_frame'] = frames[ind]
                new_event['Separate FP sequence length'] = fp_seq_count
                fp_seq_count = 0
                events_temp.append(new_event)

        if ind==(len(prediction)-1) and in_seq_fp==True:
            new_event['end_frame'] = frames[ind]
            new_event['Separate FP sequence length'] = fp_seq_count
            fp_seq_count = 0
            events_temp.append(new_event)

    # Merge of sequences + add count
    event_temp_len = len(events_temp)
    if event_temp_len==0:
        return pd.DataFrame()

    merged_event_point = 0
    merge_on_last_index = False
    if event_temp_len > 1:
        for index in np.arange(1,event_temp_len):
            if (events_temp[index]['frame_id'] - events_temp[merged_event_point]['end_frame'])<=sep_seq_param_len_between_adj:
                # Merge close sequences
                events_temp[merged_event_point]['end_frame'] = events_temp[index]['end_frame']
                events_temp[merged_event_point]['Separate FP sequence length'] = events_temp[index]['end_frame']-events_temp[merged_event_point]['frame_id']
                if (event_temp_len-index)==1:
                    merge_on_last_index = True                    
            else:
                events.append(events_temp[merged_event_point])
                merged_event_point = merged_event_point + 1
        if merge_on_last_index:
            events.append(events_temp[merged_event_point])
        else:
            events.append(events_temp[-1])
    else:
        events = events_temp

    for index in np.arange(len(events)):
        events[index]['Separate FP sequence count'] = np.ceil(events[index]['Separate FP sequence length']/sep_seq_param_len_for_single_count)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data

def approach_event_transform(comp_data):
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

def leave_event_transform(comp_data):
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

def approach_event_presence_transform(comp_data):
    minimal_presence_seq_len = 3
    key = 'User_Status_gt'
    user_move_type = comp_data[key]
    move_type_mask_approach = np.full(np.shape(user_move_type), False)
    move_type_mask_approach[user_move_type=='Approach_PC']   = True

    presence_pred = comp_data['detection']
    presence_pred_at_approach = presence_pred[move_type_mask_approach==True] #assuming that approach labeling is in a single sequence of consecutive frames
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
    
    duration_from_app_end = np.where(np.array(presence_pred_at_approach)==1)[0][-1]-np.where(np.array(presence_pred_at_approach)==1)[0][0]-(minimal_presence_seq_len-1)

    if seq_embeded_count>0 and ((duration_from_app_end/30 >= 1) and (duration_from_app_end/30 < 2)):
        new_event['detection'] = True
        new_event['state'] = 1
    else:
        new_event['detection'] = False
        new_event['state'] = 0
    if (duration_from_app_end/30 >= 2):
        new_event['detection_gt'] = False
        new_event['detection'] = True
        new_event['state'] = 0


    # Add statistics about the event
    # Length of the presence sequence out of the entire approach event
    new_event['Approach event presence detected percent'] = len(np.where(np.array(presence_pred_at_approach)==1)[0])/len(np.array(presence_pred_at_approach))
    # Length of the sequence of presence=1 within the approach event
    if np.all(np.diff(np.where(np.array(presence_pred_at_approach)==1)[0])):
        new_event['Approach event presence detected length'] = len(np.where(np.array(presence_pred_at_approach)==1)[0]) - (minimal_presence_seq_len-1)
    else:
        new_event['Approach event presence detected length'] = len(np.where(np.array(presence_pred_at_approach)==1)[0]) - (minimal_presence_seq_len-1)*3
    # Length (in frames) from the first detected sequence to the end of the approach event
    new_event['Presence seq duration prior to approach event end'] = duration_from_app_end
    new_event['Presence seq duration from approach event start'] = np.where(np.array(presence_pred_at_approach)==1)[0][0] + 1


    events = []
    events.append(new_event)
    transform_data = pd.DataFrame.from_records(events)
    return transform_data

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

def calc_flicker_metrics(bin_vec):
    seq_len_vec = []
    seq_num = 1
    curr_seq_len = 1
    prev = bin_vec[0]
    for curr in bin_vec[1:]:
        if prev==curr:
            curr_seq_len = curr_seq_len + 1
        else:
            seq_num = seq_num + 1
            seq_len_vec.append(curr_seq_len)
            curr_seq_len = 1
        prev = curr
    
    # Handle last sequence
    if curr_seq_len>1:
        seq_len_vec.append(curr_seq_len)

    avg_seq_len = np.mean(seq_len_vec)
    med_seq_len = np.median(seq_len_vec)

    return seq_num, avg_seq_len, med_seq_len
