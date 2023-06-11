import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt

def check_if_bb_is_on_the_edge_or_no_face(res_edge_x, res_edge_y, bb_left, bb_top, bb_width, bb_height):
        # nan_frames = (np.isnan(bb_left) | (bb_left == None))
        nan_frames = len(bb_left) * [False]
        for f in range(len(bb_left)):
            if type(bb_left[f]) is not list:
                try:
                    if np.isnan(bb_left[f]) or bb_left[f] is None:
                        nan_frames[f] = True
                except:
                    if list(bb_left)[f] is None:
                        nan_frames[f] = True
        is_on_edge = False
        is_no_face = False
        if np.sum(nan_frames) == len(nan_frames):
            is_no_face = True
        edge_tolerace_in_pixels = 10
        for frame in range(len(bb_left)):
            if nan_frames[frame]:
                continue
            else:
                if type(bb_left[frame]) is not list:
                    if bb_left[frame] < edge_tolerace_in_pixels or (res_edge_x - (bb_left[frame] + bb_width[frame])) < edge_tolerace_in_pixels:
                        is_on_edge = True
                    if bb_top[frame] < edge_tolerace_in_pixels or (res_edge_y - (bb_top[frame] + bb_height[frame])) < edge_tolerace_in_pixels:
                        is_on_edge = True
                else:
                    for b_ in range(len(bb_left[frame])):
                        if bb_left[frame][b_] < edge_tolerace_in_pixels or (res_edge_x - (bb_left[frame][b_] + bb_width[frame][b_])) < edge_tolerace_in_pixels:
                            is_on_edge = True
                        if bb_top[frame][b_] < edge_tolerace_in_pixels or (res_edge_y - (bb_top[frame][b_] + bb_height[frame][b_])) < edge_tolerace_in_pixels:
                            is_on_edge = True
        return is_on_edge, is_no_face

