import numpy as np
import os
from classes_and_utils.utils import save_json

from utils.sheldon_export_header import create_sheldon_list_header

class UpdateListManager():
    def __init__(self) -> None:
        self.per_video_example_hash = {}
        self.exp_in_UpdateList = None #Pointer to the experiment that was choosen: main exp or ref exp
        self.state = None #State that was choised: 'TP'/ 'FP'/ 'FN'
        self.show_unique = None #Boolean that says if the user choose unique value
        self.comp_index = -999 # Index of comparison exp TODO: need to change it - this is very implicitly
        self.saved_list = None 
        self.saved_sheldon = ''


    def unpack_list_request(self, request, main_exp, comp_exp):
        """
        Accepts a request to /update_list route and the masks boolean dictionary and return parameters for
        extraction or saving of an example list

        :param request: request from either table.html (link writen in macros.html) or in examples_list.html
        :param masks: exp.masks (exp is an instance of ParallelExperiment)
        :return: parameters that allow the extraction or saving of an example list
        """
      
        # This is the parsing from new pivot table
        self.cell_name = request.args.get('cell_name') if "cell_name" in request.args else None
        self.state = request.args.get('stat') if "stat" in request.args else None  #This is a string contain 'TP' / 'FP' / 'FN
        
        #self.comp_index = 0 if ('ref' in request.args and len(comp_exp)>0) else\
        #                 -1
        self.comp_index = 0 if comp_exp is not None else -1
        self.exp_in_UpdateList = comp_exp if self.comp_index > -1 else main_exp
        
        # masks = exp.masks

        self.show_unique = 'unique' in request.args
        self.saved_sheldon = ''
      

    def save_examples_list(self, arr_of_examples, cell_name, save_stats_dir, state):
        """

        :param arr_of_examples: nd array, an array of nd arrays of the form: (video_name, Index, frame)
        :param save: Boolean, indicates whether to save the list of examples or not
        :param save_stats_dir: folder to 'saved by user'
        :param state: the state (TP/FP/FN) of the requested example
        """
        # saving the examples as a list of lists

        list_of_examples = []
        for i in range(len(arr_of_examples)):
            list_of_examples.append(list(arr_of_examples[i, :]))
        # adding the partitions to name of the file
        save_dir = os.path.join(save_stats_dir, 'saved lists')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.saved_list = os.path.join(save_dir, 'example_list_' + state)
        self.saved_list += cell_name.replace("*","_")
        self.saved_list += '.json'
        save_json(self.saved_list, list_of_examples)

    def create_collapsing_list(self, arr_of_examples):
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




    def manage_list_request(self, request, main_exp, comp_exp):
        """
        Accepts a the requests to /update_list route and returns all the parameter needed to show and save the list of examples asked by the user
        :param request: request from either table.html (link writen in macros.html) or in examples_list.html
        :param exp: exp is an instance of ParallelExperiment
        :return: all the parameter needed to show and save the list of examples asked by the user
        """
        # get the names of requested states and partitions, a save boolean and a dictionary of {partition_class: selected_option} (example {"vehicles":"bus"})
        if not 'button_pressed' in request.args:
            self.unpack_list_request(request, main_exp, comp_exp)

        if 'sheldon' in request.args:
            self.export_list_to_sheldon(self.per_video_example_hash, 
                                        self.exp_in_UpdateList.sheldon_header_data, 
                                        self.exp_in_UpdateList.save_stats_dir, 
                                        self.cell_name,
                                        self.state, 
                                        self.show_unique, 
                                        self.comp_index)
            return
        
        if "save_list" in request.args:
            self.save_examples_list(self.list_of_examples, self.cell_name, self.exp_in_UpdateList.save_stats_dir, self.state)
            return

        # extracting the example list for requested partitions and state
        self.list_of_examples = self.exp_in_UpdateList.get_ids(self.cell_name, self.state, show_unique=self.show_unique)

        # exp_in_UpdateList.state = state ## TODO: TEMP - move it to the right place
        # caculate a per_video_example_hash for a collapsing list of examples and a save path for the user to see

        self.per_video_example_hash = self.create_collapsing_list(self.list_of_examples)


    def export_list_to_sheldon(self, images_list, sheldon_header_data, output_dir, cell_name, states, is_unique, comp_index):
        segmentation_list = cell_name.split("*") if cell_name !="*" else ['All']
        sheldon_list = []
        header = {}

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
        if comp_index > -1:
            saved_file = saved_file+'REF-'

        saved_file = saved_file + '-'.join(segmentation_list) + "-"+states
        if is_unique:
            saved_file = saved_file+'-unique'
        saved_file+='.json'

    
        with open(saved_file, 'w') as f:
            for event in sheldon_list:
                f.write(event+'\n')
            
        self.saved_sheldon = saved_file


