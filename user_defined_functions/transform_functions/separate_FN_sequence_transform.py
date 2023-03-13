import pandas as pd
import numpy as np

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

