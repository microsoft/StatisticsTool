import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None


def basic_event_transform(df):
    """
    purpose:
    -------- 
    transforms a long matrix into a shorter one. each time gt & det changes mutual state, a new event is declared
    
    example:
    --------
    input:
            idx	gt	det
            0	1	1
            1	1	1
            2	1	0
            3	1	1
            4	1	1
            5	1	0
            6	0	1
            7	1	1
            8	1	1
            9	1	1
    output:
            gt	    det	    frame_id	end_frame
            1	    1	    0	        1
            1	    0	    2	        2
            1	    1	    3	        4
            1	    0	    5	        5
            0	    1	    6	        6
            1	    1	    7	        9

    notice:
    ------- 
    only metadata of first row (frame) of event is kept! partitioning functions comsuming per-frame annotations will be distorted

    """

    # detect changes for detection and detection_gt separately
    df['diff_gt'] = df['detection_gt'].astype(int).diff().fillna(0)
    df['diff_det'] = df['detection'].astype(int).diff().fillna(0)

    # generate event_idx column --> rows which belong to the same event will have the same event_idx
    df['diff_of_diffs'] = df['diff_gt'] - df['diff_det']
    df['event_start_flag'] = 0
    df['event_start_flag'][0] = 1 # first event starts at first index (row)
    df.loc[df['diff_of_diffs'] != 0, 'event_start_flag'] = 1
    df['event_idx'] = df['event_start_flag'].cumsum() # rows which belong to the same event have the same event_idx
    df['row_index'] = df['frame_id'] # copy original index to prepare for 'end_frame' 

    # group events --> squash rows that have the same event_idx
    df_out = df.groupby('event_idx').first().reset_index()
    df_out['frame_id'] = df_out['row_index'] # frame_id is convention for 'first index of event'
    df_out['end_frame'] = df.groupby('event_idx').last().reset_index()['row_index'] # end_frame is convention for 'last index of event'

    df_out.drop(['diff_gt', 'diff_det', 'diff_of_diffs', 'event_start_flag', 'event_idx', 'row_index'], axis=1, inplace=True) # drop aux calculation columns

    return df_out







