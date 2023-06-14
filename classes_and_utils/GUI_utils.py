import base64
from datetime import datetime
import sys, os
from glob import glob

from utils.image_util import draw_detection_on_figure, read_frame_from_video

sys.path.append(os.path.join(os.path.join(os.path.realpath(__file__), '..'), '..'))
from utils.AzureStorageHelper import *
from classes_and_utils.ParallelExperiment import *
from classes_and_utils.VideoEvaluation import compare_predictions_directory
from classes_and_utils.utils import loading_json, save_json
from utils.sheldon_export_header import *
import pickle
import json
from pathlib import Path

READING_FUNCTIONS = 'reading_functions'
EVALUATION_FUNCTIONS = 'evaluation_functions'
OVERLAP_FUNCTIONS = 'overlap_functions'
PARTITIONING_FUNCTIONS = 'partitioning_functions'
STATISTICS_FUNCTIONS = 'statistics_functions'
TRANSFORM_FUNCTIONS = 'transform_functions'

METADATA_EXTENTION = '.metadata.json'
EXPERIMENT_EXTENTION = '.pkl'
WIKI_URL =  "https://www.deviceswiki.com/wiki/Statistics_Tool"
INTERMEDIATE_RESULTS_DIR="intermediate resutls"
CONFIG_FILE_NAME = "configs"

MAIN_EXP = 'main'
REF_EXP = 'ref'

def get_configs_folder():
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG_FILE_NAME)
    return folder

