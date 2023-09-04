import numpy as np
import pandas as pd
from dash import html

from classes_and_utils.ParallelExperiment import ParallelExperiment


class UniqueHelper:

    def __init__(self,exp,ref_exp, evaluation_function, overlap_function):
        self.exp = exp
        self.ref_exp = ref_exp
        main_ref_dict, ref_main_dict = UniqueHelper.match_main_ref_predictions(self.exp, self.ref_exp, evaluation_function, overlap_function)
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
        unique_array = self.exp.detections_images_dict[mask & (self.exp.get_confusion_masks()[stat_func]!=ref_stat_in_main_index)]

        stat_main_ref = self.main_ref_dict.copy()
        stat_main_ref[self.exp.get_confusion_masks()[stat_func]==False]=-1
        
        main_stat_in_ref_index = pd.Series(np.zeros(len(mask_ref), dtype=bool))
        main_stat_in_ref_index[main_stat_in_ref_index.index.isin(stat_main_ref[stat_main_ref!=-1])] = True
        unique_array_ref = self.ref_exp.detections_images_dict[mask_ref & (self.ref_exp.get_confusion_masks()[stat_func]!=main_stat_in_ref_index)]

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

    @staticmethod       
    def match_frame_predictions(predictions, ref_predictions, evaluation_function, overlap_function):
        """
        Match beween 2 set of preditcions in a frame using the user defined functions in the experiment object.
        :param (in/out) predictions: predictions in the main reort. The predictions filled with thier matched one and overlap values
        :param (in/out) ref_predictions: predictions in the ref reort. The predictions filled with thier matched one and overlap values
        :param exp: experiment object 

        """
        if not len(ref_predictions) or not len(predictions):
                mat=[]
        else:
            mat = np.zeros((len(predictions), len(ref_predictions)))
        
        for i, pred in enumerate(predictions):
            for j, ref in enumerate(ref_predictions):
                #check if all gt attributes are equal in main and ref predictions
                if pred['detection_gt'] and ref['detection_gt']:
                    match = True
                    for key in pred: 
                        if '_gt' in key:
                            if pred[key] != ref[key]:
                                match = False
                                break
                    if match:
                        pred['matching'] = j
                        ref['matching'] = i
                elif not (pred['detection_gt'] or ref['detection_gt']) and pred['detection'] and ref['detection']:
                    overlap = overlap_function(pred, ref)
                    mat[i, j] = round(overlap, 2)
                #TN in main and in ref experiments mark as overlapped detection
                elif not pred['detection_gt'] and not ref['detection_gt'] and not pred['detection'] and not ref['detection']:
                    mat[i, j] = round(1, 2)

        #the evaluation function should add the matched prediction to the right record in predictions list
        evaluation_function(predictions, mat)
            
    #create dictionsary for main/ref report with matched bounding box in ref/main if there is any
    @staticmethod
    def match_main_ref_predictions(exp, ref_exp, evaluation_function, overlap_function):
        """
        Match all the predictions in main reort and ref report. Detections with no matched detection in the ref report, will have no entry in the dictionary.
        :param exp: main experiment object.
        :param ref_exp: ref experiment object.
        :return: main_ref,ref_main :dictionary between detection in main report to detections in the ref report.
        """
        
        print('start calculating main/ref matched bounding boxes')
        
        main_ref = pd.Series(np.full(len(exp.comp_data),-1))
        ref_main = pd.Series(np.full(len(ref_exp.comp_data),-1))
        
        for vid in exp.comp_data['video'].unique():
            print('calculating matching bounding boxes for vid: ' + vid)
            #set frame_id as index, and keep the original index as another column
            ref_cur_video_df = ref_exp.comp_data[ref_exp.comp_data['video'] == vid].reset_index().set_index('frame_id').reset_index()
            main_cur_video_df = exp.comp_data[exp.comp_data['video'] == vid].reset_index().set_index('frame_id').reset_index()
            unique_frames = np.unique(np.concatenate([ref_cur_video_df['frame_id'],main_cur_video_df['frame_id']]))
            
            #use dictionary for performance improvements
            main_cur_video_list = main_cur_video_df.to_dict('records')
            ref_cur_video_list = ref_cur_video_df.to_dict('records')
                        
            current_main_index = 0
            current_ref_index = 0
            
            for frame in unique_frames:
                while current_ref_index < len(ref_cur_video_list) and ref_cur_video_list[current_ref_index]['frame_id'] < frame:
                    current_ref_index+=1
                    
                while current_main_index < len(main_cur_video_list) and main_cur_video_list[current_main_index]['frame_id'] < frame:
                    current_main_index+=1
                
                predictions = []
                ref_predictions = []
                
                while current_ref_index < len(ref_cur_video_list) and ref_cur_video_list[current_ref_index]['frame_id'] == frame:
                    ref_predictions.append(ref_cur_video_list[current_ref_index])
                    current_ref_index+=1

                while current_main_index < len(main_cur_video_list) and main_cur_video_list[current_main_index]['frame_id'] == frame:
                    predictions.append(main_cur_video_list[current_main_index])
                    current_main_index+=1
                
                UniqueHelper.match_frame_predictions(predictions, ref_predictions, evaluation_function=evaluation_function, overlap_function=overlap_function)
                for _, x in enumerate(predictions): 
                    if 'matching' in x:
                        main_ref[x['index']]=ref_predictions[x['matching']]['index']
                        ref_main[ref_predictions[x['matching']]['index']] = x['index']
                        
        print ('Finished calculate matched bounding boxes')      
        return main_ref, ref_main