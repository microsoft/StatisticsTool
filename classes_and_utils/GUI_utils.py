from datetime import datetime
import sys, os
from glob import glob

sys.path.append(os.path.join(os.path.join(os.path.realpath(__file__), '..'), '..'))
from app_config.constants import constants
from app_config.config import app_config
from utils.AzureStorageHelper import *
from classes_and_utils.ParallelExperiment import *
from classes_and_utils.VideoEvaluation import compare_predictions_directory, VideoEvaluation
from inspect import getmembers, isfunction
from classes_and_utils.utils import loading_json, save_json
from utils.sheldon_export_header import *
from classes_and_utils.file_storage_handler import calc_log_file_full_path
import re, pickle
import numpy as np
import json
from pathlib import Path

READING_FUNCTIONS = 'reading_functions'
EVALUATION_FUNCTIONS = 'evaluation_functions'
OVERLAP_FUNCTIONS = 'overlap_functions'
PARTITIONING_FUNCTIONS = 'partitioning_functions'
STATISTICS_FUNCTIONS = 'statistics_functions'
TRANSFORM_FUNCTIONS = 'transform_functions'
SAVED_BY_USER = "saved by user"
MAIN_EXP = 'main'
REF_EXP = 'ref'

def save_object(obj, filename):
    """
    Saves an object using pickle in a certain path
    :param obj: any python object (in this project we use it to save an instance of  class ParallelExperiment)
    :param filename: full path to the saved object
    """
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    """
    Loads a pickle file from a path
    :param filename: the path from which the function loads the pickle file
    :return: the loaded file
    """
    ## Load  pickle
    with open(filename, 'rb') as input:
        ret_exp = pickle.load(input)
    
    ## If output dir (save_stats_dir) does not exist - create it
    if not os.path.exists(ret_exp.save_stats_dir):
        pkl_output_dir = os.path.split(filename)[0]
        ret_exp.save_stats_dir = os.path.join(pkl_output_dir, SAVED_BY_USER)
        if not os.path.exists(ret_exp.save_stats_dir): # Verify if the new directory exists
            os.makedirs(ret_exp.save_stats_dir)

    ## Update values
    ret_exp.main_ref_dict=None
    ret_exp.ref_main_dict=None

    return ret_exp

def serial_num(file_name):
    """
    This function acts as a key value in python's built in function sort(),
    its goal is to make the sort() function sort according to the serial number of the files which use the form:
    **name**_serialnumber.file_type
    :param file_name: the file's name
    :return: serial_number as an int
    """

    # remove file extension from file name (name.png >>> name)
    file_name = os.path.splitext(file_name)[0]
    # find all indices of dot occurrences in the file name
    dot_occurrences = [i.start() for i in re.finditer("\.", file_name)]
    assert len(
        dot_occurrences) == 0, "file name: " + file_name + " file names are not allowed to have dots in them please change that"
    # find all indices of under line occurrences in the file name
    line_occurrences = [i.start() for i in re.finditer("_", file_name)]
    #assert len(line_occurrences) > 0, "file name: " + file_name + " does not include a serial of the form _xxxx"
    # the serial number should be after the last underline
    if len(line_occurrences) == 0:
        return int(file_name)
    last_line_occ = line_occurrences[-1]
    return int(file_name[last_line_occ + 1:])


def folder_func(output_dir):
    """
    Checks that the output directory folder is empty and then opens the appropriate sub folders
    :param output_dir: path to output directory
    :return: Boolean, indicates whether the folder was empty or not
    """
    save_stats_dir = ''
    try:
        # check that output dir is empty
        if len(os.listdir(output_dir)) > 0:
            empty = False
        # assert len(os.listdir(output_dir)) == 0, 'output directory should be empty'
        else:
            empty = True
            # opening the needed sub-folders
            single_video_hash_saving_dir = os.path.join(output_dir, "intermediate results")
            os.makedirs(single_video_hash_saving_dir)
            save_stats_dir = os.path.join(output_dir, SAVED_BY_USER)
            os.makedirs(save_stats_dir)
            # opening the needed sub-sub-folders
            save_images_dir = os.path.join(save_stats_dir, "saved images")
            save_lists_dir = os.path.join(save_stats_dir, "saved lists")
            save_tables_dir = os.path.join(save_stats_dir, "saved tables")
            os.makedirs(save_images_dir)
            os.makedirs(save_lists_dir)
            os.makedirs(save_tables_dir)
        return empty, save_stats_dir
    except FileNotFoundError:
        return "FileNotFound", save_stats_dir

