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

def precision_recall_TNR_FPR(TP, FP, FN, total_preds, **kwargs):
    TN = total_preds - (TP + FP + FN)
    if TP + FN == 0:
        recall = -1
    else:
        recall = TP / (TP + FN)
    if TP + FP == 0:
        precision = -1
    else:
        precision = TP / (TP + FP)
    if FP + TN == 0:
        fpr = -1
    else:
        fpr = FP / (FP + TN)

    if TN == 0:
        tnr = -1
    else:
        tnr = TN/(TN + FP)

    return {'Recall': round(recall, 3), 'Precision': round(precision, 3), 'FPR': round(fpr, 3), 'TNR': round(tnr, 3)}

