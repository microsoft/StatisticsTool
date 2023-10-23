import enum
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
    gt_local_path = None 
    pred, log_names_to_evaluate, pred_dir, evaluate_folders, local_gt_dir, predictionReaderFunction, gtReaderFunction, assiciation_function, transform_func, output_dir = vars
    matched = False
    for name in log_names_to_evaluate:
            #Check if file is in log names to evaluate
        name_to_match = pred
        if os.path.dirname(name) == '':
            name_to_match = os.path.basename(pred)
        else:
            name_to_match = os.path.relpath(pred, pred_dir)
        if fnmatch.fnmatch(name_to_match, name):
            matched = True
            break
    if not matched:
        return pred, ProcessResult.skipped_not_in_lognames, None

    try:
        log_name = os.path.basename(pred)

        print(f"Try to find gt for file: {pred}")
        
        pred_file = get_file_on_local_storage(pred, StoreType.Predictions, get_folder=evaluate_folders)

        if pred_file is None:
            print (f"Can't fine file {pred_file}, continue..")
            return pred, ProcessResult.failed_with_error, None
                
        video_name = get_video_name_from_pred_file(pred_file, pred, pred_dir)
        file_ext = os.path.splitext(log_name)[1]
        if evaluate_folders:
            file_ext = ''
        #if user set local gt folder
        if local_gt_dir:
            gt_local_path = find_in_store_by_video_name(local_gt_dir, video_name, log_name, os.path.exists, ext=file_ext)
            gt_local_path = os.path.join(local_gt_dir, gt_local_path)
        else: #read gt from blob
            path_on_blob = find_in_blob_by_video_name(video_name, log_name, StoreType.Annotation, ext=file_ext)
            gt_local_path = get_file_on_local_storage(path_on_blob, None, get_folder=evaluate_folders)
            
        if gt_local_path is None:
            print(f"GT file: {gt_local_path} not found for prediction: {pred}, continue with next prediction log..")
            return pred, ProcessResult.failed_with_error, None

        print(f"Starting comparing files for video {video_name}: {pred} and {gt_local_path}")

        V = VideoEvaluation(predictionReaderFunction=predictionReaderFunction,gtReaderFunction=gtReaderFunction ,associationFunction=assiciation_function, transform_func = transform_func)
        res = V.compute_dataframe(pred_file, gt_local_path, video_name)
        if not res:
            return pred, ProcessResult.skipped_reading, None

        video_folder = video_name
        if video_folder.startswith('/'):
            video_folder = video_folder[1:]
        video_folder = video_folder.replace(':',os.path.sep)
        output_file =  os.path.join(output_dir, video_folder + '.json')
        output_file = os.path.normpath(output_file)
        V.save_data(output_file)

        print(f"Finished comparing predictions for video {video_name}")
    except Exception as ex:
        print(f"Failed to compare log {pred}, continuing with next log...")
        print(ex)
        return pred, ProcessResult.failed_with_error, None
    
   

    return pred, ProcessResult.sucess, output_file

def compare_predictions_directory(pred_dir, output_dir, predictionReaderFunction,gtReaderFunction,transform_func, assiciation_function, local_gt_dir = None, log_names_to_evaluate = None, evaluate_folders=False):
    """

    :param GT_path_list:  a list of paths to GT files (matching to the preditions and images lists)
    :param pred_path_list: a list of paths to predictions files
    :param images_folders_list: a list of image folders names
    :param overlap_function: same as in VideoEvaluation
    :param readingFunction: a function that defines several file reading procedures
    :param evaluation_func: same as in VideoEvaluation
    :return: dictionary tahts maps each video file location to it's annotations (pred and GT) file location
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
    
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(handel_pred, [(pred,
                                              log_names_to_evaluate,
                                              pred_dir,
                                              evaluate_folders,
                                              local_gt_dir,
                                              predictionReaderFunction,
                                              gtReaderFunction,
                                              assiciation_function,
                                              transform_func,
                                              output_dir) for pred in pred_path_list])
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
        local_gt_dir = get_path_on_store(local_gt_dir, StoreType.Annotation)
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
