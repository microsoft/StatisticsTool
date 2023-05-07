import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt

def approach_event_presence_transform(comp_data):

    lock_event_width_in_frames = 30
    Wake_event_width_in_frames = 60
    max_delta_of_late_detection = 60
    is_plot = True

    presence_pred = np.array(comp_data['detection'])
    system_context = np.array(comp_data['System_Context_gt'])
    wake_events = np.array(comp_data['Is_Wake_event_gt'])
    lock_events = np.array(comp_data['Is_Lock_event_gt'])
   
    last_valid_frame = len(wake_events)
    for frame_index, w in enumerate(wake_events):
        if type(w) != str:
            last_valid_frame = frame_index
            break

    wake_events = wake_events[:last_valid_frame]
    lock_events = lock_events[:last_valid_frame]
    presence_pred = presence_pred[:last_valid_frame]
    system_context = system_context[:last_valid_frame]


    wake_events = [1*eval(w) for w in list(wake_events)]
    lock_events = [1*eval(l) for l in list(lock_events)]
    presence_pred = [1*p for p in presence_pred]
    system_context = [1 if sys == 'Scan_for_lock' else 0 for sys in system_context]


    wake_pred_start_end = []
    wake_gt_start_end = []
    lock_pred_start_end = []
    lock_signal = np.zeros(len(presence_pred))
    wake_signal = np.zeros(len(presence_pred))
    wake_gt = 0 if wake_events[0] == 0 else 1
    for frame in range(1, len(presence_pred)):
        if presence_pred[frame-1] and not presence_pred[frame]:
            if frame < (len(lock_signal) - lock_event_width_in_frames):
                if np.sum(presence_pred[frame: frame + lock_event_width_in_frames]) == 0:
                    lock_signal[frame: frame + lock_event_width_in_frames] = 1
                    lock_pred_start_end.append([frame, frame + lock_event_width_in_frames])
                else:
                    last_ind_before_next_wake = np.where(np.array(presence_pred[frame: frame + lock_event_width_in_frames]) == 1)[0][0]
                    lock_signal[frame: frame + lock_event_width_in_frames - last_ind_before_next_wake - 2] = 1
                    lock_pred_start_end.append([frame, frame + lock_event_width_in_frames - last_ind_before_next_wake - 2])
            else:
                if np.sum(presence_pred[frame:]) == 0:
                    lock_signal[frame: ] = 1
                    lock_pred_start_end.append([frame, len(presence_pred) - 1])
                else:
                    last_ind_before_next_wake = np.where(np.array(presence_pred[frame:]) == 1)[0][0]
                    lock_signal[frame: last_ind_before_next_wake - 2] = 1
                    lock_pred_start_end.append([frame, last_ind_before_next_wake - 2])
        if presence_pred[frame] and not presence_pred[frame - 1]:
            if frame >= int(Wake_event_width_in_frames / 2) and frame < (len(wake_signal) - int(Wake_event_width_in_frames / 2)):
                if np.sum(presence_pred[frame - int(Wake_event_width_in_frames): frame]) == 0:
                    wake_signal[frame - int(Wake_event_width_in_frames / 2) : frame + int(Wake_event_width_in_frames / 2)] = 1
                    wake_pred_start_end.append([frame - int(Wake_event_width_in_frames / 2), frame + int(Wake_event_width_in_frames / 2)])
                else:
                    wake_signal[frame  : frame + int(Wake_event_width_in_frames / 2)] = 1
                    wake_pred_start_end.append([frame , frame + int(Wake_event_width_in_frames / 2)])
            else:
                if frame < int(Wake_event_width_in_frames / 2):
                    wake_signal[: frame + int(Wake_event_width_in_frames / 2)] = 1
                    wake_pred_start_end.append([0, frame + int(Wake_event_width_in_frames / 2)])
                else:
                    wake_signal[frame - int(Wake_event_width_in_frames / 2) :] = 1
                    wake_pred_start_end.append([frame - int(Wake_event_width_in_frames / 2), len(presence_pred) - 1])
        if not wake_gt and wake_events[frame]:
            wake_gt_start_end.append([frame, -1])
            wake_gt = 1
        if wake_gt and not wake_events[frame]:
            if len(wake_gt_start_end) > 0:
                wake_gt_start_end[len(wake_gt_start_end) - 1][1] = frame - 1
            else:
                wake_gt_start_end.append([0, frame - 1])
            wake_gt = 0
        


    Wake_TP = 0
    Wake_FP = 0
    Wake_FN = 0

    Wake_TP_start_end_frame = []
    Wake_FP_start_end_frame = []
    Wake_FN_start_end_frame = []
    
    for pred_event in wake_pred_start_end:
        is_found_overlap_event = False
        distance = []
        for gt_event in wake_gt_start_end:
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
            if system_context[pred_event[0]] == 0:
                # fp = True
                # fn = False

                Wake_FP += 1
                Wake_FP_start_end_frame.append([pred_event[0], pred_event[1]])
            # if len(distance) > 0:
            #     global_minimum = 1e6
            #     fp = False
            #     fn = False
            #     start_ = -1
            #     end_ = -1
            #     for dist in distance:
            #         if dist[0] > 0:
            #             dist_ = dist[0]
            #             if dist_ < global_minimum:
            #                 global_minimum = dist_
            #                 # if dist_ < max_delta_of_late_detection:
            #                 #     fn = True
            #                 #     fp = False
            #                 # else:
            #                 #     fn = False
            #                 #     fp = True
            #                 fn = True
            #                 fp = False
            #         else:
            #             dist_ = dist[1]
            #             if dist_ < global_minimum:
            #                 global_minimum = dist_
            #                 fn = False
            #                 fp = True
                
            # if fp:
            #     Wake_FP += 1
            #     Wake_FP_start_end_frame.append([pred_event[0], pred_event[1]])
            # if fn:
            #     Wake_FN += 1
            #     Wake_FN_start_end_frame.append([pred_event[0], pred_event[1]])
            # else:
            #     Wake_FP += 1
            #     Wake_FP_start_end_frame.append([pred_event[0], pred_event[1]])

    for gt_event in wake_gt_start_end:
        is_found_overlap_event = False
        distance = []
        for pred_event in wake_pred_start_end:
            overlap = np.intersect1d(range(pred_event[0], pred_event[1]), range(gt_event[0], gt_event[1]))
            distance.append([pred_event[0] - gt_event[1], gt_event[0] - pred_event[1]])
            if len(overlap) > 0:
                is_found_overlap_event = True
                break
        if is_found_overlap_event:
            Wake_TP += 1
            Wake_TP_start_end_frame.append([gt_event[0], gt_event[1]])
        else:
            if np.sum(presence_pred[gt_event[0] : gt_event[1]]) == 0:
                Wake_FN += 1
                Wake_FN_start_end_frame.append([gt_event[0], gt_event[1]])
    events = []
    for event in range(Wake_TP):
        new_event = comp_data.iloc[Wake_TP_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = Wake_TP_start_end_frame[event][1]
        new_event['frame_id']  = Wake_TP_start_end_frame[event][0] #start_frame
        new_event['detection'] = True
        new_event['state'] = 1
        events.append(new_event)
    for event in range(Wake_FP):
        new_event = comp_data.iloc[Wake_FP_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = False #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = Wake_FP_start_end_frame[event][1]
        new_event['frame_id']  = Wake_FP_start_end_frame[event][0] #start_frame
        new_event['detection'] = True
        new_event['state'] = 0
        events.append(new_event)
    for event in range(Wake_FN):
        new_event = comp_data.iloc[Wake_FN_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = Wake_FN_start_end_frame[event][1]
        new_event['frame_id']  = Wake_FN_start_end_frame[event][0] #start_frame
        new_event['detection'] = False
        new_event['state'] = 1
        events.append(new_event)

    if is_plot:
        path_to_Save = r'C:\Work\statistic_tool_debug_work\Wake_approach_analysis'
        if not os.path.exists(path_to_Save):
            os.makedirs(path_to_Save)
        plt.figure()
        plt.plot(wake_events)
        plt.plot(wake_signal)
        plt.plot(lock_events)
        plt.plot(lock_signal)
        plt.legend(['gt wake events', 'predictions wake events', 'gt lock events', 'predictions lock events'])
        plt.title(['Wake TP: ' + str(Wake_TP), 'Wake FP: ' + str(Wake_FP), 'Wake FN: ' + str(Wake_FN)])
        fig_name = os.path.basename(comp_data.video[0])[:-len('.mp4')] + ".png"
        plt.savefig(os.path.join(path_to_Save, fig_name))
        plt.close()

    transform_data = pd.DataFrame.from_records(events)
    return transform_data