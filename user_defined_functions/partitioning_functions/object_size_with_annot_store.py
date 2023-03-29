import numpy as np
import pandas as pd


def refine_annotations(dataframe):
    """
    clean & encode multiple categories 
    """

    df_keys = list(dataframe.keys())

    # "User_Movement_Type"
    annot_to_clean = 'User_Movement_Type'
    annot_to_clean = annot_to_clean + '[header]'
    if annot_to_clean in df_keys:
        mapping = {'Approach_PC': 'far_from_PC',
                'Approach PC': 'far_from_PC', 'Walking_Unrelated': 'far_from_PC'}
        mapping.update({'Sitting_Down': 'near_PC',
                    'Leaving_PC': 'near_PC', 'Standing_Up': 'near_PC'})
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[annot_to_clean] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    # "User_Physical_Status"
    annot_to_clean = 'User_Physical_Status'
    annot_to_clean = annot_to_clean + '[header]'
    if annot_to_clean in df_keys:
        mapping = {'Standing ': 'Standing', 'Moving ': 'Moving',
                'Sitting': 'Sitting', 'Sitting ': 'Sitting', 'Stnading ': 'Standing'}
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[annot_to_clean] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    # "Light"
    annot_to_clean = 'Light'
    annot_to_clean = annot_to_clean + '[header]'
    if annot_to_clean in df_keys:
        invalid_entry = 'FilePath\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    Indoor_1\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    Indoor_1\nName: Light, dtype: object'
        mapping = {value: value for value in dataframe[annot_to_clean].unique(
        ) if value != invalid_entry}
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[annot_to_clean] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    # "location"
    annot_to_clean = 'location'
    annot_to_clean = annot_to_clean + '[header]'
    if annot_to_clean in df_keys:
        invalid_entry = 'FilePath\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    Public space\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    Public space\nName: Location, dtype: object'
        mapping = {value: value for value in dataframe[annot_to_clean].unique(
        ) if value != invalid_entry}
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[annot_to_clean] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    # "background people"
    annot_to_clean = 'background people'
    annot_to_clean = annot_to_clean + '[header]'
    if annot_to_clean in df_keys:
        invalid_entry = 'FilePath\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    1\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    1\nName: background_people, dtype: int64'
        mapping = {value: value for value in dataframe[annot_to_clean].unique(
        ) if value != invalid_entry}
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[annot_to_clean] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    # "background"
    annot_to_clean = 'background'
    annot_to_clean = annot_to_clean + '[header]'
    if annot_to_clean in df_keys:
        invalid_entry = 'FilePath\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    0\n\\\\il-filer\\R&D&E\\System\\DS\\Recordings\\Presence\\Dynamic background\\Dynamic_kitchen_working_1.mp4    0\nName: background, dtype: int64'
        mapping = {value: value for value in dataframe[annot_to_clean].unique(
        ) if value != invalid_entry}
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[annot_to_clean] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    return dataframe


