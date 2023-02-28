import numpy as np

"""
Partitioning Function instructions:
------------------------------
Input:
a. prdediction dataframe (after the modifications of the Reading function)
b. label dataframe (after the modifications of the Reading function)
c. from_file, boolean that indicates weather the dataframe was loaded (to manage type of variable)

A Reading function:

1. The high-level dictionary returned should be of the form:
{'Partition Name': Partition Dictionary}

2. The lower level "Partition Dictionary" should be of the form:
{'possible partitions': ['option 1', 'option 2', ..., 'option n'],
 'prediction masks': [predictions boolean mask for option 1, predictions boolean mask for option 2, ..., predictions boolean mask for option n],
 'labels masks': [labels boolean mask for option 1, labels boolean mask for option 2, ..., labels boolean mask for option n]}
 
Notice: the predictions boolean masks should match the boolean data frame (same for labels)
 
Notice 2: its not allowed to use the same option name for different partitions:
    for example a 'Partitions Name' = 'Time of day' will have the 'possible partitions': 'night' and 'day'
    if we use another 'Partitions Name', for example 'vehicle',
    we cant use 'night' or 'day' as 'possible partitions' this will mess up the software
    to make sure it doesnt happen an assertion was added to the examples bellow.
 
Returns:
The high-level dictionary which contains at least one Partition Dictionary
"""