'''
    directoryName -  one of the followings:
    1. evaluation_functions
    2. overlap_functions
    3. partitioning_functions
    4. reading_functions
    5. statistics_functions
    6. transform_functions
'''
def get_users_defined_functions(directoryName):
    user_defined_functions = []
    path = str(os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), 'user_defined_functions', directoryName,'*'))
    files = glob(path)
    for fullname in files:
        filename = fullname.split(os.sep)[-1]
        file_parts = filename.split('.')
        if len(file_parts) == 2 and file_parts[1] == 'py':
            user_defined_functions.append(file_parts[0])
    return user_defined_functions

def options_for_funcs():
    """
    Create lists of all the optional functions in the modules that the user needs to choose from
    :return: lists of all the optional functions
    """
    file_reading_funcs = get_users_defined_functions('reading_functions')
    Evaluation_funcs = get_users_defined_functions('evaluation_functions')
    overlap_funcs = get_users_defined_functions('overlap_functions')
    partition_funcs = get_users_defined_functions('partitioning_functions')
    statistics_funcs = get_users_defined_functions('statistics_functions')
    transformation_funcs = get_users_defined_functions('transform_functions')
    transformation_funcs.append('None')
    
    return file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs


def manage_new_report_page(request, current_file_directory):
    """
    Accepts request from multiple pages and show the available configuration files
    adds a new configuration file if request came from new_task_config.html

    :param request: request that was sent to '/create_new_report' route
    :param current_file_directory: full path to flask_GUI_main.py
    :return: list of available configuration files
    """

    # if a new config is added in the GUI
    if "add_config" in request.url:
        # unpack the fields in the request and concentrate it in a configuration dictionary
        new_config, new_config_name = unpack_new_config(request)
        path_to_save = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI_main.py'),
                                                      os.path.join('configs', new_config_name))
        # save the dictionary in the config folder as a json file
        save_json(path_to_save + '.json', new_config)
    # check what are the available config files in the config folder
    path_to_configs = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI_main.py'), 'configs')
    if not os.path.exists(path_to_configs):
        os.makedirs(path_to_configs)
    possible_configs = os.listdir(path_to_configs)
    return possible_configs


def unpack_new_config(request):
    """
    extracts the configurations names from the request and place them in a dictionary
    :param request: request that was sent to '/create_new_report' route
    :return: a dictionary with the selected configurations names
    """
    new_config_name = request.form.get('name')
    threshold = request.form.get('Threshold')
    image_width = request.form.get('image_width')
    image_height = request.form.get('image_height')
    reading_func_name = request.form.get('Reading_func')
    transform_func_name = request.form.get('transform_func')
    overlap_func_name = request.form.get('overlap_func')
    evaluation_func_name = request.form.get("evaluation_func")
    statistics_func_name = request.form.get('statistics_func')
    partitioning_func_name = request.form.get('partitioning_func')
    log_names_to_evaluate = request.form.get('log_names_to_evaluate')

    new_config = [
        {"File Reading Function": reading_func_name, "Overlap Function": overlap_func_name, "Threshold": threshold,
         "Evaluation Function": evaluation_func_name, "Image Width": image_width, "Image Height": image_height,
         "Statistics Functions": statistics_func_name, "Partitioning Functions": partitioning_func_name,
         "Transformation Function":transform_func_name, "Log Names to Evaluate":log_names_to_evaluate }]
    return new_config, new_config_name


