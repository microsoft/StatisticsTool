import numpy as np
import pandas as pd
from dash import html
from app_config.dataframe_tokens import DataFrameTokens
from experiment_engine.VideoEvaluation import VideoEvaluation

from experiment_engine.ParallelExperiment import ParallelExperiment


class UniqueHelper:

    def __init__(self,exp,ref_exp, association_function):
        self.exp = exp
        self.ref_exp = ref_exp
        main_ref_dict, ref_main_dict = UniqueHelper.match_main_ref_predictions(self.exp, self.ref_exp, association_function)
        self.main_ref_dict = main_ref_dict
        self.ref_main_dict = ref_main_dict
        
        self.cells_data = {}
        self.cells_data_ref = {}


    def calc_unique_detections(self, segmentations,stat_functions):

        stat_func = stat_functions

        mask = self.exp.get_statistics_masks(segmentations)[stat_functions]
        mask_ref = self.ref_exp.get_statistics_masks(segmentations)[stat_functions]

        unique_array=[]
        unique_array_ref=[]

        stat_ref_main = self.ref_main_dict.copy()
        stat_ref_main[self.ref_exp.get_confusion_masks()[stat_func]==False]=-1
        
        ref_stat_in_main_index = pd.Series(np.zeros(len(mask), dtype=bool))
        ref_stat_in_main_index[ref_stat_in_main_index.index.isin(stat_ref_main[stat_ref_main!=-1])] = True
        unique_mask = mask & (self.exp.get_confusion_masks()[stat_func]!=ref_stat_in_main_index)
        unique_array = self.exp.get_list_array(unique_mask)

        stat_main_ref = self.main_ref_dict.copy()
        stat_main_ref[self.exp.get_confusion_masks()[stat_func]==False]=-1
        
        main_stat_in_ref_index = pd.Series(np.zeros(len(mask_ref), dtype=bool))
        main_stat_in_ref_index[main_stat_in_ref_index.index.isin(stat_main_ref[stat_main_ref!=-1])] = True
        unique_ref_mask = mask_ref & (self.ref_exp.get_confusion_masks()[stat_func]!=main_stat_in_ref_index)
        unique_array_ref = self.ref_exp.get_list_array(unique_ref_mask)

        return unique_array, unique_array_ref

    def get_ids(self, cell_key, state, is_ref):
        ids = []
        cells = self.cells_data if not is_ref else self.cells_data_ref
        for x in cells[cell_key][state]:
            ids.append(x)
        ids = np.array(ids)

        return ids

    def get_cell_stat_data(self, stat, segmentations):
        cell_name = ParallelExperiment.cell_name_from_segmentations(segmentations)

        if cell_name not in self.cells_data:
            self.cells_data[cell_name], self.cells_data_ref[cell_name] = self.calc_cell_data(segmentations)
        
        return self.cells_data[cell_name][stat], self.cells_data_ref[cell_name][stat]

    def calc_cell_data(self, segmentations):
        cells_data_ref = {}
        cells_data = {}
        
        for stat in self.exp.get_confusion_masks().keys():
            unique, unique_ref = self.calc_unique_detections(segmentations, stat)
            cells_data_ref[stat] = unique_ref
            cells_data[stat] = unique

        return cells_data, cells_data_ref
            
    #create dictionsary for main/ref report with matched bounding box in ref/main if there is any
    
    @staticmethod
    def get_gt_columns(comp_data):
        gt_data = pd.DataFrame()
        suffix_len = len(DataFrameTokens.GT_ANNOT_SUFFIX)
        # iterate over the columns of the comp_data dataframe
        for col in comp_data.columns:
            # check if the column name ends with '_gt'
            if col.endswith(DataFrameTokens.GT_ANNOT_SUFFIX):
                # check if a column without the '_gt' suffix already exists in the comp_data dataframe
                if col[:-suffix_len] in comp_data.columns:
                    # use the existing column name without the '_gt' suffix
                    gt_data[col[:-suffix_len]] = comp_data[col]
        
        gt_data[DataFrameTokens.LABELS_GROUP_KEY] = comp_data[DataFrameTokens.LABELS_GROUP_KEY]
        gt_data[DataFrameTokens.UNIQUE_BATCH_TOKEN] = comp_data[DataFrameTokens.UNIQUE_BATCH_TOKEN]
        return gt_data


    
    @staticmethod
    def match_main_ref_predictions(exp, ref_exp, association_function):
        """
        Match all the predictions in main reort and ref report. Detections with no matched detection in the ref report, will have no entry in the dictionary.
        :param exp: main experiment object.
        :param ref_exp: ref experiment object.
        :return: main_ref,ref_main :dictionary between detection in main report to detections in the ref report.
        """
        
        print('start calculating main/ref matched bounding boxes')
        
        main_ref = pd.Series(np.full(len(exp.comp_data),-1))
        ref_main = pd.Series(np.full(len(ref_exp.comp_data),-1))

        exp_no_value = exp.comp_data[exp.comp_data[DataFrameTokens.HAS_VALUE_TOKEN] == False]
        exp_has_value = exp.comp_data[exp.comp_data[DataFrameTokens.HAS_VALUE_TOKEN] == True]
        ref_no_value = ref_exp.comp_data[ref_exp.comp_data[DataFrameTokens.HAS_VALUE_TOKEN] == False]
        ref_has_value = ref_exp.comp_data[ref_exp.comp_data[DataFrameTokens.HAS_VALUE_TOKEN] == True]

        exp_gt = UniqueHelper.get_gt_columns(exp_no_value)
        ref_exp_gt = UniqueHelper.get_gt_columns(ref_no_value)

        for vid in exp.comp_data[DataFrameTokens.UNIQUE_BATCH_TOKEN].unique():
            vid_str = vid
            if DataFrameTokens.VIDEO_TOKEN in exp.comp_data.columns:
                vid_str = str(exp.comp_data.loc[exp.comp_data[DataFrameTokens.UNIQUE_BATCH_TOKEN] == vid][DataFrameTokens.VIDEO_TOKEN].iloc[0])
            print('calculating matching bounding boxes for data: ' + str(vid_str))
            #set frame_id as index, and keep the original index as another column
            ref_cur_video_df = ref_has_value.loc[(ref_has_value[DataFrameTokens.UNIQUE_BATCH_TOKEN] == vid)]
            main_cur_video_df = exp_has_value.loc[(exp_has_value[DataFrameTokens.UNIQUE_BATCH_TOKEN] == vid) ]
            cur_main_ref, cur_ref_main = VideoEvaluation.create_association_indexes(main_cur_video_df, ref_cur_video_df, association_function)    

            main_ref.loc[cur_main_ref.index] =cur_main_ref
            ref_main.loc[cur_ref_main.index] =cur_ref_main


            #for rows without prediction, there is only gt so assiciate the gt data instead           
            ref_cur_video_df_nv = ref_exp_gt.loc[(ref_exp_gt[DataFrameTokens.UNIQUE_BATCH_TOKEN] == vid)]
            main_cur_video_df_nv = exp_gt.loc[(exp_gt[DataFrameTokens.UNIQUE_BATCH_TOKEN] == vid) ]
            cur_main_ref, cur_ref_main = VideoEvaluation.create_association_indexes(main_cur_video_df_nv, ref_cur_video_df_nv, association_function)    

            main_ref.loc[cur_main_ref.index] =cur_main_ref
            ref_main.loc[cur_ref_main.index] =cur_ref_main
                        
        print ('Finished calculate matched bounding boxes')      
        return main_ref, ref_main