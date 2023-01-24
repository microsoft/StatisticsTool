import math
import pathlib
import pandas as pd, os, numpy as np, base64, matplotlib, re
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2
import matplotlib.patches as mpatches
from io import BytesIO
from classes_and_utils.utils import loading_json


# Irit's totos:
# todo return number of processed files on GUI
# todo automatically make sure every bounding box was processed (make sure we didn't forget any bounding box)

# Ben's todo:
# todo return number of prediction bounding boxes that didn't have a GT at all

class ParallelExperiment:
    """
    A class that combines the intermediate results from individual videos into two large data structures,
    one for predictions and one for GT, and returns segmented statistics,
    segmented list of bounding boxes ids, example images with bounding box overlay from the entire experiment

    ...

    Attributes:
    ----------
        inputs:
        ----------
        files_dir : str
            Path to intermediate results folder
        statistic_funcs : function
            A function that wraps all the statistics (e.g precision - recall) needed. example in statisticsFunctions.py
        segmentation_funcs : function
            A function that partition the data (e.g day/night, bus/car/person). example in partitioningFunctions.py
        save_stats_dir : str
            path to 'saved by user' folder in the output folder - this is where the images, tables, and lists that are
             saved in the GUI are stored

        non inputs (internal):
        ----------
        masks : dictionary
            A dictionary that contains boolean arrays that indicates which bounding box belongs to which partitions and which TP/FP/FN
            for example: {'total_stats': {'TP': TP_bolean_mask, ... }, 'size':{'possible partitions': ['large', 'small'], 'prediction masks': [prd_large_mask, prd_small_mask], 'labels masks': [label_large_mask, label_small_mask]}}
        ID_storage : dictionary
            A dictionary that holds the ids of bounding boxes in two arrays (id = (video name, index in original data structure, frame number))
            the keys are 'prediction', 'labels' (one array for predictions and one for labels)
        segmented_ID : dictionary
            A dictionary that holds the id's for the segmented examples.
            for one partition: id_dict = {'primary partition option 1':{'TP': array_of_TP_ids, 'FP': array_of_FP_ids ....}, 'primary partition option 2' : {'TP': array_of_TP_ids, 'FP': array_of_FP_ids ....}]
            for two partitions : id dict = {'primary partition option 1':{'secondary partition option 1':{'TP': array_of_TP_ids, 'FP': array_of_FP_ids ....} ....} ....}
            theres also an option for 3 partitions by the same logic
        combined_prd_dataframe : pandas dataframe
            Aggregation of all the videos prediction data in a single dataframe
        combined_label_dataframe : pandas dataframe
            Aggregation of all the videos label data in a single dataframe
        state : str
            indicates if the requested example is TP/FP/FN
        label_or_prd : str
            indicates if the requested example is a prediction or label

    Methods
    -------
    OneFileProcedure(filename)
        Loads a single video intermediate results, and aggregates two dataframes with bounding box data,
        one for predictions and one for ground truth

    combine_from_text(save_dataframe=False)
        Iterates over all the single video results in self.files_dir and aggregate them
        into two dataframes  one for predictions and one for ground truth

    get_TP_FP_FN_masks(prd_state, label_state, threshold, from_file=False)
        Aceepts the 'state' column of the preditions and labels aggregated dataframe and return boolean masks of TP/FP/FN

    get_segmentation_masks(threshold, from_file=False, label_file_dir=None, prd_file_dir=None)
        Calculates the bolean segmentation masks (self.masks) and the ids of prediction/labels (self.ID_storage)

    statistics_visualization(primary_segmentation=None, secondary_segmentation=None, tertiary_segmentations=None , show_total_stats=None, save=False)
        Return the segmented statistics and id_dict for GUI needs

    get_ids(id_dict, state='TP', total=False, primary=None, secondary=None, tertiary=None)
        Return the ids of examples that belongs to a certein partition (and sub partitions)

    frame_visualization(frame_labels, frame_prds, wanted_bb, matched, image)
        Returns an image of a frame and the bounding boxes of the frame are overlayed on top
        (selected bounding box and its match has a thick frame)

    is_label_or_prd()
        Returns self.label_or_prd

    visualize(bb_id, from_file=False, label_file_dir=None, prd_file_dir=None)
        Accepts a bb_id and display its frame by calling self.frame_visualization()

    """
    def __init__(self, statistic_funcs, files_dir, save_stats_dir, image_width, image_height,segmentation_funcs,video_annotation_dict, overlap_function, evaluation_function):
        self.files_dir = files_dir
        self.statistic_funcs = statistic_funcs
        self.evaluation_function = evaluation_function
        self.overlap_function = overlap_function
        self.save_stats_dir = save_stats_dir
        self.segmentation_funcs = segmentation_funcs
        self.masks = None
        self.ID_storage = {}
        self.segmented_ID = {}
        self.image_width = int(image_width)
        self.image_height = int(image_height)
        self.video_annotation_dict = video_annotation_dict
        
    
        



    def combine_from_text(self, save_dataframe=False):
        """
        Agrregates the data from the intermediate results folder to two dataframes one for predictions and one for GT

        :param save_dataframe: Boolean, whether to save the aggregated Dataframes, default: false

        """
        saved_files_paths = [file for file in os.listdir(self.files_dir)]
        
        datafrme_dict = []
        for file_name in saved_files_paths:
            df = pd.read_json (os.path.join(self.files_dir, file_name))
            datafrme_dict.append(df)
            continue
          
        # concatenate the dictionary of dataframes into a single dataframe
        self.comp_data = pd.concat(datafrme_dict).reset_index(drop=True)
              
        if save_dataframe:
            self.combined_prd_dataframe.to_csv(os.path.join(self.save_stats_dir, 'combined prediction dataframe.csv'))
            self.combined_label_dataframe.to_csv(os.path.join(self.save_stats_dir, 'combined labels dataframe.csv'))

    @staticmethod
    def get_TP_FP_FN_masks(comp_data, threshold, from_file=False):
        """

        :param prd_state: state column (which containts either overlap float or FP ) of the aggregated predictions, dataframe self.combined_prd_dataframe
        :param label_state: state column (which containts either overlap float or FN ) of the aggregated labels, dataframe self.combined_label_dataframe
        :param threshold: float , above this value an overlap is considered a hit (the prediction will be TP)
        :param from_file: Boolean, indicates whether the dataframe was loaded from a saved file, default: false
        :return: Boolean masks of TP, FP, FN that indicates which row in the predictions dataframe is TP/FP
                 and which row in the labels dataframe is a FN (row = bounding box)
        """
        #first key from 'detection' key in input
        key = 'detection'
        FN_mask = ((comp_data[key+'_gt']==True) & ((comp_data['state']<threshold) | (comp_data[key]==False) ))
        FP_mask = ((comp_data[key]==True) & (comp_data['state']<threshold))
        TP_mask = ((comp_data[key]==True) &((comp_data['state']>=threshold) & (comp_data[key+'_gt']==True)))
        
        return TP_mask, FP_mask, FN_mask
               

    def get_segmentation_masks(self, threshold, from_file=False, label_file_dir=None, prd_file_dir=None):
        """
        Calculates the boolean segmentation masks (self.masks) and the ids of prediction/labels (self.ID_storage)

        :param threshold: float , above this value an overlap is considered a hit (the prediction will be TP)
        :param from_file: Boolean, indicates whether the dataframe should be loaded from a saved file, default: false
        :param label_file_dir: The path in which to load the saved label file , default: None
        :param prd_file_dir: The path in which to load the saved prediction file , default: None
        """
        assert threshold >= 0, 'threshold should be a positive number'
        if from_file:
            assert label_file_dir and prd_file_dir, 'if loading from file is selected than the label and prediction paths are needed'
            self.combined_prd_dataframe = pd.read_csv(os.path.join(self.save_stats_dir, prd_file_dir))
            self.combined_label_dataframe = pd.read_csv(os.path.join(self.save_stats_dir, label_file_dir))

        # calculate the boolean masks of TP/FP/FN (which row/bounding box in the dataframes is TP/FP/FN)
        TP_mask, FP_mask, FN_mask = self.get_TP_FP_FN_masks(self.comp_data, threshold, from_file)
        # calculate the boolean masks of the partitions (which row/bounding box in the dataframes belongs to which partition)
        self.wanted_segmentations = self.segmentation_funcs(self.comp_data, from_file)
        # initialize self.masks with the total masks for TP/FP/FN
        self.masks = {'total_stats': {'TP': TP_mask, 'FP': FP_mask, 'FN': FN_mask}}
        # Add the segmentation masks to self.masks
        self.masks.update(self.wanted_segmentations)

        video_name = self.comp_data['video'].values.copy()[:, np.newaxis]
        frame = self.comp_data['frame_id'].values.astype(int).copy()[:, np.newaxis] 
        index = self.comp_data.index.to_series().values.copy()[:, np.newaxis]
        if 'end_frame' in self.comp_data.keys():
            end_frames = self.comp_data['end_frame'].values.astype(int).copy()[:, np.newaxis]
        else:
            end_frames = frame
        
        self.ID_storage['prediction'] = np.concatenate((video_name, index, frame, end_frames), axis=1)
        
        self.ID_storage['label'] = self.ID_storage['prediction']


    def statistics_visualization(self, primary_segmentation=None, secondary_segmentation=None, tertiary_segmentation=None):
        """
        Calculates the segmented statistics and the relevant examples (self.segmented_ID)

        :param primary_segmentation: name of the #1 partition asked for in the GUI
        :param secondary_segmentation: name of the #2 partition asked for in the GUI
        :param tertiary_segmentation: name of the #3 partition asked for in the GUI
        :return: The segmented statistic and segmented states as dictionaries and as dataframes (statistics_df, state_df, statistics_dict, state_dict)

        """
        # if the primary partition is None then the function returns the none segmented statistics (total statistics) and examples
        if primary_segmentation is None:
            # the amount of TP/FP/FN is the sum of True booleans in the appropriate place in self.masks
            TP, FP, FN = sum(self.masks['total_stats']['TP']), sum(self.masks['total_stats']['FP']), sum(self.masks['total_stats']['FN'])
            # calculating the statistics
            if self.statistic_funcs.__name__=='presence_leave_flicker_seq_count':
                statistics_dict = {'Leave Flicker Count': len(self.comp_data['Presence leave flicker sequence num'])}
            elif self.statistic_funcs.__name__=='presence_approach_flicker_seq_count':
                statistics_dict = {'Approach Flicker Count': len(self.comp_data['Presence approach flicker sequence num'])}
            elif self.statistic_funcs.__name__=='sep_seq_count':
                if 'Separate FN sequence count' in self.comp_data.keys():
                    statistics_dict = {'Separate FN Sequence Count': sum(self.comp_data['Separate FN sequence count'])}
                else:
                    statistics_dict = {'Separate FP Sequence Count': sum(self.comp_data['Separate FP sequence count'])}
            else:
                statistics_dict = self.statistic_funcs(TP, FP, FN, len(self.comp_data['frame_id']))
            state_dict = {'TP': TP, 'FP': FP, 'FN': FN, 'TOTAL_PRED': len(self.comp_data['frame_id'])}
            # getting the ids of the TP/FP/FN examples
            self.segmented_ID['total'] = {'TP': self.ID_storage["prediction"][self.masks['total_stats']['TP']], 'FP': self.ID_storage['prediction'][self.masks['total_stats']['FP']], 'FN': self.ID_storage['label'][self.masks['total_stats']['FN']]}
            # turning the dictionaries into pandas dataframes
            statistics_df = pd.DataFrame(statistics_dict, index=[0])
            state_df = pd.DataFrame(state_dict, index=[0])

        # if the primary partition is not None then segmented statistics and examples are calculated
        else:
            assert primary_segmentation in self.masks.keys(), 'Primary segmentation should be based on the keys of the self.masks dictionary'
            assert secondary_segmentation in self.masks.keys() or secondary_segmentation is None, 'secondary segmentation should be based on the keys of the self.masks dictionary'
            assert tertiary_segmentation in self.masks.keys() or tertiary_segmentation is None, 'tertiary_segmentation should be based on the keys of the self.masks dictionary'

            # possible partitions for the primary partition (e.g if the primary example is 'size' then possible partitions will be 'big' and 'small')
            prime_possible_partitions = self.masks[primary_segmentation]['possible partitions']
            statistics_dict, state_dict = {}, {}
            # if primary segmentation is not None and secondary segmentation is None then only one partition is asked for
            if secondary_segmentation is None:
                for i, seg_name in enumerate(prime_possible_partitions):
                    # for a specific partition, the partitioned - TP mask is the element wise multiplication between the total TP mask and the partition mask (same for FP/FN)
                    TP_mask = self.masks['total_stats']['TP'] & self.masks[primary_segmentation]['masks'][i]
                    FP_mask = self.masks['total_stats']['FP'] & self.masks[primary_segmentation]['masks'][i]
                    FN_mask = self.masks['total_stats']['FN'] & self.masks[primary_segmentation]['masks'][i]
                    # the number of TP is the sum of the mask (same for FP/FN)
                    num_TP, num_FP, num_FN = np.sum(TP_mask), np.sum(FP_mask), np.sum(FN_mask)
                    total_preds = sum(self.masks[primary_segmentation]['masks'][i])
                    # calculating the statistics
                    if self.statistic_funcs.__name__=='presence_leave_flicker_seq_count':
                        temp_stat_d = {'Leave Flicker Count': total_preds}
                    elif self.statistic_funcs.__name__=='presence_approach_flicker_seq_count':
                        temp_stat_d = {'Approach Flicker Count': total_preds}
                    elif self.statistic_funcs.__name__=='sep_seq_count':
                        if 'Separate FN sequence count' in self.comp_data.keys():
                            temp_stat_d = {'Separate FN Sequence Count': sum(self.comp_data['Separate FN sequence count']*FN_mask)}
                        else:
                            temp_stat_d = {'Separate FP Sequence Count': sum(self.comp_data['Separate FP sequence count']*FP_mask)}
                    else:
                        temp_stat_d = self.statistic_funcs(num_TP, num_FP, num_FN, total_preds)
                    temp_stat_d.update({'TOTAL_PREDS':total_preds})
                    # updating the statistics and state dictionaries with tuple keys that allow multi-indexing in pandas
                    statistics_dict.update({(seg_name, stat_name): temp_stat_d[stat_name] for stat_name in temp_stat_d})
                    state_dict.update({(seg_name, name): stat for name, stat in zip(['TP', 'FP', 'FN'], [num_TP, num_FP, num_FN])})
                    # update self.segmented_ID with the relevent example that belongs to the current partition - TP/FP/FN
                    self.segmented_ID[seg_name] = {'TP': self.ID_storage["prediction"][TP_mask], 'FP': self.ID_storage['prediction'][FP_mask], 'FN': self.ID_storage['label'][FN_mask]}

                # Constructing multi-index dataframes from the statistics/state dictionaries (this is what we save when the user ask to save the table in the GUI)
                index = pd.MultiIndex.from_tuples([tup for tup in statistics_dict], names=['Primary', 'Statistics'])
                statistics_df = pd.DataFrame(statistics_dict.values(), index=index)
                statistics_df = statistics_df.unstack(level=1)
                index2 = pd.MultiIndex.from_tuples([tup for tup in state_dict], names=['Primary', 'Statistics'])
                state_df = pd.DataFrame(state_dict.values(), index=index2)

            # if the primary and secondary partitions are asked for (not None) and the tertiary is None
            elif secondary_segmentation and tertiary_segmentation is None:
                # possible partitions for the secondary partition
                sec_possible_partitions = self.masks[secondary_segmentation]['possible partitions']
                for i, seg_name in enumerate(prime_possible_partitions):
                    self.segmented_ID[seg_name] = {}
                    for j, seg_name2 in enumerate(sec_possible_partitions):
                        # for a specific sub partition, the partitioned - TP mask is the element wise multiplication between the total TP mask and the two partitions masks (same for FP/FN)
                        TP_mask = self.masks['total_stats']['TP'] & self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j]
                        FP_mask = self.masks['total_stats']['FP'] & self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j]
                        FN_mask = self.masks['total_stats']['FN'] & self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j]
                        # the number of TP is the sum of the mask (same for FP/FN)
                        num_TP, num_FP, num_FN = np.sum(TP_mask), np.sum(FP_mask), np.sum(FN_mask)
                        total_preds = sum(self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j])
                        # calculating the statistics
                        if self.statistic_funcs.__name__=='presence_leave_flicker_seq_count':
                            temp_stat_d = {'Leave Flicker Count': total_preds}
                        elif self.statistic_funcs.__name__=='presence_approach_flicker_seq_count':
                            temp_stat_d = {'Approach Flicker Count': total_preds}
                        elif self.statistic_funcs.__name__=='sep_seq_count':
                            if 'Separate FN sequence count' in self.comp_data.keys():
                                temp_stat_d = {'Separate FN Sequence Count': sum(self.comp_data['Separate FN sequence count']*FN_mask)}
                            else:
                                temp_stat_d = {'Separate FP Sequence Count': sum(self.comp_data['Separate FP sequence count']*FP_mask)}
                        else:
                            temp_stat_d = self.statistic_funcs(num_TP, num_FP, num_FN, total_preds)
                        temp_stat_d.update({'TOTAL_PREDS':total_preds})
                        # updating the statistics and state dictionaries with tuple keys that allow multi-indexing in pandas
                        statistics_dict.update({(seg_name, seg_name2, stat_name): temp_stat_d[stat_name] for stat_name in temp_stat_d})
                        state_dict.update({(seg_name, seg_name2, name): stat for name, stat in zip(['TP', 'FP', 'FN'], [num_TP, num_FP, num_FN])})
                        # update self.segmented_ID with the relevant example that belongs to the current sub partition - TP/FP/FN
                        self.segmented_ID[seg_name][seg_name2] = {'TP': self.ID_storage["prediction"][TP_mask], 'FP': self.ID_storage['prediction'][FP_mask], 'FN': self.ID_storage['label'][FN_mask]}

                # Constructing multi-index dataframes from the statistics/state dictionaries (this is what we save when the user ask to save the table in the GUI)
                index = pd.MultiIndex.from_tuples([tup for tup in statistics_dict], names=['Primary', 'Secondary ', 'Statistics'])
                statistics_df = pd.DataFrame(statistics_dict.values(), index=index)
                statistics_df = statistics_df.unstack(level=1)
                index2 = pd.MultiIndex.from_tuples([tup for tup in state_dict], names=['Primary', 'Secondary', 'Statistics'])
                state_df = pd.DataFrame(state_dict.values(), index=index2)

            # if all three partitions are asked for (not None)
            else:
                # possible partitions for the secondary and tertiary partition
                sec_possible_partitions = self.masks[secondary_segmentation]['possible partitions']
                tert_possible_partitions = self.masks[tertiary_segmentation]['possible partitions']
                for i, seg_name in enumerate(prime_possible_partitions):
                    self.segmented_ID[seg_name] = {}
                    for j, seg_name2 in enumerate(sec_possible_partitions):
                        self.segmented_ID[seg_name][seg_name2] = {}
                        for k, seg_name3 in enumerate(tert_possible_partitions):
                            # for a specific sub-sub partition, the partitioned - TP mask is the element wise multiplication between the total TP mask and the three partitions masks (same for FP/FN)
                            TP_mask = self.masks['total_stats']['TP'] & self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j] & self.masks[tertiary_segmentation]['masks'][k]
                            FP_mask = self.masks['total_stats']['FP'] & self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j] & self.masks[tertiary_segmentation]['masks'][k]
                            FN_mask = self.masks['total_stats']['FN'] & self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j] & self.masks[tertiary_segmentation]['masks'][k]
                            # the number of TP is the sum of the mask (same for FP/FN)
                            num_TP, num_FP, num_FN = np.sum(TP_mask), np.sum(FP_mask), np.sum(FN_mask)
                            total_preds = sum(self.masks[primary_segmentation]['masks'][i] & self.masks[secondary_segmentation]['masks'][j] & self.masks[tertiary_segmentation]['masks'][k])
                            # calculating the statistics
                            if self.statistic_funcs.__name__=='presence_leave_flicker_seq_count':
                                temp_stat_d = {'Leave Flicker Count': total_preds}
                            elif self.statistic_funcs.__name__=='presence_approach_flicker_seq_count':
                                temp_stat_d = {'Approach Flicker Count': total_preds}
                            elif self.statistic_funcs.__name__=='sep_seq_count':
                                if 'Separate FN sequence count' in self.comp_data.keys():
                                    temp_stat_d = {'Separate FN Sequence Count': sum(self.comp_data['Separate FN sequence count']*FN_mask)}
                                else:
                                    temp_stat_d = {'Separate FP Sequence Count': sum(self.comp_data['Separate FP sequence count']*FP_mask)}
                            else:
                                temp_stat_d = self.statistic_funcs(num_TP, num_FP, num_FN, total_preds)
                            temp_stat_d.update({'TOTAL_PREDS':total_preds})
                            # updating the statistics and state dictionaries with tuple keys that allow multi-indexing in pandas
                            statistics_dict.update({(seg_name, seg_name2, seg_name3, stat_name): temp_stat_d[stat_name] for stat_name in temp_stat_d})
                            state_dict.update({(seg_name, seg_name2, seg_name3, name): stat for name, stat in zip(['TP', 'FP', 'FN'], [num_TP, num_FP, num_FN])})
                            # update self.segmented_ID with the relevant example that belongs to the current sub-sub partition - TP/FP/FN
                            self.segmented_ID[seg_name][seg_name2][seg_name3] = {'TP': self.ID_storage["prediction"][TP_mask], 'FP': self.ID_storage['prediction'][FP_mask], 'FN': self.ID_storage['label'][FN_mask]}

                # Constructing multi-index dataframes from the statistics/state dictionaries (this is what we save when the user ask to save the table in the GUI)
                index = pd.MultiIndex.from_tuples([tup for tup in statistics_dict], names=['Primary', 'Secondary', 'Tertiary', 'Statistics'])
                statistics_df = pd.DataFrame(statistics_dict.values(), index=index)
                statistics_df = statistics_df.unstack(level=1)
                index2 = pd.MultiIndex.from_tuples([tup for tup in state_dict], names=['Primary', 'Secondary', 'Tertiary', 'Statistics'])
                state_df = pd.DataFrame(state_dict.values(), index=index2)

        return statistics_df, state_df, statistics_dict, state_dict

    def get_ids(self, show_unique, state, total=False, primary=None, secondary=None, tertiary=None):
        """
        This function returns the ids of examples that belongs to the asked partitions and state (TP/FP/FN)

        :param state: The state (TP/FP/FN) in which its examples ids are wanted
        :param total: Boolean, wheather to show the total statistics - without partitions
        :param primary: #1 partition asked for
        :param secondary: #2 partition asked for
        :param tertiary: #3 partition asked for
        :return: return the ids of the examples that belongs to the requested state and partitions
        """

        if not show_unique:
            segments = self.segmented_ID
        else:
            segments = self.unique
        # used in is_label_or_prd()
        self.state = state
        # if total experiment examples are asked
        if total:
            return segments['total'][state]

        

        

        assert primary in segments or primary is None, 'primary must be one of id_dict keys or None'
        if secondary:
            assert secondary in segments[primary], 'secondary must be one of id_dict[primary] keys or None'
        if tertiary:
            assert tertiary in segments[primary][secondary], 'tertiary must be one of id_dict[primary][secondary] keys or None'

        if primary:
            # if only a primary partition is chosen
            if not secondary:
                # if 'TP' is a key in segments[primary] it means that there is no second partitions in segments
                if 'TP' in segments[primary]:
                    return segments[primary][state]

                # there is at least a second partition in segments
                sec_keys = list(segments[primary].keys())
                # the first option in the second partition options in segments
                first_key = sec_keys[0]
                # if 'TP' is a key in segments[primary][first_key] it means that there is no third partitions in segments
                if 'TP' in segments[primary][first_key]:
                    # aggregate the ids
                    ids = segments[primary][first_key][state]
                    for i in range(1,len(sec_keys)):
                        ids = np.concatenate((ids, segments[primary][sec_keys[i]][state]), axis=0)
                    return ids

                # there is a third partition in segments
                tert_keys = list(segments[primary][first_key].keys())
                # aggregate the ids
                for i in range(len(sec_keys)):
                    for j in range(len(tert_keys)):
                        if i == j == 0:
                            ids = segments[primary][sec_keys[i]][tert_keys[j]][state]
                        else:
                            ids = np.concatenate((ids, segments[primary][sec_keys[i]][tert_keys[j]][state]), axis=0)
                return ids

            # if a primary and a secondary partitions are chosen but not a tertiary
            elif not tertiary:
                # if 'TP' is a key in segments[primary][first_key] it means that there is no third partitions in segments
                if 'TP' in segments[primary][secondary]:
                    return segments[primary][secondary][state]

                # there is a third partition in segments
                tert_keys = list(segments[primary][secondary].keys())
                # the first option in the third partition options in segments
                first_key = tert_keys[0]
                # aggregate the ids
                ids = segments[primary][secondary][first_key][state]
                for i in range(1, len(tert_keys)):
                    ids = np.concatenate((ids, segments[primary][secondary][tert_keys[i]][state]), axis=0)
                return ids
            # if three partitions are chosen
            else:
                ids = segments[primary][secondary][tertiary][state]
                return ids

    def frame_visualization_no_bb(self, data, image):
        if image is not None:
            shape = np.shape(image)
            orig_image_height, orig_image_width = shape[0], shape[1]
            result = cv2.resize(image, (self.image_width, self.image_height))
        else:
            result = np.full((self.image_height, self.image_width), 125, dtype=np.uint8)
        text = data.to_string()
        y0, dy = 60, 70
        
        for ind,i in enumerate(data.keys()):
            y = y0 + ind*dy
            result = cv2.putText(result, f'{i} - {data.values[ind]}', (50, y ), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA)
       # result=cv2.putText(result, data.to_string(), (10,450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 8, cv2.LINE_4)
        fig = plt.figure()
        plt.imshow(result)
        red_patch = mpatches.Patch(color=(0, 0, 1), label='prediction')
        green_patch = mpatches.Patch(color=(0, 1, 0), label='GT')
        plt.legend(ncol=2, loc='lower left', fontsize='small', handles=[red_patch, green_patch], bbox_to_anchor=(0, 1))
        # used example in https://matplotlib.org/3.3.0/faq/howto_faq.html to show matplotlib figure on a web app
        output = BytesIO()
        fig.savefig(output, format="png")
        ret_data = base64.b64encode(output.getbuffer()).decode("ascii")
        return ret_data, fig

    def frame_visualization(self, bb_index, image):
        """
        Overlay a frame's bounding boxes on top of the frame

        :param frame_labels: list of x,y,w,h arrays of a frame's Ground Truth bounding boxes
        :param frame_prds: list of x,y,w,h arrays of a single frame's predicted bounding boxes
        :param selected_bb: the bounding box example that was chosen
        :param matched:  the matching bounding box to the wanted_bb
        :param image: the frame of the selected bounding box
        :return: encoded image for html use and a matplotlib figure, of the relevant frame with an overlay of its bounding boxes
        """

        bb_obj=self.comp_data.loc[bb_index]
        all_frmae_obj=self.comp_data[((self.comp_data['frame_id']==bb_obj['frame_id']) & (self.comp_data['video']==bb_obj['video']))]
        
        label_bbs = []
        prd_bbs = []
        matched = []

        for ind in range(0,len(all_frmae_obj)):
            obj=all_frmae_obj.iloc[ind]
            if not math.isnan(obj['x_gt']):
                label_bbs.append([obj['x_gt'],obj['y_gt'],obj['width_gt'],obj['height_gt']])
            if not math.isnan(obj['x']):
                prd_bbs.append([obj['x'], obj['y'], obj['width'], obj['height']])
        
        selected_bb = [bb_obj['x'], bb_obj['y'], bb_obj['width'], bb_obj['height']]
        if not math.isnan(obj['x_gt']):
            matched = [bb_obj['x_gt'],bb_obj['y_gt'],bb_obj['width_gt'],bb_obj['height_gt']]
            
      
        # if an image is availble we resize it to a fixed size and save its dimensions for bounding box scaling
        if image is not None:
            shape = np.shape(image)
            orig_image_height, orig_image_width = shape[0], shape[1]
            result = cv2.resize(image, (self.image_width, self.image_height))
        # when the image is not available we use a black background to display the bounding boxes
        #TODO take care of that possibility
        else:
            orig_image_width, orig_image_height = self.image_width, self.image_height
            result = np.zeros((self.image_width, self.image_height, 3), dtype=np.uint8)
        # iterating over the frame's GT and prediction bounding boxes
        for i, bb_list in enumerate([label_bbs, prd_bbs]):
            for temp_bb in bb_list:
                (x, y, w, h) = temp_bb
                # when bounding box coordinates are normalized between 0-1
                # a pixel position in the image plane is equals to (normalized_x * image_horizontal_size, normalized_y * image_vertical_size)
                if x <= 1 and y <= 1 and w <= 1 and h <= 1:
                    bb_x_coordinate = x * orig_image_width
                    bb_y_coordinate = y * orig_image_height
                    bb_width = w * orig_image_width
                    bb_height = h * orig_image_height
                # bounding box coordinates are not normalized
                else:
                    bb_x_coordinate = x
                    bb_y_coordinate = y
                    bb_width = w
                    bb_height = h

                # Match the BB to the image after the resize
                width_ratio = self.image_width / orig_image_width
                height_ratio = self.image_height / orig_image_height
                bb_x_top_left = bb_x_coordinate * width_ratio
                bb_y_top_left = bb_y_coordinate * height_ratio
                bb_x_bottom_right = (bb_x_coordinate + bb_width) * width_ratio
                bb_y_bottom_right = (bb_y_coordinate + bb_height) * height_ratio

                # represents the top left corner of rectangle
                start_point = (int(bb_x_top_left), int(bb_y_top_left))
                # represents the bottom right corner of rectangle
                end_point = (int(bb_x_bottom_right), int(bb_y_bottom_right))
                # green for labels, blue for predictions
                color = (0, 255, 0) if i == 0 else (0, 0, 255)
                # Line thickness of 1 px
                thickness = 1
                # Draw the selected or matching bounding box with thickness of 3 px
                if np.array_equal(temp_bb, selected_bb, equal_nan=True) or np.array_equal(temp_bb, matched, equal_nan=True):
                    thickness = 3
                # Draw a rectangle that represents the bounding box
                cv2.rectangle(result, start_point, end_point, color, thickness)

        fig = plt.figure()
        plt.imshow(result)
        red_patch = mpatches.Patch(color=(0, 0, 1), label='prediction')
        green_patch = mpatches.Patch(color=(0, 1, 0), label='GT')
        plt.legend(ncol=2, loc='lower left', fontsize='small', handles=[red_patch, green_patch], bbox_to_anchor=(0, 1))
        # used example in https://matplotlib.org/3.3.0/faq/howto_faq.html to show matplotlib figure on a web app
        output = BytesIO()
        fig.savefig(output, format="png")
        data = base64.b64encode(output.getbuffer()).decode("ascii")
        return data, fig

    def is_label_or_prd(self):
        if self.state in ['TP', 'FP']:
            self.label_or_prd = 'prediction'
        else:
            self.label_or_prd = 'label'

    def read_image(self, frame_id, images_folder):
        frame = None
        if pathlib.Path(images_folder).suffix == ".mp4":
            vid = cv2.VideoCapture(images_folder)
            vid.set(cv2.CAP_PROP_POS_FRAMES, int(frame_id))
            _, frame = vid.read()
        else:
            # filtering out images that don't have the frame number in them before a more exact filtering
            optional_images_names = [name for name in os.listdir(images_folder) if str(frame_id) in name]
            
            # finding the exact frame image by using the correct images names form: blabla_framenumber.bla
            for opt in optional_images_names:
                dots = [i.start() for i in re.finditer("\.", opt)]
                lines = [i.start() for i in re.finditer("_", opt)]
                last_dot_idx = dots[-1]
                last_line_idx = lines[-1]+1 if len(lines)>0 else 0
                opt_frame_number = int(opt[last_line_idx: last_dot_idx])
                if opt_frame_number == int(frame_id):
                    frame = cv2.imread(os.path.join(images_folder, opt))
                    break
        
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame
                
    def visualize(self, bb_id, from_file=False, label_file_dir=None, prd_file_dir=None):
        """
        this function searches the right bounding box and its frame and calls self.frame_visualization() to visualize it

        :param bb_id: the id of the bounding box example that was asked for
        :param from_file: Boolean, indicates whether the dataframe was loaded from a saved file, default: false
        :param label_file_dir: the path to extract the label file if from_file is True, default: None
        :param prd_file_dir: the path to extract the predictions file if from_file is True, default: None
        :return: returns the output of self.frame_visualization() which is an encoded image for html use and a matplotlib figure,
         of the relevant frame with an overlay of its bounding boxes
        """
        # checks what is the relevant dataframe to search for the asked example (predictions or labels)
        self.is_label_or_prd()
        # if the prediction and label dataframes are loaded from a file - for future development
        if from_file:
            assert label_file_dir and prd_file_dir, 'if loading from file is selected than the label and prediction paths are needed'
            self.combined_prd_dataframe = pd.read_csv(os.path.join(self.save_stats_dir, prd_file_dir))
            self.combined_label_dataframe = pd.read_csv(os.path.join(self.save_stats_dir, label_file_dir))
        # the video name (image folder name) and bounding box index are needed for identification of the correct bounding box (the frame id is not necessary)
        
        _, bb_index,frame_id,_ = bb_id
        
        data = self.comp_data.loc[bb_index]
        image_folder=data['video']
        frame_image = self.read_image(frame_id, image_folder)

       
        if 'x' not in data:
            return self.frame_visualization_no_bb(data, frame_image)

        
        # returning the output of frame_visualization which is are an encoded image (for html use) and matplotlib figure
        return self.frame_visualization(bb_index, frame_image)






def combine_video_results(save_stats_dir, statistic_funcs, files_dir, segmentation_funcs, threshold, image_width, image_height,video_annotation_dict, overlap_function, evaluation_function):
    """

    :param save_stats_dir: same as in ParallelExperiment
    :param statistic_funcs: same as in ParallelExperiment
    :param files_dir: same as in ParallelExperiment
    :param segmentation_funcs: same as in ParallelExperiment
    :param threshold: the threshold to use (above the threshold a prediction is TP)
    :param image_width: the image width size to reshape to
    :param image_height: the image height size to reshapw to
    :return:
    """
    exp = ParallelExperiment(save_stats_dir=save_stats_dir, statistic_funcs=statistic_funcs, files_dir=files_dir, segmentation_funcs=segmentation_funcs, image_width=image_width, image_height=image_height,video_annotation_dict=video_annotation_dict, evaluation_function=evaluation_function, overlap_function=overlap_function)
    exp.combine_from_text(False)
    exp.get_segmentation_masks(float(threshold))
    return exp