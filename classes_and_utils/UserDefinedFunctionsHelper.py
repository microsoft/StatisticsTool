import os,importlib,sys
from glob import glob
from pathlib import Path
from app_config.config import AppConfig
from app_config.constants import Constants, UserDefinedConstants
from classes_and_utils.utils import loading_json
from utils.report_metadata import *
from utils.report_metadata import READING_FUNCTION_OLD_TOKEN
from utils.report_metadata import GT_READING_FUNC_TOKEN
from utils.report_metadata import PREDICTIONS_READING_TOKEN
from utils.report_metadata import PARTITIONING_FUNC_TOKEN
from utils.report_metadata import STATISTICS_FUNC_TOKEN
from utils.report_metadata import TRANSFORM_FUNC_TOKEN
from utils.report_metadata import OVERLAP_FUNC_TOKEN
from utils.report_metadata import EVALUATION_FUNC_TOKEN
from utils.report_metadata import THRESHOLD_TOKEN
from utils.report_metadata import CONFUSION_FUNC_TOKEN
from utils.report_metadata import LOGS_TO_EVALUATE_TOKEN

class UdfObject:
    def __init__(self,func_type,func_name,params):
        self.func_type  = func_type
        self.func_name  = func_name
        self.func       = get_userdefined_function(self.func_type,self.func_name)
        self.params     = params
    
    def __call__(self, *kargs):
        self.func(*kargs, **self.params)

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
    if hasattr(module,Constants.UDF_USER_ARGUMENT_FUNCTION):
        return getattr(module,Constants.UDF_USER_ARGUMENT_FUNCTION)
    else:
        return None

def get_users_defined_functions(directoryName):
    user_defined_functions = []
    path = os.path.join(get_external_lib_path(), Constants.USER_DEFINED_FUNCTIONS, directoryName,'*')
    files = glob(path)
    for fullname in files:
        filename = fullname.split(os.sep)[-1]
        file_parts = filename.split('.')
        if len(file_parts) == 2 and file_parts[1] == 'py':
            #user_defined_functions.append(file_parts[0])
            arguments = ''
            arg_func = get_udf_argument_function(directoryName,file_parts[0])
            if arg_func is not None:
                arguments = arg_func()
            udf = {'func_name':file_parts[0],'func_arguments':arguments} 
            user_defined_functions.append(udf)
        
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
        prediction_reading_func = config_dict[READING_FUNCTION_OLD_TOKEN]    
    else:
        prediction_reading_func = config_dict.get(PREDICTIONS_READING_TOKEN)    

    gt_reading_func = config_dict.get(GT_READING_FUNC_TOKEN)
    partitioning_func = config_dict.get(PARTITIONING_FUNC_TOKEN) 
    statistics_func = config_dict.get(STATISTICS_FUNC_TOKEN)
    transform_func = config_dict.get(TRANSFORM_FUNC_TOKEN)
    overlap_func = config_dict.get(OVERLAP_FUNC_TOKEN)
    evaluation_func = config_dict.get(EVALUATION_FUNC_TOKEN)
    threshold = config_dict.get(THRESHOLD_TOKEN)
    confusion_func = config_dict.get(CONFUSION_FUNC_TOKEN)
    
    gt_reading_obj          = UdfObject(UserDefinedConstants.READING_FUNCTIONS,gt_reading_func['func_name'],gt_reading_func['params'])
    overlap_obj             = UdfObject(UserDefinedConstants.OVERLAP_FUNCTIONS,overlap_func['func_name'],overlap_func['params']) 
    evaluation_obj          = UdfObject(UserDefinedConstants.EVALUATION_FUNCTIONS,evaluation_func['func_name'],evaluation_func['params']) 
    statistics_obj          = UdfObject(UserDefinedConstants.STATISTICS_FUNCTIONS,statistics_func['func_name'],statistics_func['params']) 
    partitioning_obj        = UdfObject(UserDefinedConstants.PARTITIONING_FUNCTIONS,partitioning_func['func_name'],partitioning_func['params']) 
    transform_obj           = UdfObject(UserDefinedConstants.TRANSFORM_FUNCTIONS,transform_func['func_name'],transform_func['params']) 
    prediction_reading_obj  = UdfObject(UserDefinedConstants.READING_FUNCTIONS,prediction_reading_func['func_name'],prediction_reading_func['params']) 
    confusion_obj           = UdfObject(UserDefinedConstants.CONFUSION_FUNCTIONS,confusion_func['func_name'],confusion_func['params']) 
    #gt_reading_func = get_userdefined_function(UserDefinedConstants.READING_FUNCTIONS,gt_reading_func_name)
    #overlap_func = get_userdefined_function(UserDefinedConstants.OVERLAP_FUNCTIONS,overlap_func_name)
    #evaluation_func = get_userdefined_function(UserDefinedConstants.EVALUATION_FUNCTIONS,evaluation_func_name)
    #statistics_func = get_userdefined_function(UserDefinedConstants.STATISTICS_FUNCTIONS,statistics_func_name) 
    #partitioning_func = get_userdefined_function(UserDefinedConstants.PARTITIONING_FUNCTIONS,partitioning_func_name)
    #transform_func = get_userdefined_function(UserDefinedConstants.TRANSFORM_FUNCTIONS,transform_func_name)
    #prediction_reading_func = get_userdefined_function(UserDefinedConstants.READING_FUNCTIONS, prediction_reading_func_name)
    #confusion_func = get_userdefined_function(UserDefinedConstants.CONFUSION_FUNCTIONS, confusion_func_name)

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

    
    #return prediction_reading_func,gt_reading_func, overlap_func, evaluation_func, statistics_func, partitioning_func, transform_func, threshold, log_names_to_evaluate,confusion_func
    return prediction_reading_obj,gt_reading_obj, overlap_obj, evaluation_obj, statistics_obj, partitioning_obj, transform_obj, threshold, log_names_to_evaluate,confusion_obj
