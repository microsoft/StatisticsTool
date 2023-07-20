
import json
import math
import pickle
import pandas as pd, os
import numpy as np

from app_config.constants import Constants, UserDefinedConstants
from classes_and_utils.UserDefinedFunctionsHelper import get_userdefined_function, load_config_dict
from utils.report_metadata import CONFIG_TOKEN, create_metadata


class ParallelExperiment:
 
    def __init__(self, comp_data, threshold, partitioning_func, calc_experiment = True):
        self.comp_data = comp_data
        self.segmentations_masks = {}
        self.detections_images_dict = {}
        self.cell_statistics_map = {}
    
        if calc_experiment:
            self.segmentations_masks, self.detections_images_dict = ParallelExperiment.calc_experiment(comp_data, threshold, partitioning_func)
       
    
    @staticmethod
    def experiment_from_evaluation_files(compared_videos, threshold, partitioning_func, clac_experiment_statistics = True):
        
        datafrme_dict = []
        for file_name in compared_videos:
            df = pd.read_json (file_name)
            datafrme_dict.append(df)
            continue
        
        if len(datafrme_dict) > 0:
            # concatenate the dictionary of dataframes into a single dataframe
            comp_data = pd.concat(datafrme_dict).reset_index(drop=True)
        
        exp = ParallelExperiment(comp_data, threshold, partitioning_func, clac_experiment_statistics)
        return exp
    
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
               
    @staticmethod
    def calc_experiment(comp_data, threshold, segmentation_func):
        
        threshold = float(threshold)
        assert threshold >= 0, 'threshold should be a positive number'
       
        # calculate the boolean masks of TP/FP/FN (which row/bounding box in the dataframes is TP/FP/FN)
        TP_mask, FP_mask, FN_mask = ParallelExperiment.get_TP_FP_FN_masks(comp_data, threshold)
        # calculate the boolean masks of the partitions (which row/bounding box in the dataframes belongs to which partition)
        wanted_segmentations = segmentation_func(comp_data)
        # initialize masks with the total masks for TP/FP/FN
        segmentations_masks = {'total_stats': {'TP': TP_mask, 'FP': FP_mask, 'FN': FN_mask}}
        # Add the segmentation masks to masks
        segmentations_masks.update(wanted_segmentations)

        video_name = comp_data['video'].values.copy()[:, np.newaxis]
        frame = comp_data['frame_id'].values.astype(int).copy()[:, np.newaxis] 
        index = comp_data.index.to_series().values.copy()[:, np.newaxis]
        if 'end_frame' in comp_data.keys():
            end_frames = comp_data['end_frame'].values.astype(int).copy()[:, np.newaxis]
        else:
            end_frames = frame
        detections_images_dict = {}
        detections_images_dict['prediction'] = np.concatenate((video_name, index, frame, end_frames), axis=1)
        
        detections_images_dict['label'] = detections_images_dict['prediction']

        return segmentations_masks, detections_images_dict

    def get_masks(self):
        return self.segmentations_masks
    
    @staticmethod
    def cell_name_from_segmentations(segmentations):
        if len(segmentations) < 1:
            return '*'
        # Combine all the keys and values into a single list
        all_items = []
        for d in segmentations:
            for k, v in d.items():
                all_items.append((k, v))
        
        # Sort the list by key
        sorted_items = sorted(all_items, key=lambda x: x[0])
        
        # Combine the sorted items into a single string
        result = ''
        for k, v in sorted_items:
            result += f'{k}-{v},'
        
        # Remove the trailing comma and return the result
        return result[:-1]
    @staticmethod
    def segmentations_from_name(cell_name):
        if cell_name == '*':
            return []
        # Split the string into key-value pairs
        pairs = cell_name.split(',')
        
        # Create a list of dictionaries from the pairs
        result = []
        for pair in pairs:
            k, v = pair.split('-')
            result.append({k: v})
        
        return result
     
    def get_statistics_masks(self, segmentations):
        cell_name = ParallelExperiment.cell_name_from_segmentations(segmentations)
        
        if cell_name not in self.cell_statistics_map:
            len_ = len(self.segmentations_masks['total_stats']['TP'])
            segmentation_mask = np.ones([len_], dtype=bool)
            for curr_segmentation in segmentations:
                assert(len(curr_segmentation)==1)
                seg_cat, seg_value = list(curr_segmentation.keys())[0], list(curr_segmentation.values())[0]
                seg_idx = self.segmentations_masks[seg_cat]['possible partitions'].index(seg_value)
                segmentation_mask &= self.segmentations_masks[seg_cat]['masks'][seg_idx]
        
            TP_masks = self.segmentations_masks['total_stats']['TP'] & segmentation_mask
            FP_masks = self.segmentations_masks['total_stats']['FP'] & segmentation_mask
            FN_masks = self.segmentations_masks['total_stats']['FN'] & segmentation_mask

            self.cell_statistics_map[cell_name] = tuple([TP_masks, FP_masks, FN_masks, np.sum(segmentation_mask)])
        
        return self.cell_statistics_map[cell_name]

    def get_cell_data(self, segmentations, statistic_funcs):
        TP_masks, FP_masks, FN_masks, total = self.get_statistics_masks(segmentations)

        TP, FP, FN, total_examples = np.sum(TP_masks), np.sum(FP_masks), np.sum(FN_masks), np.sum(total)
        TN = total_examples - (TP + FP + FN)

        statistics_dict = statistic_funcs(TP, FP, FN, total_examples)
        statistics_dict.update({'TP': TP, 'FP': FP, 'FN': FN, 'TN': TN, 'TOTAL_EXAMPLES': total_examples})
        
        return statistics_dict

    def get_ids(self, cell_key, state):
        segmentations = ParallelExperiment.segmentations_from_name(cell_name=cell_key)
        TP_masks, FP_masks, FN_masks, _ = self.get_statistics_masks(segmentations)
        
        if state == 'TP':
            return self.detections_images_dict['prediction'][TP_masks]
        elif state == 'FP':
            return self.detections_images_dict['prediction'][FP_masks]
        elif state == 'FN':
            return self.detections_images_dict['label'][FN_masks]
        

       
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


    def save_experiment(self, out_folder, config_name, report_run_info):

        report_name = os.path.splitext(os.path.split(config_name)[-1])[0]
        report_file_name = report_name + Constants.EXPERIMENT_EXTENSION
        report_output_file = os.path.join(out_folder, report_file_name)

        with open(report_output_file, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(self.comp_data, output, pickle.HIGHEST_PROTOCOL)

        config = load_config_dict(config_name)
        
        metadata = create_metadata(report_run_info, config)
       
        output_file = os.path.join(out_folder,report_name+Constants.METADATA_EXTENTION)
        with open(output_file, 'w') as f:
            json.dump(metadata, f)

        return report_output_file
    
   
    