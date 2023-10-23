import csv
from datetime import datetime
from flask import request,redirect
import urllib.parse
from app_config.constants import Constants, Tags,URLs
from experiment_engine.UserDefinedFunctionsHelper import get_configs_folder, load_config, get_suites_folder,get_users_defined_functions,get_udf_argument_function
from app_config.constants import UserDefinedConstants
from flask_server.flask_report_view import ReportViewer_Routes,ReportViewer_Tags

from flask_server.flask_server import server
from experiment_engine.ParallelExperiment import *
from experiments_handlers.ExperimentRunner import run_experiment
from utils.report_metadata import *

class NewReport_Routes:
    NAV_NEW_REPORT = '/new_report/nav_new_report'
    GET_ALL_CONFIGS_AND_SUITES = '/new_report/get_all_configs_and_suits'
    GET_SUITE = '/new_report/get_suite'
    SAVE_SUITE = '/new_report/save_suite'
    GET_ALL_USER_DEFINED_FUNCTIONS = '/new_report/get_all_user_defined_functions'
    GET_UDF_USER_ARGUMENTS = '/new_report/get_udf_user_arguments'
    GET_CONFIGURATION = '/new_report/get_configuration'
    SAVE_CONFIGURATION = '/new_report/save_configuration'
    CALCULATING_PAGE = '/new_report/calculating_page'

class NewReport_Tags:
    CONFIG = 'config'
    CONFIG_NAME = 'configName'
    CONFIGS = 'configs'
    SUITES  = 'suites'
    SUITE = 'suite'
    CONFIGURATIONS = 'configurations'
    FUNC_TYPE = 'func_type'
    FUNC_NAME = 'func_name'
    OUTPUT_PATH = 'output_path'
    MESSAGE = 'messages'
    ERROR_MESSAGE = 'errorMessage'
    NUM_SUCCESS_FILES = 'num_success_files'
    READING_FUNCTION_SKIPPED = 'reading_function_skipped'
    NOT_JSON_FILES = 'not_json_files'
    FAILED_WITH_ERROR = 'failed_with_error'
    SKIPPED_NOT_IN_LOGNAMES = 'skipped_not_in_lognames'
    OK = 'ok'
    LINK = 'link'
    FILES = 'files'
    READING_FUNCTION_SKIPPED = 'reading_function_skipped'
    NOT_JSON_FILES = 'not_json_files'
    FAILED_WITH_ERROR = 'failed_with_error'
    SKIPPED_NOT_IN_LOGNAMES = 'skipped_not_in_lognames'
    MESSAGES = 'messages'
    ERROR_MESSAGE = 'errorMessage'
    SUITE_NAME = 'suite_Name'
    PREDICTIONS_DIRECTORY = 'predictions_directory'
    GROUND_TRUTH_DIRECTORY = 'groundtruth_directory'
    REPORTER_OUTPUT_DIRECTORY = 'reporter_output_directory'

@server.route(NewReport_Routes.NAV_NEW_REPORT, methods=['GET', 'POST'])
def nav_report_func():
    url = "{}?{}={}".format(URLs.INDEX_HTML,Tags.NEW_REPORT,'true')
    return redirect(url)

@server.route(NewReport_Routes.GET_ALL_CONFIGS_AND_SUITES, methods=['GET', 'POST'])
def get_all_configs_and_suits():
    possible_configs = manage_new_report_page()
    possible_suites = get_possible_suites()
    
    data = {
        NewReport_Tags.CONFIGS: possible_configs,
        NewReport_Tags.SUITES : possible_suites
    }
    
    return json.dumps(data)


@server.route(NewReport_Routes.GET_SUITE, methods=['GET'])
def get_suite():
    suite_name = request.args.get(NewReport_Tags.SUITE)
    configs = get_suite_configurations(suite_name)
    return json.dumps(configs)

@server.route(NewReport_Routes.SAVE_SUITE, methods=['GET','POST'])
def save_suite():
    suite_name = request.json[NewReport_Tags.SUITE]
    configs = request.json[NewReport_Tags.CONFIGURATIONS]
    data = {
        NewReport_Tags.CONFIGURATIONS: list(csv.reader([configs]))[0]
    }
    json_object = json.dumps(data)
    
    folder = get_suites_folder()
    file_name = suite_name
    if os.path.splitext(file_name)[1] != Constants.JSON_EXTENSION:
        file_name += Constants.JSON_EXTENSION
    path = os.path.join(folder,file_name)
    with open(path, "w") as js:
        js.write(json_object)

    return json.dumps(get_possible_suites())

