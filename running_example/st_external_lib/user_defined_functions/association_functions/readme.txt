Association Function :
------------------------------
    This function takes in two lists of bounding boxes, predictions_list and gt_list, and returns a dictionary of associations
    between the predictions and ground truth boxes. The associations are determined based on the overlap between the boxes,
    which is calculated using the Dice coefficient. The function also takes in a threshold argument, which is used to filter
    out associations with low overlap scores.

    Args:
        predictions_list (list): A list of bounding boxes representing the predicted locations of objects.
        gt_list (list): A list of bounding boxes representing the ground truth locations of objects.
        **kwargs: Additional keyword arguments.

    Returns:
        dict: A dictionary of associations between the predictions and ground truth boxes. The keys are the indices of the
        predictions in the predictions_list, and the values are the indices of the associated ground truth boxes in the gt_list.