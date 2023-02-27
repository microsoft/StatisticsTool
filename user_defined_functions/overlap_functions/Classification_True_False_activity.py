
"""
Overlap Function instructions:
------------------------------

Input:
prediction and groun truth dictionaries that contains prediction and label dictionaries with the same keys and values as added in user defined reading function


An Overlap function should:
1. Extract the relevant information from dictionaries (e.g the XYWH coordinates for detection tasks)
2. return overlap score between pred and label. The score will be used with the threshold to determine if the pred and the label are the same detection.

Returns:
A numerical score

"""

def Classification_True_False_activity(pred_row, labels_row):
    if pred_row['activity'] == labels_row['activity']:
        return 1.0
    return 0.0 

