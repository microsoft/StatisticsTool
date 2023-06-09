import numpy as np
import os
from classes_and_utils.utils import save_json

from utils.sheldon_export_header import *

class UpdateListManager():
    
    @staticmethod  
    def create_collapsing_list(arr_of_examples):
        """
        :param arr_of_examples: nd array, an array of nd arrays of the form: (video_name, Index, frame)
        :return:
        """
        # removing the .json for display
        # for example in arr_of_examples:
        #     example[0] = example[0].replace(".json", "")
        if len(arr_of_examples) < 1:
            return {}

        # unique video names (image folder names) and an array with values corresponds to the index of certain video
        video_names, v_idx_arr = np.unique(arr_of_examples[:, 0], return_inverse=True)
        per_video_example_hash = {}
        # getting the list in a hierarchy of the form:  1. video 2. frame 3. bouding box index
        per_video_example_hash = dict.fromkeys(video_names)
        for key in per_video_example_hash.keys():
            per_video_example_hash[key] = {}
        
        start_index = -1
        start_frame = -1
        prev_frame = -999
        prev_vid = ''
        for ind, example in enumerate(arr_of_examples):
            if example[1] - prev_frame > 1 or prev_vid != example[0]:
                prev_vid = example[0]
                start_index = example[1]
                start_frame = example[2]
                
            prev_frame = example[1]
            if start_frame not in per_video_example_hash[example[0]]:
                start_index = example[1]
                start_frame = example[2]
                per_video_example_hash[example[0]][start_frame] = {}
                (((per_video_example_hash[example[0]])[start_frame]))['frames']  = []

            
            (((per_video_example_hash[example[0]])[start_frame])['frames']).append(example)
            ((per_video_example_hash[example[0]])[start_frame])['end_frame'] = example[3]

        return per_video_example_hash



    @staticmethod
    def manage_list_request(results_table, main_path, cell_name, stat, show_unique, show_ref_report, save_sheldon_file):
        """
        Accepts a the requests to /update_list route and returns all the parameter needed to show and save the list of examples asked by the user
        :param request: request from either table.html (link writen in macros.html) or in examples_list.html
        :param exp: exp is an instance of ParallelExperiment
        :return: all the parameter needed to show and save the list of examples asked by the user
        """
        # get the names of requested states and partitions, a save boolean and a dictionary of {partition_class: selected_option} (example {"vehicles":"bus"})
        
        exp = results_table.get_ref_exp() if show_ref_report else results_table.get_main_exp()
        # masks = exp.masks

        saved_sheldon = ''

        list_of_examples = results_table.get_ids(cell_name, stat, show_ref_report = show_ref_report, unique=show_unique)

        per_video_example_hash = UpdateListManager.create_collapsing_list(list_of_examples)

        if save_sheldon_file:
            saved_sheldon = UpdateListManager.export_list_to_sheldon(per_video_example_hash, 
                                        exp.sheldon_header_data, 
                                        main_path, 
                                        cell_name,
                                        stat, 
                                        show_unique, 
                                        show_ref_report)
            

        # extracting the example list for requested partitions and state

        # exp_in_UpdateList.state = state ## TODO: TEMP - move it to the right place
        # caculate a per_video_example_hash for a collapsing list of examples and a save path for the user to see

        
        return per_video_example_hash, saved_sheldon

    @staticmethod
    def export_list_to_sheldon(images_list, sheldon_header_data, report_path, cell_name, states, is_unique, show_ref_report):
        segmentation_list = cell_name.split("*") if cell_name !="*" else ['All']
        sheldon_list = []
        header = {}

        output_dir = os.path.dirname(report_path)
        #TODO: Move sheldon header to here
        #Jump file header should be created only when exporting it (on UI)
        new_sheldon_header = create_sheldon_list_header(\
            sheldon_header_data[PRIMARY_LOG][LOGS_PATH],
            sheldon_header_data[PRIMARY_LOG][LOG_FILE_NAME],
            sheldon_header_data[SECONDARY_LOG][LOGS_PATH],
            sheldon_header_data[SECONDARY_LOG][LOG_FILE_NAME],
             '') 


        header['header']=new_sheldon_header
        header['header']['segmentation']= segmentation_list
        if is_unique:
            header['header']['segmentation'].append('unique')


        sheldon_list.append(json.dumps(header))
        for file in list(images_list.keys()):
            for event_key, actual_event in images_list[file].items():
                sheldon_link={}
                sheldon_link['keys']={}
                sheldon_link['keys']['type']='debug'
                sheldon_link['message']={}
                sheldon_link['message']['IsChecked']='False'

                vid_name = actual_event['frames'][0][0].replace(".mp4","")
                sheldon_link['message']['Video Location']=vid_name
                sheldon_link['message']['Frame Number']= actual_event['frames'][0][2]
                sheldon_link['message']['end_frame'] = actual_event['end_frame']

                # sheldon_link['message']['primary_log_path'] = calc_log_file_full_path(header['header'][PRIMARY_LOG][LOG_FILE_NAME], vid_name, header['header'][PRIMARY_LOG][LOGS_PATH])
                # sheldon_link['message']['secondary_log_path'] = calc_log_file_full_path(header['header'][SECONDARY_LOG][LOG_FILE_NAME], vid_name, header['header'][SECONDARY_LOG][LOGS_PATH])

                sheldon_list.append(json.dumps(sheldon_link))
        
        name = ''

        # TODO: Need to check if output_dir  exists. If not, need to ask new directory from the user
        assert(os.path.exists(output_dir))
        
        saved_file = output_dir + os.path.sep
        if show_ref_report > -1:
            saved_file = saved_file+'REF-'

        saved_file = saved_file + '-'.join(segmentation_list) + "-"+states
        if is_unique:
            saved_file = saved_file+'-unique'
        saved_file+='.json'

    
        with open(saved_file, 'w') as f:
            for event in sheldon_list:
                f.write(event+'\n')
            
        return saved_file


