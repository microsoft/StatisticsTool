import numpy as np
import pandas as pd
from dash import html


class UniqueHelper:

    def __init__(self,exp,ref_exp):
        self.exp = exp
        self.ref_exp = ref_exp
        self.exp.main_ref_dict, self.exp.ref_main_dict = UniqueHelper.match_main_ref_predictions(self.exp,self.ref_exp)
        self.main_ref_dict = self.exp.main_ref_dict
        self.ref_main_dict = self.exp.ref_main_dict
        self.cells_data = {}
        self.cells_data_ref = {}


    def calc_unique_detections(self,column_keys,row_keys,stat_functions):

        unique_out = {}
        unique_ref_out = {}
        unique = unique_out
        unique_ref = unique_ref_out

        stat_func = None
        if list(column_keys[0].values())[0] == 'None' and list(row_keys[0].values())[0] == 'None':
            stat_func = stat_functions
        else:
            lst_partitions = []
            for x in column_keys + row_keys:
                part = list(x.values())[0]
                if part != 'None':
                    lst_partitions.append(part)

            lst_partitions.append(stat_functions)                    
            stat_func = tuple(lst_partitions)                    


            partitions_parts_list = stat_func

        #if no partition is selected will take total stats
        if type(stat_func) is str:
            if stat_func not in self.exp.masks['total_stats']:
                return None,None,None

            partitions_parts_list = [stat_func]
            mask = self.exp.masks['total_stats'][stat_func]
            mask_ref = self.ref_exp.masks['total_stats'][stat_func]
            if 'total' not in unique_out:
                unique_out['total'] = {}
            unique = unique_out['total']
            if 'total' not in unique_ref_out:
                unique_ref_out['total'] = {}
            unique_ref = unique_ref_out['total']
            unique[stat_func] = {}
            unique_ref[stat_func] = {}
        else:
            if partitions_parts_list[-1] not in self.exp.masks['total_stats']:
                return None,None,None
                
            #calculated current partition masks        
            mask = pd.Series(True, range(self.exp.comp_data.shape[0]))
            mask_ref = pd.Series(True, range(self.ref_exp.comp_data.shape[0]))
            for n in partitions_parts_list[:-1]:
                for seg in self.exp.masks.keys():
                    if 'possible partitions' in self.exp.masks[seg] and n in self.exp.masks[seg]['possible partitions']:
                        cur_mask = self.exp.masks[seg]['masks'][self.exp.masks[seg]['possible partitions'].index(n)]
                        cur_mask_ref = self.ref_exp.masks[seg]['masks'][self.ref_exp.masks[seg]['possible partitions'].index(n)]
                        break    
                mask = mask & cur_mask
                mask_ref = mask_ref & cur_mask_ref
            
            mask = mask & self.exp.masks['total_stats'][partitions_parts_list[-1]]
            mask_ref = mask_ref & self.ref_exp.masks['total_stats'][partitions_parts_list[-1]]

        current_unique_segment = unique
        current_unique_segment_ref = unique_ref
        
        for seg in partitions_parts_list[:-1]:
            if seg not in current_unique_segment:
                current_unique_segment[seg] = {}
            if seg not in current_unique_segment_ref:
                current_unique_segment_ref[seg] = {}

            current_unique_segment=current_unique_segment[seg]
            current_unique_segment_ref=current_unique_segment_ref[seg]

        unique_array=[]
        unique_array_ref=[]

        for val in mask.index[mask==True]:
            if val not in self.main_ref_dict or self.ref_exp.masks['total_stats'][partitions_parts_list[-1]][self.main_ref_dict[val]] != self.exp.masks['total_stats'][partitions_parts_list[-1]][val]:
                unique_array.append(self.exp.ID_storage['prediction'][val])

        for val in mask_ref.index[mask_ref==True]:
            if val not in self.ref_main_dict or self.exp.masks['total_stats'][partitions_parts_list[-1]][self.ref_main_dict[val]] != self.ref_exp.masks['total_stats'][partitions_parts_list[-1]][val]:
                unique_array_ref.append(self.ref_exp.ID_storage['prediction'][val])

        tup = None
        if type(stat_func) is str:
            tup = tuple([stat_func])
        else:
            tup = stat_func    
        return unique_array,unique_array_ref,tup

    def get_ids(self, cell_key, state, is_ref):
        ids = []
        cells = self.cells_data if not is_ref else self.cells_data_ref
        for x in cells[cell_key][state]:
            ids.append(x)
        ids = np.array(ids)

        return ids

    def get_cell_stat_data(self, cell_name, stat, segmentations):
        if cell_name not in self.cells_data or cell_name not in self.cells_data_ref:
            self.calc_cell_data(cell_name, segmentations)

        return self.cells_data[cell_name][stat], self.cells_data_ref[cell_name][stat]

    def calc_cell_data(self, cell_name, segmentations):
        
        if cell_name in self.cells_data and cell_name in self.cells_data_ref:
            return
        
          #todo - hagai
        dict = {'None':'None'}
        lst = []
        lst.append(dict)
        cols = []
        rows = lst
        if segmentations == []:
            cols = lst
        else:
            cols = segmentations

        uniqueTP, uniqueTP_ref, _ = self.calc_unique_detections(cols,rows,'TP')
        uniqueFP, uniqueFP_ref, _ = self.calc_unique_detections(cols,rows,'FP')
        uniqueFN, uniqueFN_ref, _  = self.calc_unique_detections(cols,rows,'FN')
               

        self.cells_data_ref[cell_name] = {
            'TP':uniqueTP_ref,
            'FP':uniqueFP_ref,
            'FN':uniqueFN_ref
        }

        self.cells_data[cell_name] = {
            'TP':uniqueTP,
            'FP':uniqueFP,
            'FN':uniqueFN
        }

    @staticmethod       
    def match_frame_predictions(predictions, ref_predictions, exp):
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
                    overlap = exp.overlap_function(pred, ref)
                    mat[i, j] = round(overlap, 2)

        #the evaluation function should add the matched prediction to the right record in predictions list
        exp.evaluation_function(predictions, mat)
            
    #create dictionsary for main/ref report with matched bounding box in ref/main if there is any
    @staticmethod
    def match_main_ref_predictions(exp, ref_exp):
        """
        Match all the predictions in main reort and ref report. Detections with no matched detection in the ref report, will have no entry in the dictionary.
        :param exp: main experiment object.
        :param ref_exp: ref experiment object.
        :return: main_ref,ref_main :dictionary between detection in main report to detections in the ref report.
        """
        
        print('start calculating main/ref matched bounding boxes')
        
        main_ref = {}
        ref_main = {}
        
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
                
                UniqueHelper.match_frame_predictions(predictions, ref_predictions, exp)
                for _, x in enumerate(predictions): 
                    if 'matching' in x:
                        main_ref[x['index']]=ref_predictions[x['matching']]['index']
                        ref_main[ref_predictions[x['matching']]['index']] = x['index']
                        
        print ('Finished calculate matched bounding boxes')      
        return main_ref, ref_main