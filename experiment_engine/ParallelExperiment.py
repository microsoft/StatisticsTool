
import json
import math
import pickle
import pandas as pd, os
import numpy as np
import shutil

from app_config.constants import Constants, UserDefinedConstants
from app_config.dataframe_tokens import DataFrameTokens
from experiment_engine.UserDefinedFunctionsHelper import load_config_dict
from experiment_engine.file_storage_handler import StoreType, get_path_on_store, parallel_get_files_on_local_storage
from utils.image_util import prepare_example_image
from utils.report_metadata import create_metadata


class ParallelExperiment:
 
    def __init__(self, comp_data, partitioning_func,confusion_func):
        self.comp_data = comp_data
        self.segmentations_masks = {}
        self.cell_statistics_map = {}
    
        self.confusion_masks, self.segmentations_masks = ParallelExperiment.calc_experiment(comp_data, partitioning_func,confusion_func)
       
    def get_segmentations_masks(self):
        return self.segmentations_masks
    
    def get_confusion_masks(self):
        return self.confusion_masks
    
    def get_statistics_masks(self, segmentations):
        cell_name = ParallelExperiment.cell_name_from_segmentations(segmentations)
        
        all_stats = self.confusion_masks.keys()
        assert len(all_stats)>0, 'There should be at least one statistic calc for cell'
        
        if cell_name not in self.cell_statistics_map:
            len_ = len(list(self.confusion_masks.values())[0])
            segmentation_mask = np.ones([len_], dtype=bool)
            for curr_segmentation in segmentations:
                assert(len(curr_segmentation)==1)
                seg_cat, seg_value = list(curr_segmentation.keys())[0], list(curr_segmentation.values())[0]
                seg_idx = self.segmentations_masks[seg_cat]['possible partitions'].index(seg_value)
                segmentation_mask &= self.segmentations_masks[seg_cat]['masks'][seg_idx]
        
            masks = {}
            for key in self.confusion_masks.keys():
                masks[key] = self.confusion_masks[key] & segmentation_mask
                
            self.cell_statistics_map[cell_name] = masks
        
        return self.cell_statistics_map[cell_name]

    def get_cell_data(self, segmentations, statistic_funcs):
        confusion_masks = self.get_statistics_masks(segmentations)
        confusion_sums = {}
        for mask in confusion_masks.keys():
            confusion_sums[mask] = np.sum(confusion_masks[mask])
            
        statistics = statistic_funcs(confusion_masks, self.comp_data)
        
        return confusion_sums, statistics

    def get_list_array(self, mask):
        if DataFrameTokens.VIDEO_TOKEN in self.comp_data.columns:
            batch_key = DataFrameTokens.VIDEO_TOKEN
        else:
            batch_key = DataFrameTokens.UNIQUE_BATCH_TOKEN
            
        arr = self.comp_data[mask][[batch_key,DataFrameTokens.LABELS_GROUP_KEY,DataFrameTokens.END_EVENT_TOKEN]].to_numpy()
        list_arr = np.insert(arr,1,self.comp_data[mask].index.to_numpy(), axis=1)
        return list_arr

    
    def get_ids(self, cell_key, state):
        segmentations = ParallelExperiment.segmentations_from_name(cell_name=cell_key)
        confusion_masks = self.get_statistics_masks(segmentations)
        
        return self.get_list_array(confusion_masks[state])
    
    def get_sample_images_paths(self, sample, local_store):
        paths = {}
        
        video = sample[DataFrameTokens.VIDEO_TOKEN]
        
        data_file = ''
        if DataFrameTokens.FRAME_FILE_DATA_TOKEN in sample:
            data_file = sample[DataFrameTokens.FRAME_FILE_DATA_TOKEN]
        paths[StoreType.Predictions]=self.get_sample_image_path_on_store(video, data_file, StoreType.Predictions, local_store)
                      
        if DataFrameTokens.FRAME_FILE_ANNOTATION_TOKEN in sample:
            paths[StoreType.Annotations]=self.get_sample_image_path_on_store(video, sample[DataFrameTokens.FRAME_FILE_ANNOTATION_TOKEN], StoreType.Annotations, local_store)
            
        if DataFrameTokens.FRAME_FILE_GT_TOKEN in sample:
            paths[StoreType.Data]=self.get_sample_image_path_on_store(video, sample[DataFrameTokens.FRAME_FILE_GT_TOKEN], StoreType.Data, local_store) 
            
        return paths
        
    
    def get_sample_image_path_on_store(self, video_file, file_name, store_type, local_store):
        path_on_blob = video_file
        if file_name:
            path_on_blob = file_name
        if local_store:
            path_on_blob = os.path.join(local_store,video_file)
        if not os.path.splitext(str(path_on_blob))[1]:
            path_on_blob = path_on_blob + '.mp4' #Add default mp4 extension for all video names without extension
        
        path_on_blob = get_path_on_store(path_on_blob, store_type)
    
        return path_on_blob
    
    
    def get_example_images_local_path(self, sample_index, local_store)    :
        sample = self.comp_data.loc[sample_index]
        local_paths = {}
        pred_bbs, label_bbs, selected_pred_index, selected_label_index = self.get_detection_bounding_boxes(sample_index)
       
        frame_id = None
        try:
            frame_id = int(sample[DataFrameTokens.LABELS_GROUP_KEY])
        except:
            pass
        
        local_paths = self.get_sample_images_paths(sample, local_store)
        
        file_store_dict = {value: key for key, value in local_paths.items()}
        
        local_video_path = parallel_get_files_on_local_storage(file_store_dict)
        
        images = {}
        if len (local_video_path) > 0 and local_video_path[0]: images[StoreType.Predictions] = local_video_path[0]
        if len (local_video_path) > 1 and local_video_path[1]: images[StoreType.Annotations] = local_video_path[1]
        if len (local_video_path) > 2 and local_video_path[2]: images[StoreType.Data] = local_video_path[2]
        
        for key,image in images.items():
            if image:
                images[key] = prepare_example_image(image, frame_id, prd_bbs=pred_bbs, label_bbs=label_bbs, selected_pred=selected_pred_index, selected_label=selected_label_index)
        
        return images
    
    def get_detection_bounding_boxes(self, sample_index):
        bb_obj = self.comp_data.loc[sample_index]

        label_bbs = []
        prd_bbs = []
        matched = []
        
        all_frmae_obj=self.comp_data[((self.comp_data[DataFrameTokens.LABELS_GROUP_KEY]==bb_obj[DataFrameTokens.LABELS_GROUP_KEY]) & (self.comp_data[DataFrameTokens.UNIQUE_BATCH_TOKEN]==bb_obj[DataFrameTokens.UNIQUE_BATCH_TOKEN]))]

        if DataFrameTokens.BB_X in bb_obj and bb_obj[DataFrameTokens.BB_X] is not None:  
            matched.append([bb_obj[DataFrameTokens.BB_X], bb_obj[DataFrameTokens.BB_Y], bb_obj[DataFrameTokens.BB_WIDTH], bb_obj[DataFrameTokens.BB_HEIGHT]])
        pred_index = -1
        label_index = -1
        for ind in all_frmae_obj.index:
            obj=all_frmae_obj.loc[ind]
            if DataFrameTokens.BB_X+DataFrameTokens.GT_ANNOT_SUFFIX in obj and not math.isnan(obj[DataFrameTokens.BB_X+DataFrameTokens.GT_ANNOT_SUFFIX]):
                label_bbs.append([obj[DataFrameTokens.BB_X+DataFrameTokens.GT_ANNOT_SUFFIX],obj[DataFrameTokens.BB_Y+DataFrameTokens.GT_ANNOT_SUFFIX],obj[DataFrameTokens.BB_WIDTH+DataFrameTokens.GT_ANNOT_SUFFIX],obj[DataFrameTokens.BB_HEIGHT+DataFrameTokens.GT_ANNOT_SUFFIX]])
                if ind == sample_index:
                    label_index = len(label_bbs)-1
            if DataFrameTokens.BB_X in obj  and not math.isnan(obj[DataFrameTokens.BB_X]):
                prd_bbs.append([obj[DataFrameTokens.BB_X], obj[DataFrameTokens.BB_Y], obj[DataFrameTokens.BB_WIDTH], obj[DataFrameTokens.BB_HEIGHT]])
                if ind == sample_index:
                    pred_index = len(prd_bbs) -1            
    

        return prd_bbs, label_bbs, pred_index, label_index
    
    def get_sample_properties_text_list(self, sample_index):
        data = self.comp_data.loc[sample_index]

        sample_variables_text_list = [f"{key}: {data[key]}" for key in data.keys()]

        return sample_variables_text_list
    
    @staticmethod
    def combine_evaluation_files(compared_videos):
        

        batch_id = 0
        datafrme_dict = []
        for file_name in compared_videos:
            df = pd.read_json (file_name)
            df[DataFrameTokens.UNIQUE_BATCH_TOKEN] = batch_id
            batch_id = batch_id + 1
            datafrme_dict.append(df)
            continue
        
        if len(datafrme_dict) > 0:
            # concatenate the dictionary of dataframes into a single dataframe            
            comp_data = pd.concat(datafrme_dict).reset_index(drop=True)
        
        return comp_data              
    @staticmethod
    def calc_experiment(comp_data, segmentation_func,confusion_func):
        confusion_calc_func = confusion_func 

        # calculate the boolean masks of TP/FP/FN (which row/bounding box in the dataframes is TP/FP/FN)
        confusion_masks = confusion_calc_func(comp_data)
        
        # add Total example to statistics functions for unified calculation in future ones (e.g. unique calculation)
        confusion_masks[UserDefinedConstants.ALL_RAWS_IN_SEGMENT] = pd.Series(np.ones(len(comp_data), dtype=bool))
        
        # calculate the boolean masks of the partitions (which row/bounding box in the dataframes belongs to which partition)
        
        wanted_segmentations = {}
        if segmentation_func:
            try:
                wanted_segmentations = segmentation_func(comp_data)
            except Exception as ex:
                print("------------ERROR------------")
                print("Failed to calculate partitioning with given partitioning user defined functions, continue without segmentations\n")
                print(ex)
                print('\n\n')

        # Add the segmentation masks to masks
        segmentations_masks = wanted_segmentations

        return confusion_masks, segmentations_masks
  
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
 
    @staticmethod
    def save_experiment(comp_data, out_folder, config_name, report_run_info, intermediate_dir=None):
        report_name = os.path.splitext(os.path.split(config_name)[-1])[0]
        report_file_name = report_name + Constants.EXPERIMENT_EXTENSION
        report_output_file = os.path.join(out_folder, report_file_name)

        with open(report_output_file, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(comp_data, output, pickle.HIGHEST_PROTOCOL)

        config = load_config_dict(config_name)

        metadata = create_metadata(report_run_info, config)

        output_file = os.path.join(out_folder, report_name + Constants.METADATA_EXTENTION)
        with open(output_file, 'w') as f:
            json.dump(metadata, f)

        if intermediate_dir and os.path.exists(intermediate_dir):
            shutil.rmtree(intermediate_dir)

        return report_output_file
    
   
    