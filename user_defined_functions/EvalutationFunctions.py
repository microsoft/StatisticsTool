from scipy.optimize import linear_sum_assignment
"""
Evaluation Function instructions:
------------------------------

Input:
a. list of predictions and labels dictionaries to fill with 'state' and 'matching' keys.
has the form:
for i in range(len(predictions_dict_list)):
        predictions_dict_list[i]['state'] = grade that will be used with threshold to decide TP/FP/FN - 0 if there is no matching label
        predictions_dict_list[i]['matching'] = index in array of matching labels, if any, otherwise don't set the key
    # label that don't have a match is a FN
    for j in range(len(labels_dict_list)):
        labels_dict_list[j]['state'] = grade that will be used with threshold to decide TP/FP/FN - 0 if there is no matching label
        labels_dict_list[j]['matching'] = index in array of matching perdictions, if any, otherwise don't set the key
notice:
a. the overlap matrix rows corresponds to the index in the prediction list (i'th row >> i'th prediction in the list)
b. the overlap matrix columns corresponds to the index in the labels list (j'th column >> j'th label in the list)

"""




def Zvi_evaluation_func(predictions_dict_list, labels_dict_list, overlap_mat):

    for i in range(len(predictions_dict_list)):
        predictions_dict_list[i]['state'] = 0
        
    # label that don't have a match is a FN
    for j in range(len(labels_dict_list)):
        labels_dict_list[j]['state'] = 0

   
    if len(overlap_mat) > 0:
        prd_ind, label_ind = linear_sum_assignment(overlap_mat, maximize=True)

        # labels and predictions that have a match will be evaluated according to their overlap (threshold dependent)
        for i, j in zip(prd_ind, label_ind):
            predictions_dict_list[i]['state'] = overlap_mat[i][j]
            predictions_dict_list[i]['matching'] = j
            labels_dict_list[j]['matching']=i
            labels_dict_list[j]['state'] = overlap_mat[i][j]
