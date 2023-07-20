"""
Reading Function instructions:
------------------------------

Input:
a. Accept as input a path to the data file (any type that the user preffered)
b. kwargs - Additional options and parameters that can be passed to the function.

A reading function should:
1. Read the input file (The type of the file is defined by the user according to user prefference)
2. Convert the input data to panda's data frame format. The data frame should have at least the following columns:
    a. frame_id
    b. predictions (1 or more) - array with predictions results for the current frame:
        each element in the array should be dictionary with at least the following keys:
            a. detection (mandatory) - True/False : For TP/FP calculation.
            b. predictioon (not mandatory) - prediction dictionary for comparing between gt/prediction

        If the  prediction is bounding box in the format below, it can be shown as rectangles on frame view:
        - Bounding box columns, using the following names:
                        i.   'x' is the minimal x coordinate
                        ii.  'y' is the minimal y coordinate
                        iii. 'width' is the width of the bounding box (column name will be 'width')
                        iv.  'height' is the height of the bounding box (column name will be 'height')
        
        exmaples for output rows in the dataframe:

            classification example:           
            {'frame_id':frame_id, 'predictions': [{'detection':True, 'prediction':{'classification':'Active'}}]}
            {'frame_id':frame_id, 'predictions': [{'detection':False, 'prediction':{'classification':'Not_Active'}}]}
           
            detection example:
            {'frame_id': frame_id, 'predictions' [{'detection':True, 'prediction':{'object_id':1, 'x':10,'y':20,'width':10,'height':10}}]}
            {'frame_id': frame_id, 'predictions' [{'detection':False}]}



Returns:
pandas dataframe
"""