def unpack_calc_request(request, current_file_directory):
    """
    Accepts request from new_report.html and unpack the parameters for a new report as variables

    :param request: request that was sent to '/calculating_page' route
    :param current_file_directory: full path to flask_GUI_main.py
    :return: parameters needed for a new report
    """
    # receiving the wanted configuration file name from the form
    config_file_name = request.form.get('Configuration')
    # receiving the wanted directories names from the form
    prd_dir = request.form.get('Predictions Directory')
    GT_dir = request.form.get('Ground Truth Directory')
    output_dir = request.form.get('Reporter Output Directory')
    
    output_dir=os.path.join(output_dir, datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    os.makedirs(output_dir)
    
    single_video_hash_saving_dir = os.path.join(output_dir, "intermediate results")
    
    # finding the wanted configuration file location and loading it
    config_path = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI_main.py'),
                                                 os.path.join('configs', config_file_name))
    config_file = loading_json(config_path)
    config_dict = config_file[0]
    return config_file_name, prd_dir, GT_dir, output_dir, single_video_hash_saving_dir, config_dict


def unpack_calc_config_dict(config_dict):
    """
    Accepts a dictionary with configuration names and returns the correct functions and variables
    :param config_dict: a dictionary with the selected configuration for the report
    :return: the functions mentioned in the configuration dictionary
    """
    # extracting the configuration from the config file (which is a dictionary at this point)
    transform_func_name = 'None'
    if 'Transformation Function' in config_dict:
        transform_func_name = config_dict['Transformation Function']
    reading_func_name = config_dict["File Reading Function"]
    overlap_func_name = config_dict["Overlap Function"]
    evaluation_func_name = config_dict["Evaluation Function"]
    threshold = config_dict["Threshold"]
    log_names_to_evaluate = None
    
    if "Log Names to Evaluate" in config_dict.keys():
        log_names_to_evaluate = config_dict["Log Names to Evaluate"]
        if type(log_names_to_evaluate) == str:
            if log_names_to_evaluate.isspace() or log_names_to_evaluate == '':
                log_names_to_evaluate = None
            else:
                log_names_to_evaluate = log_names_to_evaluate.split(',')

    if "Image Width" in config_dict.keys():
        image_width = config_dict["Image Width"]
        image_height = config_dict["Image Height"]
    # Case Image width and height weren't supplied in the JSON
    else:
        # Set default size 500x500
        image_width = 500
        image_height = 500
    statistics_func_name = config_dict["Statistics Functions"]
    partitioning_func_name = config_dict["Partitioning Functions"]


    reading_func = get_userdefined_function(READING_FUNCTIONS,reading_func_name)
    overlap_func = get_userdefined_function(OVERLAP_FUNCTIONS,overlap_func_name)
    evaluation_func = get_userdefined_function(EVALUATION_FUNCTIONS,evaluation_func_name)
    statistics_func = get_userdefined_function(STATISTICS_FUNCTIONS,statistics_func_name)
    partitioning_func = get_userdefined_function(PARTITIONING_FUNCTIONS,partitioning_func_name)
    transform_func = None
    if transform_func_name != 'None':
        transform_func = get_userdefined_function(TRANSFORM_FUNCTIONS,transform_func_name)
    return reading_func, overlap_func, evaluation_func, statistics_func, partitioning_func, transform_func, threshold, image_width, image_height, log_names_to_evaluate

def get_userdefined_function(func_type,func_name):
    module_name = 'user_defined_functions' + "." + func_type + "." + func_name
    module = __import__(module_name, fromlist='user_defined_functions')
    reading_func = getattr(module,func_name)
    return reading_func

