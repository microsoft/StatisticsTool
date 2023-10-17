import pathlib
import os
from classes_and_utils.ParallelExperiment import ParallelExperiment
from classes_and_utils.VideoEvaluation import VideoEvaluation

from classes_and_utils.file_storage_handler import *
from utils.LogsParser import get_video_name_from_pred_file
from utils.report_metadata import create_run_info

def compare_predictions_directory(pred_dir, output_dir, predictionReaderFunction,gtReaderFunction,transform_func, assiciation_function, local_gt_dir = None, log_names_to_evaluate = None):
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
    
    output_files = []

    pred_file_name = ''
    gt_file_name = ''
    
    succeded = []
    failed = []
    skipped_not_json = []
    skipped_reading_fnc = []
    skipped_not_in_lognames = []

    print (f"total files num: {len(pred_path_list)}")
    for pred in pred_path_list:
        gt_local_path = None
        
        #Check if file is json
        if not pred.endswith('.json'):
            print (f"not .json file skipping: {pred}")
            skipped_not_json.append(pred)
            continue
        
        #Check if file is in log names to evaluate
        log_name = os.path.basename(pred)
        if log_names_to_evaluate != None:
            if log_name not in log_names_to_evaluate:
                skipped_not_in_lognames.append(pred)
                continue

        try:
            print(f"Try to find gt for file: {pred}")
            
            pred_file = get_file_on_local_storage(pred, StoreType.Predictions)

            if pred_file is None:
                failed.append(pred)
                print (f"Can't fine file {pred_file}, continue..")
                continue
                    
            video_name = get_video_name_from_pred_file(pred_file, pred, pred_dir)
            
            #if user set local gt folder
            if local_gt_dir:
                gt_local_path = find_in_store_by_video_name(local_gt_dir, video_name, log_name, os.path.exists)
            else: #read gt from blob
                path_on_blob = find_in_blob_by_video_name(video_name, log_name, StoreType.Annotation)
                gt_local_path = get_file_on_local_storage(path_on_blob)
              
            if gt_local_path is None:
                failed.append(pred)
                print(f"GT file: {gt_local_path} not found for prediction: {pred}, continue with next prediction log..")
                continue

            V = VideoEvaluation(predictionReaderFunction=predictionReaderFunction,gtReaderFunction=gtReaderFunction ,associationFunction=assiciation_function, transform_func = transform_func)
            res = V.compute_dataframe(pred_file, gt_local_path, video_name)
            if not res:
                print (f"Reading function didn't read file: {pred} and gt:{gt_local_path}")
                skipped_reading_fnc.append(pred)
                continue
            
            #if succeded - save prediction log file name for report metadata
            pred_file_name = os.path.basename(pred)

            print(f"Starting comparing files for video {video_name}: {pred} and {gt_local_path}")
        except Exception as ex:
            failed.append(pred)
            print(f"Failed to compare log {pred}, continuing with next log...")
            print(ex)
            continue
        
        video_folder = video_name
        if video_folder.startswith('/'):
            video_folder = video_folder[1:]
        video_folder = video_folder.replace(':',os.path.sep)
        output_file =  os.path.join(output_dir, video_folder + '.json')
        output_file = os.path.normpath(output_file)
        V.save_data(output_file)
        output_files.append(output_file)
        succeded.append(pred)

        print(f"Finished comparing predictions for video {video_name}")
        print(f"\n\n#Succeeded: {len(succeded)}; #Skipped_reading: {len(skipped_reading_fnc)}; #Skipped_not_json: {len(skipped_not_json)}; #Failed: {len(failed)}; #Not_in_lognames: {len(skipped_not_in_lognames)} #Total Files: {len(pred_path_list)}\n\n")

    print("\nFinished all Predictions!\n")
    print ("Failed Predictions: ")
    for x in failed: print(x)
    print ("\n Skipped by reading func: ")
    for x in skipped_reading_fnc: print(x)
   
    #TODO: Indeed need to save this information, but not as a jump file header.
    #Jump file header should be created only when exporting it (on UI)
    if not os.path.exists(pred_dir):
        pred_dir = get_path_on_store(pred_dir, StoreType.Predictions)
    if not os.path.exists(pred_dir):
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

def run_experiment(pred_dir, output_dir, predictionReaderFunction,gtReaderFunction,transform_func, assiciation_function, local_gt_dir, log_names_to_evaluate):
        # extract all the intermediate results from the raw prediction-label files

    compared_videos, report_run_info, process_result = compare_predictions_directory(pred_dir=pred_dir, output_dir=output_dir,
                                                                                     predictionReaderFunction=predictionReaderFunction,
                                                                                     gtReaderFunction=gtReaderFunction, 
                                                                                     transform_func=transform_func, 
                                                                                     assiciation_function=assiciation_function, 
                                                                                     local_gt_dir=local_gt_dir, 
                                                                                     log_names_to_evaluate=log_names_to_evaluate)

    if len(compared_videos) == 0:
        return process_result, None

    # combine the intermediate results for further statistics and example extraction
    comp_data = ParallelExperiment.combine_evaluation_files(compared_videos)

    return comp_data, report_run_info, process_result
