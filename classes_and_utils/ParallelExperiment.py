
import json
import math
import pickle
import pandas as pd, os
import numpy as np

from app_config.constants import Constants


# Irit's totos:
# todo return number of processed files on GUI
# todo automatically make sure every bounding box was processed (make sure we didn't forget any bounding box)

# Ben's todo:
# todo return number of prediction bounding boxes that didn't have a GT at all

class ParallelExperiment:
 
    def __init__(self, statistic_funcs, segmentation_funcs,report_metadata, overlap_function, evaluation_function):
        self.statistic_funcs = statistic_funcs
        self.evaluation_function = evaluation_function
        self.overlap_function = overlap_function
        self.segmentation_funcs = segmentation_funcs
        self.masks = None
        self.ID_storage = {}
        self.segmented_ID = {}
        self.segmented_ID_new = {}
        self.report_metadata = report_metadata
        
    
    def combine_from_text(self, compared_videos):
        self.comp_data = None
        datafrme_dict = []
        for file_name in compared_videos:
            df = pd.read_json (file_name)
            datafrme_dict.append(df)
            continue
        
        if len(datafrme_dict) > 0:
            # concatenate the dictionary of dataframes into a single dataframe
            self.comp_data = pd.concat(datafrme_dict).reset_index(drop=True)
       
    @staticmethod
    def get_TP_FP_FN_masks(comp_data, threshold):
        """
        :param threshold: float , above this value an overlap is considered a hit (the prediction will be TP)
        :return: Boolean masks of TP, FP, FN that indicates which row in the predictions dataframe is TP/FP
                 and which row in the labels dataframe is a FN (row = bounding box)
        """
        #first key from 'detection' key in input
        key = 'detection'
        FN_mask = ((comp_data[key+'_gt']==True) & ((comp_data['state']<threshold) | (comp_data[key]==False) ))
        FP_mask = ((comp_data[key]==True) & (comp_data['state']<threshold))
        TP_mask = ((comp_data[key]==True) &((comp_data['state']>=threshold) & (comp_data[key+'_gt']==True)))
        TN_mask = (comp_data[key+'_gt']==False) & (comp_data[key]==False)
        if len(comp_data)!=(sum(FN_mask)+sum(FP_mask)+sum(TP_mask)+sum(TN_mask)):
            print('Masks sizes doesnt match dataset size !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        return TP_mask, FP_mask, FN_mask
               

    def get_segmentation_masks(self, threshold):

        assert threshold >= 0, 'threshold should be a positive number'
       
        # calculate the boolean masks of TP/FP/FN (which row/bounding box in the dataframes is TP/FP/FN)
        TP_mask, FP_mask, FN_mask = self.get_TP_FP_FN_masks(self.comp_data, threshold)
        # calculate the boolean masks of the partitions (which row/bounding box in the dataframes belongs to which partition)
        self.wanted_segmentations = self.segmentation_funcs(self.comp_data)
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

    def calc_cell_name(self, segmentations):
        cell_name = ""
        if len(segmentations) > 0: # This is the empty table case
            #list(segmentations.keys())[0] != 'None':
            for curr_segmentation in segmentations:
                assert(len(curr_segmentation)==1)
                _, seg_value = list(curr_segmentation.keys())[0], list(curr_segmentation.values())[0]
                cell_name = cell_name + "{}*".format(seg_value)
        else:
            cell_name = "*"

        return cell_name
    
    def get_cell_data(self, cell_name, segmentations,):
        len_ = len(self.masks['total_stats']['TP'])
        segmentation_mask = np.ones([len_], dtype=bool)
        
        for curr_segmentation in segmentations:
            assert(len(curr_segmentation)==1)
            seg_cat, seg_value = list(curr_segmentation.keys())[0], list(curr_segmentation.values())[0]
            seg_idx = self.masks[seg_cat]['possible partitions'].index(seg_value)
            segmentation_mask &= self.masks[seg_cat]['masks'][seg_idx]
      
        TP_masks = self.masks['total_stats']['TP'] & segmentation_mask
        FP_masks = self.masks['total_stats']['FP'] & segmentation_mask
        FN_masks = self.masks['total_stats']['FN'] & segmentation_mask

        TP, FP, FN, total_examples = np.sum(TP_masks), np.sum(FP_masks), np.sum(FN_masks), np.sum(segmentation_mask)
        TN = total_examples - (TP + FP + FN)

        statistics_dict = self.statistic_funcs(TP, FP, FN, total_examples)
        statistics_dict.update({'TP': TP, 'FP': FP, 'FN': FN, 'TN': TN, 'TOTAL_EXAMPLES': total_examples})
        statistics_dict['cell_name'] = cell_name

        if not hasattr(self, 'segmented_ID_new'): # temp just for backward compatability
            self.segmented_ID_new = {}

        self.segmented_ID_new[cell_name] = {
            'TP': self.ID_storage["prediction"][TP_masks],\
            'FP': self.ID_storage['prediction'][FP_masks],\
            'FN': self.ID_storage['label'][FN_masks]}

        return statistics_dict

    def get_ids(self, cell_key, state):
        ids = self.segmented_ID_new[cell_key][state]
        return ids

       
    def get_detection_bounding_boxes(self, detection_index):
        bb_obj = self.comp_data.loc[detection_index]

        label_bbs = []
        prd_bbs = []
        matched = []
        
        all_frmae_obj=self.comp_data[((self.comp_data['frame_id']==bb_obj['frame_id']) & (self.comp_data['video']==bb_obj['video']))]

        if 'x' in bb_obj and bb_obj['x'] is not None:  
            matched.append([bb_obj['x'], bb_obj['y'], bb_obj['width'], bb_obj['height']])
        pred_index = -1
        label_index = -1
        for ind in all_frmae_obj.index:
            obj=all_frmae_obj.loc[ind]
            if 'x_gt' in obj and not math.isnan(obj['x_gt']):
                label_bbs.append([obj['x_gt'],obj['y_gt'],obj['width_gt'],obj['height_gt']])
                if ind == detection_index:
                    label_index = len(label_bbs)-1
            if 'x' in obj  and not math.isnan(obj['x']):
                prd_bbs.append([obj['x'], obj['y'], obj['width'], obj['height']])
                if ind == detection_index:
                    pred_index = len(prd_bbs) -1            
    

        return prd_bbs, label_bbs, pred_index, label_index
    

    def get_detection_properties_text_list(self, detection_index):
        data = self.comp_data.loc[detection_index]

        detection_variables_text_list = [f"{key}: {data[key]}" for key in data.keys()]

        return detection_variables_text_list
    
    def get_detection_video_frame(self, detection_index):
        data = self.comp_data.loc[detection_index]
        
        video=data['video']
         
        return video


    def save_experiment(self, out_folder, config_file_name, config_folder):
        """
        Saves an object using pickle in a certain path
        :param obj: any python object (in this project we use it to save an instance of  class ParallelExperiment)
        :param filename: full path to the saved object
        """
        report_name = os.path.splitext(config_file_name)[0]
        report_file_name = report_name + Constants.EXPERIMENT_EXTENSION
        report_output_file = os.path.join(out_folder, report_file_name)

        with open(report_output_file, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

        metadata = {}  

        config_file_path = os.path.join(config_folder, config_file_name)
        if os.path.exists(config_file_path):
            with open(config_file_path) as conf:
                metadata = json.load(conf)[0]
        
        metadata.update(self.report_metadata)
        output_file = os.path.join(out_folder,report_name+Constants.METADATA_EXTENTION)
        with open(output_file, 'w') as f:
            json.dump(metadata, f)

        return report_output_file

def experiment_from_video_evaluation_files(statistic_funcs, compared_videos, segmentation_funcs, threshold, report_metadata, overlap_function, evaluation_function):
    """

    param statistic_funcs: same as in ParallelExperiment
    :param compared_videos: same as in ParallelExperiment
    :param segmentation_funcs: same as in ParallelExperiment
    :param threshold: the threshold to use (above the threshold a prediction is TP)
    :return:
    """
    exp = ParallelExperiment(statistic_funcs=statistic_funcs, segmentation_funcs=segmentation_funcs, 
                            report_metadata=report_metadata, 
                            evaluation_function=evaluation_function, overlap_function=overlap_function)
                            
    exp.combine_from_text(compared_videos)
    exp.get_segmentation_masks(float(threshold))
    return exp