def manage_video_analysis(config_file_name, prd_dir, single_video_hash_saving_dir, save_stats_dir, config_dict, gt_dir = None):
    """

    :param config_file_name: the name of the selected configurations file
    :param prd_dir: the folder that contains the predictions
    :param GT_dir: the folder that contains the GT
    :param single_video_hash_saving_dir: the folder in which to save the intermediate results to (and load them in combine_video_results())
    :param save_stats_dir: the folder in which to save the final results to (e.g report, example images and tables etc. )
    :param images_dir: the folder that contains the images
    :param config_dict: a dictionary with the selected configuration for the report
    :return:
    """

    # extract the functions specified in the configuration file
    reading_func, overlap_func, evaluation_func, statistics_funcs, partitioning_func, transform_func, threshold, image_width, image_height, log_names_to_evaluate = unpack_calc_config_dict(
        config_dict)
    # extract matching lists of absolute paths for the predictions, labels and images
  
    # extract all the intermediate results from the raw prediction-label files
    compared_videos, sheldon_header_data = compare_predictions_directory(pred_dir=prd_dir, output_dir = single_video_hash_saving_dir, overlap_function=overlap_func, 
                                                                 readerFunction=reading_func, transform_func=transform_func, evaluation_func=evaluation_func, gt_dir = gt_dir, log_names_to_evaluate = log_names_to_evaluate)
   
    if len(compared_videos) == 0:
        return None

    # combine the intermediate results for further statistics and example extraction
    exp = experiment_from_video_evaluation_files(statistic_funcs=statistics_funcs,
                                compared_videos=compared_videos, segmentation_funcs=partitioning_func,
                                threshold=threshold, image_width=image_width, image_height=image_height,
                                sheldon_header_data=sheldon_header_data, evaluation_function = evaluation_func, 
                                overlap_function = overlap_func, save_stats_dir = save_stats_dir)

    save_object(exp, os.path.join(save_stats_dir, 'report_' + config_file_name.replace('.json', '') + '.pkl'))
    return exp


def unpack_stats_request(request):
    """
    Accepts requests for /stats route from multiple pages and returns the partition names that were selected and a save Boolean
    :param request: request from either Reporter_page.html or table.html
    :return: partition names that were selected and a save Boolean
    """
    unique = request.form.get('unique')
    if request.form.get('partition0'):
        # request to show statistics from Reporter_page.html
        primary = request.form.get('partition0') if request.form.get('partition0') != 'N/A' else None
        secondary = request.form.get('partition1') if (
                request.form.get('partition1') != 'N/A' and primary is not None) else None
        tertiary = request.form.get('partition2') if (
                request.form.get('partition2') != 'N/A' and secondary is not None) else None
        save = False
    # elif 'stats_pivot' in request.referrer: ##Temp to parse requests from new dash pivot table
    #     request_inputs = request.json['inputs']
    #     segmentaion_cat_2_axis = {segmentation_category:curr_input['id']  for curr_input in request_inputs\
    #                              for segmentation_category in curr_input['value']}
    #     if len(segmentaion_cat_2_axis)>3:
    #         assert "Currently can't treatmore than 3 segmentations"
    #     segmentations = list(segmentaion_cat_2_axis.keys())
    #     primary   = segmentations[0] if len(segmentations) >=1 else None
    #     secondary = segmentations[1] if len(segmentations) >=2 else None
    #     tertiary  = segmentations[2] if len(segmentations) >=3 else None
    #     save = True
    else:
        # request to save the statistics from table.html
        primary = request.args.get('primary') if request.args.get('primary') != 'None' else None
        secondary = request.args.get('secondary') if (
                request.args.get('secondary') != 'None' and primary is not None) else None
        tertiary = request.args.get('tertiary') if (
                request.args.get('tertiary') != 'None' and secondary is not None) else None
        save = True
    return primary, secondary, tertiary, save, unique


def save_tables(statistics_df, state_df, save, primary, secondary, tertiary, save_stats_dir):
    """

    :param statistics_df: pandas dataframe of the partitioned statistics (e.g precision - recall) (multi index)
    :param state_df: pandas dataframe of the partitioned states (e.g TP/FP/FN) (multi index)
    :param save: Boolean, indicates whether or not to save the statistics
    :param primary: #1 partition selected
    :param secondary: #2 partition selected
    :param tertiary: #3 partition selected
    :param save_stats_dir: folder to which the data will be saved
    :return: the path to which the data was saved
    """
    save_path = None
    if save == True:
        save_path = os.path.join(os.path.join(save_stats_dir, 'saved tables'), "segmented_statistics")
        # adding the partitions to the name of the saved file
        for name in [primary, secondary, tertiary]:
            if name:
                partition_name = "_" + name
                save_path += partition_name
        save_path += '.xlsx'
        writer = pd.ExcelWriter(save_path, engine='xlsxwriter')
        statistics_df.to_excel(writer, sheet_name='statistics', startcol=3)
        state_df.to_excel(writer, sheet_name='state_count', startcol=3)
        writer.save()
    return save_path


