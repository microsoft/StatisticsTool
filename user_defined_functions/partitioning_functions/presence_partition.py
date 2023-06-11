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

def presence_partition(dataframe, from_file=False):
    desired_masks = {}

    # Per clip annotations
    if 'Is_leave_at_end_of_film' in dataframe.columns:
        in_end_of_film = np.array(dataframe['Is_leave_at_end_of_film'])
        not_in_end_of_film = np.logical_not(in_end_of_film)
        clip_is_leave_at_end_of_film_dict = {'possible partitions': ['True','False'], 'masks': [in_end_of_film, not_in_end_of_film]}
        desired_masks.update({"Per event: Is leave event at end of film": clip_is_leave_at_end_of_film_dict})
    if 'General_User_Wheelchair_gt' in dataframe.columns:
        is_wheelchair = np.array(dataframe['General_User_Wheelchair_gt'].values.astype(bool))
        not_is_wheelchair = np.logical_not(is_wheelchair)
        clip_is_wheelchair_dict = {'possible partitions': ['True','False'], 'masks': [is_wheelchair, not_is_wheelchair]}
        desired_masks.update({"Per clip: Is user sits on wheelchair": clip_is_wheelchair_dict})
    if 'is_pop_up' in dataframe.columns:
        is_pop_up = np.array(dataframe['is_pop_up'].values.astype(bool))
        not_is_pop_up = np.logical_not(is_pop_up)
        is_pop_up_dict = {'possible partitions': ['True','False'], 'masks': [is_pop_up, not_is_pop_up]}
        desired_masks.update({"Per event: Is popup": is_pop_up_dict})
    if 'is_user_working' in dataframe.columns:
        is_user_working = np.array(dataframe['is_user_working'].values.astype(bool))
        not_is_user_working = np.logical_not(is_user_working)
        is_user_working_dict = {'possible partitions': ['True','False'], 'masks': [is_user_working, not_is_user_working]}
        desired_masks.update({"Per event: Is user working": is_user_working_dict})
    if "User_Gender_gt" in dataframe.columns:
        clip_user_gender = dataframe['User_Gender_gt'].values.astype(object)
        clip_user_gender_mask_male   = np.full(np.shape(clip_user_gender), False)
        clip_user_gender_mask_female = np.full(np.shape(clip_user_gender), False)
        clip_user_gender_mask_other  = np.full(np.shape(clip_user_gender), True)
        clip_user_gender_mask_male[clip_user_gender=='m'] = True
        clip_user_gender_mask_male[clip_user_gender=='M'] = True
        clip_user_gender_mask_female[clip_user_gender=='f'] = True
        clip_user_gender_mask_female[clip_user_gender=='F'] = True

        clip_user_gender_mask_other[clip_user_gender=='m'] = False
        clip_user_gender_mask_other[clip_user_gender=='M'] = False
        clip_user_gender_mask_other[clip_user_gender=='f'] = False
        clip_user_gender_mask_other[clip_user_gender=='F'] = False
        clip_user_gender_dict = {'possible partitions': ['Male','Female','Other'], 'masks': [clip_user_gender_mask_male,clip_user_gender_mask_female,clip_user_gender_mask_other]}
        desired_masks.update({"Per clip: User Gender": clip_user_gender_dict})
    if "User_Complexion_gt" in dataframe.columns:
        # VeryFair/ Fair/ Medium/ Olive/ Brown / Black  / Uknown
        clip_user_complexion = dataframe['User_Complexion_gt'].values.astype(object)
        clip_user_complexion_mask_very_fair = np.full(np.shape(clip_user_complexion), False)
        clip_user_complexion_mask_fair      = np.full(np.shape(clip_user_complexion), False)
        clip_user_complexion_mask_medium    = np.full(np.shape(clip_user_complexion), False)
        clip_user_complexion_mask_olive     = np.full(np.shape(clip_user_complexion), False)
        clip_user_complexion_mask_brown     = np.full(np.shape(clip_user_complexion), False)
        clip_user_complexion_mask_black     = np.full(np.shape(clip_user_complexion), False)
        clip_user_complexion_mask_other     = np.full(np.shape(clip_user_complexion), True)
        clip_user_complexion_mask_very_fair[clip_user_complexion=='VeryFair'] = True
        clip_user_complexion_mask_fair[clip_user_complexion=='Fair']          = True
        clip_user_complexion_mask_medium[clip_user_complexion=='Medium']      = True
        clip_user_complexion_mask_olive[clip_user_complexion=='Olive']        = True
        clip_user_complexion_mask_brown[clip_user_complexion=='Brown']        = True
        clip_user_complexion_mask_black[clip_user_complexion=='Black']        = True

        clip_user_complexion_mask_other[clip_user_complexion=='VeryFair'] = False
        clip_user_complexion_mask_other[clip_user_complexion=='Fair']     = False
        clip_user_complexion_mask_other[clip_user_complexion=='Medium']   = False
        clip_user_complexion_mask_other[clip_user_complexion=='Olive']    = False
        clip_user_complexion_mask_other[clip_user_complexion=='Brown']    = False
        clip_user_complexion_mask_other[clip_user_complexion=='Black']    = False
        clip_user_complexion_dict = {'possible partitions': ['Very fair','Fair','Medium','Olive','Brown','Black','Other'], 'masks': [clip_user_complexion_mask_very_fair,clip_user_complexion_mask_fair,clip_user_complexion_mask_medium,clip_user_complexion_mask_olive,clip_user_complexion_mask_brown,clip_user_complexion_mask_black,clip_user_complexion_mask_other]}
        desired_masks.update({"Per clip: User Complexion": clip_user_complexion_dict})
    if "Enviroment_gt" in dataframe.columns:
        # Outdoor/Indoor
        clip_enviroment = dataframe['Enviroment_gt'].values.astype(object)
        clip_environment_mask_outdoor = np.full(np.shape(clip_enviroment), False)
        clip_environment_mask_indoor  = np.full(np.shape(clip_enviroment), False)
        clip_environment_mask_other   = np.full(np.shape(clip_enviroment), True)
        clip_environment_mask_outdoor[clip_enviroment=='Outdoor'] = True
        clip_environment_mask_outdoor[clip_enviroment=='OutDoor'] = True
        clip_environment_mask_indoor[clip_enviroment=='Indoor']   = True
        clip_environment_mask_indoor[clip_enviroment=='InDoor']   = True

        clip_environment_mask_other[clip_enviroment=='Outdoor'] = False
        clip_environment_mask_other[clip_enviroment=='OutDoor'] = False
        clip_environment_mask_other[clip_enviroment=='Indoor']  = False
        clip_environment_mask_other[clip_enviroment=='InDoor']  = False
        clip_user_environment_dict = {'possible partitions': ['Outdoor','Indoor','Other'], 'masks': [clip_environment_mask_outdoor,clip_environment_mask_indoor,clip_environment_mask_other]}
        desired_masks.update({"Per clip: User Environment (Indoor/Outdoor)": clip_user_environment_dict})
    if "Location_gt" in dataframe.columns:
        # Office, Open Space, Kitchen, Reception, Conference Room, Cafe etc.
        clip_location = dataframe['Location_gt'].values.astype(object)
        clip_location_mask_public_space      = np.full(np.shape(clip_location), False)
        clip_location_mask_office            = np.full(np.shape(clip_location), False)
        clip_location_mask_open_space_office = np.full(np.shape(clip_location), False)
        clip_location_mask_outdoor           = np.full(np.shape(clip_location), False)
        clip_location_mask_reception         = np.full(np.shape(clip_location), False)
        clip_location_mask_cafe              = np.full(np.shape(clip_location), False)
        clip_location_mask_home_office       = np.full(np.shape(clip_location), False)
        clip_location_mask_small_office      = np.full(np.shape(clip_location), False)
        clip_location_mask_other             = np.full(np.shape(clip_location), True)
        clip_location_mask_public_space[clip_location=='PublicSpace']          = True
        clip_location_mask_office[clip_location=='Office']                     = True
        clip_location_mask_open_space_office[clip_location=='OpenSpaceOffice'] = True
        clip_location_mask_outdoor[clip_location=='OutDoor']                   = True
        clip_location_mask_reception[clip_location=='Reception']               = True
        clip_location_mask_cafe[clip_location=='Cafe']                         = True
        clip_location_mask_home_office[clip_location=='HomeOffice']            = True
        clip_location_mask_small_office[clip_location=='SmallOffice']          = True

        clip_location_mask_other[clip_location=='PublicSpace']     = False
        clip_location_mask_other[clip_location=='Office']          = False
        clip_location_mask_other[clip_location=='OpenSpaceOffice'] = False
        clip_location_mask_other[clip_location=='OutDoor']         = False
        clip_location_mask_other[clip_location=='Reception']       = False
        clip_location_mask_other[clip_location=='Cafe']            = False
        clip_location_mask_other[clip_location=='HomeOffice']      = False
        clip_location_mask_other[clip_location=='SmallOffice']     = False
        clip_user_location_dict = {'possible partitions': ['Public Space','Office','Open Space Office','Outdoor','Reception','Cafe','Home Office','Small Office','Other'], 'masks': [clip_location_mask_public_space,clip_location_mask_office,clip_location_mask_open_space_office,clip_location_mask_outdoor,clip_location_mask_reception,clip_location_mask_cafe,clip_location_mask_home_office,clip_location_mask_small_office,clip_location_mask_other]}
        desired_masks.update({"Per clip: User Location": clip_user_location_dict})
    if "General_Background_People_gt" in dataframe.columns:
        # Empty,One,Few (2-5), Several (5-10) ,Crowded (10+)
        clip_general_bg_people = dataframe['General_Background_People_gt'].values.astype(object)
        clip_genral_bg_people_mask_empty   = np.full(np.shape(clip_general_bg_people), False)
        clip_genral_bg_people_mask_one     = np.full(np.shape(clip_general_bg_people), False)
        clip_genral_bg_people_mask_few     = np.full(np.shape(clip_general_bg_people), False)
        clip_genral_bg_people_mask_several = np.full(np.shape(clip_general_bg_people), False)
        clip_genral_bg_people_mask_crowded = np.full(np.shape(clip_general_bg_people), False)
        clip_genral_bg_people_mask_other   = np.full(np.shape(clip_general_bg_people), True)
        clip_genral_bg_people_mask_empty[clip_general_bg_people=='Empty']     = True
        clip_genral_bg_people_mask_one[clip_general_bg_people=='One']         = True
        clip_genral_bg_people_mask_few[clip_general_bg_people=='Few']         = True
        clip_genral_bg_people_mask_several[clip_general_bg_people=='Several'] = True
        clip_genral_bg_people_mask_crowded[clip_general_bg_people=='Crowded'] = True

        clip_genral_bg_people_mask_other[clip_general_bg_people=='Empty']   = False
        clip_genral_bg_people_mask_other[clip_general_bg_people=='One']     = False
        clip_genral_bg_people_mask_other[clip_general_bg_people=='Few']     = False
        clip_genral_bg_people_mask_other[clip_general_bg_people=='Several'] = False
        clip_genral_bg_people_mask_other[clip_general_bg_people=='Crowded'] = False
        clip_general_bg_people_dict = {'possible partitions': ['Empty','One','Few','Several','Crowded','Other'], 'masks': [clip_genral_bg_people_mask_empty,clip_genral_bg_people_mask_one,clip_genral_bg_people_mask_few,clip_genral_bg_people_mask_several,clip_genral_bg_people_mask_crowded,clip_genral_bg_people_mask_other]}
        desired_masks.update({"Per clip: General Background People": clip_general_bg_people_dict})
    if "General_Natural_Light_gt" in dataframe.columns:
        # Dark/Dusk/Sunny/Cloudy/NA/Changing/Unknown
        clip_natural_light = dataframe['General_Natural_Light_gt'].values.astype(object)
        clip_natural_light_mask_dark     = np.full(np.shape(clip_natural_light), False)
        clip_natural_light_mask_dusk     = np.full(np.shape(clip_natural_light), False)
        clip_natural_light_mask_sunny    = np.full(np.shape(clip_natural_light), False)
        clip_natural_light_mask_cloudy   = np.full(np.shape(clip_natural_light), False)
        clip_natural_light_mask_changing = np.full(np.shape(clip_natural_light), False)
        clip_natural_light_mask_other    = np.full(np.shape(clip_natural_light), True)
        clip_natural_light_mask_dark[clip_natural_light=='Dark']         = True
        clip_natural_light_mask_dusk[clip_natural_light=='Dusk']         = True
        clip_natural_light_mask_sunny[clip_natural_light=='Sunny']       = True
        clip_natural_light_mask_cloudy[clip_natural_light=='Cloudy']     = True
        clip_natural_light_mask_changing[clip_natural_light=='Changing'] = True

        clip_natural_light_mask_other[clip_natural_light=='Dark']     = False
        clip_natural_light_mask_other[clip_natural_light=='Dusk']     = False
        clip_natural_light_mask_other[clip_natural_light=='Sunny']    = False
        clip_natural_light_mask_other[clip_natural_light=='Cloudy']   = False
        clip_natural_light_mask_other[clip_natural_light=='Changing'] = False
        clip_natural_light_dict = {'possible partitions': ['Dark','Dusk','Sunny','Cloudy','Changing','Other'], 'masks': [clip_natural_light_mask_dark,clip_natural_light_mask_dusk,clip_natural_light_mask_sunny,clip_natural_light_mask_cloudy,clip_natural_light_mask_changing,clip_natural_light_mask_other]}
        desired_masks.update({"Per clip: Natural Light": clip_natural_light_dict})
    if "General_Artificial_Light_gt" in dataframe.columns:
        # Dark/Dim/Lighted/Bright/NA/Changing/Unknown
        clip_artificial_light = dataframe['General_Artificial_Light_gt'].values.astype(object)
        clip_artificial_light_mask_dark     = np.full(np.shape(clip_artificial_light), False)
        clip_artificial_light_mask_dim      = np.full(np.shape(clip_artificial_light), False)
        clip_artificial_light_mask_lighted  = np.full(np.shape(clip_artificial_light), False)
        clip_artificial_light_mask_bright   = np.full(np.shape(clip_artificial_light), False)
        clip_artificial_light_mask_changing = np.full(np.shape(clip_artificial_light), False)
        clip_artificial_light_mask_other    = np.full(np.shape(clip_artificial_light), True)
        clip_artificial_light_mask_dark[clip_artificial_light=='Dark']         = True
        clip_artificial_light_mask_dim[clip_artificial_light=='Dim']           = True
        clip_artificial_light_mask_lighted[clip_artificial_light=='Lighted']   = True
        clip_artificial_light_mask_bright[clip_artificial_light=='Bright']     = True
        clip_artificial_light_mask_changing[clip_artificial_light=='Changing'] = True

        clip_artificial_light_mask_other[clip_artificial_light=='Dark']     = False
        clip_artificial_light_mask_other[clip_artificial_light=='Dim']      = False
        clip_artificial_light_mask_other[clip_artificial_light=='Lighted']  = False
        clip_artificial_light_mask_other[clip_artificial_light=='Bright']   = False
        clip_artificial_light_mask_other[clip_artificial_light=='Changing'] = False
        clip_artificial_light_dict = {'possible partitions': ['Dark','Dim','Lighted','Bright','Changing','Other'], 'masks': [clip_artificial_light_mask_dark,clip_artificial_light_mask_dim,clip_artificial_light_mask_lighted,clip_artificial_light_mask_bright,clip_artificial_light_mask_changing,clip_artificial_light_mask_other]}
        desired_masks.update({"Per clip: Artificial Light": clip_artificial_light_dict})
    if "Device_Posture_gt" in dataframe.columns:
        # Degrees
        clip_device_posture = dataframe['Device_Posture_gt'].values.astype(object)
        clip_device_posture_mask_90    = np.full(np.shape(clip_device_posture), False)
        clip_device_posture_mask_110   = np.full(np.shape(clip_device_posture), False)
        clip_device_posture_mask_130   = np.full(np.shape(clip_device_posture), False)
        clip_device_posture_mask_other = np.full(np.shape(clip_device_posture), True)
        clip_device_posture_mask_90[clip_device_posture==90]   = True
        clip_device_posture_mask_110[clip_device_posture==110] = True
        clip_device_posture_mask_130[clip_device_posture==130] = True

        clip_device_posture_mask_other[clip_device_posture==90]  = False
        clip_device_posture_mask_other[clip_device_posture==110] = False
        clip_device_posture_mask_other[clip_device_posture==130] = False
        clip_device_posture_dict = {'possible partitions': ['90','110','130','Other'], 'masks': [clip_device_posture_mask_90,clip_device_posture_mask_110,clip_device_posture_mask_130,clip_device_posture_mask_other]}
        desired_masks.update({"Per clip: Device Posture": clip_device_posture_dict})
    if "External_Monitor_gt" in dataframe.columns:
        # Yes/No
        clip_external_monitor = dataframe['External_Monitor_gt'].values.astype(object)
        clip_external_monitor_mask_yes   = np.full(np.shape(clip_external_monitor), False)
        clip_external_monitor_mask_no    = np.full(np.shape(clip_external_monitor), False)
        clip_external_monitor_mask_other = np.full(np.shape(clip_external_monitor), True)
        clip_external_monitor_mask_yes[clip_external_monitor=='Yes'] = True
        clip_external_monitor_mask_no[clip_external_monitor=='No']   = True
        
        clip_external_monitor_mask_other[clip_external_monitor=='Yes'] = False
        clip_external_monitor_mask_other[clip_external_monitor=='No']  = False
        clip_external_monitor_dict = {'possible partitions': ['Yes','No','Other'], 'masks': [clip_external_monitor_mask_yes,clip_external_monitor_mask_no,clip_external_monitor_mask_other]}
        desired_masks.update({"Per clip: External Monitor": clip_external_monitor_dict})
    if 0:#"Clip_Duration [MIN]_gt" in dataframe.columns:
        clip_duration = dataframe['Clip_Duration [MIN]_gt'].values.astype(object)
        clip_duration_mask_other           = np.full(np.shape(clip_duration),False)
        clip_duration_mask_other[clip_duration=='NA'] = True

        clip_duration_min = np.ones(np.shape(clip_duration))
        ftr = [60,1,1/60]
        for ind, curr_dur in enumerate(clip_duration):
            if clip_duration[ind]=='NA' or clip_duration[ind]==None:
                clip_duration_min[ind] = -1
            else:
                clip_duration_min[ind] = sum([a*b for a,b in zip(ftr, map(int,curr_dur.split(':')))])

        clip_duration_mask_smaller_1_min   = np.full(np.shape(clip_duration),False)
        clip_duration_mask_between_1_2_min = np.full(np.shape(clip_duration),False)
        clip_duration_mask_between_2_3_min = np.full(np.shape(clip_duration),False)
        clip_duration_mask_between_3_5_min = np.full(np.shape(clip_duration),False)
        clip_duration_mask_larger_5_min    = np.full(np.shape(clip_duration),False)
        clip_duration_mask_smaller_1_min[np.logical_and((clip_duration_min>0),(clip_duration_min<=1))] = True
        clip_duration_mask_between_1_2_min[np.logical_and((clip_duration_min>1),(clip_duration_min<=2))] = True
        clip_duration_mask_between_2_3_min[np.logical_and((clip_duration_min>2),(clip_duration_min<=3))] = True
        clip_duration_mask_between_3_5_min[np.logical_and((clip_duration_min>3),(clip_duration_min<=5))] = True
        clip_duration_mask_larger_5_min[clip_duration_min>5] = True
        clip_duration_dict = {'possible partitions': ['Smaller than 1 min','Between 1-2 min','Between 2-3 min','Between 3-5 min','Larger than 5 min','Other'], 'masks': [clip_duration_mask_smaller_1_min,clip_duration_mask_between_1_2_min,clip_duration_mask_between_2_3_min,clip_duration_mask_between_3_5_min,clip_duration_mask_larger_5_min,clip_duration_mask_other]}
        desired_masks.update({"Per clip: Video Duration": clip_duration_dict})


    # Per frame annotations
    if "Multiple People_gt" in dataframe.columns:
        multiple = dataframe['Multiple People_gt'].values.astype(object)
        multiple_mask = multiple > 0
        mult_dict = {'possible partitions': ['one person', 'multiple persons'], 'masks': [np.logical_not( multiple_mask), multiple_mask]}
        desired_masks.update({"Per frame: Multiple": mult_dict})

    if "relevant_gt" in dataframe.columns:
        relevant = dataframe['relevant_gt'].values.astype(object)
        relevant_mask = relevant > 0
        relevant_dict = {'possible partitions': ['non relevant', 'relevant'], 'masks': [np.logical_not(relevant_mask), relevant_mask]}
        desired_masks.update({"Per frame: Relevant": relevant_dict})

    if "static_gt" in dataframe.columns:
        static = dataframe['static_gt'].values.astype(object)
        static_mask = static > 0
        static_dict = {'possible partitions': ['not static', 'ken static'], 'masks': [np.logical_not(static_mask), static_mask]}    
        desired_masks.update({"Per frame: Static": static_dict})

    if "static_gt" in dataframe.columns:
        presence = dataframe['detection_gt'].values.astype(object)
        presence_mask = presence > 0
        presence_dict = {'possible partitions': ['no presence', 'has presence'], 'masks': [np.logical_not(presence_mask), presence_mask]}
        desired_masks.update({"Per frame: Presence": presence_dict})

    if 'Activity_ROI_gt' in dataframe.columns:
        Activity_roi = dataframe['Activity_ROI_gt'].values.astype(object)
        activity_roi_true = np.full(np.shape(Activity_roi), False)
        activity_roi_true[Activity_roi=='True'] = True
        activity_roi_False = np.logical_not(activity_roi_true)
        Activity_roi_dict = {'possible partitions': ['True','False'], 'masks': [activity_roi_true, activity_roi_False]}
        desired_masks.update({"Per frame: is Activity": Activity_roi_dict})

    if 'Presence_ROI_gt' in dataframe.columns:
        presence_roi = dataframe['Presence_ROI_gt'].values.astype(object)
        presence_roi_true = np.full(np.shape(presence_roi), False)
        presence_roi_true[presence_roi=='True'] = True
        presence_roi_False = np.logical_not(presence_roi_true)
        presence_roi_dict = {'possible partitions': ['True','False'], 'masks': [presence_roi_true, presence_roi_False]}
        desired_masks.update({"Per frame: is Presence": presence_roi_dict})
    if 'is_on_edge' in dataframe.columns:
        is_on_edge = np.array(dataframe['is_on_edge'].values.astype(bool))
        is_on_edge_dict = {'possible partitions': ['True','False'], 'masks': [is_on_edge, np.logical_not(is_on_edge)]}
        desired_masks.update({"Per frame: is BB on the edge": is_on_edge_dict})
    if 'is_no_face' in dataframe.columns:
        is_no_face = np.array(dataframe['is_no_face'].values.astype(bool))
        is_no_face_dict = {'possible partitions': ['True','False'], 'masks': [is_no_face, np.logical_not(is_no_face)]}
        desired_masks.update({"Per frame: is No Face BB in the wake event": is_no_face_dict})

    if "User_Status_gt" in dataframe.columns:
        # NoUser/Approach_PC/PassBy_PC/Sitting_Down/OnPC_Working/OnPC_Idle/OnPC_Other/Standing_Up/Leaving_PC/Unrelated_PC/Unknown
        user_status = dataframe['User_Status_gt'].values.astype(object)
        enable_approach_split = dataframe['enable_approach_split'].values.astype(object)
        user_stat_mask_no_user     = np.full(np.shape(user_status), False)
        if enable_approach_split[0] == False:
            user_stat_mask_app_pc = np.full(np.shape(user_status), False)
        else:
            Approach_split_roi    = dataframe['Approach_split_roi_gt'].values.astype(object)
            Approach_split_trans  = dataframe['Approach_split_trans_gt'].values.astype(object)
            Approach_split_oo_roi = dataframe['Approach_split_oo_roi_gt'].values.astype(object)
            user_stat_mask_app_pc_roi    = np.full(np.shape(user_status), False)
            user_stat_mask_app_pc_trans  = np.full(np.shape(user_status), False)
            user_stat_mask_app_pc_oo_roi = np.full(np.shape(user_status), False)
        user_stat_mask_passby_pc   = np.full(np.shape(user_status), False)
        user_stat_mask_sit_down    = np.full(np.shape(user_status), False)
        user_stat_mask_onPC_work   = np.full(np.shape(user_status), False)
        user_stat_mask_onPC_idle   = np.full(np.shape(user_status), False)
        user_stat_mask_onPC_other  = np.full(np.shape(user_status), False)
        user_stat_mask_stand_up    = np.full(np.shape(user_status), False)
        user_stat_mask_leave_pc    = np.full(np.shape(user_status), False)
        user_stat_mask_unrelate_pc = np.full(np.shape(user_status), False)
        user_stat_mask_popup_approach_pc = np.full(np.shape(user_status), False)
        user_stat_mask_other = np.full(np.shape(user_status), True)
        user_stat_mask_no_user[user_status=='NoUser']           = True
        if enable_approach_split[0] == False:
            user_stat_mask_app_pc[user_status=='Approach_PC']       = True
        else:
            user_stat_mask_app_pc_roi[Approach_split_roi==True]       = True
            user_stat_mask_app_pc_trans[Approach_split_trans==True]   = True
            user_stat_mask_app_pc_oo_roi[Approach_split_oo_roi==True] = True
        user_stat_mask_passby_pc[user_status=='PassBy_PC']      = True
        user_stat_mask_sit_down[user_status=='Sitting_Down']    = True
        user_stat_mask_onPC_work[user_status=='OnPC_Working']   = True
        user_stat_mask_onPC_idle[user_status=='OnPC_Idle']      = True
        user_stat_mask_onPC_other[user_status=='OnPC_Other']    = True
        user_stat_mask_stand_up[user_status=='Standing_Up']     = True
        user_stat_mask_leave_pc[user_status=='Leaving_PC']      = True 
        user_stat_mask_unrelate_pc[user_status=='Unrelated_PC'] = True 
        user_stat_mask_popup_approach_pc[user_status=='Popup_Approach_PC'] = True 

        user_stat_mask_other[user_status=='NoUser']       = False
        if enable_approach_split[0] == False:
            user_stat_mask_other[user_status=='Approach_PC']  = False
        else:
            user_stat_mask_other[Approach_split_roi==True]    = False
            user_stat_mask_other[Approach_split_trans==True]  = False
            user_stat_mask_other[Approach_split_oo_roi==True] = False
        user_stat_mask_other[user_status=='PassBy_PC']    = False
        user_stat_mask_other[user_status=='Sitting_Down'] = False
        user_stat_mask_other[user_status=='OnPC_Working'] = False
        user_stat_mask_other[user_status=='OnPC_Idle']    = False
        user_stat_mask_other[user_status=='OnPC_Other']   = False
        user_stat_mask_other[user_status=='Standing_Up']  = False
        user_stat_mask_other[user_status=='Leaving_PC']   = False 
        user_stat_mask_other[user_status=='Unrelated_PC'] = False 
        user_stat_mask_other[user_status=='Popup_Approach_PC'] = False 
        if enable_approach_split[0] == False:
            user_stat_dict = {'possible partitions': ['No user','Unrelated PC','Pass By PC','Approach PC','Popup Approach PC', 'Leaving PC','Sitting Down','Standing Up','On PC Working','On PC Idle','On PC Other','Other'], 'masks': [user_stat_mask_no_user,user_stat_mask_unrelate_pc,user_stat_mask_passby_pc,user_stat_mask_app_pc,user_stat_mask_popup_approach_pc, user_stat_mask_leave_pc,user_stat_mask_sit_down,user_stat_mask_stand_up,user_stat_mask_onPC_work,user_stat_mask_onPC_idle,user_stat_mask_onPC_other,user_stat_mask_other]}
        else:
            user_stat_dict = {'possible partitions': ['No user','Unrelated PC','Pass By PC','Approach PC ROI','Approach PC Transition','Approach PC out of ROI','Leaving PC','Sitting Down','Standing Up','On PC Working','On PC Idle','On PC Other','Other'], 'masks': [user_stat_mask_no_user,user_stat_mask_unrelate_pc,user_stat_mask_passby_pc,user_stat_mask_app_pc_roi,user_stat_mask_app_pc_trans,user_stat_mask_app_pc_oo_roi,user_stat_mask_leave_pc,user_stat_mask_sit_down,user_stat_mask_stand_up,user_stat_mask_onPC_work,user_stat_mask_onPC_idle,user_stat_mask_onPC_other,user_stat_mask_other]}
        desired_masks.update({"Per frame: User status": user_stat_dict})

    if "Background_People_gt" in dataframe.columns:
        # Empty,One,Few (2-5), Several (5-10) ,Crowded (10+)
        bg_people = dataframe['Background_People_gt'].values.astype(object)
        bg_people_mask_empty   = np.full(np.shape(bg_people), False)
        bg_people_mask_one     = np.full(np.shape(bg_people), False)
        bg_people_mask_few     = np.full(np.shape(bg_people), False)
        bg_people_mask_several = np.full(np.shape(bg_people), False)
        bg_people_mask_crowded = np.full(np.shape(bg_people), False)
        bg_people_mask_other   = np.full(np.shape(bg_people), True)
        bg_people_mask_empty[bg_people=='Empty']     = True 
        bg_people_mask_one[bg_people=='One']         = True 
        bg_people_mask_few[bg_people=='Few']         = True 
        bg_people_mask_several[bg_people=='Several'] = True 
        bg_people_mask_crowded[bg_people=='Crowded'] = True 

        bg_people_mask_other[bg_people=='Empty']   = False 
        bg_people_mask_other[bg_people=='One']     = False 
        bg_people_mask_other[bg_people=='Few']     = False 
        bg_people_mask_other[bg_people=='Several'] = False 
        bg_people_mask_other[bg_people=='Crowded'] = False 
        bg_people_dict = {'possible partitions': ['Empty','One','Few','Several','Crowded','Other'], 'masks': [bg_people_mask_empty,bg_people_mask_one,bg_people_mask_few,bg_people_mask_several,bg_people_mask_crowded,bg_people_mask_other]}
        desired_masks.update({"Per frame: Background People": bg_people_dict})

    if "Background_Dynamic_Objects_gt" in dataframe.columns:
        # False/True
        bg_dyn_obj = dataframe['Background_Dynamic_Objects_gt'].values.astype(object)
        bg_dyn_obj_true  = np.full(np.shape(bg_dyn_obj), False)
        bg_dyn_obj_false = np.full(np.shape(bg_dyn_obj), False)
        bg_dyn_obj_other = np.full(np.shape(bg_dyn_obj), True)
        bg_dyn_obj_true[bg_dyn_obj=='True']   = True 
        bg_dyn_obj_false[bg_dyn_obj=='False'] = True 

        bg_dyn_obj_other[bg_dyn_obj=='True']  = False 
        bg_dyn_obj_other[bg_dyn_obj=='False'] = False 
        bg_dyn_obj_dict = {'possible partitions': ['Yes','No','Other'], 'masks': [bg_dyn_obj_true,bg_dyn_obj_false,bg_dyn_obj_other]}
        desired_masks.update({"Per frame: Background Dynamic Object": bg_dyn_obj_dict})

    if "Background_People_Activity_gt" in dataframe.columns:
        # NA/Static/Dynamic
        bg_people_activity = dataframe['Background_People_Activity_gt'].values.astype(object)
        bg_people_activity_static  = np.full(np.shape(bg_people_activity), False)
        bg_people_activity_dynamic = np.full(np.shape(bg_people_activity), False)
        bg_people_activity_other = np.full(np.shape(bg_people_activity), True)
        bg_people_activity_static[bg_people_activity=='Static']   = True 
        bg_people_activity_dynamic[bg_people_activity=='Dynamic'] = True 

        bg_people_activity_other[bg_people_activity=='Static']   = False 
        bg_people_activity_other[bg_people_activity=='Dynamic'] = False
        bg_people_activity_dict = {'possible partitions': ['Static','Dynamic','Other'], 'masks': [bg_people_activity_static,bg_people_activity_dynamic,bg_people_activity_other]}
        desired_masks.update({"Per frame: Background People Activity": bg_people_activity_dict})


    if "User_Physical_Status_gt" in dataframe.columns:
        #Sitting/Standing/Laying/Moving/NA
        user_phy_status = dataframe['User_Physical_Status_gt'].values.astype(object)
        user_phy_stat_mask_sit   = np.full(np.shape(user_phy_status), False)
        user_phy_stat_mask_lay   = np.full(np.shape(user_phy_status), False)
        user_phy_stat_mask_move  = np.full(np.shape(user_phy_status), False)
        user_phy_stat_mask_stand = np.full(np.shape(user_phy_status), False)
        user_phy_stat_mask_other = np.full(np.shape(user_phy_status), True)
        user_phy_stat_mask_sit[user_phy_status=='Sitting ']    = True 
        user_phy_stat_mask_lay[user_phy_status=='Laying ']     = True 
        user_phy_stat_mask_move[user_phy_status=='Moving ']    = True 
        user_phy_stat_mask_stand[user_phy_status=='Standing '] = True 

        user_phy_stat_mask_other[user_phy_status=='Sitting ']  = False
        user_phy_stat_mask_other[user_phy_status=='Laying ']   = False
        user_phy_stat_mask_other[user_phy_status=='Moving ']   = False
        user_phy_stat_mask_other[user_phy_status=='Standing '] = False
        user_phy_dict = {'possible partitions': ['Sitting','Standing','Laying','Moving','Other'], 'masks': [user_phy_stat_mask_sit,user_phy_stat_mask_stand,user_phy_stat_mask_lay,user_phy_stat_mask_move, user_phy_stat_mask_other]}
        desired_masks.update({"Per frame: User physical status": user_phy_dict})

    if "User_Movement_Type_gt" in dataframe.columns:
        #Approach_PC/Leaving_PC/Standing_Up/Sitting_Down/Walking_Unrelated
        user_move_type = dataframe['User_Movement_Type_gt'].values.astype(object)
        move_type_mask_approach = np.full(np.shape(user_move_type), False)
        move_type_mask_leave    = np.full(np.shape(user_move_type), False)
        move_type_mask_walk     = np.full(np.shape(user_move_type), False)
        move_type_mask_stand_up_sit_down = np.full(np.shape(user_move_type), False)
        move_type_mask_other = np.full(np.shape(user_move_type), True)
        move_type_mask_approach[user_move_type=='Approach_PC']           = True
        move_type_mask_leave[user_move_type=='Leaving_PC']               = True
        move_type_mask_walk[user_move_type=='Walking_Unrelated']         = True
        move_type_mask_stand_up_sit_down[user_move_type=='Standing_Up']  = True
        move_type_mask_stand_up_sit_down[user_move_type=='Sitting_Down'] = True

        move_type_mask_other[user_move_type=='Approach_PC']              = False
        move_type_mask_other[user_move_type=='Leaving_PC']               = False
        move_type_mask_other[user_move_type=='Walking_Unrelated']        = False
        move_type_mask_other[user_move_type=='Standing_Up']              = False
        move_type_mask_other[user_move_type=='Sitting_Down']             = False
        move_type_dict = {'possible partitions': ['Approach','Leave','Stand up/Sit down','Walk','Other'], 'masks': [move_type_mask_approach,move_type_mask_leave,move_type_mask_stand_up_sit_down,move_type_mask_walk,move_type_mask_other]}
        desired_masks.update({"Per frame: User Movement Type": move_type_dict})

    if "People_Outside_ROI_Only_gt" in dataframe.columns:
        people_presence_roi = dataframe['People_Outside_ROI_Only_gt'].values.astype(object)
        people_presence_roi_mask = np.full(np.shape(people_presence_roi), False)
        people_presence_roi_mask[people_presence_roi==1] = True
        people_presence_roi_dict = {'possible partitions': ['People inside ROI or empty frames','People outside 3m ROI only'], 'masks': [np.logical_not(people_presence_roi_mask), people_presence_roi_mask]}
        desired_masks.update({"Per frame: People outside 3m ROI only": people_presence_roi_dict})

    if "Presence leave event true/false ratio" in dataframe.columns:
        leave_event_presence_last_true = dataframe['Presence last True before False till end of leave event'].values.astype(object)
        leave_event_true_false_ratio   = dataframe['Presence leave event true/false ratio'].values.astype(object)
        leave_event_flicker_seq_num    = dataframe['Presence leave flicker sequence num'].values.astype(object)
        leave_event_flicker_seq_mean_len   = dataframe['Presence leave flicker sequence mean length'].values.astype(object)
        leave_event_flicker_seq_median_len = dataframe['Presence leave flicker sequence median length'].values.astype(object)

        leave_event_flicker_seq_num_mask_below_2  = np.full(np.shape(leave_event_flicker_seq_num), False)
        leave_event_flicker_seq_num_mask_3_4      = np.full(np.shape(leave_event_flicker_seq_num), False)
        leave_event_flicker_seq_num_mask_5_6      = np.full(np.shape(leave_event_flicker_seq_num), False)
        leave_event_flicker_seq_num_mask_7_10     = np.full(np.shape(leave_event_flicker_seq_num), False)
        leave_event_flicker_seq_num_mask_above_10 = np.full(np.shape(leave_event_flicker_seq_num), False)
        leave_event_flicker_seq_num_mask_below_2[np.logical_and((leave_event_flicker_seq_num>0),(leave_event_flicker_seq_num<=2))] = True
        leave_event_flicker_seq_num_mask_3_4[np.logical_and((leave_event_flicker_seq_num>2),(leave_event_flicker_seq_num<=4))] = True
        leave_event_flicker_seq_num_mask_5_6[np.logical_and((leave_event_flicker_seq_num>4),(leave_event_flicker_seq_num<=6))] = True
        leave_event_flicker_seq_num_mask_7_10[np.logical_and((leave_event_flicker_seq_num>6),(leave_event_flicker_seq_num<=10))] = True
        leave_event_flicker_seq_num_mask_above_10[leave_event_flicker_seq_num>10] = True
        leave_event_flicker_seq_num_dict = {'possible partitions': ['Smaller/equal to 2','3/4','5/6','7/8/9/10','Larger than 10'], 'masks': [leave_event_flicker_seq_num_mask_below_2,leave_event_flicker_seq_num_mask_3_4,leave_event_flicker_seq_num_mask_5_6,leave_event_flicker_seq_num_mask_7_10,leave_event_flicker_seq_num_mask_above_10]}
        desired_masks.update({"Per event: Leave event true/false flicker sequence num": leave_event_flicker_seq_num_dict})

        if 0: # Histogram visualization for leave events
            import plotly.express as px

            counts, bins = np.histogram(leave_event_presence_last_true/30, bins=20)
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig1 = px.bar(x=bins, y=counts, labels={'x':'Seconds', 'y':'count'})
            fig1.layout.title.text='Presence leave event last detected true'

            fig11 = px.histogram(leave_event_presence_last_true/30)
            fig11.layout.xaxis.title.text = 'Seconds'
            fig11.layout.title.text='Presence leave event last detected true'

            fig2 = px.histogram(leave_event_true_false_ratio)
            fig2.layout.xaxis.title.text = 'Percent [%]'
            fig2.layout.title.text='True/False presence prediction during leave event'

            counts, bins = np.histogram(leave_event_flicker_seq_num, bins=30)
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig3 = px.bar(x=bins, y=counts, labels={'x':'True/false flicker sequence number', 'y':'count'})
            fig3.layout.title.text='Presence leave true/false flicker sequence number'

            fig33 = px.histogram(leave_event_flicker_seq_num)
            fig33.layout.xaxis.title.text = 'True/false flicker sequence number'
            fig33.layout.title.text='Presence leave true/false flicker sequence number'

            fig4 = px.histogram(leave_event_flicker_seq_mean_len)
            fig4.layout.xaxis.title.text = 'True/false flicker sequence mean length'
            fig4.layout.title.text='Presence leave true/false flicker sequence mean length'

            fig5 = px.histogram(leave_event_flicker_seq_median_len)
            fig5.layout.xaxis.title.text = 'True/false flicker sequence median length'
            fig5.layout.title.text='Presence leave true/false flicker sequence median length'

            fig1.show()
            fig3.show()

    if "Presence approach flicker sequence num" in dataframe.columns:
        app_event_flicker_seq_num = dataframe['Presence approach flicker sequence num'].values.astype(object)
        app_event_flicker_seq_mean_len = dataframe['Presence approach flicker sequence mean length'].values.astype(object)
        app_event_flicker_seq_median_len = dataframe['Presence approach flicker sequence median length'].values.astype(object)
        app_event_flicker_seq_num_mask_below_2  = np.full(np.shape(app_event_flicker_seq_num), False)
        app_event_flicker_seq_num_mask_3_4      = np.full(np.shape(app_event_flicker_seq_num), False)
        app_event_flicker_seq_num_mask_5_6      = np.full(np.shape(app_event_flicker_seq_num), False)
        app_event_flicker_seq_num_mask_7_10     = np.full(np.shape(app_event_flicker_seq_num), False)
        app_event_flicker_seq_num_mask_above_10 = np.full(np.shape(app_event_flicker_seq_num), False)
        app_event_flicker_seq_num_mask_below_2[np.logical_and((app_event_flicker_seq_num>0),(app_event_flicker_seq_num<=2))] = True
        app_event_flicker_seq_num_mask_3_4[np.logical_and((app_event_flicker_seq_num>2),(app_event_flicker_seq_num<=4))] = True
        app_event_flicker_seq_num_mask_5_6[np.logical_and((app_event_flicker_seq_num>4),(app_event_flicker_seq_num<=6))] = True
        app_event_flicker_seq_num_mask_7_10[np.logical_and((app_event_flicker_seq_num>6),(app_event_flicker_seq_num<=10))] = True
        app_event_flicker_seq_num_mask_above_10[app_event_flicker_seq_num>10] = True
        app_event_flicker_seq_num_dict = {'possible partitions': ['Smaller/equal to 2','3/4','5/6','7/8/9/10','Larger than 10'], 'masks': [app_event_flicker_seq_num_mask_below_2,app_event_flicker_seq_num_mask_3_4,app_event_flicker_seq_num_mask_5_6,app_event_flicker_seq_num_mask_7_10,app_event_flicker_seq_num_mask_above_10]}
        desired_masks.update({"Per event: Approach event true/false flicker sequence num": app_event_flicker_seq_num_dict})

    if "Approach event presence detected length" in dataframe.columns:
        app_event_presence_det_len = dataframe['Approach event presence detected length'].values.astype(object)
        app_event_mask_0_15_frames   = np.full(np.shape(app_event_presence_det_len), False)
        app_event_mask_16_45_frames  = np.full(np.shape(app_event_presence_det_len), False)
        app_event_mask_46_105_frames = np.full(np.shape(app_event_presence_det_len), False)
        app_event_mask_106_up_frames = np.full(np.shape(app_event_presence_det_len), False)
        app_event_mask_0_15_frames[app_event_presence_det_len<=15] = True
        app_event_mask_16_45_frames[np.logical_and(app_event_presence_det_len>15, app_event_presence_det_len<=45)] = True
        app_event_mask_46_105_frames[np.logical_and(app_event_presence_det_len>45, app_event_presence_det_len<=105)] = True
        app_event_mask_106_up_frames[app_event_presence_det_len>105] = True

        app_event_presence_det_len_dict     = {'possible partitions': ['Fewer than 16 frames','Between 16-45 frames','Between 46-105 frames','More than 105 frames'], 'masks': [app_event_mask_0_15_frames,app_event_mask_16_45_frames,app_event_mask_46_105_frames,app_event_mask_106_up_frames]}
        desired_masks.update({"Per event: Presence event activity detection length": app_event_presence_det_len_dict})

    if "Approach event presence detected percent" in dataframe.columns:
        app_event_presence_det_prct = dataframe['Approach event presence detected percent'].values.astype(object)
        app_event_det_prct_mask_0_60   = np.full(np.shape(app_event_presence_det_prct), False)
        app_event_det_prct_mask_60_70  = np.full(np.shape(app_event_presence_det_prct), False)
        app_event_det_prct_mask_70_80  = np.full(np.shape(app_event_presence_det_prct), False)
        app_event_det_prct_mask_80_90  = np.full(np.shape(app_event_presence_det_prct), False)        
        app_event_det_prct_mask_90_100 = np.full(np.shape(app_event_presence_det_prct), False)
        app_event_det_prct_mask_0_60[app_event_presence_det_prct<=0.6] = True
        app_event_det_prct_mask_60_70[np.logical_and(app_event_presence_det_prct>0.6, app_event_presence_det_prct<=0.7)] = True
        app_event_det_prct_mask_70_80[np.logical_and(app_event_presence_det_prct>0.7, app_event_presence_det_prct<=0.8)] = True
        app_event_det_prct_mask_80_90[np.logical_and(app_event_presence_det_prct>0.8, app_event_presence_det_prct<=0.9)] = True
        app_event_det_prct_mask_90_100[app_event_presence_det_prct>0.9] = True    

        app_event_presence_det_prct_dict    = {'possible partitions': ['Fewer than 60%','Between 60-70 %','Between 70-80 %','Between 80-90 %','Between 90-100 %'], 'masks': [app_event_det_prct_mask_0_60,app_event_det_prct_mask_60_70,app_event_det_prct_mask_70_80,app_event_det_prct_mask_80_90,app_event_det_prct_mask_90_100]}
        desired_masks.update({"Per event: Presence event activity detection percent":app_event_presence_det_prct_dict})

    if "Presence seq duration prior to approach event end" in dataframe.columns:
        app_event_presence_duration_prior_to_end = dataframe['Presence seq duration prior to approach event end'].values.astype(object)
        app_event_presence_dur_prior_to_end_mask_0_30  = np.full(np.shape(app_event_presence_duration_prior_to_end), False)
        app_event_presence_dur_prior_to_end_mask_31_60 = np.full(np.shape(app_event_presence_duration_prior_to_end), False)
        app_event_presence_dur_prior_to_end_mask_61_90 = np.full(np.shape(app_event_presence_duration_prior_to_end), False)
        app_event_presence_dur_prior_to_end_mask_90_up = np.full(np.shape(app_event_presence_duration_prior_to_end), False)
        app_event_presence_dur_prior_to_end_mask_0_30[app_event_presence_duration_prior_to_end<=30] = True
        app_event_presence_dur_prior_to_end_mask_31_60[np.logical_and(app_event_presence_duration_prior_to_end>30, app_event_presence_duration_prior_to_end<=60)] = True
        app_event_presence_dur_prior_to_end_mask_61_90[np.logical_and(app_event_presence_duration_prior_to_end>60, app_event_presence_duration_prior_to_end<=90)] = True
        app_event_presence_dur_prior_to_end_mask_90_up[app_event_presence_duration_prior_to_end>90] = True

        app_event_presence_dur_prior_to_end_dict = {'possible partitions': ['Fewer than 30 frames','Between 31-60 frames','Between 61-90 frames','More than 90 frames'], 'masks': [app_event_presence_dur_prior_to_end_mask_0_30,app_event_presence_dur_prior_to_end_mask_31_60,app_event_presence_dur_prior_to_end_mask_61_90,app_event_presence_dur_prior_to_end_mask_90_up]}
        desired_masks.update({"Per event: Presence event activity first det duration from event end":app_event_presence_dur_prior_to_end_dict})

    if "Presence seq duration prior to approach event start" in dataframe.columns:
        app_event_presence_duration_from_app_start = dataframe['Presence seq duration from approach event start'].values.astype(object)
        app_event_presence_dur_from_start_mask_0_10  = np.full(np.shape(app_event_presence_duration_from_app_start), False)
        app_event_presence_dur_from_start_mask_11_20 = np.full(np.shape(app_event_presence_duration_from_app_start), False)
        app_event_presence_dur_from_start_mask_21_30 = np.full(np.shape(app_event_presence_duration_from_app_start), False)
        app_event_presence_dur_from_start_mask_31_up = np.full(np.shape(app_event_presence_duration_from_app_start), False)
        app_event_presence_dur_from_start_mask_0_10[app_event_presence_duration_from_app_start<=10] = True
        app_event_presence_dur_from_start_mask_11_20[np.logical_and(app_event_presence_duration_from_app_start>10, app_event_presence_duration_from_app_start<=20)] = True
        app_event_presence_dur_from_start_mask_21_30[np.logical_and(app_event_presence_duration_from_app_start>20, app_event_presence_duration_from_app_start<=30)] = True
        app_event_presence_dur_from_start_mask_31_up[app_event_presence_duration_from_app_start>30] = True

        app_event_presence_dur_from_start_dict   = {'possible partitions': ['Fewer than 16 frames','Between 16-45 frames','Between 46-105 frames','More than 105 frames'], 'masks': [app_event_presence_dur_from_start_mask_0_10,app_event_presence_dur_from_start_mask_11_20,app_event_presence_dur_from_start_mask_21_30,app_event_presence_dur_from_start_mask_31_up]}
        desired_masks.update({"Per event: Presence event activity first det duration from event start":app_event_presence_dur_from_start_dict})

    if "Approach pop up indication" in dataframe.columns:
        approach_pop_up_indication = dataframe['Approach pop up indication'].values.astype(object)
        app_event_pop_up_true  = np.full(np.shape(approach_pop_up_indication), False)
        app_event_pop_up_false = np.full(np.shape(approach_pop_up_indication), False)
        app_event_pop_up_true[approach_pop_up_indication==True]  = True
        app_event_pop_up_false[approach_pop_up_indication==False] = True

        app_event_pop_up_dict = {'possible partitions': ['Pop up approach','Regular approach'], 'masks': [app_event_pop_up_true,app_event_pop_up_false]}
        desired_masks.update({"Per event: Approach event pop up indication": app_event_pop_up_dict})


    if 0: # Histogram visualization for approach events
        import plotly.express as px
        #fig1 = px.histogram(app_event_presence_det_len)
        #fig1.layout.xaxis.title.text = 'Frames'
        #fig1.layout.title.text='Presence detected sequence length during approach event'

        #fig2 = px.histogram(app_event_presence_det_prct)
        #fig2.layout.xaxis.title.text = 'Percent'
        #fig2.layout.title.text='Presence detected sequence percentage out of approach event frame'

        counts, bins = np.histogram(app_event_presence_duration_prior_to_end/30, bins=20)
        bins = 0.5 * (bins[:-1] + bins[1:])
        fig3 = px.bar(x=bins, y=counts, labels={'x':'Seconds', 'y':'count'})
        fig3.layout.title.text='Presence detected sequence duration from end of approach event'
            
        fig33 = px.histogram(app_event_presence_duration_prior_to_end)
        fig33.layout.xaxis.title.text = 'Frames'
        fig33.layout.title.text='Presence detected sequence duration from end of approach event'

        #counts, bins = np.histogram(app_event_presence_duration_from_app_start/30, bins=20)
        #bins = 0.5 * (bins[:-1] + bins[1:])
        #fig4 = px.bar(x=bins, y=counts, labels={'x':'Seconds', 'y':'count'})
        #fig4.layout.title.text='Presence detected sequence duration from start of approach event'

        #fig44 = px.histogram(app_event_presence_duration_from_app_start)
        #fig44.layout.xaxis.title.text = 'Frames'
        #fig44.layout.title.text='Presence detected sequence duration from start of approach event'

        counts, bins = np.histogram(app_event_flicker_seq_num, bins=20)
        bins = 0.5 * (bins[:-1] + bins[1:])
        fig5 = px.bar(x=bins, y=counts, labels={'x':'True/false flicker sequence number', 'y':'count'})
        fig5.layout.title.text='Presence approach true/false flicker sequence number'

        fig55 = px.histogram(app_event_flicker_seq_num)
        fig55.layout.xaxis.title.text = 'True/false flicker sequence number'
        fig55.layout.title.text='Presence approach true/false flicker sequence number'

        fig6 = px.histogram(app_event_flicker_seq_mean_len)
        fig6.layout.xaxis.title.text = 'True/false flicker sequence mean length'
        fig6.layout.title.text='Presence approach true/false flicker sequence mean length'

        fig7 = px.histogram(app_event_flicker_seq_median_len)
        fig7.layout.xaxis.title.text = 'True/false flicker sequence median length'
        fig7.layout.title.text='Presence approach true/false flicker sequence median length'

        # Split 'total mis' to pop up and no pop up
        pop_up = dataframe['Approach pop up indication'].values.astype(object)
        total_mis_loc = np.where(app_event_presence_duration_prior_to_end/30==-2)[0]
        total_mis_pop_up_num = sum(pop_up[total_mis_loc])
        total_mis_regular_num = len(total_mis_loc) - total_mis_pop_up_num
        print('Total mis num = ' + str(len(total_mis_loc)) + 
        ', Total mis - pop up num = ' + str(total_mis_pop_up_num) + 
        ', Total mis - regular approaches num = ' + str(total_mis_regular_num))

        pop_up_reason = dataframe['Approach event pop up reason index'].values.astype(object)
        print('Total regular approaches = ' + str(len(np.where(pop_up==0)[0])) + 
        ', Total pop up approches = ' + str(len(pop_up_reason)-len(np.where(pop_up==0)[0])) + 
        ', Pop up reason 2 event num = ' + str(len(np.where(pop_up==2)[0])) + 
        ', Pop up reason 3 event num = ' + str(len(np.where(pop_up==3)[0])))


        fig3.show()
        fig4.show()

    if 0: # Figure of presence indication as a function of the frame num from end of approach event
        import plotly.express as px
        import plotly.graph_objects as go
        app_ind_from_end = dataframe['Approach_index_from_event_end_gt'].values.astype(object)
        det = dataframe['detection'].values.astype(object)
        min_val,max_val = [min(app_ind_from_end),max(app_ind_from_end)]
        app_mat = np.zeros((max_val - min_val,4))
        for ind in np.arange(max_val - min_val):
            app_mat[ind,0] = ind + min_val
            temp_loc = np.where(app_ind_from_end == (ind + min_val))
            temp_det = det[temp_loc]
            if len(temp_det)>0:
                app_mat[ind,1] = sum(temp_det)/len(temp_det)
            else:
                app_mat[ind,1] = 0
            app_mat[ind,3] = len(temp_det)
        app_mat[:,2] = 1 - app_mat[:,1]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=app_mat[:,0], y=app_mat[:,1],mode='lines',name='Presence pred=1'))
        fig.add_trace(go.Scatter(x=app_mat[:,0], y=app_mat[:,2],mode='lines',name='Presence pred=0'))
        fig.update_layout(title="Presence prediction vs. frame num from end of approach event",xaxis_title="Frames from last approach frame")
        fig.show()




    return desired_masks