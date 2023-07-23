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

def precision_recall_f1(TP, FP, FN, total_preds, **kwargs):
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