def stats_4_html(primary, secondary, tertiary, masks):
    """
    Accepts the partitions needed and returns their arrangement in a table as rows, columns etc.

    :param primary: #1 partition selected
    :param secondary: #2 partition selected
    :param tertiary: #3 partition selected
    :param masks: the exp.masks dictionary that contains the boolean masks for the partitions
    :return: titles of the rows, sub-rows, column etc. of the statistical table to be shown to the user
    """
    wanted_seg = {}
    # extract the partition options for each partition (example: for the partition "vehicles" the options could be 'car' and 'bus')
    for partition in [primary, secondary, tertiary]:
        if partition:
            wanted_seg[partition] = masks[partition]['possible partitions']
    # the number of partitions that was asked for by the user will determine the arrangement of the table
    seg_num = len(wanted_seg)
    columns, sub_rows, rows = [], [], []
    # if there is one or more partitions the row's titles will be the 1st partition
    if seg_num > 0:
        rows += wanted_seg[primary]
    # if there are two or more partitions the column's titles will be the second partition
    if seg_num > 1:
        columns += wanted_seg[secondary]
    # if there are three partitions the sub rows will be the 3rd partition
    if seg_num == 3:
        sub_rows += wanted_seg[tertiary]
    return columns, sub_rows, rows, wanted_seg, seg_num