def leave_event_presence_transform(comp_data):
    lock_event_width_in_frames = 150
    Wake_event_width_in_frames = 60
    max_delta_of_late_detection = 60
    is_plot = True

    user_move_type = comp_data['User_Status_gt']
    presence_pred = np.array(comp_data['detection'])
    system_context = comp_data['System_Context_gt']
    wake_events = np.array(comp_data['Is_Wake_event_gt'])
    lock_events = np.array(comp_data['Is_Lock_event_gt'])
    frame_id = np.array(comp_data['frame_id'])

    try:
        fps_original_video = int(comp_data['fps_original_video'][0])
        fps_golden = int(comp_data['fps_golden'][0])
    except:
        try:
            fps_original_video = int(comp_data['fps_original_video_gt'][0])
            fps_golden = int(comp_data['fps_golden_gt'][0])
        except:
            fps_original_video = 30
            fps_golden = 30


    fps_ratio = fps_golden / fps_original_video

    lock_event_width_in_frames = int(lock_event_width_in_frames * fps_ratio)
    Wake_event_width_in_frames = int(Wake_event_width_in_frames * fps_ratio)

    last_valid_frame = len(lock_events)

    for frame_index, w in enumerate(lock_events):
        if type(w) != str:
            last_valid_frame = frame_index
            break

    wake_events = wake_events[:last_valid_frame]
    lock_events = lock_events[:last_valid_frame]
    presence_pred = presence_pred[:last_valid_frame]
    frame_id = frame_id[:last_valid_frame]

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

    if len(lock_pred_start_end) > 1:
        lock_pred_start_end_ = []
        last_item_can_be_merged = True
        for pred_event_ind in range(len(lock_pred_start_end) - 1):
            if lock_pred_start_end[pred_event_ind][1] > lock_pred_start_end[pred_event_ind + 1][0]:
                lock_pred_start_end_.append([lock_pred_start_end[pred_event_ind][0], lock_pred_start_end[pred_event_ind + 1][1]])
                last_item_can_be_merged = False
            else:
                if last_item_can_be_merged:
                    lock_pred_start_end_.append(lock_pred_start_end[pred_event_ind])
                last_item_can_be_merged = True
        if last_item_can_be_merged:
            lock_pred_start_end_.append(lock_pred_start_end[-1])

        lock_pred_start_end = lock_pred_start_end_
    
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
            if np.sum(presence_pred[gt_event[0] : gt_event[1]]) > 0:
                Lock_FN += 1
                Lock_FN_start_end_frame.append([gt_event[0], gt_event[1]])
                
    events = []
    res_edge_x = comp_data['frames_size_detection_gt'][0][0]
    res_edge_y = comp_data['frames_size_detection_gt'][0][1]
    user_status = np.array(comp_data['User_Status_gt'])
    try:
        bb_left = np.array(comp_data['Left_gt'])
        bb_top = np.array(comp_data['Top_gt'])
        bb_width = np.array(comp_data['Width_gt'])
        bb_height = np.array(comp_data['Height_gt'])
    except:
        nan_array = np.array(len(comp_data) * [None])
        bb_left = nan_array
        bb_top = nan_array
        bb_width = nan_array
        bb_height = nan_array
    for ind in range(len(bb_left)):
        if type(bb_left[ind]) is list:
            if len(bb_left[ind]) == 0:
                bb_left[ind] = None
                bb_top[ind] = None
                bb_width[ind] = None
                bb_height[ind] = None
    for event in range(Lock_TP):
        frames_range = range(Lock_TP_start_end_frame[event][0], Lock_TP_start_end_frame[event][1])
        is_on_edge, is_no_face = check_if_bb_is_on_the_edge_or_no_face(res_edge_x, res_edge_y, bb_left[frames_range], bb_top[frames_range], bb_width[frames_range], bb_height[frames_range])
        is_user_working = True if np.unique(user_status[frames_range])[0] == 'OnPC_Working' else False
        new_event = comp_data.iloc[Lock_TP_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = frame_id[Lock_TP_start_end_frame[event][1]]
        new_event['frame_id']  = frame_id[Lock_TP_start_end_frame[event][0]] #start_frame
        new_event['detection'] = True
        new_event['state'] = 1
        new_event['is_on_edge'] = is_on_edge
        new_event['is_no_face'] = is_no_face
        new_event['is_user_working'] = is_user_working
        new_event['Is_leave_at_end_of_film'] = True if frame_id[Lock_TP_start_end_frame[event][1]] >= frame_id[-1] else False
        events.append(new_event)
    for event in range(Lock_FP):
        frames_range = range(Lock_FP_start_end_frame[event][0], Lock_FP_start_end_frame[event][1])
        is_on_edge, is_no_face = check_if_bb_is_on_the_edge_or_no_face(res_edge_x, res_edge_y, bb_left[frames_range], bb_top[frames_range], bb_width[frames_range], bb_height[frames_range])
        is_user_working = True if np.unique(user_status[frames_range])[0] == 'OnPC_Working' else False
        new_event = comp_data.iloc[Lock_FP_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = False #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = frame_id[Lock_FP_start_end_frame[event][1]]
        new_event['frame_id']  = frame_id[Lock_FP_start_end_frame[event][0]] #start_frame
        new_event['detection'] = True
        new_event['state'] = 0
        new_event['is_on_edge'] = is_on_edge
        new_event['is_no_face'] = is_no_face
        new_event['is_user_working'] = is_user_working
        new_event['Is_leave_at_end_of_film'] = True if frame_id[Lock_FP_start_end_frame[event][1]] >= frame_id[-1] else False
        events.append(new_event)
    for event in range(Lock_FN):
        frames_range = range(Lock_FN_start_end_frame[event][0], Lock_FN_start_end_frame[event][1])
        is_on_edge, is_no_face = check_if_bb_is_on_the_edge_or_no_face(res_edge_x, res_edge_y, bb_left[frames_range], bb_top[frames_range], bb_width[frames_range], bb_height[frames_range])
        is_user_working = True if np.unique(user_status[frames_range])[0] == 'OnPC_Working' else False
        new_event = comp_data.iloc[Lock_FN_start_end_frame[event][0]].to_dict()
        new_event['detection_gt'] = True #setting event GT to True at all time. Only TP and FN are possible
        new_event['end_frame'] = frame_id[Lock_FN_start_end_frame[event][1]]
        new_event['frame_id']  = frame_id[Lock_FN_start_end_frame[event][0]] #start_frame
        new_event['detection'] = False
        new_event['state'] = 1
        new_event['is_on_edge'] = is_on_edge
        new_event['is_no_face'] = is_no_face
        new_event['is_user_working'] = is_user_working
        new_event['Is_leave_at_end_of_film'] = True if frame_id[Lock_FN_start_end_frame[event][1]] >= frame_id[-1] else False
        events.append(new_event)

    if is_plot:
        path_to_Save = r'C:\Work\statistic_tool_debug_work\Lock_leave_analysis'
        if not os.path.exists(path_to_Save):
            os.makedirs(path_to_Save)
        plt.figure()
        plt.plot(frame_id, lock_events)
        plt.plot(frame_id, lock_signal)
        plt.legend(['gt events', 'predictions events'])
        plt.title(['Lock TP: ' + str(Lock_TP), 'Lock FP: ' + str(Lock_FP), 'Lock FN: ' + str(Lock_FN)])
        fig_name = os.path.basename(comp_data.video[0])[:-len('.mp4')] + ".png"
        plt.savefig(os.path.join(path_to_Save, fig_name))
        plt.close()

    transform_data = pd.DataFrame.from_records(events)
    return transform_data