@server.route(NewReport_Routes.GET_ALL_USER_DEFINED_FUNCTIONS, methods=['GET'])
def get_user_defined_functions_list():
    
    functions = dict()
    functions[UserDefinedConstants.READING_FUNCTIONS_KEY]       = get_users_defined_functions(UserDefinedConstants.READING_FUNCTIONS_KEY)
    functions[UserDefinedConstants.PARTITIONING_FUNCTIONS_KEY]  = get_users_defined_functions(UserDefinedConstants.PARTITIONING_FUNCTIONS_KEY)
    functions[UserDefinedConstants.STATISTICS_FUNCTIONS_KEY]    = get_users_defined_functions(UserDefinedConstants.STATISTICS_FUNCTIONS_KEY)
    functions[UserDefinedConstants.TRANSFORM_FUNCTIONS_KEY]     = get_users_defined_functions(UserDefinedConstants.TRANSFORM_FUNCTIONS_KEY)
    functions[UserDefinedConstants.CONFUSION_FUNCTIONS_KEY]     = get_users_defined_functions(UserDefinedConstants.CONFUSION_FUNCTIONS_KEY)
    functions[UserDefinedConstants.ASSOCIATION_FUNCTIONS_KEY]   = get_users_defined_functions(UserDefinedConstants.ASSOCIATION_FUNCTIONS_KEY)

    return json.dumps(functions)

@server.route(NewReport_Routes.GET_UDF_USER_ARGUMENTS, methods=['GET'])
def get_udf_user_arguments():

    func_type = request.args[NewReport_Tags.FUNC_TYPE]
    func_name = request.args[NewReport_Tags.FUNC_NAME]

    f = get_udf_argument_function(func_type,func_name)
    user_args = f()
    return json.dumps(user_args)

@server.route(NewReport_Routes.GET_CONFIGURATION,methods=['GET'])
def get_config():
    config_name = request.args.get(NewReport_Tags.CONFIG)
    config_dict = load_config_dict(config_name)

    return json.dumps(config_dict)

@server.route(NewReport_Routes.SAVE_CONFIGURATION,methods=['POST'])
def save_configuration():
    config_name = request.json[NewReport_Tags.CONFIG_NAME]
    if os.path.splitext(config_name)[1] != Constants.JSON_EXTENSION:
        config_name += Constants.JSON_EXTENSION
    dic = request.json
    del dic[NewReport_Tags.CONFIG_NAME]
    configs_folder = get_configs_folder()
    path_to_save = os.path.join(configs_folder, config_name)
    
    with open(path_to_save, 'w', encoding='utf-8') as f:
        json.dump([dic], f, ensure_ascii=False, indent=4)

    configs_folder = get_configs_folder()
    possible_configs = os.listdir(configs_folder)

    return  json.dumps(possible_configs)
    

