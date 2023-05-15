import numpy as np
import pandas as pd


def refine_annotations(dataframe):
    """
    clean & encode multiple categories 
    """

    df_keys = list(dataframe.keys())

    # "Enviroment"
    annot_to_clean = 'Enviroment[header]'
    remapped_annot = annot_to_clean
    if annot_to_clean in df_keys:
        mapping = {value: value for value in dataframe[annot_to_clean].unique()}
        mapping.update({'Indoor ': 'Indoor'})
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[remapped_annot] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')
        
    # "Location"
    annot_to_clean = 'Location[header]'
    remapped_annot = annot_to_clean
    if annot_to_clean in df_keys:
        mapping = {value: value for value in dataframe[annot_to_clean].unique()}
        mapping.update({'Reception ': 'Reception'})
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[remapped_annot] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    # "Background_People_COMPRESSED"
    annot_to_clean = 'Background_People[sequence]'
    remapped_annot = annot_to_clean.replace('[sequence]', '_COMPRESSED[sequence]')
    if annot_to_clean in df_keys:
        mapping = {value: value for value in dataframe[annot_to_clean].unique()}
        mapping.update({'Empty': 'FALSE', 'One': 'TRUE', 'Few': 'TRUE', 'Crowded': 'TRUE', 'Several': 'TRUE'})
        # perform mapping to new categories, notice: old categories that are not found in the mapping dict are converted to NaN
        dataframe[remapped_annot] = dataframe[annot_to_clean].map(
            mapping).fillna('NA')

    return dataframe


def general_clip_and_sequence(dataframe, from_file=False):
    desired_masks = {}

    # refine annotations
    # ------------------
    dataframe = refine_annotations(dataframe)

    # header annotations (clip level)
    # -------------------------------
    annot_headers = [annot for annot in dataframe.keys() if '[header]' in annot]
    dummy_counter = 0
    desired_masks_annot_store = {}
    for annot_header in annot_headers:
        print(annot_header)
        annot = dataframe[annot_header]
        annot_header = annot_header.replace('[header]', '')
        annot = annot.fillna('NA')
        annot = annot.astype(str)
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

    # sequence annotations
    # --------------------
    dummy_counter = 0
    desired_masks_annot_store = {}
    annot_headers = [annot for annot in dataframe.keys() if '[sequence]' in annot]
    for annot_header in annot_headers:
        print(annot_header)
        annot = dataframe[annot_header]
        annot_header = annot_header.replace('[sequence]', '')
        annot = annot.fillna('NA')
        annot = annot.astype(str)
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

    # empty/non-empty
    # ---------------
    near_empty_clips = (dataframe['video'].str.contains('not_working'))
    empty_clips = (dataframe['video'].str.contains('Empty'))
    non_empty_clips = np.logical_not(near_empty_clips | empty_clips)

    empty_clips = {'possible partitions': [
        'near-empty', 'empty clips', 'non-empty clips'], 'masks': [near_empty_clips, empty_clips, non_empty_clips]}
    desired_masks_empty_clips = {'empty_clips': empty_clips}

    desired_masks.update(desired_masks_empty_clips)

    # Presence_ROI
    # ------------
    dataframe['Presence_ROI[sequence]'] = dataframe['Presence_ROI[sequence]'].map({"True": True, "False": False}).fillna('NA')
    Presence_ROI_TRUE = (dataframe['Presence_ROI[sequence]'] == True)
    Presence_ROI_FALSE = (dataframe['Presence_ROI[sequence]'] == False)
    Presence_ROI_NA = np.logical_not(Presence_ROI_TRUE | Presence_ROI_FALSE)

    Presence_ROI_masks = {'possible partitions': ['Presence_ROI_TRUE', 'Presence_ROI_FALSE', 'Presence_ROI_NA'], 'masks': [Presence_ROI_TRUE, Presence_ROI_FALSE, Presence_ROI_NA]}
    desired_masks_Presence_ROI = {'Presence_ROI': Presence_ROI_masks}

    desired_masks.update(desired_masks_Presence_ROI)

    # Activity_ROI
    # ------------
    dataframe['Activity_ROI[sequence]'] = dataframe['Activity_ROI[sequence]'].map({"True": True, "False": False}).fillna('NA')
    Activity_ROI_TRUE = (dataframe['Activity_ROI[sequence]'] == True)
    Activity_ROI_FALSE = (dataframe['Activity_ROI[sequence]'] == False)
    Activity_ROI_NA = np.logical_not(Activity_ROI_TRUE | Activity_ROI_FALSE)

    Activity_ROI_masks = {'possible partitions': ['Activity_ROI_TRUE', 'Activity_ROI_FALSE', 'Activity_ROI_NA'], 'masks': [Activity_ROI_TRUE, Activity_ROI_FALSE, Activity_ROI_NA]}
    desired_masks_Activity_ROI = {'Activity_ROI': Activity_ROI_masks}

    desired_masks.update(desired_masks_Activity_ROI)

    # Experiment_Subfolder
    # --------------------
    if dataframe['video'][0].split('/')[0] == 'Experiments':
        dataframe['Experiment_Subfolder'] = dataframe['video'].apply(lambda x: x.split('/')[1])

    current_annotation_categories = list(dataframe['Experiment_Subfolder'].unique())
    if len(current_annotation_categories) == 1:
        current_annotation_categories.append(
            'NOT_' + current_annotation_categories[0])
    masks = []
    for cat in current_annotation_categories:
        masks.append(np.array(dataframe['Experiment_Subfolder'] == cat))
    curr_desired_mask = {'possible partitions': [str(val) for val in current_annotation_categories], 'masks': masks}
    desired_masks_Experiment_Subfolder = {'Experiment_Subfolder': curr_desired_mask}

    desired_masks.update(desired_masks_Experiment_Subfolder) 

    # making sure there is no same 'possible partitions' for different partitions
    all_the_options = []
    for key in desired_masks:
        for option_list in desired_masks[key]['possible partitions']:
            all_the_options.append(option_list)
    assert len(all_the_options) == len(np.unique(all_the_options)
                                       ), 'two partition options cant have the same name'

    return desired_masks
