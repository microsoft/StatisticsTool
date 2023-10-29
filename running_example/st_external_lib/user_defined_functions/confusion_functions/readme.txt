
confusion_matrix :
------------------------------

Arguments:
    = dataframe (pandas.DataFrame): The input dataframe containing all the information regarding to predictions and gts.
    - **kwargs: Additional keyword arguments.

Returns:
    dict: A dictionary masks contains the desired confusion matrix
    

Calculates the confusion matrix for a given dataframe and returns a map of masks for each confusion group.
Example of result:
{'TP':TP_mask,'FP':FP_Mask,'TN':TN_Mask}

Each user defined function should be in seperate file where the name of the file and the name of the user defined function in the file should be the same. 

As with all user-defined functions, it is possible to add parameters to user-defined function. 
These parameters can be added by the user who creates the report at report creation time. 
The function that describes the parameters for each function should be in the same file as the function and in the following format:

def get_function_arguments():
        return { "variable1": "string", "variable2": "string"}
