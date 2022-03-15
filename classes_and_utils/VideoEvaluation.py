import numpy as np, os
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
       detection_metric : function
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
       dictionary_list : list
           a list that contains each frames bounding boxes data and overlap matrix (first object is the image folder name)
       empty_frames : set
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

    def __init__(self, GT_path, pred_path, detection_metric, readerFunction, save_stats_dir,
                 evaluation_func, image_folder, empty_GT_frame_func=None, saving_mat_file_dir=None,
                 file_loading_func=None):
        self.GT_path = GT_path
        self.pred_path = pred_path
        self.detection_metric = detection_metric
        self.readerFunction = readerFunction
        self.save_stats_dir = save_stats_dir
        self.evaluation_func = evaluation_func
        self.empty_GT_frame_func = empty_GT_frame_func
        self.saving_mat_file_dir = saving_mat_file_dir
        self.file_loading_func = file_loading_func
        self.image_folder = image_folder
        self.dictionary_list = [image_folder]
        self.empty_frames = set()

    def load_data(self, path, GT):
        """
        :param path: path to predictions/GT file in its raw form
        :param GT: Boolean that indicates whether this current file is a GT or prediction
        :return: dictionary of the form: {frame_number: list of bounding boxes data}
        """
        # load file from path using a user specified function that returns a pandas dataframe representation of the data
        df, self.empty_GT_frame_func = self.readerFunction(path)
        # keep values from same frame together in a dictionary
        frame_hash = {}
        for row in df.itertuples(index=True):
            # turn each row's namedtuple into a dictionary for convenient
            row = row._asdict()
            frame_num = row['frame_id']
            # if the file belongs to GT and the user specified an "empty_GT_frame_func" then empty frames numbers will
            # be saved in a set and will not be saved in the dictionary
            if GT and self.empty_GT_frame_func:
                if self.empty_GT_frame_func(row):
                    self.empty_frames.add(frame_num)
                    continue
            # adding keys for later use ('state' - eg:FP/TP/FN, 'matching' -  matching predictions/labels index)
            row['state'] = None
            row['matching'] = None
            # if exists frame_num list in the frame_hash add row else create new list in frame_hash
            if frame_num in frame_hash:
                frame_hash[frame_num].append(row)
            else:
                frame_hash[frame_num] = [row]
        return frame_hash

    def compare(self):
        """
        :return: a list of dictionaries each belongs to a different frame:
          each dictionary contains the data of the frame's bounding boxes (predictions & labels) and an overlap matrix
        """
        # load the per frame bounding box hash table (dictionary) for labels and predictions
        label_frame_hash = self.load_data(self.GT_path, GT=True)
        pred_frame_hash = self.load_data(self.pred_path, GT=False)
        # Iterate over all frames in the predictions data and compare predictions-labels of the same frame to yield an overlap matrix
        for frame_num in pred_frame_hash:
            # if a prediction frame has no GT (not even an empty one) we do not include it into our calculations
            if frame_num not in label_frame_hash and frame_num not in self.empty_frames:
                continue
            prd_BB_list = pred_frame_hash[frame_num]
            # initialize a dictionary for each frame that will collect all the frame's data including an overlap matrix
            temp_d = {'frame_num': frame_num, 'predictions': [], 'labels': [], 'matrix': []}
            # if a frame exists at the predictions file but not in the labels file we save the prediction as FP
            if frame_num in self.empty_frames:
                for prd_BB in prd_BB_list:
                    prd_BB['state'] = 'FP'
                    temp_d['predictions'].append(prd_BB)
                self.dictionary_list.append(temp_d)
                continue
            # if frame number exists in both label and predictions data an overlap matrix is calculated
            label_BB_list = label_frame_hash[frame_num]
            temp_d['matrix'] = np.zeros((len(prd_BB_list), len(label_BB_list)))
            for i, prd_BB in enumerate(prd_BB_list):
                temp_d['predictions'].append(prd_BB)
                for j, label_BB in enumerate(label_BB_list):
                    overlap = self.detection_metric(prd_BB, label_BB)
                    temp_d['matrix'][i, j] = round(overlap, 2)
                    if i == 0:
                        temp_d['labels'].append(label_BB)  # adding the labels only once (not every loop)

            temp_d['matrix'] = temp_d['matrix'].tolist()
            self.dictionary_list.append(temp_d)

        # Iterate over all frames in label data
        for frame_num in label_frame_hash:
            label_BB_list = label_frame_hash[frame_num]
            # if a frame exists at the labels file but not in the predictions file we save the labels as FN
            if frame_num not in pred_frame_hash:
                temp_d = {'frame_num': frame_num, 'predictions': [], 'labels': [], 'matrix': []}
                for label_BB in label_BB_list:
                    label_BB['state'] = 'FN'
                    temp_d['labels'].append(label_BB)
                self.dictionary_list.append(temp_d)
                continue
        # option to save midway - for future development (don't forget to end the path with ".json")
        if self.saving_mat_file_dir:
            save_json(self.saving_mat_file_dir, self.dictionary_list)

    def Decide_state(self, from_file=False):
        """
        :param from_file: Boolean, loading self.dictionary_list from a file or not - for future development
        :return: saves this video intermediate results as a json file in self.save_stats_dir:
        the intermediate results are the same as in self.dictionary_list but with a matching between labels and predictions
        """
        # if we saved midway this is how we can load it back - for future development
        if from_file:
            assert self.file_loading_func, 'file_loading_func was not set !'
            list_of_dict = self.file_loading_func(self.saving_mat_file_dir)
        else:
            list_of_dict = self.dictionary_list

        for idx, temp_d in enumerate(list_of_dict):
            # the first object in self.dictionary_list is the name of the image folder of the video (see init)
            if idx == 0:
                continue
            # calling a user specified self.evaluation_func that accepts a frame dictionary and matches predictions & labels
            list_of_dict[idx] = self.evaluation_func(temp_d)
        # saving a json file of this video's intermediate results
        save_json(self.save_stats_dir, list_of_dict)


def run_one_video(GT_path, pred_path, image_folder, detection_metric, readerFunction, save_stats_dir, evaluation_func, file_loading_func=None, empty_GT_frame_func=None, saving_mat_file_dir=None):
    """
    :params - same as VideoEvaluation class
    :return: performs all the class methods of VideoEvaluation and saves intermediate results
    """
    V = VideoEvaluation(GT_path=GT_path, pred_path=pred_path,
                        detection_metric=detection_metric, readerFunction=readerFunction, save_stats_dir=save_stats_dir,
                        evaluation_func=evaluation_func, image_folder=image_folder, file_loading_func=file_loading_func,
                        empty_GT_frame_func=empty_GT_frame_func, saving_mat_file_dir=None)
    V.compare()
    V.Decide_state()


def run_multiple_Videos(GT_path_list, pred_path_list, images_folders_list, image_folder_fullpath_list, detection_metric,
                        readerFunction, save_stats_dir, evaluation_func, file_loading_func=None,
                        saving_mat_file_dir=None):
    """

    :param GT_path_list:  a list of paths to GT files (matching to the preditions and images lists)
    :param pred_path_list: a list of paths to predictions files
    :param images_folders_list: a list of image folders names
    :param image_folder_fullpath_list: a list of image folders full path
    :param detection_metric: same as in VideoEvaluation
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
        save_stats_file = os.path.join(save_stats_dir, image_folder_name + '.json')
        run_one_video(GT_path, pred_path, image_folder_fullpath, detection_metric, readerFunction, save_stats_file, evaluation_func, file_loading_func=None, saving_mat_file_dir=None)



