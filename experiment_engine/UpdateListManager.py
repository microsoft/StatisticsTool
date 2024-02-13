import numpy as np
import os
from app_config.config import AppConfig
from app_config.constants import Constants
from experiment_engine.UserDefinedFunctionsHelper import load_function_from_file
from flask_server.dash_apps.results_table import Results_table

from utils.report_metadata import *

class UpdateListManager():
    END_FRAME_LIST = 'end_frame'
    FRAMES = 'frames'
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
                (((per_video_example_hash[example[0]])[start_frame]))[UpdateListManager.FRAMES]  = []

            (((per_video_example_hash[example[0]])[start_frame])[UpdateListManager.FRAMES]).append(example)
            ((per_video_example_hash[example[0]])[start_frame])[UpdateListManager.END_FRAME_LIST] = example[3]

        return per_video_example_hash

    @staticmethod
    def create_list_html(examples, comp_index,main_path,ref_path,unique):
        a=[]
        unique_flag = '' if unique is False else 'unique'

        txt=f'<li><a style="font-family: Arial, Helvetica, sans-serif;" target'
        txt += ' href='+"'javascript:window.parent.postMessage({{"+'"action":"show_image","value":"/show_im?'
        txt += 'example_vid={}&example_index={}&example_frame={}&comp_index={}&main_path={}&ref_path={}&{}"}})'+"'> Frame - {}, Index # {}</a> </li>"
        for vid_key in examples:
            a.append(f'<li><span style="cursor: pointer; font-family: Arial, Helvetica, sans-serif;">{vid_key}</span><ul>')
            for frame_key in examples[vid_key]:
                a.append(f'<li><span style="cursor: pointer; font-family: Arial, Helvetica, sans-serif;"> Frame # {frame_key}-{examples[vid_key][frame_key][UpdateListManager.END_FRAME_LIST]}</span><ul>')
                for example_name in examples[vid_key][frame_key][UpdateListManager.FRAMES]:
                    line = txt.format(example_name[0],example_name[1],example_name[2],comp_index,main_path,ref_path,unique_flag,example_name[2],example_name[1])
                    a.append(line)
                a.append('</ul></li>')
            a.append('</ul></li>')
            
        return "".join(a)

    @staticmethod
    def manage_list_request(results_table, main_path, ref_path, cell_name, stat, show_unique, show_ref_report, save_json_file):
        """
        Accepts a the requests to /update_list route and returns all the parameter needed to show and save the list of examples asked by the user
        :param request: request from either table.html (link writen in macros.html) or in examples_list.html
        :param exp: exp is an instance of ParallelExperiment
        :return: all the parameter needed to show and save the list of examples asked by the user
        """
        # get the names of requested states and partitions, a save boolean and a dictionary of {partition_class: selected_option} (example {"vehicles":"bus"})
        
        output_path = ''

        list_of_examples = results_table.get_ids(cell_name, stat, show_ref_report = show_ref_report, unique=show_unique)

        per_video_example_hash = UpdateListManager.create_collapsing_list(list_of_examples)
        
        if save_json_file:
            output_path = UpdateListManager.export_list(per_video_example_hash,
                                        results_table,
                                        cell_name,
                                        stat, 
                                        show_unique, 
                                        show_ref_report)
            

        # extracting the example list for requested partitions and state

        # exp_in_UpdateList.state = state ## TODO: TEMP - move it to the right place
        # caculate a per_video_example_hash for a collapsing list of examples and a save path for the user to see

        list_html = UpdateListManager.create_list_html(per_video_example_hash, 0 if show_ref_report else -1, main_path, ref_path, show_unique)
        return list_html, output_path

 
    @staticmethod
    def export_list(images_list, results_table:Results_table, cell_name, states, is_unique, show_ref_report):
        app_config = AppConfig.get_app_config()
        if (app_config.custom_export_function):
            try:
                if os.path.exists(app_config.custom_export_function):
                    path = app_config.custom_export_function
                else:
                    path = os.path.join(Constants.SDK_CUSTOMIZATION_FOLDER, app_config.custom_export_function)
                               
                func = load_function_from_file(path)
                output_dir = results_table.main_path if not show_ref_report else results_table.ref_path
                output_file = func(images_list, results_table.get_main_exp(), results_table.get_ref_exp(), output_dir, cell_name, states, is_unique, show_ref_report)
            except Exception as ex:
                print('\nFatal Error: \nFailed to load external storage helper.')
                print (ex)
                return 'Failed!!'
        else:        
            output_file = UpdateListManager.export_list_to_json(images_list, results_table.main_path, results_table.ref_path, cell_name, states, is_unique, show_ref_report)
        
                    
        return output_file 
    
    @staticmethod
    def export_list_to_json(images_list, report_path, ref_report_path, cell_name, states, is_unique, show_ref_report):
        segmentation_list = cell_name.split("*") if cell_name !="*" else ['All']
        json_list = []
        header = {}
        output_dir = os.path.dirname(report_path)
       
        #TODO: Move json header to here
        #Jump file header should be created only when exporting it (on UI)
        new_json_header = create_run_info(\
            os.path.split(report_path)[0],
            os.path.split(report_path)[1],
            os.path.split(ref_report_path)[0] if ref_report_path else '',
            os.path.split(ref_report_path)[1] if ref_report_path else '',
             '') 


        header['header']=new_json_header
        header['header']['segmentation']= segmentation_list
        if is_unique:
            header['header']['segmentation'].append('unique')


        json_list.append(json.dumps(header))
        for file in list(images_list.keys()):
            for event_key, actual_event in images_list[file].items():
                json_link={}
                json_link['keys']={}
                json_link['keys']['type']='debug'
                json_link['message']={}
                json_link['message']['IsChecked']='False'

                vid_name = actual_event[UpdateListManager.FRAMES][0][0].replace(".mp4","")
                json_link['message']['Video Location']=vid_name
                json_link['message']['Frame Number']= actual_event[UpdateListManager.FRAMES][0][2]
                json_link['message']['end_frame'] = actual_event[UpdateListManager.END_FRAME_LIST]

                json_list.append(json.dumps(json_link))
        
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
            for event in json_list:
                f.write(event+'\n')
            
        return saved_file


