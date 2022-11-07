import pandas as pd
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