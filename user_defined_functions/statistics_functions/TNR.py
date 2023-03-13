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

def TNR(TP, FP, FN, total_preds):
    TN = total_preds - (TP + FP + FN)
    if TN == 0:
        tnr = -1
    else:
        tnr = TN/(TN + FP)
    return {'TNR': round(tnr, 3)}