def object_size_with_annot_store(dataframe, from_file=False):
    # annot_headers = ['Experiment_Name ', 'Enviroment', 'Location', 'Human_Presence', 'General_Background_People', 'General_User_Description',
    #                  'General_Background_Description', 'General_Device_Use', 'General_Natural_Light', 'General_Artificial_Light', 'Reflection', 'Device_Posture', 'Sensor', 'File_type']
    # annot_headers = ['Enviroment', 'Location']
    # annot_headers = ['Enviroment', 'Location']
    annot_headers = ['Enviroment', 'Location', 'User_Movement_Type',
                     'User_Physical_Status', 'Light', 'location', 'background people', 'background']

    annot_headers = [val + '[header]' for val in annot_headers]

    img_width = 1920
    img_height = 1080

    # object_size: small / medium / large
    # -----------------------------------
    tiny_object_pct = 0.052  # 100px @1920
    small_object_pct = 0.15625  # 300px @1920
    large_object_pct = 0.3125  # 600px @1920

    type_ = float if from_file else object
    label_width = dataframe['width_gt'].values.astype(type_)
    prd_width = dataframe['width'].values.astype(type_)

    # build conditions
    gt_exists = dataframe['detection_gt'].notnull().values.astype('bool')
    tiny_obejcts = ((label_width <= (tiny_object_pct * img_width)) & gt_exists) | (
        (prd_width < (tiny_object_pct * img_width)) & np.logical_not(gt_exists))
    small_obejcts = (((label_width < (small_object_pct * img_width)) & (label_width > (tiny_object_pct * img_width))) & gt_exists) | (
        ((prd_width < (small_object_pct * img_width)) & (prd_width > (tiny_object_pct * img_width))) & np.logical_not(gt_exists))
    large_obejcts = ((label_width > (large_object_pct * img_width)) & gt_exists) | (
        (prd_width > (large_object_pct * img_width)) & np.logical_not(gt_exists))
    medium_objects = np.logical_not(
        (tiny_obejcts | small_obejcts | large_obejcts))

    size = {'possible partitions': [
        'tiny', 'small', 'medium', 'large'], 'masks': [tiny_obejcts, small_obejcts, medium_objects, large_obejcts]}

    desired_masks = {'size': size}

    # annotation store
    # ----------------
    dataframe = refine_annotations(dataframe)

    dummy_counter = 0
    desired_masks_annot_store = {}
    for annot_header in annot_headers:
        print(annot_header)
        annot = dataframe[annot_header]
        annot_header = annot_header.replace('[header]', '')
        current_annotation_categories = list(annot.unique())
        # this is a patch to correct mixed numeric/string annotation
        if annot_header in ['User_Movement_Type', 'User_Physical_Status', 'Light', 'location', 'background people', 'background']:
            current_annotation_categories = list(
                set([str(i) for i in current_annotation_categories]))
            annot = annot.astype(str)
        # next steps of tool fails in case of single category --> add fake empty annotation, for example: "NOT_Indoor"
        if len(current_annotation_categories) == 1:
            current_annotation_categories.append(
                'NOT_' + current_annotation_categories[0])
        masks = []
        for cat in current_annotation_categories:
            dummy_counter += 1
            masks.append(np.array(annot == cat))
        curr_desired_mask = {'possible partitions': [str(
            val) + '_[' + str(annot_header) + ']' for val in current_annotation_categories], 'masks': masks}
        desired_masks_annot_store[annot_header] = curr_desired_mask

    desired_masks.update(desired_masks_annot_store)

    # person on edges
    # ---------------
    elongation_ratio_medium = 2
    elongation_ratio_high = 3
    margin_px = 20

    gt_bb_on_boundary = ((dataframe['x_gt'] < 0 + margin_px) | (
        dataframe['x_gt'] + dataframe['width_gt'] > img_width - margin_px))
    prd_bb_on_boundary = ((dataframe['x'] < 0 + margin_px) | (
        dataframe['x'] + dataframe['width'] > img_width - margin_px))

    gt_high_elongation = (
        (dataframe['height_gt'] / dataframe['width_gt']) > elongation_ratio_high) & gt_bb_on_boundary
    gt_medium_elongation = ((dataframe['height_gt'] / dataframe['width_gt']) > elongation_ratio_medium) & (
        (dataframe['height_gt'] / dataframe['width_gt']) <= elongation_ratio_high) & gt_bb_on_boundary
    gt_low_elongation = np.logical_not(
        (gt_high_elongation | gt_medium_elongation)) & gt_bb_on_boundary
    gt_inside = np.logical_not(gt_bb_on_boundary)

    prd_high_elongation = (
        (dataframe['height'] / dataframe['width']) > elongation_ratio_high) & prd_bb_on_boundary
    prd_medium_elongation = ((dataframe['height'] / dataframe['width']) > elongation_ratio_medium) & (
        (dataframe['height'] / dataframe['width']) <= elongation_ratio_high) & prd_bb_on_boundary
    prd_low_elongation = np.logical_not(
        (prd_high_elongation | prd_medium_elongation)) & prd_bb_on_boundary
    prd_inside = np.logical_not(prd_bb_on_boundary)

    high_elongation = (gt_exists & gt_high_elongation) | (
        np.logical_not(gt_exists) & prd_high_elongation)
    medium_elongation = (gt_exists & gt_medium_elongation) | (
        np.logical_not(gt_exists) & prd_medium_elongation)
    low_elongation = (gt_exists & gt_low_elongation) | (
        np.logical_not(gt_exists) & prd_low_elongation)
    inside = (gt_exists & gt_inside) | (np.logical_not(gt_exists) & prd_inside)

    boundary = {'possible partitions': ['inside', 'low_elongation_on_boundary', 'medium_elongation_on_boundary',
                                        'high_elongation_on_boundary'], 'masks': [inside, low_elongation, medium_elongation, high_elongation]}

    desired_masks_boundary = {'boundary': boundary}

    desired_masks.update(desired_masks_boundary)

    # clip duration binning
    # ---------------------
    bins = [0, 5/60, 10/60, 0.5, 1, 10, 20, 999999999]
    labels = ['0-5sec', '5-10sec', '10-30sec',
              '0.5-1min', '1-10min', '10-20min', '>20min']

    time_vals = pd.DatetimeIndex(dataframe['Clip_Duration [MIN]2[header]'])
    dataframe['Clip_Duration_Minutes[header]'] = time_vals.hour * \
        60 + time_vals.minute + time_vals.second / 60

    dataframe['Clip_Duration_Minutes_Binned[header]'] = pd.cut(
        dataframe['Clip_Duration_Minutes[header]'], bins=bins, labels=labels)
    dataframe['Clip_Duration_Minutes_Binned[header]'] = dataframe['Clip_Duration_Minutes_Binned[header]'].values.add_categories(
        'missing duration')
    dataframe['Clip_Duration_Minutes_Binned[header]'].fillna(
        'missing duration', inplace=True)
    labels = labels + ['missing duration']
    masks = []
    for label in labels:
        curr_mask = (
            dataframe['Clip_Duration_Minutes_Binned[header]'] == label)
        masks.append(curr_mask)

    clip_duration = {'possible partitions': labels, 'masks': masks}
    desired_masks_clip_duration = {'clip_duration': clip_duration}

    desired_masks.update(desired_masks_clip_duration)

    # iou
    # ---
    bins = [-1, 0, 0.25, 0.5, 0.75, 1.1]
    labels = ['0', '0-0.25', '0.25-0.5', '0.5-0.75', '0.75-1']

    dataframe['iou_binned'] = pd.cut(
        dataframe['iou'], bins=bins, labels=labels)
    dataframe['iou_binned'] = dataframe['iou_binned'].values.add_categories(
        'missing iou')
    dataframe['iou_binned'].fillna('missing iou', inplace=True)
    labels = labels + ['missing iou']
    masks = []
    for label in labels:
        curr_mask = (dataframe['iou_binned'] == label)
        masks.append(curr_mask)

    iou = {'possible partitions': labels, 'masks': masks}
    desired_masks_iou = {'iou': iou}

    desired_masks.update(desired_masks_iou)

    # empty/non-empty
    # ---------------
    bins = ['~empty clips', 'non-empty clips']
    labels = ['near-empty', 'empty clips', 'non-empty clips']

    near_empty_clips = (dataframe['video'].str.contains('not_working'))
    empty_clips = (dataframe['video'].str.contains('Empty'))
    non_empty_clips = np.logical_not(near_empty_clips | empty_clips)

    empty_clips = {'possible partitions': [
        'near-empty', 'empty clips', 'non-empty clips'], 'masks': [near_empty_clips, empty_clips, non_empty_clips]}
    desired_masks_empty_clips = {'empty_clips': empty_clips}

    desired_masks.update(desired_masks_empty_clips)

    # making sure there is no same 'possible partitions' for different partitions
    all_the_options = []
    for key in desired_masks:
        for option_list in desired_masks[key]['possible partitions']:
            all_the_options.append(option_list)
    assert len(all_the_options) == len(np.unique(all_the_options)
                                       ), 'two partition options cant have the same name'

    return desired_masks
