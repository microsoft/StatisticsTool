import numpy as np
import pandas as pd
from dash import html

from classes_and_utils.GUI_utils import match_main_ref_predictions,calc_unique_detections, get_link_for_update_list, MAIN_EXP, REF_EXP

class UniqueHelper:

    def __init__(self,exp,ref_exp):
        self.exp = exp
        self.ref_exp = ref_exp
        self.exp.main_ref_dict, self.exp.ref_main_dict = match_main_ref_predictions(self.exp,self.ref_exp)
        self.main_ref_dict = self.exp.main_ref_dict
        self.ref_main_dict = self.exp.ref_main_dict


    def generate_unique_html_dash_element(self,column_keys,row_keys,stat,exp_name, cell_name):
        '''
            stat: TP,TN,FN
        '''        
        unique_array,unique_array_ref,tup = self.calc_unique_detections(column_keys,row_keys,stat)
        link_unique = get_link_for_update_list(cell_name=cell_name, 
                                                stat=stat, 
                                                is_ref = exp_name==REF_EXP,
                                                is_unique = True)
        num = 0
        if exp_name == MAIN_EXP:
            num = len(unique_array)
        else:
            num = len(unique_array_ref)

        txt_unique = "(unique: " + str(num) + ")"
        unique = html.A(txt_unique ,href=link_unique, target="example-list-div")
        return unique


    def calc_unique_detections(self,column_keys,row_keys,segmentation):

        unique_out = {}
        unique_ref_out = {}
        unique = unique_out
        unique_ref = unique_ref_out

        partition = None
        if list(column_keys[0].values())[0] == 'None' and list(row_keys[0].values())[0] == 'None':
            partition = segmentation
        else:
            lst_partitions = []
            for x in column_keys + row_keys:
                part = list(x.values())[0]
                if part != 'None':
                    lst_partitions.append(part)

            lst_partitions.append(segmentation)                    
            partition = tuple(lst_partitions)                    


            partitions_parts_list = partition

        #if no partition is selected will take total stats
        if type(partition) is str:
            if partition not in self.exp.masks['total_stats']:
                return None,None,None

            partitions_parts_list = [partition]
            mask = self.exp.masks['total_stats'][partition]
            mask_ref = self.ref_exp.masks['total_stats'][partition]
            if 'total' not in unique_out:
                unique_out['total'] = {}
            unique = unique_out['total']
            if 'total' not in unique_ref_out:
                unique_ref_out['total'] = {}
            unique_ref = unique_ref_out['total']
            unique[partition] = {}
            unique_ref[partition] = {}
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
        if type(partition) is str:
            tup = tuple([partition])
        else:
            tup = partition    
        return unique_array,unique_array_ref,tup
