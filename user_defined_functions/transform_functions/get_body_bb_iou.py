import numpy as np
import pandas as pd
from user_defined_functions.overlap_functions.IOU import IOU


def get_body_bb_iou(comp_data):
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
    
    return comp_data