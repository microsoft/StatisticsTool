
import numpy as np, os
import pandas as pd


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

    def __init__(self, overlap_function, predictionReaderFunction,gtReaderFunction, evaluation_func, transform_func):
        self.overlap_function = overlap_function
        self.predictionReaderFunction = predictionReaderFunction
        self.gtReaderFunction = gtReaderFunction
        self.evaluation_func = evaluation_func
        self.transform_func = transform_func
        self.comp_data = []


    def load_data(self, pred_file, gt_file):

        pred_data = self.predictionReaderFunction(pred_file)
       
        if pred_data is None: #The user defined reader function doesn't recognize this file
            print (f"reader function could't parse {pred_file} log")
            return None
            
        gt_data = self.gtReaderFunction(gt_file)
        
        if gt_data is None:
            print (f"failed to parse or no data for gt file: {gt_file}")
            return None
        
        if  len(gt_data) == 0:
            print(f"gt file parser returns with no lines for file: {gt_file}")
            return None
        
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
        if 'detection_gt' not in self.comp_data.keys():
            self.comp_data['detection_gt'] = None
        self.comp_data.loc[self.comp_data['detection_gt'].isnull(), 'detection_gt']=False
        
        if video_name:
                video_name = video_name.replace('\\','/')

        self.comp_data['video']=video_name
        
        #Add end_frame same as current frame
        #end_frame can be manipulate in transformation function callback in order to calculate statistics per events.
        self.comp_data['end_frame'] = self.comp_data.loc[:,'frame_id']

    def create_frames_dictionary(self, loaded_dataframe, threshold_in):
        frames_dict = loaded_dataframe.to_dict()
        threshold = None
        try:
            threshold = float(threshold_in)
        except:
            print(f'failed to parse threshold set threshold to None')
            threshold = None

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
                    if threshold and overlap < threshold:
                        overlap = 0
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

    def compute_dataframe(self, pred_file, gt_file, threshold, video_name = None):
        """
        :return: a list of dictionaries each belongs to a different frame:
          each dictionary contains the data of the frame's bounding boxes (predictions & labels) and an overlap matrix
        """
        # load the per frame bounding box hash table (dictionary) for labels and predictions
        loaded_data = self.load_data(pred_file, gt_file)
        if loaded_data is None:
            return False
        
        frames_dict = self.create_frames_dictionary(loaded_data, threshold)
        
        self.create_dataframe_from_dict(frames_dict, video_name)

        if self.transform_func:
            self.comp_data=self.transform_func(self.comp_data)    

        return True  
        
 