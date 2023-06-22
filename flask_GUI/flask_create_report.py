
from datetime import datetime
from flask import render_template, request,redirect
import urllib.parse
from app_config.constants import Constants
from classes_and_utils.UserDefinedFunctionsHelper import get_configs_folder, load_config, options_for_funcs,get_suites_folder,get_users_defined_functions
from app_config.constants import UserDefinedConstants

from flask_GUI.flask_server import server
from classes_and_utils.ParallelExperiment import *
from classes_and_utils.utils import loading_json, save_json
from classes_and_utils.VideoEvaluation import compare_predictions_directory


@server.route('/new_report/show_config', methods=['GET', 'POST'])
def show_config():
    config_name = request.args.get('Configuration')
    path_to_wanted_config = os.path.join(get_configs_folder(), config_name)
    config_file = loading_json(path_to_wanted_config)
    config_dict = config_file[0]
    return render_template('show_config.html', config_dict=config_dict, config_name=config_name)

@server.route('/new_report/create_new_report', methods=['GET', 'POST'])
def new_report_func():
    possible_configs = manage_new_report_page(request)
    return render_template('new_report.html', possible_configs=possible_configs, wiki_page = Constants.WIKI_URL)

@server.route('/new_report/nav_new_report', methods=['GET', 'POST'])
def nav_report_func():
    possible_configs = manage_new_report_page(request)
    possible_suites = get_possible_suites()
    js_possible_configs = json.dumps(possible_configs)
    js_possible_suites = json.dumps(possible_suites)
    return redirect(f'/static/index.html?new_report=true&possible_configs={js_possible_configs}&possible_suites={js_possible_suites}')

@server.route('/new_report/get_suite', methods=['GET'])
def get_suite():
    suite_name = request.args.get('suite')
    configs = get_suite_configurations(suite_name)
    return json.dumps(configs)

@server.route('/new_report/save_suite', methods=['GET','POST'])
def save_suite():
    suite_name = request.json['suite']
    configs = request.json['configurations']
    data = {
        'configurations': configs
    }
    json_object = json.dumps(data)
    
    folder = get_suites_folder()
    file_name = suite_name
    if os.path.splitext(file_name)[1] != ".json":
        file_name += ".json"
    path = os.path.join(folder,file_name)
    with open(path, "w") as js:
        js.write(json_object)

    return json.dumps(get_possible_suites())

@server.route('/new_report/get_all_user_defined_functions', methods=['GET'])
def get_user_defined_functions_list():
    
    functions = dict()
    functions[UserDefinedConstants.READING_FUNCTIONS] = get_users_defined_functions(UserDefinedConstants.READING_FUNCTIONS)
    functions[UserDefinedConstants.EVALUATION_FUNCTIONS] = get_users_defined_functions(UserDefinedConstants.EVALUATION_FUNCTIONS)
    functions[UserDefinedConstants.OVERLAP_FUNCTIONS] = get_users_defined_functions(UserDefinedConstants.OVERLAP_FUNCTIONS)
    functions[UserDefinedConstants.PARTITIONING_FUNCTIONS] = get_users_defined_functions(UserDefinedConstants.PARTITIONING_FUNCTIONS)
    functions[UserDefinedConstants.STATISTICS_FUNCTIONS] = get_users_defined_functions(UserDefinedConstants.STATISTICS_FUNCTIONS)
    functions[UserDefinedConstants.TRANSFORM_FUNCTIONS] = get_users_defined_functions(UserDefinedConstants.TRANSFORM_FUNCTIONS)
   
    return json.dumps(functions)

@server.route('/new_report/calculating_page', methods=['GET', 'POST'])
def calculating():
    # extract the user specified directories and names
    suite_name, config_file_names, prd_dir, GT_dir, output_dir = unpack_calc_request(request)
    
    config_names_list = config_file_names.split(',')
    if not suite_name:
        suite_name = "run"
    output_dir = os.path.join(output_dir,suite_name+'-'+datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    
    print("suite output folder: "+output_dir)
        

    for config_file_name in config_names_list:
    # making sure save_stats_dir is empty and opening the appropriate folders
        try:
            report_dir=os.path.join(output_dir,f'{os.path.splitext(config_file_name)[0]}-{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}')
            print("report output folder: " + report_dir)
            os.makedirs(report_dir)
        except:
            return render_template('Not_found.html')
        
        # calculate the intermediate results for all the videos then combine them
        exp, results_text, report_file_name = manage_video_analysis(config_file_name, prd_dir, report_dir, gt_dir=GT_dir)
    
    output_path = output_dir.replace('\\','/')

    if exp == 'TypeError' or exp is None or report_file_name is None:
        link = 'None'
    else:
        link = "/viewer/Report_Viewer?&report_file_path=" +  urllib.parse.quote(output_path)

    results_text = results_text.split('\n')
    results_text.append(f"Output folder: {output_path}.")
    return render_template('message.html', link=link, text=results_text)

@server.route('/new_report/add_config', methods=['GET', 'POST'])
def new_task_func():
    file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs = options_for_funcs()
    return render_template('new_task_config.html', 
                           file_reading_funcs=file_reading_funcs, 
                           Evaluation_funcs=Evaluation_funcs, 
                           overlap_funcs=overlap_funcs, 
                           partition_funcs=partition_funcs, 
                           statistics_funcs=statistics_funcs,
                           transformation_funcs=transformation_funcs)


def unpack_calc_request(request):
    """
    Accepts request from new_report.html and unpack the parameters for a new report as variables

    :param request: request that was sent to '/calculating_page' route
    :return: parameters needed for a new report
    """
    # receiving the wanted configuration file name from the form
    config_file_names = request.form.get('Configurations')
    suite_name = request.form.get('Suite Name')
    # receiving the wanted directories names from the form
    prd_dir = request.form.get('Predictions Directory')
    GT_dir = request.form.get('Ground Truth Directory')
    output_dir = request.form.get('Reporter Output Directory')
    
    return suite_name,config_file_names, prd_dir, GT_dir, output_dir


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

def get_possible_suites():
    suites_folder = get_suites_folder()
    if not os.path.exists(suites_folder):
        os.makedirs(suites_folder)
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
    reading_func, overlap_func, evaluation_func, statistics_funcs, partitioning_func, transform_func, threshold, log_names_to_evaluate = load_config(config_file_name)
    
    intermediate_dir = os.path.join(save_stats_dir,Constants.INTERMEDIATE_RESULTS_DIR)
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
    configs_folder = get_configs_folder()
    report_file_name = exp.save_experiment(folder_name, config_file_name, configs_folder)
    return exp, user_text, report_file_name

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

