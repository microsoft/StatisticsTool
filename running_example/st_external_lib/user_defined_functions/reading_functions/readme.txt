"""
Reading Function instructions:
------------------------------

Input:
a. Accept as input a path to the data file (any type that the user preffered)
b. kwargs - Additional options and parameters that can be passed to the function.


Returns:
    pandas dataframe

A reading function should:
1. Read the input file (The type of the file is defined by the user according to user prefference)
2. Convert the input data to panda's data frame format. 
Special columns in the DataFrame
The enum of all saved keys: app_config\dataframe_tokens.py
    a. DataFrameTokens.LABELS_GROUP_KEY = 'frame_id' - Unique key for detections in same inference. This used to match between detections and ground truth data. 
        In some cases there can be several detections per key. For example the key can be frame_id in video and the detections are bounding boxes in same frame.
    b. DataFrameTokens.VIDEO_TOKEN = 'video' - Name of the video or images folder related to current prediction. If path of the right image/video will added, the video image will be shown in the GUI.
    
    c. DataFrameTokens.BB_X, DataFrameTokens.BB_Y, DataFrameTokens.BB_WIDTH, DataFrameTokens.BB_HEIGHT = 'x', 'y', 'width', 'height' - Bounding box information. 
        If this data is added, the bounding boxes will be presented over the image in the image window.

 
  
Each user defined function should be in seperate file where the name of the file and the name of the user defined function in the file should be the same. 

As with all user-defined functions, it is possible to add parameters to user-defined function. 
These parameters can be added by the user who creates the report at report creation time. 
The function that describes the parameters for each function should be in the same file as the function and in the following format:

    def get_function_arguments():
        return { "variable1": "string", "variable2": "string"}