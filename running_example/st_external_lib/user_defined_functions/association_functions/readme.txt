Association Function :
------------------------------

Arguments:

- predictions_list (list): A list of bounding boxes representing the predicted locations of objects.
- gt_list (list): A list of bounding boxes representing the ground truth locations of objects.
- **kwargs: Additional keyword arguments.

Returns:

- dict: A dictionary of associations between the predictions and ground truth boxes. The keys of the dictionary are the indices of the predictions in the predictions_list, and the values are the indices of the associated ground truth boxes in the gt_list.


This function takes in two lists: predictions_list (a list of predictions) and gt_list (a list of ground truth annotations). 
The function should calculate and return a dictionary of associations between the predictions and ground truth boxes. 
The associations should be determined based on the specific use case, such as bounding box overlap.


Each user defined function should be in seperate file where the name of the file and the name of the user defined function in the file should be the same. 


As with all user-defined functions, it is possible to add parameters to user-defined function. 
These parameters can be added by the user who creates the report at report creation time. 
The function that describes the parameters for each function should be in the same file as the function and in the following format:

    def get_function_arguments():
        return { "variable1": "string", "variable2": "string"}

