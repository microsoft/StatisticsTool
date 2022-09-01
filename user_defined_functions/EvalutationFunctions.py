from scipy.optimize import linear_sum_assignment
"""
Evaluation Function instructions:
------------------------------

Input:
a. list of predictions and labels dictionaries to fill with 'state' and 'matching' keys.

Output:
fill each prediction with it's matching state and matching index in labels list:
fill the prediction array with the following format:

for i in range(len(predictions_dict_list)):
        predictions_dict_list[i]['state'] = grade that will be used with threshold to decide TP/FP/FN - 0 if there is no matching label
        predictions_dict_list[i]['matching'] = index in array of matching labels, if any, otherwise don't set the key

notice:
a. the overlap matrix rows corresponds to the index in the prediction list (i'th row >> i'th prediction in the list)
b. the overlap matrix columns corresponds to the index in the labels list (j'th column >> j'th label in the list)

"""




def min_distance_evaluation(predictions_dict_list, overlap_mat):
    for i in range(len(predictions_dict_list)):
        predictions_dict_list[i]['state'] = 0

    if len(overlap_mat) > 0:
        prd_ind, label_ind = linear_sum_assignment(overlap_mat, maximize=True)

        # labels and predictions that have a match will be evaluated according to their overlap (threshold dependent)
        for i, j in zip(prd_ind, label_ind):
            predictions_dict_list[i]['state'] = overlap_mat[i][j]
            if overlap_mat[i][j] > 0:
                predictions_dict_list[i]['matching'] = j