def manage_stats_request(request, exp):
    """
    Manages all the procedures needed when a request is received by /stats route
    :param request: request from either Reporter_page.html or table.html
    :param exp: the ParallelExperiment instance
    :return: all the parameters needed for displaying the statistics results on table.html
    """
    # unpack the values of the request from different pages
    primary, secondary, tertiary, save, unique = unpack_stats_request(request)
    # get the partitioned statistics

   
    statistics_df, state_df, statistics_dict, state_dict = exp.statistics_visualization(primary_segmentation=primary,
                                                                                        secondary_segmentation=secondary,
                                                                                        tertiary_segmentation=tertiary)
    # if asked to save the stats save_tables will do that
    # save_path = save_tables(statistics_df, state_df, save, primary, secondary, tertiary, exp.save_stats_dir)
    save_path = '' # TODO: need to re-use it with new pivot table
    # combined names and dictionaries of the statistics (e.g precision/recall) and states (e.g FP/FN/TP)
    wanted_statistics_names = list(set([index[-1] for index in statistics_dict])) + ['TP', 'FP', 'FN']
    statistics_dict.update(state_dict)
    
    # get the values of the rows, columns etc. for the html table if those values exists
    columns, sub_rows, rows, wanted_seg, seg_num = stats_4_html(primary, secondary, tertiary, exp.masks)
    return statistics_dict, wanted_seg, seg_num, wanted_statistics_names, columns, sub_rows, rows, primary, secondary, tertiary, save_path, unique

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
        # total, primary, secondary, tertiary = None, None, None, None
        # mytup is a tuple that varies in size and include the names of the selected
        # row, sub row, column (partitions) if exists, and the name of the state chosen from the table.
        # mytup is a match to a key in the statistics/state dictionary
        # if "tup" in request.args: # Related to old table. Need to get rid of it after starting use new pivot table
        #     mytup = request.args.get('tup')
        #     mytup = eval(mytup)
        #     # the statistics chosen for example list (such as TP/FP/FN)
        #     state = mytup[-1]
        #     cell_key = "*".join(mytup[:-1])+"*" ##TODO:get it directly from the cell!!
        # request came from examples_list.html to save the example list
        # mytup = [] #request.args.get('mytup')
        
        # This is the parsing from new pivot table
        self.cell_name = request.args.get('cell_name') if "cell_name" in request.args else None
        self.state = request.args.get('stat') if "stat" in request.args else None  #This is a string contain 'TP' / 'FP' / 'FN
        
        self.comp_index = 0 if ('ref' in request.args and len(comp_exp)>0) else\
                         -1
        self.exp_in_UpdateList = comp_exp[self.comp_index] if self.comp_index > -1 else \
                                 main_exp
        
        # masks = exp.masks

        self.show_unique = 'unique' in request.args
        self.saved_sheldon = ''
        # The options for possible partitions available 'time of day' 'vehicles'
        # opt = [seg for seg in masks.keys() if seg != 'total_stats']
        # a dictionary that will hold the "class" of partition and the choice, for example {'vehicle': 'bus'}
        # cl_and_choice = {}
        # if the length of mytup is only 1, it only holds the name of the state/statistics (no partitions)
        # if len(mytup) == 1:
        #     total = True
        # else:
        #     # when the length of mytup is larger than 1 the primary segmentation is 1st object in mytup
        #     if len(mytup) > 1:
        #         primary = mytup[0]
        #         # checking which "class" of partition matches this " partition option"
        #         # like matching which class does 'bus' match to in {'time of day', 'vehicles'}
        #         for cl in opt:
        #             if primary in masks[cl]['possible partitions']:
        #                 cl_and_choice[cl] = primary
        #     if len(mytup) > 2:
        #         secondary = mytup[1]
        #         for cl in opt:
        #             if secondary in masks[cl]['possible partitions']:
        #                 cl_and_choice[cl] = secondary
        #     if len(mytup) > 3:
        #         tertiary = mytup[2]
        #         for cl in opt:
        #             if tertiary in masks[cl]['possible partitions']:
        #                 cl_and_choice[cl] = tertiary

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




    def manage_list_request(self, request, main_exp, comp_exp, report_type):
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
        self.list_of_examples = self.exp_in_UpdateList.get_ids_new(self.cell_name, self.state, show_unique=self.show_unique)

        if report_type == 'ORIG':
            raise Exception('Original report is not supported anymore')
            # list_of_examples = exp_in_UpdateList.get_ids(show_unique=show_unique, state=state, total=total, primary=primary, secondary=secondary, tertiary=tertiary)

        # exp_in_UpdateList.state = state ## TODO: TEMP - move it to the right place
        # caculate a per_video_example_hash for a collapsing list of examples and a save path for the user to see

        self.per_video_example_hash = self.create_collapsing_list(self.list_of_examples)


    def export_list_to_sheldon(self, images_list, sheldon_header_data,output_dir, cell_name, states, is_unique, comp_index):
        segmentation_list = cell_name.split("*") if cell_name !="*" else ['All']
        sheldon_list = []
        header = {}
        header['header']=sheldon_header_data
        header['header']['segmentation']= segmentation_list
        if is_unique:
            header['header']['segmentation'].append('unique')


        sheldon_list.append(json.dumps(header))
        for file in list(images_list.keys()):
            for event in images_list[file]:
                sheldon_link={}
                sheldon_link['keys']={}
                sheldon_link['keys']['type']='debug'
                sheldon_link['message']={}
                sheldon_link['message']['IsChecked']='False'

                vid = images_list[file][event]['frames'][0][0]
                sheldon_link['message']['Video Location']=vid
                sheldon_link['message']['Frame Number']= images_list[file][event]['frames'][0][2]
                sheldon_link['message']['end_frame'] = images_list[file][event]['end_frame']

                sheldon_link['message']['primary_log_path'] = calc_log_file_full_path(header['header'][PRIMARY_LOG][LOG_FILE_NAME], vid, header['header'][PRIMARY_LOG][LOGS_PATH])
                sheldon_link['message']['secondary_log_path'] = calc_log_file_full_path(header['header'][SECONDARY_LOG][LOG_FILE_NAME], vid, header['header'][SECONDARY_LOG][LOGS_PATH])

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





def manage_image_request(request, main_exp, comp_exp):
    """
    Accepts the requests to /show_im route and returns an encoded image and the path where the image was saved (if it was saved)

    :param request: request from either example_image (to save) or in examples_list.html
    :param exp: exp is an instance of ParallelExperiment
    :return: an encoded image and the path where the image was saved (if it was saved)
    """
    save_path = False
    # request came from examples_list.html to show an example image
    exp = main_exp
    comp_ind=eval(request.args.get('comp_index'))
    if comp_ind>-1:
        exp = comp_exp[comp_ind]

    if request.args.get('example_name'):
        example_id = request.args.get('example_name')
        example_id = eval(example_id.replace(" ", ","))
        example_id[0] += ".json"
        global last_example_id
        last_example_id = example_id
        data, fig = exp.visualize(bb_id=example_id)
    # request came from examples_image.html to show an save an example image (an keep showing it)
    else:
        data, fig = exp.visualize(bb_id=last_example_id)
        name = last_example_id[0].replace('.json', '') + str(last_example_id[1]) + '.png'
        save_path = os.path.join(os.path.join(exp.save_stats_dir, 'saved images'), name)
        fig.savefig(save_path)
    return data, save_path


