import enum
import uuid
import concurrent
import os
import fnmatch
from experiment_engine.ParallelExperiment import ParallelExperiment
from experiment_engine.VideoEvaluation import VideoEvaluation

from experiment_engine.file_storage_handler import *
from utils.LogsParser import get_video_name_from_pred_file
from utils.report_metadata import create_run_info
from app_config.constants import Constants

class ProcessResult(enum.Enum):
    sucess = 0
    skipped_reading = 1
    failed_with_error = 2
    skipped_not_in_lognames = 3

def handel_pred(vars):
    """
    This function handles a single prediction file and compares it to its corresponding ground truth file.
    It returns the prediction file path, the result of the comparison, and the output file path.

    :param vars: a tuple containing the following variables:
        - pred: the path to the prediction file
        - log_names_to_evaluate: a list of log names to evaluate
        - pred_dir: the path to the predictions directory
        - evaluate_folders: a boolean indicating whether to evaluate folders
        - local_gt_dir: the path to the local ground truth directory
        - predictionReaderFunction: a function that reads the prediction file
        - gtReaderFunction: a function that reads the ground truth file
        - assiciation_function: a function that associates predictions with ground truth
        - transform_func: a function that transforms the data
        - output_dir: the path to the output directory

    :return: a tuple containing the prediction file path, the result of the comparison, and the output file path
    """
    gt_local_path = None 
    pred, pred_dir, evaluate_folders, local_gt_dir, predictionReaderFunction, gtReaderFunction, assiciation_function, transform_func, output_dir = vars
    
    try:
        log_name = os.path.basename(pred)

        print(f"Try to find gt for file: {pred}")
        
        pred_file = get_file_on_local_storage(pred, StoreType.Predictions, get_folder=evaluate_folders)

        if pred_file is None:
            print (f"Can't fine file {pred_file}, continue..")
            return pred, ProcessResult.failed_with_error, None
                
        video_name = get_video_name_from_pred_file(pred_file, pred, pred_dir)
        
        if evaluate_folders:
            file_ext = ''
        #if user set local gt folder
        if local_gt_dir:
            gt_local_path = find_in_store_by_video_name(local_gt_dir, video_name, log_name, os.path.exists)
            gt_local_path = os.path.join(local_gt_dir, gt_local_path)
        else: #read gt from blob
            path_on_blob = find_in_blob_by_video_name(video_name, log_name, StoreType.Annotations)
            if path_on_blob:
                gt_local_path = get_file_on_local_storage(path_on_blob, None, get_folder=evaluate_folders)
            
        if gt_local_path is None:
            print(f"GT file: {gt_local_path} not found for prediction: {pred}, continue without gt..")
            gtReaderFunction = None
            
        print(f"Starting comparing files for video {video_name}: {pred} and {gt_local_path}")

        V = VideoEvaluation(predictionReaderFunction=predictionReaderFunction,gtReaderFunction=gtReaderFunction ,associationFunction=assiciation_function, transform_func = transform_func)
        res = V.compute_dataframe(pred_file, gt_local_path, video_name)
        if not res:
            return pred, ProcessResult.skipped_reading, None

        output_file_name = video_name.replace('/', '_')[:10] + '_' + str(uuid.uuid4().hex[:6]) + '.json'
        output_file_name = os.path.join(output_dir, output_file_name)
        output_file_name = os.path.normpath(output_file_name)
        V.save_data(output_file_name)

        print(f"Finished comparing predictions for video {video_name}")
    except Exception as ex:
        print(f"Failed to compare log {pred}, continuing with next log...")
        print(ex)
        return pred, ProcessResult.failed_with_error, None
    
   

    return pred, ProcessResult.sucess, output_file_name

