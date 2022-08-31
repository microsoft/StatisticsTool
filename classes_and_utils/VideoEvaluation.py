from cProfile import label
from genericpath import isdir
import numpy as np, os
import math
import pandas as pd
from classes_and_utils.utils import save_json


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
       GT_path : str
           the path to the video's GT data structure file
       pred_path : str
           the path to the video's prediction data structure file
       frame_column_name : str
           the frame number column name in the original data structure
       overlap_function : function
           a function to evaluate the overlap between a prediction and a label (e.g IOU)
       readerFunction : function
           a function to read the original data structure as a pandas dataframe
       save_stats_dir : str
           the path in which to save the output file (intermediate results) don't forget to add ".json"
       evaluation_func : function
           a function that dictates how each bounding box will be classified (e.g TP/FP/FN) from the overlap matrix
       image_folder : str
           The path to the video's images folder
       empty_GT_frame_func : function
           a function that accepts a GT row from the labels data structures and return whether or not it is empty (no label on it)
           and decides weather to discard it or not (default None)
       saving_mat_file_dir : str
           a path in which to save the data which indludes an overlap matrix before the Decide_state method (default None)
       file_loading_func : function
           a function that will load the data in case of saving the data after calculating overlap matrix (default None) don't forget to add ".json"
       comp_data : list
           a list that contains each frames bounding boxes data and overlap matrix (first object is the image folder name)
       empty_frames_pred : set
            a set that contains the indices of empty GT rows (GT with no label on it), determined byempty_frames : set
       empty_frames_GT : set
            a set that contains the indices of empty GT rows (GT with no label on it), determined by
       Methods
       -------
       load_data(path)
           takes a path to a prediction/label data-structure in which the rows are bounding boxes data and returns
           a dictionary of the form: {frame_number: list of bounding boxes data}
       compare()
           calculates each frames overlap matrix
       Decide_state(from_file=False)
           decides each bounding box's state (e.g TP/FP/FN) and saves the output of the class

       """

    def __init__(self, GT_path, pred_path, overlap_function, readerFunction, save_stats_dir,
                 evaluation_func, image_folder, empty_GT_frame_func=None, saving_mat_file_dir=None,
                 file_loading_func=None):
        self.GT_path = GT_path
        self.pred_path = pred_path
        self.overlap_function = overlap_function
        self.readerFunction = readerFunction
        self.save_stats_dir = save_stats_dir
        self.evaluation_func = evaluation_func
        self.empty_GT_frame_func = empty_GT_frame_func
        self.saving_mat_file_dir = saving_mat_file_dir
        self.file_loading_func = file_loading_func
        self.image_folder = image_folder
        self.comp_data = [image_folder]
        self.empty_frames_GT = set()
        self.empty_frames_pred = set()


    def load_data(self, pred_path, gt_path):
        
        
        if os.path.isdir(pred_path):
            pred_path = os.path.join(pred_path,os.listdir(pred_path)[0])
        if os.path.isdir(gt_path):
            gt_path = os.path.join(gt_path,os.listdir(gt_path)[0])

        pred_data = self.readerFunction(pred_path)
        gt_data = self.readerFunction(gt_path)
       
        
        gt_data.rename(columns={'predictions': 'gt'}, inplace=True)
        
        loaded_dataframe = pred_data.merge(gt_data, left_on='frame_id', right_on='frame_id',how='inner')
        
        return loaded_dataframe

    def compare(self):
        """
        :return: a list of dictionaries each belongs to a different frame:
          each dictionary contains the data of the frame's bounding boxes (predictions & labels) and an overlap matrix
        """
        # load the per frame bounding box hash table (dictionary) for labels and predictions
        loaded_data = self.load_data(self.pred_path, self.GT_path)
       
        # Iterate over all frames in the predictions data and compare predictions-labels of the same frame to yield an overlap matrix
        loaded_data['matrix'] = ''
        for frame_num in loaded_data.index:
            
            prediction = loaded_data.loc[frame_num]['predictions']
            
            gt = loaded_data.loc[frame_num]['gt']
           
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
      
            loaded_data.at[frame_num,'matrix'] = mat
        
        self.comp_data = loaded_data
        # option to save midway - for future development (don't forget to end the path with ".json")
        if self.saving_mat_file_dir:
            save_json(self.saving_mat_file_dir, self.comp_data)

    def Decide_state(self, from_file=False):
        """
        :param from_file: Boolean, loading self.comp_data from a file or not - for future development
        :return: saves this video intermediate results as a json file in self.save_stats_dir:
        the intermediate results are the same as in self.comp_data but with a matching between labels and predictions
        """
        # if we saved midway this is how we can load it back - for future development
        if from_file:
            assert self.file_loading_func, 'file_loading_func was not set !'
            comp_data = self.file_loading_func(self.saving_mat_file_dir)
        else:
            comp_data = self.comp_data

        for ind in comp_data.index:
            frame_data = comp_data.loc[ind]
            # calling a user specified self.evaluation_func that accepts a frame dictionary and matches predictions & labels
            self.evaluation_func(frame_data)
            gt_list = frame_data['gt'] 
            predictions_list = frame_data['predictions'] 
            for x in gt_list: 
                if x['state']==0 and 'prediction' in x and x['prediction']: 
                    predictions_list.append({'matching':x,'state':0, 'detection': False}) 

        
def add_dict(dict_in, key, new_obj):
    if type(dict_in) == dict:
        for j, p in enumerate(dict_in):
            add_dict(dict_in[p], p, new_obj)
    else:
        if key in new_obj:
            key = key+'_gt'
        new_obj[key] = dict_in

def run_one_video(GT_path, pred_path, image_folder, overlap_function, readerFunction, save_stats_dir, evaluation_func, file_loading_func=None, empty_GT_frame_func=None, saving_mat_file_dir=None):
    """
    :params - same as VideoEvaluation class
    :return: performs all the class methods of VideoEvaluation and saves intermediate results
    """
    V = VideoEvaluation(GT_path=GT_path, pred_path=pred_path,
                        overlap_function=overlap_function, readerFunction=readerFunction, save_stats_dir=save_stats_dir,
                        evaluation_func=evaluation_func, image_folder=image_folder, file_loading_func=file_loading_func,
                        empty_GT_frame_func=empty_GT_frame_func, saving_mat_file_dir=None)
    V.compare()
    V.Decide_state()
    V.comp_data.drop(['gt','matrix'],axis=1,inplace=True)
    V.comp_data = V.comp_data.explode('predictions')
    V.comp_data = V.comp_data.reset_index(drop=True)
    
    new_data = []    
    pred_arr = V.comp_data.to_numpy()
    keys = V.comp_data.keys()
    for row in pred_arr:
        new_obj={}
        for i, key in enumerate(keys):
            add_dict(row[i],key,new_obj)
            
        new_data.append(new_obj)
    V.comp_data = pd.DataFrame(new_data)
    V.comp_data.loc[V.comp_data['detection_gt'].isnull(), 'detection_gt']=False
    V.comp_data['video']=image_folder
    # saving a json file of this video's intermediate results
    #save_json(self.save_stats_dir, comp_data.to_dict())
    V.comp_data.to_json(save_stats_dir)

def run_multiple_Videos(GT_path_list, pred_path_list, images_folders_list, image_folder_fullpath_list, overlap_function,
                        readerFunction, save_stats_dir, evaluation_func, file_loading_func=None,
                        saving_mat_file_dir=None):
    """

    :param GT_path_list:  a list of paths to GT files (matching to the preditions and images lists)
    :param pred_path_list: a list of paths to predictions files
    :param images_folders_list: a list of image folders names
    :param image_folder_fullpath_list: a list of image folders full path
    :param overlap_function: same as in VideoEvaluation
    :param readingFunction: a function that defines several file reading procedures
    :param save_stats_dir: same as in VideoEvaluation
    :param evaluation_func: same as in VideoEvaluation
    :param file_loading_func: same as in VideoEvaluation
    :param saving_mat_file_dir: same as in VideoEvaluation
    :return:
    """
    for GT_path, pred_path, image_folder_fullpath, image_folder_name in zip(GT_path_list, pred_path_list, image_folder_fullpath_list, images_folders_list):
        # the save_stats_file - where the intermediate results are saved:
        # is defined by save_stats_dir and the folders name
        print(f"Start compare files: {pred_path} with: {GT_path}")
        save_stats_file = os.path.join(save_stats_dir, image_folder_name + '.json')
        run_one_video(GT_path, pred_path, image_folder_fullpath, overlap_function, readerFunction, save_stats_file, evaluation_func, file_loading_func=None, saving_mat_file_dir=None)



