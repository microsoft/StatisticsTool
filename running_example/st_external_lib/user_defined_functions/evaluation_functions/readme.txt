"""
Partitioning Function instructions:
------------------------------
Input:
a.  Dataframe that contains combined data that was loaded from prediction logs and from annotation logs. 
    The data is after the overlap/evaluation/threshold calculation (According to user defined functions)

Returns:

1. Dictionary with possible partitions in the following form:
{'Partition1 Name': Partition1 Dictionary (see below for dictionary stracture), 'Partition2 Name': Partition2 Dictionary(see below for dictionary stracture)}

2. Each "Partition Dictionary" should be in the following form:
{'possible partitions': ['option 1', 'option 2', ..., 'option n'],
 'prediction masks': [predictions boolean mask for option 1, predictions boolean mask for option 2, ..., predictions boolean mask for option n]}
 
Notice: the predictions boolean masks should be in the same size asthe dataframe with True/False values 

Example {'size':{'possible partitions': ['large', 'small','medium'], 'masks': [large_mask, small_mask, medium_mask]},'position':{'possible partitions': ['right', 'center','left'], 'masks': [right_mask, center_mask, left_mask]}}
"""