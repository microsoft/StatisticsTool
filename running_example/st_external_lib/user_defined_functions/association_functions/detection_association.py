from scipy.optimize import linear_sum_assignment
import numpy as np


THRESHOLD_KEY=  'threshold'


def detection_association(predictions_list, gt_list, **kwargs):
    
    assert THRESHOLD_KEY in kwargs, 'association function must have threshold argument.'

    threshold = float(kwargs[THRESHOLD_KEY])

    if not len(gt_list) or not len(predictions_list):
        overlap_mat=[]
    else:
        overlap_mat = np.zeros((len(predictions_list), len(gt_list)))
    
    prediction_associate = {}
        
    for i, prd_BB in enumerate(predictions_list):
        for j, label_BB in enumerate(gt_list):
            if is_valid_bb(prd_BB) != is_valid_bb(label_BB):
                overlap = 0
            elif not is_valid_bb(prd_BB): #both are they are matched as False
                overlap = 1
            else:
                overlap = Dice(prd_BB, label_BB)

            if threshold and overlap < threshold:
                overlap = 0
            overlap_mat[i, j] = round(overlap, 2)
    

    if len(overlap_mat) > 0:
        prd_ind, label_ind = linear_sum_assignment(overlap_mat, maximize=True)

        # labels and predictions that have a match will be evaluated according to their overlap (threshold dependent)
        for i, j in zip(prd_ind, label_ind):
            if overlap_mat[i][j] > threshold:
                prediction_associate[i] = j

    return prediction_associate

def get_function_arguments():
    return { "threshold":"string"}


def is_valid_bb(row):
    retval = ('x' in row and row['x']!=None) \
        and ('y' in row and row['y']!=None) \
        and ('width' in row and row['width']!=None) \
        and ('height' in row and row['height']!=None)
    return retval

def Dice(pred_row, labels_row):

    predictions = [pred_row['x'], pred_row['y'], pred_row['width'], pred_row['height']]
    labels = [labels_row['x'], labels_row['y'], labels_row['width'], labels_row['height']]
    # calculate (xmin, ymin, xmax, ymax) from the data available
    label_xmin = labels[0]
    label_xmax = label_xmin + labels[2]
    label_ymin = labels[1]
    label_ymax = label_ymin + labels[3]

    prediction_xmin = predictions[0]
    prediction_xmax = prediction_xmin + predictions[2]
    prediction_ymin = predictions[1]
    prediction_ymax = prediction_ymin + predictions[3]

    # calculate the intersection of the two bounding boxed
    intersect_xmin = max(label_xmin, prediction_xmin)
    intersect_xmax = min(label_xmax, prediction_xmax)
    intersect_ymin = max(label_ymin, prediction_ymin)
    intersect_ymax = min(label_ymax, prediction_ymax)
    # handle cases of no overlap
    if intersect_xmax < intersect_xmin or intersect_ymax < intersect_ymin:
        return 0.0
    # calculate metric
    intersect_area = (intersect_xmax - intersect_xmin) * (intersect_ymax - intersect_ymin)
    label_area = (label_ymax - label_ymin) * (label_xmax - label_xmin)
    prediction_area = (prediction_ymax - prediction_ymin) * (prediction_xmax - prediction_xmin)
    dice = 2*intersect_area / float(label_area + prediction_area)
    assert dice >= 0, 'dice coefficients should be larger or equal 0'
    assert dice <= 1, 'dice coefficients should be smaller or equal 0'
    return dice
