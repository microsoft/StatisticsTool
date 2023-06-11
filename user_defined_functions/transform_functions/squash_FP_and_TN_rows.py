import pandas as pd
import numpy as np
from user_defined_functions.overlap_functions.IOU import IOU


def non_max_suppression_fast(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))
    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")


def pick_representative_FP_rows(FP_indices, comp_data):
    if FP_indices.any() > 0:
        # apply clustering to get unique bounding boxes
        boxes = comp_data.loc[FP_indices, [
            'x', 'y', 'width', 'height']].values.astype('float')
        # convert (x_min, y_min, width, height) --> (x_min, y_min, x_max, y_max)
        boxes[:, 2] = boxes[:, 0] + boxes[:, 2]
        boxes[:, 3] = boxes[:, 1] + boxes[:, 3]
        pick = non_max_suppression_fast(boxes, 0.3)
        # convert (x_min, y_min, x_max, y_max) --> (x_min, y_min, width, height)
        if len(pick) > 0:
            pick[:, 2] = pick[:, 2] - pick[:, 0]
            pick[:, 3] = pick[:, 3] - pick[:, 1]
        else:
            pick = comp_data.loc[FP_indices, [
                'x', 'y', 'width', 'height']].values.astype('float')
        # replace FP rows with num of unique bounding boxes
        pick_idx_list = []
        for bb in pick:
            bb_distance = np.sqrt((comp_data['x'] - bb[0]) ** 2 + (comp_data['y'] - bb[1]) ** 2 + (
                comp_data['width'] - bb[2]) ** 2 + (comp_data['height'] - bb[3]) ** 2)
            pick_idx = np.nanargmin(bb_distance)  # ignoring nan values
            pick_idx_list.append(pick_idx)
        comp_data_FP = comp_data.iloc[pick_idx_list, :]
    else:
        comp_data_FP = pd.DataFrame()
    return comp_data_FP


def pick_representative_TN_row_of_empty_video(TN_indices, comp_data):
    if TN_indices.any() > 0:
        representative_row = np.where(TN_indices == True)[0][0]
        comp_data_TN = comp_data.iloc[[representative_row], :]
    else:
        comp_data_TN = pd.DataFrame()
    return comp_data_TN