def calc_unique_detections(partitions, exp, ref_exp, main_ref_dict, ref_main_dict):
    """
    Calc unique detection between two reports

    :partitions: different report partitions
    :param exp: exp is an instance of ParallelExperiment
    :param ref_exp: exp is an instance of ParallelExperiment
    :param main_ref_dict: dictinary that maps each detetion in the report with his matched detections in the ref reort
    :param ref_main_dict: dictinary that maps each detetion in the ref report with his matched detections in the reort
    :return: an encoded image and the path where the image was saved (if it was saved)
    """
    if main_ref_dict is None or ref_main_dict is None:
        return

    unique_out = {}
    unique_stats = {}
    unique_ref_out = {}
    unique_stats_ref = {}
    unique = unique_out
    unique_ref = unique_ref_out

    #iterate over all selected partitions
    for cur_partition in partitions:
       
        partitions_parts_list = cur_partition

        #if no partition is selected will take total stats
        if type(cur_partition) is str:
            if cur_partition not in exp.masks['total_stats']:
                continue

            partitions_parts_list = [cur_partition]
            mask = exp.masks['total_stats'][cur_partition]
            mask_ref = ref_exp.masks['total_stats'][cur_partition]
            if 'total' not in unique_out:
                unique_out['total'] = {}
            unique = unique_out['total']
            if 'total' not in unique_ref_out:
                unique_ref_out['total'] = {}
            unique_ref = unique_ref_out['total']
            unique[cur_partition] = {}
            unique_ref[cur_partition] = {}

        else: 
            if partitions_parts_list[-1] not in exp.masks['total_stats']:
                continue

            #calculated current partition masks        
            mask = pd.Series(True, range(exp.comp_data.shape[0]))
            mask_ref = pd.Series(True, range(ref_exp.comp_data.shape[0]))
            for n in partitions_parts_list[:-1]:
                for seg in exp.masks.keys():
                    if 'possible partitions' in exp.masks[seg] and n in exp.masks[seg]['possible partitions']:
                        cur_mask = exp.masks[seg]['masks'][exp.masks[seg]['possible partitions'].index(n)]
                        cur_mask_ref = ref_exp.masks[seg]['masks'][ref_exp.masks[seg]['possible partitions'].index(n)]
                        break    
                mask = mask & cur_mask
                mask_ref = mask_ref & cur_mask_ref
            
            mask = mask & exp.masks['total_stats'][partitions_parts_list[-1]]
            mask_ref = mask_ref & ref_exp.masks['total_stats'][partitions_parts_list[-1]]

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
            if val not in main_ref_dict or ref_exp.masks['total_stats'][partitions_parts_list[-1]][main_ref_dict[val]] != exp.masks['total_stats'][partitions_parts_list[-1]][val]:
                unique_array.append(exp.ID_storage['prediction'][val])

        for val in mask_ref.index[mask_ref==True]:
            if val not in ref_main_dict or exp.masks['total_stats'][partitions_parts_list[-1]][ref_main_dict[val]] != ref_exp.masks['total_stats'][partitions_parts_list[-1]][val]:
                unique_array_ref.append(ref_exp.ID_storage['prediction'][val])

        
        current_unique_segment[partitions_parts_list[-1]] = np.array(unique_array)
        current_unique_segment_ref[partitions_parts_list[-1]] = np.array(unique_array_ref)

        unique_stats[cur_partition] = len(unique_array)
        unique_stats_ref[cur_partition] = len(unique_array_ref)


    return unique_out, unique_ref_out,unique_stats, unique_stats_ref

def get_link_for_update_list(cell_name:str, stat:str, is_ref:bool = False, is_unique:bool = False)-> str:
    unique_flag = "&unique" if is_unique else ""
    ref_flag = "&ref" if is_ref else ""
    link = f"/update_list?cell_name={cell_name}&stat={stat}"+ref_flag+unique_flag
    return link



