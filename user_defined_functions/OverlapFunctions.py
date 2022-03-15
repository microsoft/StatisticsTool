
"""
Overlap Function instructions:
------------------------------

Input:
a. a dictionary that contains a prediction bounding box data (after modifications in Reading function)
b. a dictionary that contains a GT bounding box data (after modifications in Reading function)

An Overlap function should:
1. Extract the relevant information from dictionaries (e.g the XYWH coordinates for detection tasks)
2. calculate a metric

Returns:
A numerical score

"""


def IOU(pred_row, labels_row):
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
    iou = intersect_area / float(label_area + prediction_area - intersect_area)
    assert iou >= 0, 'iou should be larger or equal 0'
    assert iou <= 1, 'iou should be smaller or equal 0'
    return iou


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