def activity_partition(dataframe, from_file=False):
    multiple = dataframe['Multiple People_gt'].values.astype(object)
    relevant = dataframe['relevant_gt'].values.astype(object)
    static = dataframe['static_gt'].values.astype(object)
    activity = dataframe['activity_gt'].values.astype(object)

    if "User_Movement_Type_gt" in dataframe.columns:
        user_phy_status = dataframe['User_Physical_Status_gt'].values.astype(object)
        user_move_type = dataframe['User_Movement_Type_gt'].values.astype(object)

        user_phy_stat_mask = np.full(np.shape(user_phy_status), False)
        user_phy_stat_mask[user_phy_status=='Moving '] = True #Sitting/Standing/Laying/Moving/NA

        move_type_mask_approach = np.full(np.shape(user_move_type), False)
        move_type_mask_leave    = np.full(np.shape(user_move_type), False)
        move_type_mask_walk     = np.full(np.shape(user_move_type), False)
        move_type_mask_stand_up_sit_down = np.full(np.shape(user_move_type), False)
        move_type_mask_other    = np.full(np.shape(user_move_type), True)
        
        move_type_mask_approach[user_move_type=='Approach_PC']   = True
        move_type_mask_leave[user_move_type=='Leaving_PC']       = True
        move_type_mask_walk[user_move_type=='Walking_Unrelated'] = True
        move_type_mask_stand_up_sit_down[user_move_type=='Standing_Up']  = True
        move_type_mask_stand_up_sit_down[user_move_type=='Sitting_Down'] = True
        move_type_mask_other[user_move_type=='Approach_PC'] = False
        move_type_mask_other[user_move_type=='Leaving_PC'] = False
        move_type_mask_other[user_move_type=='Walking_Unrelated'] = False
        move_type_mask_other[user_move_type=='Standing_Up'] = False
        move_type_mask_other[user_move_type=='Sitting_Down'] = False

        approach_mask=np.full(np.shape(user_move_type), False)
        approach_mask[user_move_type=='Approach_PC'] = True #Approach_PC/Leaving_PC/Standing_Up/Sitting_Down/Walking_Unrelated
        leaving_mask=np.full(np.shape(user_move_type), False)
        leaving_mask[user_move_type=='Leaving_PC'] = True

    if "People_Outside_ROI_Only_gt" in dataframe.columns:
        people_activity_roi = dataframe['People_Outside_ROI_Only_gt'].values.astype(object)
        people_activity_roi_mask = np.full(np.shape(people_activity_roi), False)
        people_activity_roi_mask[people_activity_roi==1] = True

    if "Approach event activity detected length" in dataframe.columns:
        app_event_activity_det_len = dataframe['Approach event activity detected length'].values.astype(object)
        app_event_mask_0_15_frames   = np.full(np.shape(app_event_activity_det_len), False)
        app_event_mask_16_45_frames  = np.full(np.shape(app_event_activity_det_len), False)
        app_event_mask_46_105_frames = np.full(np.shape(app_event_activity_det_len), False)
        app_event_mask_106_up_frames = np.full(np.shape(app_event_activity_det_len), False)
        app_event_mask_0_15_frames[app_event_activity_det_len<=15] = True
        app_event_mask_16_45_frames[np.logical_and(app_event_activity_det_len>15, app_event_activity_det_len<=45)] = True
        app_event_mask_46_105_frames[np.logical_and(app_event_activity_det_len>45, app_event_activity_det_len<=105)] = True
        app_event_mask_106_up_frames[app_event_activity_det_len>105] = True

        app_event_activity_det_prct = dataframe['Approach event activity detected percent'].values.astype(object)
        app_event_det_prct_mask_0_60   = np.full(np.shape(app_event_activity_det_prct), False)
        app_event_det_prct_mask_60_70  = np.full(np.shape(app_event_activity_det_prct), False)
        app_event_det_prct_mask_70_80  = np.full(np.shape(app_event_activity_det_prct), False)
        app_event_det_prct_mask_80_90  = np.full(np.shape(app_event_activity_det_prct), False)        
        app_event_det_prct_mask_90_100 = np.full(np.shape(app_event_activity_det_prct), False)
        app_event_det_prct_mask_0_60[app_event_activity_det_prct<=0.6] = True
        app_event_det_prct_mask_60_70[np.logical_and(app_event_activity_det_prct>0.6, app_event_activity_det_prct<=0.7)] = True
        app_event_det_prct_mask_70_80[np.logical_and(app_event_activity_det_prct>0.7, app_event_activity_det_prct<=0.8)] = True
        app_event_det_prct_mask_80_90[np.logical_and(app_event_activity_det_prct>0.8, app_event_activity_det_prct<=0.9)] = True
        app_event_det_prct_mask_90_100[app_event_activity_det_prct>0.9] = True    

        app_event_act_duration_prior_to_end = dataframe['Active seq duration prior to approach event end'].values.astype(object)
        app_event_act_dur_prior_to_end_mask_0_30  = np.full(np.shape(app_event_act_duration_prior_to_end), False)
        app_event_act_dur_prior_to_end_mask_31_60 = np.full(np.shape(app_event_act_duration_prior_to_end), False)
        app_event_act_dur_prior_to_end_mask_61_90 = np.full(np.shape(app_event_act_duration_prior_to_end), False)
        app_event_act_dur_prior_to_end_mask_90_up = np.full(np.shape(app_event_act_duration_prior_to_end), False)
        app_event_act_dur_prior_to_end_mask_0_30[app_event_act_duration_prior_to_end<=30] = True
        app_event_act_dur_prior_to_end_mask_31_60[np.logical_and(app_event_act_duration_prior_to_end>30, app_event_act_duration_prior_to_end<=60)] = True
        app_event_act_dur_prior_to_end_mask_61_90[np.logical_and(app_event_act_duration_prior_to_end>60, app_event_act_duration_prior_to_end<=90)] = True
        app_event_act_dur_prior_to_end_mask_90_up[app_event_act_duration_prior_to_end>90] = True

        app_event_act_duration_from_app_start = dataframe['Active seq duration from approach event start'].values.astype(object)
        app_event_act_dur_from_start_mask_0_10  = np.full(np.shape(app_event_act_duration_from_app_start), False)
        app_event_act_dur_from_start_mask_11_20 = np.full(np.shape(app_event_act_duration_from_app_start), False)
        app_event_act_dur_from_start_mask_21_30 = np.full(np.shape(app_event_act_duration_from_app_start), False)
        app_event_act_dur_from_start_mask_31_up = np.full(np.shape(app_event_act_duration_from_app_start), False)
        app_event_act_dur_from_start_mask_0_10[app_event_act_duration_from_app_start<=10] = True
        app_event_act_dur_from_start_mask_11_20[np.logical_and(app_event_act_duration_from_app_start>10, app_event_act_duration_from_app_start<=20)] = True
        app_event_act_dur_from_start_mask_21_30[np.logical_and(app_event_act_duration_from_app_start>20, app_event_act_duration_from_app_start<=30)] = True
        app_event_act_dur_from_start_mask_31_up[app_event_act_duration_from_app_start>30] = True

    if "Separate FN sequence count" in dataframe.columns:
        sep_fn_seq_count = dataframe['Separate FN sequence count'].values.astype(object)
        sep_fn_seq_count_1_5   = np.full(np.shape(sep_fn_seq_count), False)
        sep_fn_seq_count_6_10  = np.full(np.shape(sep_fn_seq_count), False)
        sep_fn_seq_count_11_20 = np.full(np.shape(sep_fn_seq_count), False)
        sep_fn_seq_count_20_up = np.full(np.shape(sep_fn_seq_count), False)
        sep_fn_seq_count_1_5[sep_fn_seq_count<=5] = True
        sep_fn_seq_count_6_10[np.logical_and(sep_fn_seq_count>5, sep_fn_seq_count<=10)] = True
        sep_fn_seq_count_11_20[np.logical_and(sep_fn_seq_count>10, sep_fn_seq_count<=20)] = True
        sep_fn_seq_count_20_up[sep_fn_seq_count>20] = True

    if "Separate FP sequence count" in dataframe.columns:
        sep_fp_seq_count = dataframe['Separate FP sequence count'].values.astype(object)
        sep_fp_seq_count_1_5   = np.full(np.shape(sep_fp_seq_count), False)
        sep_fp_seq_count_6_10  = np.full(np.shape(sep_fp_seq_count), False)
        sep_fp_seq_count_11_20 = np.full(np.shape(sep_fp_seq_count), False)
        sep_fp_seq_count_20_up = np.full(np.shape(sep_fp_seq_count), False)
        sep_fp_seq_count_1_5[sep_fp_seq_count<=5] = True
        sep_fp_seq_count_6_10[np.logical_and(sep_fp_seq_count>5, sep_fp_seq_count<=10)] = True
        sep_fp_seq_count_11_20[np.logical_and(sep_fp_seq_count>10, sep_fp_seq_count<=20)] = True
        sep_fp_seq_count_20_up[sep_fp_seq_count>20] = True

    if 0:
        import matplotlib.pyplot as plt
        from statsmodels.graphics.mosaicplot import mosaic
        seq_len = dataframe['end_frame']-dataframe['frame_id']
        seq_len_arr = np.array(seq_len.sort_values())
        square_ceil = np.int(np.ceil(np.sqrt(len(seq_len_arr))))
        diff_for_square = square_ceil*square_ceil - len(seq_len_arr)
        seq_len_arr_padd = np.append(seq_len_arr,np.zeros(np.int(diff_for_square)))
        seq_len_mat = seq_len_arr_padd.reshape(square_ceil,square_ceil)

        my_dict = {}
        for ind1 in np.arange(square_ceil):
            for ind2 in np.arange(square_ceil):
                my_dict[np.array2string(ind1),np.array2string(ind2)] = seq_len_mat[ind1,ind2]

        labelizer=lambda k:my_dict[k]
        mosaic(seq_len_mat,gap=0.01, title='Separate FP sequence mosaic', labelizer=labelizer)
        plt.savefig("mosaic.png") # save file in C:\Working_Folder\DataScienceSIL


    if 0: # Histogram visualization for sep FN/FP seq
        import plotly.express as px
        fig = px.histogram(sep_fn_seq_count)
        fig.layout.xaxis.title.text = 'Separate FN sequence count'
        fig.layout.title.text='Separate FN sequence count sum = ' + np.array2string(np.array(sep_fn_seq_count.sum()))

        fig = px.histogram(sep_fp_seq_count)
        fig.layout.xaxis.title.text = 'Separate FP sequence count'
        fig.layout.title.text='Separate FP sequence count sum = ' + np.array2string(np.array(sep_fp_seq_count.sum()))

    if 0: # Histogram visualization for approach events
        import plotly.express as px
        fig1 = px.histogram(app_event_activity_det_len)
        fig1.layout.xaxis.title.text = 'Frames'
        fig1.layout.title.text='Activity detected sequence length during approach event'

        fig2 = px.histogram(app_event_activity_det_prct)
        fig2.layout.xaxis.title.text = 'Percent'
        fig2.layout.title.text='Activity detected sequence percentage out of approach event frame'

        counts, bins = np.histogram(app_event_act_duration_prior_to_end, bins=20)
        bins = 0.5 * (bins[:-1] + bins[1:])
        fig3 = px.bar(x=bins, y=counts, labels={'x':'Frames', 'y':'count'})
        fig3.layout.title.text='Activity detected sequence duration from end of approach event'

        fig33 = px.histogram(app_event_act_duration_prior_to_end)
        fig33.layout.xaxis.title.text = 'Frames'
        fig33.layout.title.text='Activity detected sequence duration from end of approach event'

        counts, bins = np.histogram(app_event_act_duration_from_app_start, bins=20)
        bins = 0.5 * (bins[:-1] + bins[1:])
        fig4 = px.bar(x=bins, y=counts, labels={'x':'Frames', 'y':'count'})
        fig4.layout.title.text='Activity detected sequence duration from start of approach event'

        fig44 = px.histogram(app_event_act_duration_from_app_start)
        fig44.layout.xaxis.title.text = 'Frames'
        fig44.layout.title.text='Activity detected sequence duration from start of approach event'


    multiple_mask = multiple > 0
    relevant_mask = relevant > 0
    static_mask = static > 0
    activity_mask = activity > 0

    mult_dict = {'possible partitions': ['one person', 'multiple persons'], 'masks': [np.logical_not( multiple_mask), multiple_mask]}
    relevant_dict = {'possible partitions': ['non relevant', 'relevant'], 'masks': [np.logical_not(relevant_mask), relevant_mask]}
    static_dict = {'possible partitions': ['not static', 'ken static'], 'masks': [np.logical_not(static_mask), static_mask]}
    activity_dict = {'possible partitions': ['no activity', 'has activity'], 'masks': [np.logical_not(activity_mask), activity_mask]}

    desired_masks = {'Multiple': mult_dict, "Relevant":relevant_dict, "Static":static_dict, "Has Person":activity_dict}
    if "User_Movement_Type_gt" in dataframe.columns:
        user_phy_dict = {'possible partitions': ['NA/Sit/Stand/Lay','Moving'], 'masks': [np.logical_not(user_phy_stat_mask), user_phy_stat_mask]}
        move_type_dict = {'possible partitions': ['Approach','Leave','Stand up/Sit down','Walk','Other'], 'masks': [move_type_mask_approach,move_type_mask_leave,move_type_mask_stand_up_sit_down,move_type_mask_walk,move_type_mask_other]}
        desired_masks = {'Multiple': mult_dict, "Relevant":relevant_dict, "Static":static_dict, "Has Person":activity_dict, "User physical status":user_phy_dict, "Movement Type":move_type_dict}

    if "People_Outside_ROI_Only_gt" in dataframe.columns:
        people_activity_roi_dict = {'possible partitions': ['People inside ROI or empty frames','People outside 3m ROI only'], 'masks': [np.logical_not(people_activity_roi_mask), people_activity_roi_mask]}
        desired_masks = {'Multiple': mult_dict, "Relevant":relevant_dict, "Static":static_dict, "Has Person":activity_dict, "People outside 3m ROI only":people_activity_roi_dict}

    if "Approach event activity detected length" in dataframe.columns:
        app_event_activity_det_len_dict     = {'possible partitions': ['Fewer than 16 frames','Between 16-45 frames','Between 46-105 frames','More than 105 frames'], 'masks': [app_event_mask_0_15_frames,app_event_mask_16_45_frames,app_event_mask_46_105_frames,app_event_mask_106_up_frames]}
        app_event_activity_det_prct_dict    = {'possible partitions': ['Fewer than 60%','Between 60-70 %','Between 70-80 %','Between 80-90 %','Between 90-100 %'], 'masks': [app_event_det_prct_mask_0_60,app_event_det_prct_mask_60_70,app_event_det_prct_mask_70_80,app_event_det_prct_mask_80_90,app_event_det_prct_mask_90_100]}
        app_event_act_dur_prior_to_end_dict = {'possible partitions': ['Fewer than 30 frames','Between 31-60 frames','Between 61-90 frames','More than 90 frames'], 'masks': [app_event_act_dur_prior_to_end_mask_0_30,app_event_act_dur_prior_to_end_mask_31_60,app_event_act_dur_prior_to_end_mask_61_90,app_event_act_dur_prior_to_end_mask_90_up]}
        app_event_act_dur_from_start_dict   = {'possible partitions': ['Fewer than 16 frames','Between 16-45 frames','Between 46-105 frames','More than 105 frames'], 'masks': [app_event_act_dur_from_start_mask_0_10,app_event_act_dur_from_start_mask_11_20,app_event_act_dur_from_start_mask_21_30,app_event_act_dur_from_start_mask_31_up]}

        desired_masks = {'Multiple': mult_dict, "Relevant":relevant_dict, "Static":static_dict, "Has Person":activity_dict,
        "Approach event activity detection length":app_event_activity_det_len_dict,
        "Approach event activity detection percent":app_event_activity_det_prct_dict,
        "Approach event activity first det duration from event end":app_event_act_dur_prior_to_end_dict,
        "Approach event activity first det duration from event start":app_event_act_dur_from_start_dict}

    if "Separate FN sequence count" in dataframe.columns:
        sep_fn_seq_count_dict = {'possible partitions': ['Sep. FN seq. count <= 5','Sep. FN seq. count between 6-10','Sep. FN seq. count between 11-20','Sep. FN seq. count >20'], 'masks': [sep_fn_seq_count_1_5,sep_fn_seq_count_6_10,sep_fn_seq_count_11_20,sep_fn_seq_count_20_up]}
        desired_masks = {'Multiple': mult_dict, "Relevant":relevant_dict, "Static":static_dict, "Has Person":activity_dict, "Separate FN sequence count":sep_fn_seq_count_dict}

    if "Separate FP sequence count" in dataframe.columns:
        sep_fp_seq_count_dict = {'possible partitions': ['Sep. FP seq. count <= 5','Sep. FP seq. count between 6-10','Sep. FP seq. count between 11-20','Sep. FP seq. count >20'], 'masks': [sep_fp_seq_count_1_5,sep_fp_seq_count_6_10,sep_fp_seq_count_11_20,sep_fp_seq_count_20_up]}
        desired_masks = {'Multiple': mult_dict, "Relevant":relevant_dict, "Static":static_dict, "Has Person":activity_dict, "Separate FP sequence count":sep_fp_seq_count_dict}


    return desired_masks

