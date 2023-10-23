import os,importlib,sys
from glob import glob
from pathlib import Path
from app_config.config import AppConfig
from app_config.constants import Constants, UserDefinedConstants
from utils.report_metadata import *


class UdfObject:
    def __init__(self,func_type,func_name,params):
        self.func_type  = func_type
        self.func_name  = func_name
        self.func       = get_userdefined_function(self.func_type,self.func_name)
        self.params     = params
    
    def __call__(self, *kargs):
        return self.func(*kargs, **self.params)

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
            arguments = ''
            arg_func = get_udf_argument_function(directoryName,file_parts[0])
            if arg_func is not None:
                arguments = arg_func()
            udf = {Constants.CONFIG_FUNCTION_NAME_TOKEN:file_parts[0],Constants.CONFIG_FUNCTION_PARAMS_TOKEN:arguments} 
            user_defined_functions.append(udf)
        
    return user_defined_functions

def load_config_dict(config_file_name):
    config_path = os.path.join(get_configs_folder(), config_file_name)
    config_file = None
    with open(config_path) as json_file:
        config_file = json.load(json_file)
    config_dict = config_file[0]

    return config_dict

def load_function_object(func_conf, func_type):
    if func_conf == None:
        return None
    func = UdfObject(func_type,func_conf[Constants.CONFIG_FUNCTION_NAME_TOKEN],func_conf[Constants.CONFIG_FUNCTION_PARAMS_TOKEN] if Constants.CONFIG_FUNCTION_PARAMS_TOKEN in func_conf.keys() else None)
    return func

def load_function_from_dict(config_dict, func_type):
    func = None
    func_conf = config_dict.get(func_type)
    if func_conf:
        func = load_function_object(func_conf, func_type)
    return func

def load_config(config_file_name):
    
    config_dict = load_config_dict(config_file_name)
    
    gt_reading_obj = load_function_from_dict(config_dict, UserDefinedConstants.GT_READING_FUNCTIONS_KEY)
    statistics_obj = load_function_from_dict(config_dict, UserDefinedConstants.STATISTICS_FUNCTIONS_KEY)
    partitioning_obj = load_function_from_dict(config_dict, UserDefinedConstants.PARTITIONING_FUNCTIONS_KEY)
    transform_obj = load_function_from_dict(config_dict, UserDefinedConstants.TRANSFORM_FUNCTIONS_KEY)
    association_obj = load_function_from_dict(config_dict, UserDefinedConstants.ASSOCIATION_FUNCTIONS_KEY)
    confusion_obj = load_function_from_dict(config_dict, UserDefinedConstants.CONFUSION_FUNCTIONS_KEY)
    prediction_reading_obj = load_function_from_dict(config_dict, UserDefinedConstants.READING_FUNCTIONS_KEY)
    
    evaluate_folders = config_dict.get(UserDefinedConstants.EVALUATE_FOLDERS_KEY)

    if gt_reading_obj == None:
        gt_reading_obj = prediction_reading_obj

    log_names_to_evaluate = None
    if UserDefinedConstants.LOGS_TO_EVALUATE_KEY in config_dict.keys():
        log_names_to_evaluate = config_dict[UserDefinedConstants.LOGS_TO_EVALUATE_KEY]
        if type(log_names_to_evaluate) == str:
            if log_names_to_evaluate.isspace() or log_names_to_evaluate == '':
                log_names_to_evaluate = None
            else:
                log_names_to_evaluate = log_names_to_evaluate.split(',')

    return log_names_to_evaluate, prediction_reading_obj, gt_reading_obj, association_obj, transform_obj, evaluate_folders, statistics_obj, partitioning_obj, confusion_obj
