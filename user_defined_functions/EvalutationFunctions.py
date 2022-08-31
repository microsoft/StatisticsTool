from scipy.optimize import linear_sum_assignment
"""
Evaluation Function instructions:
------------------------------

Input:
a. dictionary that combines the data of the bounding boxes in a frame.
has the form:
{'frame_id': frame number, 'predictions': list of predictions data dictionaries, 'labels': list of labels data dictionaries, 'matrix': overlap matrix}

notice:
a. the overlap matrix rows corresponds to the index in the prediction list (i'th row >> i'th prediction in the list)
b. the overlap matrix columns corresponds to the index in the labels list (j'th column >> j'th label in the list)

An Evaluation function should match between labels and predictions:
1. tag predictions/labels that don't have a match as FP/FN
2. matched predictions/labels dictionary will have a 'matching' key  with value equals to index of the match
3. matched predictions/labels dictionary will have a 'state' key with value equals to overlap with the match

Returns the same input dictionary after the changes
"""




def Zvi_evaluation_func(temp_d):

    predictions_d_list = temp_d['predictions']  # predictions list of dictionaries for current frame index
    labels_d_list = temp_d['gt'] # labels list of dictionaries for current frame index (copy is to avoid looping while changing the original)

    for i in range(len(predictions_d_list)):
        predictions_d_list[i]['state'] = 0
        
    # label that don't have a match is a FN
    for j in range(len(labels_d_list)):
        labels_d_list[j]['state'] = 0

    overlap_mat = temp_d['matrix']  # columns are labels and rows are predictions
    if len(overlap_mat) > 0:
        prd_ind, label_ind = linear_sum_assignment(overlap_mat, maximize=True)

        # labels and predictions that have a match will be evaluated according to their overlap (threshold dependent)
        for i, j in zip(prd_ind, label_ind):
            predictions_d_list[i]['state'] = overlap_mat[i][j]
            predictions_d_list[i]['matching'] =labels_d_list[j].copy()
            labels_d_list[j]['matching']=i
            labels_d_list[j]['state'] = overlap_mat[i][j]

    return temp_d
def classification_evaluation(temp_d):
    predictions_d_list = temp_d['predictions']  # predictions list of dictionaries for current frame index
    labels_d_list = temp_d['gt'] # labels list of dictionaries for current frame index (copy is to avoid looping while changing the original)
    overlap_mat = temp_d['matrix']  # columns are labels and rows are predictions
    
    

    for ind, pred in enumerate(predictions_d_list):
        for gt_ind, gt in enumerate(labels_d_list):
            if pred.keys() == gt.keys(): 
                if pred != gt:
                    predictions_d_list[ind]['state'] = 0
                else:
                    predictions_d_list[ind]['state'] = 1

                predictions_d_list[ind]['matching'] = labels_d_list[gt_ind]
    # only calculate keys in prediction list
    for j in range(len(labels_d_list)):
        labels_d_list[j]['state'] = 1
    return temp_d

def label_centric_greedy_evaluation(temp_d):
    threshold = 0.2
    predictions_d_list = temp_d['predictions']  # predictions list of dictionaries for current frame index
    labels_d_list = temp_d['gt'] # labels list of dictionaries for current frame index (copy is to avoid looping while changing the original)
    overlap_mat = temp_d['matrix']  # columns are labels and rows are predictions
    if overlap_mat:
        matching_predictions_list = []
        # iterate over the labels indices, and calculate the overlap with every prediction
        for label_idx in range(len(labels_d_list)):
            max_overlap = 0
            match = None
            for prd_idx in range(len(predictions_d_list)):
                overlap = overlap_mat[prd_idx][label_idx]
                # if the current overlap is maximal save it as the maximal overlap and save the prediction's index
                if prd_idx not in matching_predictions_list and overlap > max_overlap and overlap >= threshold:
                    max_overlap = overlap
                    match = prd_idx
            # match labels and prediction - save the best overlap and the index of the matching prediction
            if match is not None:
                labels_d_list[label_idx]['state'] = max_overlap
                labels_d_list[label_idx]['matching'] = match
                predictions_d_list[match]['state'] = max_overlap
                predictions_d_list[match]['matching'] = label_idx
                matching_predictions_list.append(match)
            else:
                # when theres no match the labels is FN
                labels_d_list[label_idx]['state'] = 0
        # when theres no match the prediction is FP
        for prd_idx in range(len(predictions_d_list)):
            if prd_idx not in matching_predictions_list:
                predictions_d_list[prd_idx]['state'] = 0
    return temp_d

