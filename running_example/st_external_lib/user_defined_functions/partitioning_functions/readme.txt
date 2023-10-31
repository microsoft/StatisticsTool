"""
Evaluation Function instructions:
------------------------------

Input:
a. DataFrame that contains all the predictin and ground truth and all their related data that was added in "reading" functions or elsewhere down the way.
b. kwargs - Additional options and parameters that can be passed to the function.

Output:
Dictionary of dictionaries. The root dictinary is the different possible segments. 



Each root key contains a dictionary of masks that each key is an option for the current segment. The values are masks with trues in all the lines in the DataFrame that belongs the current segment option.


As with all user-defined functions, it is possible to add parameters to user-defined function. 
These parameters can be added by the user who creates the report at report creation time. 
The function that describes the parameters for each function should be in the same file as the function and in the following format:

    def get_function_arguments():
        return { "variable1": "string", "variable2": "string"}
"""