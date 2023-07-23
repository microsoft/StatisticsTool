import pandas as pd
import numpy as np


def filter_dirty_labels(comp_data, **kwargs):
    # override auto-gt detection --> if manual annotation 'General_Human_Presence[header]' == 'No' for an index
    if 'General_Human_Presence[header]' in comp_data.keys():
        comp_data.loc[comp_data['General_Human_Presence[header]'] == 'No', ['detection_gt', 'object_id_gt', 'x_gt', 'y_gt', 'width_gt', 'height_gt']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    if 'HumanPresence[sequence]' in comp_data.keys():
        comp_data.loc[comp_data['HumanPresence[sequence]'] == 'False', ['detection_gt', 'object_id_gt', 'x_gt', 'y_gt', 'width_gt', 'height_gt']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

    return comp_data