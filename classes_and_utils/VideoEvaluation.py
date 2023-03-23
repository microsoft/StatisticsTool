import pathlib
import numpy as np, os
import pandas as pd
from classes_and_utils.file_storage_handler import get_local_or_blob_full_path, list_files_in_results_path
from utils.AlgoLogsParser import parse_video_name_from_pred_file
from utils.AzureStorageHelper import StoreType, read_gt_file_from_blob
from classes_and_utils.file_storage_handler import get_local_or_blob_file
from utils.sheldon_export_header import create_sheldon_list_header

class VideoEvaluation:
    """
       A class that accepts a matching prediction-GT data structures and
        yields a file with each frame's:
         a) overlap matrix of its predictions and labels
         b) bounding boxes data, including its state (TP/FP/FN or max(overlap)) and matching label/prediction index
            divided into a predictions list and a label list

       ...

       Attributes
       ----------
       pred_path : str
           the path to the video's prediction data structure file
       overlap_function : function
           a function to evaluate the overlap between a prediction and a label (e.g IOU)
       readerFunction : function
           a function to read the original data structure as a pandas dataframe
       evaluation_func : function
           a function that dictates how each bounding box will be classified (e.g TP/FP/FN) from the overlap matrix
       
       
       comp_data : list
           a list that contains each frames bounding boxes data and overlap matrix (first object is the image folder name)
    """

    def __init__(self, overlap_function, readerFunction, evaluation_func, transform_func):
        self.overlap_function = overlap_function
        self.readerFunction = readerFunction
        self.evaluation_func = evaluation_func
        self.transform_func = transform_func
        self.comp_data = []


    def load_data(self, pred_file, gt_file):

        pred_data = self.readerFunction(pred_file)
       
        if pred_data is None: #The user defined reader function doesn't recognize this file
            raise Exception(f"reader function could't parse {pred_file} log")
            
        gt_data = self.readerFunction(gt_file)
        
        if gt_data is None:
            raise Exception(f"failed to parse or no data for gt file: {gt_file}")
        
        if  len(gt_data) == 0:
            raise Exception(f"gt file parser returns with no lines for file: {gt_file}")
        
        gt_data.rename(columns={'predictions': 'gt'}, inplace=True)
        
        loaded_dataframe = pred_data.merge(gt_data, left_on='frame_id', right_on='frame_id',how='inner')
        
        
        return loaded_dataframe

    def save_data(self, output_file_path):
        dir = os.path.split(output_file_path)[0]
        if os.path.exists(dir) == False:
            os.makedirs(dir)
        
        self.comp_data.to_json(output_file_path)

    @staticmethod
    def add_dict_recursive(dict_in, key, new_obj, add_gt=False):
        if type(dict_in) == dict:
            if key == 'matching':
                add_gt=True
            for j, p in enumerate(dict_in):
                VideoEvaluation.add_dict_recursive(dict_in[p], p, new_obj, add_gt)
        else:
            if add_gt:
                key = key+'_gt'
            new_obj[key] = dict_in

    def create_dataframe_from_dict(self, frames_dictionary, video_name):
        self.comp_data = pd.DataFrame.from_dict(frames_dictionary)
        self.comp_data.drop('gt',axis=1,inplace=True)

        self.comp_data = self.comp_data.explode('predictions')

        self.comp_data = self.comp_data.reset_index(drop=True)
        
        new_data = []   
        pred_arr = self.comp_data.to_numpy()
        keys = self.comp_data.keys()
        for row in pred_arr:
            new_obj={}
            for i, key in enumerate(keys):
                VideoEvaluation.add_dict_recursive(row[i],key,new_obj)
                
            new_data.append(new_obj)
        self.comp_data = pd.DataFrame(new_data)
        self.comp_data.loc[self.comp_data['detection_gt'].isnull(), 'detection_gt']=False
        self.comp_data['video']=video_name
        
        #Add end_frame same as current frame
        #end_frame can be manipulate in transformation function callback in order to calculate statistics per events.
        self.comp_data['end_frame'] = self.comp_data.loc[:,'frame_id']

    def create_frames_dictionary(self, loaded_dataframe):
        frames_dict = loaded_dataframe.to_dict()
        for frame_num in frames_dict['frame_id']:
            prediction = frames_dict['predictions'][frame_num]
            gt = frames_dict['gt'][frame_num]
           
            if type(prediction) is not list:
                prediction = [prediction]
            if type(gt) is not list:
                gt = [gt]        
            if not len(gt) or not len(prediction):
                mat=[]
            else:
                mat = np.zeros((len(prediction), len(gt)))
            for i, prd_BB in enumerate(prediction):
                for j, label_BB in enumerate(gt):
                    # if there is no object in row and only 1 key (it suppose to be 'detection' key) no detections and don't calculate overlap
                    if 'prediction' not in prd_BB.keys() or 'prediction' not in label_BB.keys():
                        continue
                    overlap = self.overlap_function(prd_BB['prediction'], label_BB['prediction'])
                    mat[i, j] = round(overlap, 2)
           
            self.evaluation_func(prediction, mat)

            gts = []
            for ind, x in enumerate(prediction): 
                if 'matching' in x:
                    gts.append(x['matching'])
                    x['matching'] = gt[x['matching']]
                
            for ind, x in enumerate(gt): 
                if ind not in gts  and 'prediction' in x and x['prediction']: 
                    prediction.append({'matching':x,'state':0, 'detection': False}) 
        return frames_dict

    def compute_dataframe(self, pred_file, gt_file, video_name = None):
        """
        :return: a list of dictionaries each belongs to a different frame:
          each dictionary contains the data of the frame's bounding boxes (predictions & labels) and an overlap matrix
        """
        # load the per frame bounding box hash table (dictionary) for labels and predictions
        loaded_data = self.load_data(pred_file, gt_file)
        
        frames_dict = self.create_frames_dictionary(loaded_data)
        
        self.create_dataframe_from_dict(frames_dict, video_name)

        if self.transform_func:
            self.comp_data=self.transform_func(self.comp_data)      
        
 


   

