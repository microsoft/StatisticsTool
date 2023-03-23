def determine_approach_success_mask(comp_data):
    # Parameters
    time_or_distance_based = "time"
    internal_fps = 30
    R0_time = 1 #sec from pivot
    R1_time = 2 #sec from pivot
    R0_distance = 1.3
    R1_distance = 1.7
    time_for_pop_up_detection = 0.5 #sec

    # Inits
    approach_success_mask = np.full((len(comp_data),1), False)
    pop_up_indication  = False
    pop_up_indication2 = False
    pop_up_reason_ind  = 0
    pop_up_reason_ind2 = 0
    multi_seq = False

    # Program
    user_status_label = comp_data['User_Status_gt']
    approach_ind     = np.where(user_status_label=='Approach_PC')[0]
    sitting_down_ind = np.where(user_status_label=='Sitting_Down')[0]

    # In case of more than a single approach sequence (currently handles only first sequence)
    seperator_app = np.where((np.diff(approach_ind)==1)==False)
    seperator_sit = np.where((np.diff(sitting_down_ind)==1)==False)
    if len(seperator_app[0])>0:
        if len(seperator_app[0])>1: # Doesn't support more than 2 approach sequences
            return approach_success_mask, multi_seq, pop_up_indication, pop_up_indication2, pop_up_reason_ind, pop_up_reason_ind2
        multi_seq = True
        approach_ind2 = approach_ind[(seperator_app[0][0]+1):]
        approach_ind  = approach_ind[0:(seperator_app[0][0]+1)]
        if len(seperator_sit[0])>0:
            sitting_down_ind2 = sitting_down_ind[(seperator_sit[0][0]+1):]
            sitting_down_ind  = sitting_down_ind[0:(seperator_sit[0][0]+1)]
        else:
            sitting_down_ind2 = []
    

    if time_or_distance_based=="time":
        if len(approach_ind)>0:
            pivot_frame = approach_ind[-1]
            if multi_seq==True:
                pivot_frame2 = approach_ind2[-1]
        elif len(sitting_down_ind)>0:
            pivot_frame = sitting_down_ind[0]
        else: # no approach/sitting down in video
            return approach_success_mask, multi_seq, pop_up_indication, pop_up_indication2, pop_up_reason_ind, pop_up_reason_ind2

        R0_frames_ind = np.arange(pivot_frame - R0_time*internal_fps, pivot_frame)
        R1_frames_ind = np.arange(pivot_frame - R1_time*internal_fps, pivot_frame - R0_time*internal_fps)
        if multi_seq==True:
            R0_frames_ind2 = np.arange(pivot_frame2 - R0_time*internal_fps, pivot_frame2)
            R1_frames_ind2 = np.arange(pivot_frame2 - R1_time*internal_fps, pivot_frame2 - R0_time*internal_fps)

    elif time_or_distance_based=="distance":
        # Extract distance (after completion of missing frames due to missing face BB + smoothing)
        distance = 4
        R0_frames_ind = np.where(distance < R0_distance)
        R1_frames_ind = np.intersect1d(np.where(distance < R1_distance),np.where(distance >= R0_distance))

    R0 = np.full((len(comp_data),1), False)
    R1 = np.full((len(comp_data),1), False)
    R0[R0_frames_ind] = True
    R1[R1_frames_ind] = True
    if multi_seq==True:
        R0[R0_frames_ind2] = True
        R1[R1_frames_ind2] = True

    # options for event to be pop-up
    #   1. No 'approach_PC' labels + 'sitting_down' label exists
    #   2. First 'appraoch_PC' frame is in R0
    #   3. First 'approach_PC' frame is less than time_for_pop_up_detection sec from the last frame of R1
    if (len(approach_ind)==0) or (approach_ind[0] in R0_frames_ind) or (R0_frames_ind[0] - approach_ind[0] < time_for_pop_up_detection*internal_fps): 
        pop_up_indication = True
        if (len(approach_ind)==0):
            pop_up_reason = "No approach labels"
            pop_up_reason_ind = 1
        elif (approach_ind[0] in R0_frames_ind):
            pop_up_reason = "First approach label is in R0"
            pop_up_reason_ind = 2
        elif (R0_frames_ind[0] - approach_ind[0] < time_for_pop_up_detection*internal_fps):
            pop_up_reason = "First approach label is in R1 with short duration for detection"
            pop_up_reason_ind = 3

    if multi_seq==True:
        if (len(approach_ind2)==0) or (approach_ind2[0] in R0_frames_ind2) or (R0_frames_ind2[0] - approach_ind2[0] < time_for_pop_up_detection*internal_fps): 
            pop_up_indication2 = True
            if (len(approach_ind2)==0):
                pop_up_reason2 = "No approach labels"
                pop_up_reason_ind2 = 1
            elif (approach_ind2[0] in R0_frames_ind2):
                pop_up_reason2 = "First approach label is in R0"
                pop_up_reason_ind2 = 2
            elif (R0_frames_ind2[0] - approach_ind2[0] < time_for_pop_up_detection*internal_fps):
                pop_up_reason2 = "First approach label is in R1 with short duration for detection"        
                pop_up_reason_ind2 = 3

    if pop_up_indication == True:
        if len(approach_ind) > 0:
            first_ind_for_mask = approach_ind[0]
        else: # in case of no approach and no sitting down, we exited the function earlier
            first_ind_for_mask = sitting_down_ind[0]
        last_ind_for_mask = first_ind_for_mask + int(time_for_pop_up_detection*internal_fps)
    else: # regular approach
        last_ind_for_mask = R1_frames_ind[-1]
        first_ind_for_mask = max(approach_ind[0],R1_frames_ind[0])

    if multi_seq==True:
        if pop_up_indication2 == True:
            if len(approach_ind2) > 0:
                first_ind_for_mask2 = approach_ind2[0]
            else: # in case of no approach and no sitting down, we exited the function earlier
                first_ind_for_mask2 = sitting_down_ind2[0]
            last_ind_for_mask2 = first_ind_for_mask2 + int(time_for_pop_up_detection*internal_fps)
        else: # regular approach
            last_ind_for_mask2 = R1_frames_ind2[-1]
            first_ind_for_mask2 = max(approach_ind2[0],R1_frames_ind2[0])


    approach_success_mask[first_ind_for_mask:last_ind_for_mask] = True
    if multi_seq==True:
        approach_success_mask[first_ind_for_mask2:last_ind_for_mask2] = True
    
    # Visualization
    if 0: #multi_seq==True: 
        if len(sitting_down_ind)==0:
            last_for_disp = approach_ind[-1] + 10
        else:
            last_for_disp = sitting_down_ind[-1] + 10
        if multi_seq==True:
            if len(sitting_down_ind2)==0:
                last_for_disp = approach_ind2[-1] + 10
            else:
                last_for_disp = sitting_down_ind2[-1] + 10

        import plotly.express as px
        import plotly.graph_objects as go
        fig = go.Figure()
        trace1= px.line(approach_success_mask[0:last_for_disp]*3)
        trace1.data[0].name = 'Approach Success Mask'
        trace1.data[0].line = { 'color': "red", 'dash': 'solid'}
        trace2 = px.line((user_status_label=='Approach_PC')[0:last_for_disp]*1.75)
        trace2.data[0].name = 'Approach PC labels'
        trace2.data[0].line = { 'color': "green", 'dash': 'solid'}
        trace3 = px.line((user_status_label=='Sitting_Down')[0:last_for_disp]*2)
        trace3.data[0].name = 'Sitting Down labels'
        trace3.data[0].line = { 'color': "blue", 'dash': 'solid'}
        trace4 = px.line(R0[0:last_for_disp]*1.2)
        trace4.data[0].name = 'R0 range'
        trace4.data[0].line = { 'color': "black", 'dash': 'solid'}
        trace5 = px.line(R1[0:last_for_disp]*1.1)
        trace5.data[0].name = 'R1 range'
        trace5.data[0].line = { 'color': "cyan", 'dash': 'solid'}


        fig.add_trace(trace1.data[0])
        fig.add_trace(trace2.data[0])
        fig.add_trace(trace3.data[0])
        fig.add_trace(trace4.data[0])
        fig.add_trace(trace5.data[0])
        if pop_up_indication == True:
            fig.update_layout(title="Video areas - Pop Up Approach. Reason = "+pop_up_reason,xaxis_title="Frames")
        else:
            fig.update_layout(title="Video areas - Regular Approach",xaxis_title="Frames")
        if multi_seq==True:
            if (pop_up_indication == True) and (pop_up_indication2 == True):
                fig.update_layout(title="Video areas - [First] Pop Up Approach. Reason = "+pop_up_reason+", [Second] Pop Up Approach. Reason = "+pop_up_reason2,xaxis_title="Frames")
            elif (pop_up_indication == True) and (pop_up_indication2 == False):
                fig.update_layout(title="Video areas - [First] Pop Up Approach. Reason = "+pop_up_reason+", [Second] Regular Approach",xaxis_title="Frames")
            elif (pop_up_indication == False) and (pop_up_indication2 == True):
                fig.update_layout(title="Video areas - [First] Regular Approach, [Second] Pop Up Approach. Reason = "+pop_up_reason2,xaxis_title="Frames")
            else: 
                fig.update_layout(title="Video areas - [First] Regular Approach, [Second] Regular Approach",xaxis_title="Frames")

        fig.show()
        s = 4


    return approach_success_mask, multi_seq, pop_up_indication, pop_up_indication2, pop_up_reason_ind, pop_up_reason_ind2