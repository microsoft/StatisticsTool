
import time
import numpy as np, os
import pandas as pd
from app_config.constants import UserDefinedConstants

from app_config.dataframe_tokens import DataFrameTokens

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

    def __init__(self, predictionReaderFunction,gtReaderFunction, associationFunction, transform_func):
        self.association_function = associationFunction
        self.prediction_reading_function = predictionReaderFunction
        self.gt_reading_function = gtReaderFunction
        self.transform_func = transform_func
        self.comp_data = []


    def load_data(self, pred_file, gt_file, video_name):

        self.prediction_reading_function.params[UserDefinedConstants.VIDEO_NAME_PARAM_READING_FNC] = video_name
        pred_data = self.prediction_reading_function(pred_file)
        if pred_data is None: #The user defined reader function doesn't recognize this file
            print (f"reader function could't parse {pred_file} log")
            return None, None

        self.gt_reading_function.params[UserDefinedConstants.VIDEO_NAME_PARAM_READING_FNC] = video_name
        gt_data = self.gt_reading_function(gt_file)

        if gt_data is None:
            print (f"failed to parse or no data for gt file: {gt_file}")
            return None, None

        if  len(gt_data) == 0:
            print(f"gt file parser returns with no lines for file: {gt_file}")
            return None, None
        
        #if there is no group key in the data, add it to be as the index
        if DataFrameTokens.LABELS_GROUP_KEY not in pred_data.columns:
            pred_data[DataFrameTokens.LABELS_GROUP_KEY] = pred_data.index
        
        if DataFrameTokens.LABELS_GROUP_KEY not in gt_data.columns:
            gt_data[DataFrameTokens.LABELS_GROUP_KEY] = gt_data.index
        
        pred_data[DataFrameTokens.HAS_VALUE_TOKEN] = True
        gt_data[DataFrameTokens.HAS_VALUE_TOKEN] = True

        return pred_data, gt_data
 

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
                key = key+DataFrameTokens.GT_ANNOT_SUFFIX
            new_obj[key] = dict_in

    @staticmethod
    def create_association_indexes(pred_df, gt_df, association_function):
        pred_association = pd.Series(np.full(len(pred_df),-1), index = pred_df.index)
        gt_association = pd.Series(np.full(len(gt_df),-1), index = gt_df.index)
       
        preds_dict = pred_df.replace({np.nan: None}).to_dict('index')
       
        gts_dict = gt_df.replace({np.nan: None}).to_dict('index')
        
        for frame_num in pred_df[DataFrameTokens.LABELS_GROUP_KEY].unique():
            predictions_indexes = pred_df.index[(pred_df[DataFrameTokens.LABELS_GROUP_KEY]==frame_num)]
            predictions = [preds_dict[x] for x in predictions_indexes]
            gts_indexes = gt_df.index[(gt_df[DataFrameTokens.LABELS_GROUP_KEY]==frame_num)]
            gts = [gts_dict[x] for x in gts_indexes]

            if not association_function:
                if len(gts_indexes): 
                    pred_association.loc[predictions_indexes[0]]=gts_indexes[0]
                    gt_association.loc[gts_indexes[0]]=predictions_indexes[0]
                    continue

            try:
                association_dict = association_function(predictions, gts)       
            except Exception as ex:
                print ("\n\n\n----------- EXCEPTION IN ASSICIATION FUNCTION --------------------")
                print(f"Failed in user defined association function for predictions: {predictions} and gts: {gts}")
                print (ex)
                print('\n\n\n')
                #raise ex
            try:

                for ind, _ in enumerate(predictions):
                    if ind in association_dict and len(gts_indexes) > association_dict[ind]: 
                        pred_association.loc[predictions_indexes[ind]]=gts_indexes[association_dict[ind]]
                        gt_association.loc[gts_indexes[association_dict[ind]]]=predictions_indexes[ind]
            except Exception as ex:
                print(ex)

        return pred_association, gt_association

    @staticmethod
    def create_associated_labels_dataframe(pred_df, gt_df, association_function):
        
        gt_suffix_df = gt_df.add_suffix(DataFrameTokens.GT_ANNOT_SUFFIX)
        gt_suffix_df = gt_suffix_df.rename(columns={ DataFrameTokens.LABELS_GROUP_KEY+DataFrameTokens.GT_ANNOT_SUFFIX: DataFrameTokens.LABELS_GROUP_KEY})
        
        pred_association, gt_association = VideoEvaluation.create_association_indexes(pred_df, gt_df, association_function)

        pred_matched = pred_df.loc[pred_association[pred_association > -1].index].reset_index(drop=True)
        gt_matched = gt_suffix_df.loc[pd.Index(pred_association.loc[pred_association >-1].values)].reset_index(drop=True).drop(DataFrameTokens.LABELS_GROUP_KEY, axis=1)
        
        comp_data = pred_matched.merge(gt_matched, left_index=True, right_index=True)
        
        comp_data = pd.concat([comp_data, pred_df.loc[pred_association.loc[pred_association == -1].index]], ignore_index = True)

        gt_append = gt_suffix_df.loc[gt_association.loc[gt_association == -1].index]
        gt_append = gt_append[gt_append[DataFrameTokens.LABELS_GROUP_KEY].isin(pred_df[DataFrameTokens.LABELS_GROUP_KEY].unique())]
        comp_data =  pd.concat([comp_data,gt_append], ignore_index = True)
        
        comp_data=comp_data.sort_values(by=DataFrameTokens.LABELS_GROUP_KEY).reset_index(drop=True)

        #For unique calculation fill all the entries where there is no matched label in the predictions/gt with False
        comp_data[DataFrameTokens.HAS_VALUE_TOKEN] = comp_data[DataFrameTokens.HAS_VALUE_TOKEN].fillna(False)
        comp_data[DataFrameTokens.HAS_VALUE_TOKEN+DataFrameTokens.GT_ANNOT_SUFFIX] = comp_data[DataFrameTokens.HAS_VALUE_TOKEN+DataFrameTokens.GT_ANNOT_SUFFIX].fillna(False)
        return comp_data

    def compute_dataframe(self, pred_file, gt_file, video_name = None):
        """
        :return: a list of dictionaries each belongs to a different frame:
          each dictionary contains the data of the frame's bounding boxes (predictions & labels) and an overlap matrix
        """
        # load the per frame bounding box hash table (dictionary) for labels and predictions
        start = time.time()
        
        try:
            pred_data, gt_data = self.load_data(pred_file, gt_file, video_name)
            if pred_data is None:
                return False
        except Exception as ex:
            print ("\n\n\n----------- EXCEPTION IN UDF READING FUNCTION --------------------")
            print(f"Failed in user defined load function for prediction: {pred_file} and gt: {gt_file}")
            print (ex)
            print('\n\n\n')
            raise ex
        
        end = time.time()
        load_time = end-start
        self.comp_data = self.create_associated_labels_dataframe(pred_data, gt_data, self.association_function)
        end2 = time.time()
        print(f'load: {load_time:.2f} association: {end2-end:.2f}')
        
        if DataFrameTokens.VIDEO_TOKEN not in self.comp_data and video_name:
            self.comp_data[DataFrameTokens.VIDEO_TOKEN] = video_name
        self.comp_data[DataFrameTokens.END_EVENT_TOKEN] = self.comp_data[DataFrameTokens.LABELS_GROUP_KEY]
        
        try:
            
            if self.transform_func:
                self.comp_data=self.transform_func(self.comp_data) 
               
        except Exception as ex:
            print ("\n\n\n----------- EXCEPTION IN UDF TRANSFORM FUNCTION --------------------")
            print(f"Failed in user defined transform function for prediction: {pred_file} and gt: {gt_file}")
            print (ex)
            print('\n\n\n')
            raise ex
       
        return True  
        
 