def filter_dirty_labels(comp_data):
    # override auto-gt detection --> if manual annotation 'General_Human_Presence[header]' == 'No' for an index
    if 'General_Human_Presence[header]' in comp_data.keys():
        comp_data.loc[comp_data['General_Human_Presence[header]'] == 'No', ['detection_gt', 'object_id_gt', 'x_gt', 'y_gt', 'width_gt', 'height_gt']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    if 'HumanPresence[sequence]' in comp_data.keys():
        comp_data.loc[comp_data['HumanPresence[sequence]'] == 'False', ['detection_gt', 'object_id_gt', 'x_gt', 'y_gt', 'width_gt', 'height_gt']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

    return comp_data


def squash_FP_and_TN_rows(comp_data):
    # [0] filter dirty labels
    comp_data = filter_dirty_labels(comp_data)

    # [1] calculate IOU for each index
    if ('x' in comp_data.keys()) and ('x_gt' in comp_data.keys()):
        boxes = comp_data.loc[:, ['x', 'y', 'width',
                                  'height']].values.astype('float')
        comp_data['detection_bb_packed'] = boxes.tolist()
        boxes = comp_data.loc[:, [
            'x_gt', 'y_gt', 'width_gt', 'height_gt']].values.astype('float')
        comp_data['detection_gt_bb_packed'] = boxes.tolist()
    elif 'x' in comp_data.keys() and not('x_gt' in comp_data.keys()):
        boxes = comp_data.loc[:, ['x', 'y', 'width',
                                  'height']].values.astype('float')
        comp_data['detection_bb_packed'] = boxes.tolist()
        boxes = np.nan * np.ones_like(boxes)
        comp_data['detection_gt_bb_packed'] = boxes.tolist()
    elif not('x' in comp_data.keys()) and ('x_gt' in comp_data.keys()):
        boxes = comp_data.loc[:, [
            'x_gt', 'y_gt', 'width_gt', 'height_gt']].values.astype('float')
        comp_data['detection_gt_bb_packed'] = boxes.tolist()
        boxes = np.nan * np.ones_like(boxes)
        comp_data['detection_bb_packed'] = boxes.tolist()
    else:
        comp_data['detection_bb_packed'] = pd.Series(
            [(np.nan * np.ones_like([1, 1, 1, 1])).tolist()] * len(comp_data))
        comp_data['detection_gt_bb_packed'] = comp_data['detection_bb_packed']

    comp_data['iou'] = comp_data.apply(lambda x: IOU(
        x['detection_bb_packed'], x['detection_gt_bb_packed']), axis=1)

    # [2] add column: frame_contains_person_gt (using split + apply):
    # group by frame_id then apply logical OR function on detection_gt --> if any detection_gt exists in frame value is true
    z = comp_data.groupby('frame_id', as_index=False)['detection_gt'].sum()
    z.loc[z['detection_gt'] == 0, ['detection_gt']] = False
    z.loc[z['detection_gt'] != False, ['detection_gt']] = True
    # mapping dict back to original dataframe
    zz = pd.Series(z.detection_gt.values, index=z.frame_id).to_dict()
    comp_data["frame_contains_person_gt"] = comp_data["frame_id"].map(zz)

    # [3a] frames without person - squash TN
    TN_indices = (comp_data['frame_contains_person_gt'] == False) & (
        comp_data['detection'] == False)
    comp_data_TN = pick_representative_TN_row_of_empty_video(
        TN_indices, comp_data)

    # [3b] frames with & without person - squash FP
    # frames without person: squash FP rows with similar bounding boxes
    # frames with person: squash FP rows with detection bounding boxes that have 0% overlap with gt bounding box
    FP_indices = ((comp_data['frame_contains_person_gt'] == False) & (comp_data['detection'] == True)) | (
        (comp_data['frame_contains_person_gt'] == True) & (comp_data['detection'] == True) & (comp_data['iou'] == 0))
    comp_data_FP = pick_representative_FP_rows(
        FP_indices, comp_data)

    # [3c] TP+FN indices should remain intact
    rest_of_indices = np.logical_not((FP_indices | TN_indices))
    comp_data_TP_FN = comp_data.loc[rest_of_indices, :]

    df_tuple_to_concat = (comp_data_TN, comp_data_FP, comp_data_TP_FN)

    # [4] concat squashed FP & squashed TN dataframes
    comp_data = pd.concat(df_tuple_to_concat,
                          axis=0).reset_index(drop=True)
    comp_data = comp_data.sort_values(
        by=['frame_id']).reset_index(drop=True)

    # - empty videos
    # --------------
    # 	- all frames are assumed to be the same --> GT = 0
    # 	- error type:
    # 		- prd bb exists
    # 			- FP
    # 		- prd bb does not exist
    # 			- TN
    # 		- FN, TP = 0
    # 	- squash FP inflation:
    # 		- detect rows with similar prd_bb and squash to one row, add column for total number of similar rows
    # get all indices with FP detections

    # 		- TODO: add columns: [total number of similar FP rows in clip, total number of rows in clip]

    # 	- squash TN inflation:
    # 		- all TN rows (frames) should be squashed to one row
    # get all indices with TN detections
    # 		- TODO: add columns: [total number of same TN rows in clip, total number of rows in clip]

    # - non empty videos
    # ------------------

    # 	- frame without person(s)
    # 		- error type:
    # 			- prd bb exists
    # 				- FP
    # 			- prd bb does not exist
    # 				- TN
    # 			- FN, TP = 0
    # 		- squash FP inflation:
    # 			- detect rows with similar prd_bb and squash to one row, add column for total number of similar rows
    # 			- add columns: [total number of similar FP rows in clip, total number of rows in clip]
    # 		- squash TN inflation:
    # 			- all TN rows (frames) should be squashed to one row
    # 			- add columns: [total number of same TN rows in clip, total number of rows in clip]

    # 	- frame with person(s)
    # 		- completely non-person: 0% overlap
    # 			- FP
    # 			- TN, FN, TP = 0
    # 			- squash FP inflation:
    # 				- detect rows with similar prd_bb and filter
    # 		- partial person intersect: 0<overlap<TH_low && gt not contained in prd
    # 			- FP
    # 			- TN, FN, TP = 0
    # 		- partial person contained: 0<overlap<TH_low && gt contained in prd
    # 			- FP
    # 			- TN, FN, TP = 0
    # 		- person larger than prd: 0<overlap<TH_low && prd contained in gt
    # 			- FP
    # 			- TN, FN, TP = 0
    # 		- "full" person: overlap>TH
    # 			- TP
    # 			- TN, FN, FP = 0

    return comp_data


  