def compare_predictions_directory(pred_dir, output_dir, overlap_function, readerFunction, transform_func, evaluation_func, gt_dir = None):
    """

    :param GT_path_list:  a list of paths to GT files (matching to the preditions and images lists)
    :param pred_path_list: a list of paths to predictions files
    :param images_folders_list: a list of image folders names
    :param overlap_function: same as in VideoEvaluation
    :param readingFunction: a function that defines several file reading procedures
    :param evaluation_func: same as in VideoEvaluation
    :return: dictionary tahts maps each video file location to it's annotations (pred and GT) file location
    """
    sheldon_header_data = {}
    
    pred_path_list = list_files_in_results_path(pred_dir)
    
    output_files = []

    pred_file_name = ''
    gt_file_name = ''
    succeeded = 0
    failed = 0
    #for GT_path, pred_path, image_folder_fullpath, image_folder_name in zip(GT_path_list, pred_path_list, image_folder_fullpath_list, images_folders_list):
    for pred in pred_path_list:
        gt_local_path = None
        
        if not pred.endswith('.json'):
            continue

        log_name = os.path.basename(pred)
        try:
            print(f"Try to find gt for file: {pred}")
            
            pred_file = get_local_or_blob_file(pred)

            if pred_file is None:
                print (f"Can't fine file {pred_file}, continue..")
                continue

            video_name, _ = parse_video_name_from_pred_file(pred_file)
        
            #if user set local gt folder
            if gt_dir:
                video_folder_name = pathlib.Path(video_name).stem
                #set gt_file path to be as gt_logs file format
                gt_local_path = os.path.join(gt_dir, video_folder_name+'.json')
                #if not exists set gt_file to be as algo_logs file format
                if os.path.exists(gt_local_path) == False:
                    gt_local_path = os.path.join(gt_dir, video_folder_name, log_name)
                    #if gt file is not in gt_logs format so log file name is not as the video name
                    gt_file_name = os.path.basename(gt_local_path)
            else: #read gt from blob
                gt_local_path = read_gt_file_from_blob(video_name)
                
                
            if gt_local_path is None or not os.path.exists(gt_local_path):
                print(f"Gt file: {gt_local_path} not found for prediction: {pred}, continue with next prediction log..")
                continue

            V = VideoEvaluation(overlap_function=overlap_function, readerFunction=readerFunction, evaluation_func=evaluation_func, transform_func = transform_func)
            V.compute_dataframe(pred_file, gt_local_path, video_name)
            
            #if succeded - save prediction log file name to use in sheldon header
            pred_file_name = os.path.basename(pred)

            print(f"Start compare files for video {video_name}: {pred} and {gt_local_path}")
            succeeded +=1
        except Exception as ex:
            print(f"Failed to compare log {pred}, continue with next log")
            print(ex)
            failed+=1
            continue

        output_file =  os.path.join(output_dir, video_name + '.json')
        V.save_data(output_file)
        output_files.append(output_file)

       
        print(f"finished compare predictions for video {video_name}")
    
    print('*************************************************************')
    print(f'Failed clips: {failed}. Succedded clips: {succeeded}')
    print('*************************************************************')
    sheldon_pred_dir = get_local_or_blob_full_path(pred_dir, StoreType.Predictions)
    sheldon_gt_dir = get_local_or_blob_full_path(gt_dir, StoreType.Annotation)
    sheldon_header_data = create_sheldon_list_header(primary_path=sheldon_pred_dir, primary_name=pred_file_name, secondary_path=sheldon_gt_dir, secondary_name=gt_file_name)
    return output_files, sheldon_header_data


