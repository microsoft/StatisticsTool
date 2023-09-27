import csv
from datetime import datetime
from flask import request,redirect
import urllib.parse
from app_config.constants import Args, Constants, NewReportRoutes
from classes_and_utils.UserDefinedFunctionsHelper import get_configs_folder, load_config, get_suites_folder,get_users_defined_functions,get_udf_argument_function
from app_config.constants import UserDefinedConstants

from flask_GUI.flask_server import server
from classes_and_utils.ParallelExperiment import *
from classes_and_utils.utils import loading_json, save_json
from classes_and_utils.experiments.ExperimentRunner import run_experiment
from utils.report_metadata import *


@server.route(NewReportRoutes.NAV_NEW_REPORT, methods=['GET', 'POST'])
def nav_report_func():
    return redirect(f'/static/index.html?new_report=true')

@server.route(NewReportRoutes.GET_ALL_CONFIGS_AND_SUITES, methods=['GET', 'POST'])
def get_all_configs_and_suits():
    possible_configs = manage_new_report_page()
    possible_suites = get_possible_suites()
    
    data = {
        Args.CONFIGS: possible_configs,
        Args.SUITES : possible_suites
    }
    
    return json.dumps(data)


@server.route(NewReportRoutes.GET_SUITE, methods=['GET'])
def get_suite():
    suite_name = request.args.get(Args.SUITE)
    configs = get_suite_configurations(suite_name)
    return json.dumps(configs)