@server.route(NewReport_Routes.CALCULATING_PAGE, methods=['GET', 'POST'])
def calculating():
    
    # extract the user specified directories and names
    suite_name, config_file_names, prd_dir, GT_dir, output_dir = unpack_calc_request(request)
    all_process_result = []
    
    config_names_list = config_file_names.split(',')
    if not suite_name:
        suite_name = "run"
    output_dir = os.path.join(output_dir,suite_name+'-'+datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    
    print("suite output folder: "+output_dir)
    result = dict()
    
    output_path = output_dir.replace('\\','/')
    for config_file_name in config_names_list:
    # making sure save_stats_dir is empty and opening the appropriate folders
        try:
            report_dir=os.path.join(output_dir,f'{os.path.splitext(config_file_name)[0]}-{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}')
            print("report output folder: " + report_dir)
            os.makedirs(report_dir)
            # calculate the intermediate results for all the videos then combine them
            process_result, comp_data = manage_video_analysis(config_file_name, prd_dir, report_dir, gt_dir=GT_dir)   
            process_result[NewReport_Tags.OUTPUT_PATH] = output_path if comp_data else None
            all_process_result.append(process_result)
        except Exception as e:
            result[NewReport_Tags.OK] = False
            result[NewReport_Tags.LINK] = ''
            result[NewReport_Tags.MESSAGE] = ''
            result[NewReport_Tags.ERROR_MESSAGE] = f'An error occurred while executing the {config_file_name} configuration file' 
            return  json.dumps(result)

    #link =  ReportViewer_Constants.URL + "?&" + ReportViewer_Args.REPORT_FILE_PATH + "=" + urllib.parse.quote(output_path)
    URL = ReportViewer_Routes.URL
    REPORT_FILE_PATH = ReportViewer_Tags.REPORT_FILE_PATH
    link = f"{URL}?&{REPORT_FILE_PATH}={urllib.parse.quote(output_path)}"

    num_success_files = []
    reading_function_skipped = []
    not_json_files = []
    failed_with_error = []
    skipped_not_in_lognames = []
    for res in all_process_result:
        num_success_files.append(res[NewReport_Tags.NUM_SUCCESS_FILES])
        reading_function_skipped.append(res[NewReport_Tags.READING_FUNCTION_SKIPPED])
        not_json_files.append(res[NewReport_Tags.NOT_JSON_FILES])
        failed_with_error.append(res[NewReport_Tags.FAILED_WITH_ERROR])
        skipped_not_in_lognames.append(res[NewReport_Tags.SKIPPED_NOT_IN_LOGNAMES])

    result[NewReport_Tags.OK] = True
    result[NewReport_Tags.LINK] = link
    result[NewReport_Tags.FILES] = config_names_list
    result[NewReport_Tags.NUM_SUCCESS_FILES] = num_success_files
    result[NewReport_Tags.READING_FUNCTION_SKIPPED] = reading_function_skipped
    result[NewReport_Tags.NOT_JSON_FILES] = not_json_files
    result[NewReport_Tags.FAILED_WITH_ERROR] = failed_with_error
    result[NewReport_Tags.SKIPPED_NOT_IN_LOGNAMES] = skipped_not_in_lognames
    result[NewReport_Tags.MESSAGES] = None
    result[NewReport_Tags.ERROR_MESSAGE] = ''
    return json.dumps(result)

def unpack_calc_request(request):
    """
    Accepts request from new_report.html and unpack the parameters for a new report as variables

    :param request: request that was sent to '/calculating_page' route
    :return: parameters needed for a new report
    """
    # receiving the wanted configuration file name from the form
    config_file_names = request.values[NewReport_Tags.CONFIGURATIONS]
    suite_name = request.values[NewReport_Tags.SUITE_NAME]
    # receiving the wanted directories names from the form
    prd_dir = request.values[NewReport_Tags.PREDICTIONS_DIRECTORY]
    GT_dir = request.values[NewReport_Tags.GROUND_TRUTH_DIRECTORY]
    output_dir = request.values[NewReport_Tags.REPORTER_OUTPUT_DIRECTORY]
        
    return suite_name,config_file_names, prd_dir, GT_dir, output_dir

def manage_new_report_page():
  
    configs_folder = get_configs_folder()
    # if a new config is added in the GUI
  
    if not os.path.exists(configs_folder):
        os.makedirs(configs_folder)
    possible_configs = os.listdir(configs_folder)
    return possible_configs

def get_possible_suites():
    suites_folder = get_suites_folder()
    possible_suites = os.listdir(suites_folder)
    return possible_suites

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
    log_names_to_evaluate, prediction_reading_func,gt_reading_func, association_func, transform_func, evaluate_folders, _,_,_ = load_config(config_file_name)
    
    intermediate_dir = os.path.join(save_stats_dir,Constants.INTERMEDIATE_RESULTS_DIR)
    if not os.path.exists(intermediate_dir):
        os.makedirs(intermediate_dir)
        
    # extract all the intermediate results from the raw prediction-label files

    comp_data, report_run_info, process_result = run_experiment(pred_dir=prd_dir, output_dir = intermediate_dir, 
                                                                assiciation_function=association_func,
                                                                predictionReaderFunction=prediction_reading_func,
                                                                gtReaderFunction=gt_reading_func, 
                                                                transform_func=transform_func,
                                                                local_gt_dir = gt_dir, 
                                                                log_names_to_evaluate = log_names_to_evaluate,
                                                                evaluate_folders = evaluate_folders)    
   
    report_file_name = None
    if comp_data:
        report_file_name = ParallelExperiment.save_experiment(comp_data, save_stats_dir, config_file_name, report_run_info)
    return process_result, report_file_name

def get_suite_configurations(suite_name):

    if os.path.splitext(suite_name)[1] != Constants.JSON_EXTENSION:
        suite_name += Constants.JSON_EXTENSION

    configurations = []
    suites_folder = get_suites_folder()
    with open(os.path.join(suites_folder,suite_name)) as f:
        data = json.load(f)
        for config in data[NewReport_Tags.CONFIGURATIONS]:
            configurations.append(config)
   
    return configurations

