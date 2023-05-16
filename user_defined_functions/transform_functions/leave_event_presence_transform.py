import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt

def leave_event_presence_transform(comp_data):
    lock_event_width_in_frames = 60
    Wake_event_width_in_frames = 60
    max_delta_of_late_detection = 60
    is_plot = True

    user_move_type = comp_data['User_Status_gt']
    presence_pred = np.array(comp_data['detection'])
    system_context = comp_data['System_Context_gt']
    wake_events = np.array(comp_data['Is_Wake_event_gt'])
    lock_events = np.array(comp_data['Is_Lock_event_gt'])

    last_valid_frame = len(lock_events)

    for frame_index, w in enumerate(lock_events):
        if type(w) != str:
            last_valid_frame = frame_index
            break

    wake_events = wake_events[:last_valid_frame]
    lock_events = lock_events[:last_valid_frame]
    presence_pred = presence_pred[:last_valid_frame]

    wake_events = [1*eval(w) for w in list(wake_events)]
    lock_events = [1*eval(l) for l in list(lock_events)]
    presence_pred = [1*p for p in presence_pred]


    lock_pred_start_end = []
    lock_gt_start_end = []
    lock_signal = np.zeros(len(presence_pred))
    wake_signal = np.zeros(len(presence_pred))
    wake_gt = 0 if wake_events[0] == 0 else 1
    lock_gt = 0 if lock_events[0] == 0 else 1
    is_leave_event_at_end_of_film = False
    for frame in range(1, len(presence_pred)):
        if presence_pred[frame-1] and not presence_pred[frame]:
            if frame < (len(lock_signal) - lock_event_width_in_frames):
                lock_signal[frame: frame + lock_event_width_in_frames] = 1
                lock_pred_start_end.append([frame, frame + lock_event_width_in_frames])
            else:
                lock_signal[frame: ] = 1
                lock_pred_start_end.append([frame, len(presence_pred) - 1])
        if not lock_gt and lock_events[frame]:
            lock_gt_start_end.append([frame, -1])
            lock_gt = 1
        if lock_gt and not lock_events[frame]:
            if len(lock_gt_start_end) > 0:
                lock_gt_start_end[len(lock_gt_start_end) - 1][1] = frame - 1
            else:
                lock_gt_start_end.append([0, frame - 1])
            lock_gt = 0
    if lock_gt:
        lock_gt_start_end[len(lock_gt_start_end) - 1][1] = frame
        is_leave_event_at_end_of_film = True

    Lock_TP = 0
    Lock_FP = 0
    Lock_FN = 0

    Lock_TP_start_end_frame = []
    Lock_FP_start_end_frame = []
    Lock_FN_start_end_frame = []
    
    for pred_event in lock_pred_start_end:
        is_found_overlap_event = False
        distance = []
        for gt_event in lock_gt_start_end:
            overlap = np.intersect1d(range(pred_event[0], pred_event[1]), range(gt_event[0], gt_event[1]))
            distance.append([pred_event[0] - gt_event[1], gt_event[0] - pred_event[1]])
            if len(overlap) > 0:
                is_found_overlap_event = True
                start_ = gt_event[0]
                end_ = gt_event[1]
                break
        if is_found_overlap_event:
            continue
        else:
            if len(distance) > 0:
                global_minimum = 1e6
                fp = False
                fn = False
                start_ = -1
                end_ = -1
                for dist in distance:
                    if dist[0] > 0:
                        dist_ = dist[0]
                        if dist_ < global_minimum:
                            global_minimum = dist_
                            if dist_ < max_delta_of_late_detection:
                                fn = True
                                fp = False
                            else:
                                fn = False
                                fp = True
                    else:
                        dist_ = dist[1]
                        if dist_ < global_minimum:
                            global_minimum = dist_
                            fn = False
                            fp = True
                
                if fp:
                    Lock_FP += 1
                    Lock_FP_start_end_frame.append([pred_event[0], pred_event[1]])
                if fn:
                    Lock_FN += 1
                    Lock_FN_start_end_frame.append([pred_event[0], pred_event[1]])
            else:
                Lock_FP += 1
                Lock_FP_start_end_frame.append([pred_event[0], pred_event[1]])

    for gt_event in lock_gt_start_end:
        is_found_overlap_event = False
        distance = []
        for pred_event in lock_pred_start_end:
            overlap = np.intersect1d(range(pred_event[0], pred_event[1]), range(gt_event[0], gt_event[1]))
            distance.append([pred_event[0] - gt_event[1], gt_event[0] - pred_event[1]])
            if len(overlap) > 0:
                is_found_overlap_event = True
                break
        if is_found_overlap_event:
            Lock_TP += 1
            Lock_TP_start_end_frame.append([gt_event[0], gt_event[1]])
        else:
            Lock_FN += 1
            Lock_FN_start_end_frame.append([gt_event[0], gt_event[1]])
                
    events = []
    for event in range(Lock_TP):
        new_event = comp_data.iloc[Lock_TP_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = Lock_TP_start_end_frame[event][1]
        new_event['frame_id']  = Lock_TP_start_end_frame[event][0] #start_frame
        new_event['detection'] = True
        new_event['state'] = 1
        new_event['Is_leave_at_end_of_film'] = is_leave_event_at_end_of_film
        events.append(new_event)
    for event in range(Lock_FP):
        new_event = comp_data.iloc[Lock_FP_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = False #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = Lock_FP_start_end_frame[event][1]
        new_event['frame_id']  = Lock_FP_start_end_frame[event][0] #start_frame
        new_event['detection'] = True
        new_event['state'] = 0
        new_event['Is_leave_at_end_of_film'] = is_leave_event_at_end_of_film
        events.append(new_event)
    for event in range(Lock_FN):
        new_event = comp_data.iloc[Lock_FN_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = Lock_FN_start_end_frame[event][1]
        new_event['frame_id']  = Lock_FN_start_end_frame[event][0] #start_frame
        new_event['detection'] = False
        new_event['state'] = 1
        new_event['Is_leave_at_end_of_film'] = is_leave_event_at_end_of_film
        events.append(new_event)

    if is_plot:
        path_to_Save = r'C:\Work\statistic_tool_debug_work\Lock_leave_analysis'
        if not os.path.exists(path_to_Save):
            os.makedirs(path_to_Save)
        plt.figure()
        plt.plot(lock_events)
        plt.plot(lock_signal)
        plt.legend(['gt events', 'predictions events'])
        plt.title(['Lock TP: ' + str(Lock_TP), 'Lock FP: ' + str(Lock_FP), 'Lock FN: ' + str(Lock_FN)])
        fig_name = os.path.basename(comp_data.video[0])[:-len('.mp4')] + ".png"
        plt.savefig(os.path.join(path_to_Save, fig_name))
        plt.close()

    transform_data = pd.DataFrame.from_records(events)
    return transform_data

