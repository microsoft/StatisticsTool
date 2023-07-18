import os
from glob import glob
from pathlib import Path

from app_config.constants import Constants, UserDefinedConstants
from classes_and_utils.utils import loading_json


def get_configs_folder():
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), Constants.CONFIG_FOLDER_NAME)
    return folder

def get_suites_folder():
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), Constants.SUITES_FOLDER_NAME)
    return folder

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


def load_config(config_file_name):
    
    # finding the wanted configuration file location and loading it
    config_path = os.path.join(get_configs_folder(), config_file_name)
    config_file = loading_json(config_path)
    config_dict = config_file[0]
    
    # extracting the configuration from the config file (which is a dictionary at this point)
    transform_func_name = 'None'
    if 'Transformation Function' in config_dict:
        transform_func_name = config_dict['Transformation Function']

    if "File Reading Function" in config_dict.keys():
        prediction_reading_func_name = config_dict["File Reading Function"]    
    else:
        prediction_reading_func_name = config_dict["Prediction Reading Function"]    

    if "GT Reading Function" in config_dict.keys():
        gt_reading_func_name = config_dict["GT Reading Function"]    
    else:                    
        gt_reading_func_name = ''
    
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

    prediction_reading_func = get_userdefined_function(UserDefinedConstants.READING_FUNCTIONS,prediction_reading_func_name)
    if gt_reading_func_name == '' or gt_reading_func_name == 'none':
        gt_reading_func_name = prediction_reading_func
    else:
        gt_reading_func_name = get_userdefined_function(UserDefinedConstants.READING_FUNCTIONS,gt_reading_func_name)

    overlap_func = get_userdefined_function(UserDefinedConstants.OVERLAP_FUNCTIONS,overlap_func_name)
    evaluation_func = get_userdefined_function(UserDefinedConstants.EVALUATION_FUNCTIONS,evaluation_func_name)
    statistics_func = get_userdefined_function(UserDefinedConstants.STATISTICS_FUNCTIONS,statistics_func_name)
    partitioning_func = get_userdefined_function(UserDefinedConstants.PARTITIONING_FUNCTIONS,partitioning_func_name)
    transform_func = None
    if transform_func_name != 'None':
        transform_func = get_userdefined_function(UserDefinedConstants.TRANSFORM_FUNCTIONS,transform_func_name)
    return prediction_reading_func,gt_reading_func_name, overlap_func, evaluation_func, statistics_func, partitioning_func, transform_func, threshold, log_names_to_evaluate