@server.route(NewReportRoutes.SAVE_SUITE, methods=['GET','POST'])
def save_suite():
    suite_name = request.json[Args.SUITE]
    configs = request.json[Args.CONFIGURATIONS]
    data = {
        Args.CONFIGURATIONS: list(csv.reader([configs]))[0]
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

@server.route(NewReportRoutes.GET_ALL_USER_DEFINED_FUNCTIONS, methods=['GET'])
def get_user_defined_functions_list():
    
    functions = dict()
    functions[UserDefinedConstants.READING_FUNCTIONS]       = get_users_defined_functions(UserDefinedConstants.READING_FUNCTIONS)
    functions[UserDefinedConstants.EVALUATION_FUNCTIONS]    = get_users_defined_functions(UserDefinedConstants.EVALUATION_FUNCTIONS)
    functions[UserDefinedConstants.OVERLAP_FUNCTIONS]       = get_users_defined_functions(UserDefinedConstants.OVERLAP_FUNCTIONS)
    functions[UserDefinedConstants.PARTITIONING_FUNCTIONS]  = get_users_defined_functions(UserDefinedConstants.PARTITIONING_FUNCTIONS)
    functions[UserDefinedConstants.STATISTICS_FUNCTIONS]    = get_users_defined_functions(UserDefinedConstants.STATISTICS_FUNCTIONS)
    functions[UserDefinedConstants.TRANSFORM_FUNCTIONS]     = get_users_defined_functions(UserDefinedConstants.TRANSFORM_FUNCTIONS)
    functions[UserDefinedConstants.CONFUSION_FUNCTIONS]     = get_users_defined_functions(UserDefinedConstants.CONFUSION_FUNCTIONS)
    functions[UserDefinedConstants.ASSOCIATION_FUNCTIONS]   = get_users_defined_functions(UserDefinedConstants.ASSOCIATION_FUNCTIONS)

    return json.dumps(functions)

@server.route(NewReportRoutes.GET_UDF_USER_ARGUMENTS, methods=['GET'])
def get_udf_user_arguments():

    func_type = request.args[Args.FUNC_TYPE]
    func_name = request.args[Args.FUNC_NAME]

    f = get_udf_argument_function(func_type,func_name)
    user_args = f()
    return json.dumps(user_args)

@server.route(NewReportRoutes.GET_CONFIGURATION,methods=['GET'])
def get_config():
    config_name = request.args.get(Args.CONFIG)
    config_dict = load_config_dict(config_name)

    return json.dumps(config_dict)

@server.route(NewReportRoutes.SAVE_CONFIGURATION,methods=['POST'])
def save_configuration():
    config_name = request.json[Args.CONFIG_NAME]
    if os.path.splitext(config_name)[1] != Constants.JSON_EXTENSION:
        config_name += Constants.JSON_EXTENSION
    dic = request.json
    del dic[Args.CONFIG_NAME]
    configs_folder = get_configs_folder()
    path_to_save = os.path.join(configs_folder, config_name)
    save_json(path_to_save, [dic])

    configs_folder = get_configs_folder()
    possible_configs = os.listdir(configs_folder)

    return  json.dumps(possible_configs)
    

@server.route(NewReportRoutes.CALCULATING_PAGE, methods=['GET', 'POST'])
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
            process_result, _ = manage_video_analysis(config_file_name, prd_dir, report_dir, gt_dir=GT_dir)   
            process_result[Args.OUTPUT_PATH] = output_path
            all_process_result.append(process_result)
        except Exception as e:
            result[Args.OK] = False
            result[Args.LINK] = ''
            result[Args.MESSAGE] = ''
            result[Args.ERROR_MESSAGE] = f'An error occurred while executing the {config_file_name} configuration file' 
            return  json.dumps(result)

    link = "/viewer/Report_Viewer?&report_file_path=" +  urllib.parse.quote(output_path)

    num_success_files = []
    reading_function_skipped = []
    not_json_files = []
    failed_with_error = []
    skipped_not_in_lognames = []
    for res in all_process_result:
        num_success_files.append(res['num_success_files'])
        reading_function_skipped.append(res['reading_function_skipped'])
        not_json_files.append(res['not_json_files'])
        failed_with_error.append(res['failed_with_error'])
        skipped_not_in_lognames.append(res['skipped_not_in_lognames'])

    result['ok'] = True
    result['link'] = link
    result['files'] = config_names_list
    result['num_success_files'] = num_success_files
    result['reading_function_skipped'] = reading_function_skipped
    result['not_json_files'] = not_json_files
    result['failed_with_error'] = failed_with_error
    result['skipped_not_in_lognames'] = skipped_not_in_lognames
    result['messages'] = None
    result['errorMessage'] = ''
    return json.dumps(result)

def unpack_calc_request(request):
    """
    Accepts request from new_report.html and unpack the parameters for a new report as variables

    :param request: request that was sent to '/calculating_page' route
    :return: parameters needed for a new report
    """
    # receiving the wanted configuration file name from the form
    config_file_names = request.values['Configurations']
    suite_name = request.values['Suite Name']
    # receiving the wanted directories names from the form
    prd_dir = request.values['Predictions Directory']
    GT_dir = request.values['Ground Truth Directory']
    output_dir = request.values['Reporter Output Directory']
        
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
    prediction_reading_func,gt_reading_func, overlap_func, evaluation_func, statistics_func, partitioning_func, transform_func, threshold, log_names_to_evaluate,confusion_fun = load_config(config_file_name)
    
    intermediate_dir = os.path.join(save_stats_dir,Constants.INTERMEDIATE_RESULTS_DIR)
    if not os.path.exists(intermediate_dir):
        os.makedirs(intermediate_dir)
        
    # extract all the intermediate results from the raw prediction-label files

    comp_data, report_run_info, process_result = run_experiment(pred_dir=prd_dir, output_dir = intermediate_dir, 
                                                                overlap_function=overlap_func, 
                                                                threshold=threshold,
                                                                predictionReaderFunction=prediction_reading_func,
                                                                gtReaderFunction=gt_reading_func, 
                                                                transform_func=transform_func, 
                                                                evaluation_func=evaluation_func, 
                                                                local_gt_dir = gt_dir, 
                                                                log_names_to_evaluate = log_names_to_evaluate)    
   
    report_file_name = ParallelExperiment.save_experiment(comp_data, save_stats_dir, config_file_name, report_run_info)
    return process_result, report_file_name

def get_suite_configurations(suite_name):

    if os.path.splitext(suite_name)[1] != ".json":
        suite_name += ".json"

    configurations = []
    suites_folder = get_suites_folder()
    with open(os.path.join(suites_folder,suite_name)) as f:
        data = json.load(f)
        for config in data['configurations']:
            configurations.append(config)
   
    return configurations

