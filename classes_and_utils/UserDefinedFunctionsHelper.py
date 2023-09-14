import os,importlib,sys
from glob import glob
from pathlib import Path
from app_config.config import AppConfig
from app_config.constants import Constants, UserDefinedConstants
from classes_and_utils.utils import loading_json
from utils.report_metadata import *



def get_external_lib_path():
    # need to change to use commandline arguments
    # ex_lib_path = os.environ.get('EXTERNAL_LIB_PATH')
    # if ex_lib_path != None and ex_lib_path != '':
    #     return ex_lib_path
    # else:
    #    
    app_config = AppConfig.get_app_config() 
    return app_config.external_lib_path

def get_configs_folder():
    configs_folder = os.path.join(get_external_lib_path(), Constants.CONFIG_FOLDER_NAME)
    if not os.path.exists(configs_folder):
        os.makedirs(configs_folder)
    return configs_folder

def get_suites_folder():
    suites_folder = os.path.join(get_external_lib_path(), Constants.SUITES_FOLDER_NAME)
    if not os.path.exists(suites_folder):
        os.makedirs(suites_folder)
    return suites_folder

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
    if not func_name or func_name == 'none' or func_name == 'None':
        return None
    sys.path.append(os.path.join(get_external_lib_path(),Constants.USER_DEFINED_FUNCTIONS,func_type))
    module = importlib.import_module(func_name)
    return getattr(module,func_name)

def get_udf_argument_function(func_type,func_name):
    if not func_name or func_name == 'none' or func_name == 'None':
        return None
    sys.path.append(os.path.join(get_external_lib_path(),Constants.USER_DEFINED_FUNCTIONS,func_type))
    module = importlib.import_module(func_name)
    return getattr(module,Constants.UDF_USER_ARGUMENT_FUNCTION)

def get_users_defined_functions(directoryName):
    user_defined_functions = []
    path = os.path.join(get_external_lib_path(), Constants.USER_DEFINED_FUNCTIONS, directoryName,'*')
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
    
    file_reading_funcs   = get_users_defined_functions(UserDefinedConstants.READING_FUNCTIONS)
    Evaluation_funcs     = get_users_defined_functions(UserDefinedConstants.EVALUATION_FUNCTIONS)
    overlap_funcs        = get_users_defined_functions(UserDefinedConstants.OVERLAP_FUNCTIONS)
    partition_funcs      = get_users_defined_functions(UserDefinedConstants.PARTITIONING_FUNCTIONS)
    statistics_funcs     = get_users_defined_functions(UserDefinedConstants.STATISTICS_FUNCTIONS)
    transformation_funcs = get_users_defined_functions(UserDefinedConstants.TRANSFORM_FUNCTIONS)
    confusion_funcs      = get_users_defined_functions(UserDefinedConstants.CONFUSION_FUNCTIONS)
    
    return file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs

def load_config_dict(config_file_name):
    config_path = os.path.join(get_configs_folder(), config_file_name)
    config_file = loading_json(config_path)
    config_dict = config_file[0]
    
    if READING_FUNCTION_OLD_TOKEN in config_dict.keys():
        config_dict[PREDICTIONS_READING_TOKEN] = config_dict[READING_FUNCTION_OLD_TOKEN]
        config_dict.pop(READING_FUNCTION_OLD_TOKEN)

    if GT_READING_FUNC_TOKEN not in config_dict.keys():
        config_dict[GT_READING_FUNC_TOKEN] = 'none'
    return config_dict

def load_config(config_file_name):
    
    config_dict = load_config_dict(config_file_name)
    
    # extracting the configuration from the config file (which is a dictionary at this point)
    if READING_FUNCTION_OLD_TOKEN in config_dict.keys():
        prediction_reading_func_name = config_dict[READING_FUNCTION_OLD_TOKEN]    
    else:
        prediction_reading_func_name = config_dict.get(PREDICTIONS_READING_TOKEN)    

    gt_reading_func_name = config_dict.get(GT_READING_FUNC_TOKEN)
    partitioning_func_name = config_dict.get(PARTITIONING_FUNC_TOKEN) 
    statistics_func_name = config_dict.get(STATISTICS_FUNC_TOKEN)
    transform_func_name = config_dict.get(TRANSFORM_FUNC_TOKEN)
    overlap_func_name = config_dict.get(OVERLAP_FUNC_TOKEN)
    evaluation_func_name = config_dict.get(EVALUATION_FUNC_TOKEN)
    threshold = config_dict.get(THRESHOLD_TOKEN)
    confusion_func_name = config_dict.get(CONFUSION_FUNC_TOKEN)
    
    gt_reading_func = get_userdefined_function(UserDefinedConstants.READING_FUNCTIONS,gt_reading_func_name)
    overlap_func = get_userdefined_function(UserDefinedConstants.OVERLAP_FUNCTIONS,overlap_func_name)
    evaluation_func = get_userdefined_function(UserDefinedConstants.EVALUATION_FUNCTIONS,evaluation_func_name)
    statistics_func = get_userdefined_function(UserDefinedConstants.STATISTICS_FUNCTIONS,statistics_func_name) 
    partitioning_func = get_userdefined_function(UserDefinedConstants.PARTITIONING_FUNCTIONS,partitioning_func_name)
    transform_func = get_userdefined_function(UserDefinedConstants.TRANSFORM_FUNCTIONS,transform_func_name)
    prediction_reading_func = get_userdefined_function(UserDefinedConstants.READING_FUNCTIONS, prediction_reading_func_name)
    confusion_func = get_userdefined_function(UserDefinedConstants.CONFUSION_FUNCTIONS, confusion_func_name)

    if not gt_reading_func:
        gt_reading_func = prediction_reading_func

    log_names_to_evaluate = None
    if LOGS_TO_EVALUATE_TOKEN in config_dict.keys():
        log_names_to_evaluate = config_dict[LOGS_TO_EVALUATE_TOKEN]
        if type(log_names_to_evaluate) == str:
            if log_names_to_evaluate.isspace() or log_names_to_evaluate == '':
                log_names_to_evaluate = None
            else:
                log_names_to_evaluate = log_names_to_evaluate.split(',')

    
    return prediction_reading_func,gt_reading_func, overlap_func, evaluation_func, statistics_func, partitioning_func, transform_func, threshold, log_names_to_evaluate,confusion_func

