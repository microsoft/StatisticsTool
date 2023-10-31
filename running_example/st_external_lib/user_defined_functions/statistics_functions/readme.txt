"""
Statistics Function instructions:
------------------------------
Input:
confusion_masks - Dictinary with all the masks that was calculated in the the confusion function.
                  The masks can be only part of the rows according to the current segmentatin in the report.
kwargs - Additional options and parameters that can be passed to the function.

Returns a dictionary with all the desired statistics where the key is the name and the value is numerical score:


Output Example:
{'precision': 0.65, 'recall': 0.98, 'any_other_score': 0.2}

 
  
Each user defined function should be in seperate file where the name of the file and the name of the user defined function in the file should be the same. 

As with all user-defined functions, it is possible to add parameters to user-defined function. 
These parameters can be added by the user who creates the report at report creation time. 
The function that describes the parameters for each function should be in the same file as the function and in the following format:

    def get_function_arguments():
        return { "variable1": "string", "variable2": "string"}
"""