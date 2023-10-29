
 Transform Function
 ----------------------------------------------------
Input:
    dataframe - the dataframe with all the data after the reading functions and association function were called. 
Output:
    dataframe - Transform dataframe where each row it is a prediction and may have or not have associated groundtruth/prediction.

The function can transform the data as desired. It can be used in order to calc statistics over event rather than over detections, or any other transformation that may be required.


Each user defined function should be in seperate file where the name of the file and the name of the user defined function in the file should be the same. 

As with all user-defined functions, it is possible to add parameters to user-defined function. 
These parameters can be added by the user who creates the report at report creation time. 
The function that describes the parameters for each function should be in the same file as the function and in the following format:

    def get_function_arguments():
        return { "variable1": "string", "variable2": "string"}
"""