def save_experiment(obj, out_folder, config_file_name):
    """
    Saves an object using pickle in a certain path
    :param obj: any python object (in this project we use it to save an instance of  class ParallelExperiment)
    :param filename: full path to the saved object
    """
    report_name = os.path.splitext(config_file_name)[0]
    report_file_name = report_name + EXPERIMENT_EXTENTION
    report_output_file = os.path.join(out_folder, report_file_name)

    with open(report_output_file, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    metadata = {}  

    config_file_path = os.path.join(get_configs_folder(), config_file_name)
    if os.path.exists(config_file_path):
        with open(config_file_path) as conf:
            metadata = json.load(conf)[0]
    
    metadata.update(obj.sheldon_header_data)
    output_file = os.path.join(out_folder,report_name+METADATA_EXTENTION)
    with open(output_file, 'w') as f:
        json.dump(metadata, f)

    return report_output_file

def load_object(file):
    """
    Loads a pickle file from a path
    :param filename: the path from which the function loads the pickle file
    :return: the loaded file
    """
    ret_exp = None
    ## Load  pickle
    if type(file).__name__ == 'str':
        with open(file, 'rb') as input:
            ret_exp = pickle.load(input)
    elif type(file).__name__ == 'FileStorage':
        ret_exp = pickle.load(file.stream)
    else:
        raise TypeError("Unable to load pickle")
    
    ## Update values
    ret_exp.main_ref_dict=None
    ret_exp.ref_main_dict=None

    return ret_exp

def folder_func(output_dir, config_file_name):
    """
    Checks that the output directory folder is empty and then opens the appropriate sub folders
    :param output_dir: path to output directory
    :return: Boolean, indicates whether the folder was empty or not
    """
    try:
        output_dir=os.path.join(output_dir,f'{os.path.splitext(config_file_name)[0]}-{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}')
        
        if os.path.exists(output_dir):
            return False, output_dir
        
        os.makedirs(output_dir)
       
        return True, output_dir
    except FileNotFoundError:
        return "FileNotFound", output_dir

'''
    directoryName -  one of the followings:
    1. evaluation_functions
    2. overlap_functions
    3. partitioning_functions
    4. reading_functions
    5. statistics_functions
    6. transform_functions
'''
def get_userdefined_function(func_type,func_name):
    module_name = 'user_defined_functions' + "." + func_type + "." + func_name
    module = __import__(module_name, fromlist='user_defined_functions')
    reading_func = getattr(module,func_name)
    return reading_func


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


def manage_new_report_page(request):
    """
    Accepts request from multiple pages and show the available configuration files
    adds a new configuration file if request came from new_task_config.html

    :param request: request that was sent to '/create_new_report' route
    :param current_file_directory: full path to flask_GUI_main.py
    :return: list of available configuration files
    """
    configs_folder = get_configs_folder()
    # if a new config is added in the GUI
    if "add_config" in request.url:
        # unpack the fields in the request and concentrate it in a configuration dictionary
        new_config, new_config_name = unpack_new_config(request)
        path_to_save = os.path.join(configs_folder, new_config_name+'.json')
        # save the dictionary in the config folder as a json file
        save_json(path_to_save, new_config)
    # check what are the available config files in the config folder
   
    if not os.path.exists(configs_folder):
        os.makedirs(configs_folder)
    possible_configs = os.listdir(configs_folder)
    return possible_configs


def unpack_new_config(request):
    """
    extracts the configurations names from the request and place them in a dictionary
    :param request: request that was sent to '/create_new_report' route
    :return: a dictionary with the selected configurations names
    """
    new_config_name = request.form.get('name')
    threshold = request.form.get('Threshold')
    reading_func_name = request.form.get('Reading_func')
    transform_func_name = request.form.get('transform_func')
    overlap_func_name = request.form.get('overlap_func')
    evaluation_func_name = request.form.get("evaluation_func")
    statistics_func_name = request.form.get('statistics_func')
    partitioning_func_name = request.form.get('partitioning_func')
    log_names_to_evaluate = request.form.get('log_names_to_evaluate')

    new_config = [
        {"File Reading Function": reading_func_name, "Overlap Function": overlap_func_name, "Threshold": threshold,
         "Evaluation Function": evaluation_func_name, "Statistics Functions": statistics_func_name, "Partitioning Functions": partitioning_func_name,
         "Transformation Function":transform_func_name, "Log Names to Evaluate":log_names_to_evaluate }]
    return new_config, new_config_name


def unpack_calc_request(request):
    """
    Accepts request from new_report.html and unpack the parameters for a new report as variables

    :param request: request that was sent to '/calculating_page' route
    :return: parameters needed for a new report
    """
    # receiving the wanted configuration file name from the form
    config_file_name = request.form.get('Configuration')
    # receiving the wanted directories names from the form
    prd_dir = request.form.get('Predictions Directory')
    GT_dir = request.form.get('Ground Truth Directory')
    output_dir = request.form.get('Reporter Output Directory')
    
    return config_file_name, prd_dir, GT_dir, output_dir


def load_config(config_file_name):
    
    # finding the wanted configuration file location and loading it
    config_path = os.path.join(get_configs_folder(), config_file_name)
    config_file = loading_json(config_path)
    config_dict = config_file[0]
    
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
    return reading_func, overlap_func, evaluation_func, statistics_func, partitioning_func, transform_func, threshold, log_names_to_evaluate


def manage_video_analysis(config_file_name, prd_dir, save_stats_dir, gt_dir = None):
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
    reading_func, overlap_func, evaluation_func, statistics_funcs, partitioning_func, transform_func, threshold, log_names_to_evaluate = load_config(config_file_name)
    
    intermediate_dir = os.path.join(save_stats_dir,INTERMEDIATE_RESULTS_DIR)
    if not os.path.exists(intermediate_dir):
        os.makedirs(intermediate_dir)
        
    # extract all the intermediate results from the raw prediction-label files
    compared_videos, sheldon_header_data, user_text = compare_predictions_directory(pred_dir=prd_dir, output_dir = intermediate_dir, overlap_function=overlap_func, 
                                                                 readerFunction=reading_func, transform_func=transform_func, evaluation_func=evaluation_func, gt_dir = gt_dir, log_names_to_evaluate = log_names_to_evaluate)
   
    if len(compared_videos) == 0:
        return None, user_text, None

    # combine the intermediate results for further statistics and example extraction
    exp = experiment_from_video_evaluation_files(statistic_funcs=statistics_funcs,
                                compared_videos=compared_videos, segmentation_funcs=partitioning_func,
                                threshold=threshold, sheldon_header_data=sheldon_header_data, evaluation_function = evaluation_func, 
                                overlap_function = overlap_func)
    
    folder_name = save_stats_dir
    
    report_file_name = save_experiment(exp, folder_name, config_file_name)
    return exp, user_text, report_file_name

def manage_image_request(request, main_exp, ref_exp,main_directory, use_ref, local_path, example_name):
    """
    Accepts the requests to /show_im route and returns an encoded image and the path where the image was saved (if it was saved)

    :param request: request from either example_image (to save) or in examples_list.html
    :param exp: exp is an instance of ParallelExperiment
    :return: an encoded image and the path where the image was saved (if it was saved)
    """
    
    save_path = False
    data = None
    image = None
    # request came from examples_list.html to show an example image

    if example_name:
        example_id = eval(example_name.replace(" ", ","))
   
    video, bb_index,frame_id,_ = example_id
    if local_path:
        video = os.path.join(local_path,video)
    
    image = read_frame_from_video(video, frame_id)
    
    exp = main_exp
    if use_ref:
        exp = ref_exp
    
    pred_bbs, label_bbs, selected_pred_index, selected_label_index = exp.get_detection_bounding_boxes(bb_index)
    detection_text_list = exp.get_detection_properties_text_list(bb_index)
    out_figure = draw_detection_on_figure(image, pred_bbs, label_bbs=label_bbs, selected_pred=selected_pred_index, selected_label=selected_label_index)
    if out_figure is not None:
        data = base64.b64encode(out_figure.getbuffer()).decode("ascii")
    
    if out_figure and 'save_image' in request.args:
        name = example_id[0].replace('.json', '')
        name = name.replace(':','')
        if name.startswith('/'):
            name = name[1:]
        
        save_path = os.path.join(os.path.join(main_directory, 'saved images'), name)
        save_path = os.path.normpath(save_path)
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        save_file = os.path.join(save_path,  str(example_id[1]) + '.png')
        with open(save_file, "wb") as outfile:
            outfile.write(out_figure.getbuffer())
        
    return detection_text_list, data, save_path


