"""
Statistics Function instructions:
------------------------------
Input:
Integers that indicate the number of TP, FP, FN, total_preds

A Statistics function should:
1. Calculate the statistics (if the denominator is 0 please return -1)
2. Round the statistics number, preferably 3 digits after the decimal point

Returns a dictionary with the following form:
{'Statistics Name': Statistics numerical score}
"""

def precision_recall(TP, FP, FN, total_preds):
    if TP + FN == 0:
        recall = -1
    else:
        recall = TP / (TP + FN)
    if TP + FP == 0:
        precision = -1
    else:
        precision = TP / (TP + FP)
    return {'Recall': round(recall, 3), 'Precision': round(precision, 3)}

def TNR(TP, FP, FN, total_preds):
    TN = total_preds - (TP + FP + FN)
    if TN == 0:
        tnr = -1
    else:
        tnr = TN/(TN + FP)
    return {'TNR': round(tnr, 3)}

def precision_recall_f1(TP, FP, FN, total_preds):
    param = TP + FN
    if param == 0:
        recall = -1
    else:
        recall = TP / param
    
    param2 = TP + FP
    if param2 == 0:
        precision = -1
    else:
        precision = TP / param2
    
    if precision < 0 or recall < 0:
        f1 = -1
    else:
        f1 = 2 * (precision * recall) / (precision + recall)
    return {'Recall': round(recall, 3), 'Precision': round(precision, 3), 'F1': round(f1, 3)}

def sep_FP_seq_count(total_preds):
    return {'Separate FP Sequence Count': total_preds}

def sep_FN_seq_count(total_preds):
    return {'Separate FN Sequence Count': total_preds}

def presence_leave_flicker_seq_count(TP, FP, FN, total_preds):
    return {'Leave Flicker Count': total_preds}

def presence_approach_flicker_seq_count(TP, FP, FN, total_preds):
    return {'Approach Flicker Count': total_preds}