def compare_predictions_directory(pred_dir, output_dir, predictionReaderFunction,gtReaderFunction,transform_func, assiciation_function, local_gt_dir = None, log_names_to_evaluate = None, evaluate_folders=False):
    """
    This function compares all prediction files in a directory to their corresponding ground truth files.
    It returns a dictionary that maps each video file location to its annotations (prediction and ground truth) file location.

    :param pred_dir: the path to the predictions directory
    :param output_dir: the path to the output directory
    :param predictionReaderFunction: a function that reads the prediction file
    :param gtReaderFunction: a function that reads the ground truth file
    :param transform_func: a function that transforms the data
    :param assiciation_function: a function that associates predictions with ground truth
    :param local_gt_dir: the path to the local ground truth directory
    :param log_names_to_evaluate: a list of log names to evaluate
    :param evaluate_folders: a boolean indicating whether to evaluate folders

    :return: a dictionary that maps each video file location to its annotations (prediction and ground truth) file location
    """
    pred_path_list = list_files_in_path(pred_dir, StoreType.Predictions)
    
    if evaluate_folders:
        pred_path_list = list_files_parent_dirs(pred_path_list)

    output_files = []

    pred_file_name = ''
    gt_file_name = ''
    
    succeded = []
    failed = []
    skipped_not_json = []
    skipped_reading_fnc = []
    skipped_not_in_lognames = []

    print(f"total files num: {len(pred_path_list)}")
    logs_to_evaluate = []
    
    for pred in pred_path_list:
        for name in log_names_to_evaluate:
                #Check if file is in log names to evaluate
            name_to_match = pred
            if os.path.dirname(name) == '':
                name_to_match = os.path.basename(pred)
            else:
                name_to_match = os.path.relpath(pred, pred_dir)
            if fnmatch.fnmatch(name_to_match, name):
                logs_to_evaluate.append(pred)
                break
    
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(handel_pred, [(pred,
                                              pred_dir,
                                              evaluate_folders,
                                              local_gt_dir,
                                              predictionReaderFunction,
                                              gtReaderFunction,
                                              assiciation_function,
                                              transform_func,
                                              output_dir) for pred in logs_to_evaluate])
        executor.shutdown(wait=True) 

    output_files = []
    succeded = []
    failed = []
    skipped_not_json = []
    skipped_reading_fnc = []
    skipped_not_in_lognames = []

    for future in list(results):
        pred, res, output_file = future
       
        if res == ProcessResult.sucess:
            output_files.append(output_file)
            succeded.append(pred)
        elif res == ProcessResult.skipped_reading:
            skipped_reading_fnc.append(pred)
        elif res == ProcessResult.failed_with_error:
            failed.append(pred)
        elif res == ProcessResult.skipped_not_in_lognames:
            skipped_not_in_lognames.append(pred)
    
        
    print("\nFinished all Predictions!\n")
    print ("Failed Predictions: ")
    for x in failed: print(x)
    print ("\n Skipped by reading func: ")
    for x in skipped_reading_fnc: print(x)

    if not os.path.exists(pred_dir):
        pred_dir = get_path_on_store(pred_dir, StoreType.Predictions)
    if not os.path.exists(local_gt_dir):
        local_gt_dir = get_path_on_store(local_gt_dir, StoreType.Annotations)
    video_dir = '' #TODO:ADD Blob link
    
    process_result = dict()
    process_result['num_success_files'] = len(succeded)
    process_result['reading_function_skipped'] = len(skipped_reading_fnc)
    process_result['not_json_files'] = len(skipped_not_json)
    process_result['failed_with_error'] = len(failed)
    process_result['skipped_not_in_lognames'] = len(skipped_not_in_lognames)

    report_run_info = create_run_info(primary_path=pred_dir, primary_name=pred_file_name, secondary_path=local_gt_dir, secondary_name=gt_file_name, video_path=video_dir)
    return output_files, report_run_info,process_result

def run_experiment(pred_dir, output_dir, predictionReaderFunction,gtReaderFunction,transform_func, assiciation_function, local_gt_dir, log_names_to_evaluate, evaluate_folders):
    """
    Runs an experiment by comparing predictions to ground truth and returning intermediate and combined results.

    Args:
        pred_dir (str): Path to directory containing prediction files.
        output_dir (str): Path to directory where output files will be saved.
        predictionReaderFunction (function): Function to read prediction files.
        gtReaderFunction (function): Function to read ground truth files.
        transform_func (function): Function to transform prediction and ground truth data.
        assiciation_function (function): Function to associate prediction and ground truth data.
        local_gt_dir (str): Path to directory containing local ground truth files.
        log_names_to_evaluate (list): List of log names to evaluate.
        evaluate_folders (bool): Whether to evaluate folders.

    Returns:
        tuple: A tuple containing the combined evaluation data, a report of the experiment run, and the process result.
    """
    # extract all the intermediate results from the raw prediction-label files
    compared_videos, report_run_info, process_result = compare_predictions_directory(pred_dir=pred_dir, output_dir=output_dir,
                                                                                     predictionReaderFunction=predictionReaderFunction,
                                                                                     gtReaderFunction=gtReaderFunction, 
                                                                                     transform_func=transform_func, 
                                                                                     assiciation_function=assiciation_function, 
                                                                                     local_gt_dir=local_gt_dir, 
                                                                                     log_names_to_evaluate=log_names_to_evaluate,
                                                                                     evaluate_folders=evaluate_folders)

    if len(compared_videos) == 0:
        return None, None, process_result

    # combine the intermediate results for further statistics and example extraction
    comp_data = ParallelExperiment.combine_evaluation_files(compared_videos)

    return comp_data, report_run_info, process_result
