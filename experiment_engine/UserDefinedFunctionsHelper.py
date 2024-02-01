import os,importlib,sys
from glob import glob
from pathlib import Path
from app_config.config import AppConfig
from app_config.constants import Constants, UserDefinedConstants
from utils.report_metadata import *


class UdfObject:
    """
    A class representing a user-defined function object.

    Attributes:
    - func_type (str): The type of the user-defined function.
    - func_name (str): The name of the user-defined function.
    - func (function): The user-defined function.
    - params (dict): The parameters of the user-defined function.
    """
    def __init__(self,func_type,func_name,params):
        self.func_type  = func_type
        self.func_name  = func_name
        self.func       = get_userdefined_function(self.func_type,self.func_name)
        self.params     = params
    
    def __call__(self, *kargs):
        """
        Calls the user-defined function with the given arguments.

        Args:
        - *kargs: The arguments to pass to the user-defined function.

        Returns:
        - The result of the user-defined function.
        """
        return self.func(*kargs, **self.params)

def get_external_lib_path():
    """
    Gets the path to the external library.

    Returns:
    - The path to the external library.
    """
    app_config = AppConfig.get_app_config() 
    return app_config.external_lib_path

def get_configs_folder():
    """
    Gets the path to the folder containing the configuration files.

    Returns:
    - The path to the folder containing the configuration files.
    """
    configs_folder = os.path.join(get_external_lib_path(), Constants.CONFIG_FOLDER_NAME)
    if not os.path.exists(configs_folder):
        os.makedirs(configs_folder)
    return configs_folder

def get_suites_folder():
    """
    Gets the path to the folder containing the test suites.

    Returns:
    - The path to the folder containing the test suites.
    """
    suites_folder = os.path.join(get_external_lib_path(), Constants.SUITES_FOLDER_NAME)
    if not os.path.exists(suites_folder):
        os.makedirs(suites_folder)
    return suites_folder

def get_userdefined_function(func_type,func_name):
    """
    Gets the user-defined function with the given type and name.

    Args:
    - func_type (str): The type of the user-defined function.
    - func_name (str): The name of the user-defined function.

    Returns:
    - The user-defined function.
    """
    if not func_name or func_name == 'none' or func_name == 'None':
        return None
    path = os.path.abspath(os.path.join(get_external_lib_path(),Constants.USER_DEFINED_FUNCTIONS,func_type))
    
    if path not in sys.path:
        sys.path.append(path)
    
    module = importlib.import_module(func_name)
    return getattr(module,func_name)

def get_udf_argument_function(func_type,func_name):
    """
    Gets the argument function for the user-defined function with the given type and name.

    Args:
    - func_type (str): The type of the user-defined function.
    - func_name (str): The name of the user-defined function.

    Returns:
    - The argument function for the user-defined function.
    """
    if not func_name or func_name == 'none' or func_name == 'None':
        return None
    path = os.path.abspath(os.path.join(get_external_lib_path(),Constants.USER_DEFINED_FUNCTIONS))
    
    if path not in sys.path:
        sys.path.append(path)
        
    module = importlib.import_module(func_type+"."+func_name)
    if hasattr(module,Constants.UDF_USER_ARGUMENT_FUNCTION):
        return getattr(module,Constants.UDF_USER_ARGUMENT_FUNCTION)
    else:
        return None

def get_users_defined_functions(directoryName):
    """
    Gets the user-defined functions in the given directory.

    Args:
    - directoryName (str): The name of the directory containing the user-defined functions.

    Returns:
    - A list of dictionaries representing the user-defined functions.
    """
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
    """
    Loads the configuration dictionary from the given configuration file.

    Args:
    - config_file_name (str): The name of the configuration file.

    Returns:
    - The configuration dictionary.
    """
    config_path = os.path.join(get_configs_folder(), config_file_name)
    config_file = None
    with open(config_path) as json_file:
        config_file = json.load(json_file)
    config_dict = config_file[0]

    return config_dict

def load_function_object(func_conf, func_type):
    """
    Loads the user-defined function object from the given configuration and type.

    Args:
    - func_conf (dict): The configuration for the user-defined function.
    - func_type (str): The type of the user-defined function.

    Returns:
    - The user-defined function object.
    """
    if func_conf == None:
        return None
    func = UdfObject(func_type,func_conf[Constants.CONFIG_FUNCTION_NAME_TOKEN],func_conf[Constants.CONFIG_FUNCTION_PARAMS_TOKEN] if Constants.CONFIG_FUNCTION_PARAMS_TOKEN in func_conf.keys() else None)
    return func

def load_function_from_dict(config_dict, func_type):
    """
    Loads the user-defined function from the given configuration dictionary and type.

    Args:
    - config_dict (dict): The configuration dictionary.
    - func_type (str): The type of the user-defined function.

    Returns:
    - The user-defined function.
    """
    func = None
    func_conf = config_dict.get(func_type)
    if func_conf:
        func = load_function_object(func_conf, func_type)
    return func

def load_config(config_file_name):
    """
    Loads the configuration from the given configuration file.

    Args:
    - config_file_name (str): The name of the configuration file.

    Returns:
    - A tuple containing the following:
        - log_names_to_evaluate (list): The names of the logs to evaluate.
        - prediction_reading_obj (UdfObject): The user-defined function object for reading predictions.
        - gt_reading_obj (UdfObject): The user-defined function object for reading ground truth.
        - association_obj (UdfObject): The user-defined function object for association.
        - transform_obj (UdfObject): The user-defined function object for transformation.
        - evaluate_folders (list): The folders to evaluate.
        - statistics_obj (UdfObject): The user-defined function object for statistics.
        - partitioning_obj (UdfObject): The user-defined function object for partitioning.
        - confusion_obj (UdfObject): The user-defined function object for confusion.
    """
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
