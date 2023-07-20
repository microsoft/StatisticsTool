import numpy as np
import pandas as pd

def size_horizontal_vertical_and_bbox_meta(dataframe, from_file=False, img_width=1920, img_height=1080, **kwargs):
    type_ = float if from_file else object
    prd_width = dataframe['width'].values.astype(type_)
    prd_height = dataframe['height'].values.astype(type_)
    label_width = dataframe['width_gt'].values.astype(type_)
    label_height = dataframe['height_gt'].values.astype(type_)
    prd_x = dataframe['x'].values.astype(type_)
    label_x = dataframe['x_gt'].values.astype(type_)
    prd_y = dataframe['y'].values.astype(type_)
    label_y = dataframe['y_gt'].values.astype(type_)

    prd_x2 = prd_x + prd_width
    prd_y2 = prd_y + prd_height
    label_x2 = label_x + label_width
    label_y2 = label_y + label_height

    prd_y_center = (2*prd_y + prd_height)/2
    label_y_center = (2*label_y + label_height)/2
    prd_x_center = (2*prd_x + prd_width)/2
    label_x_center = (2*label_x + label_width)/2

    # masking by the area of the bounding box

    tiny_object_pct = 0.052  # 100px @1920
    small_object_pct = 0.15625  # 300px @1920
    large_object_pct = 0.3125  # 600px @1920

    gt_exists = dataframe['detection_gt'].notnull().values.astype('bool')
    tiny_obejcts = ((label_width <= (tiny_object_pct * img_width)) & gt_exists) | (
        (prd_width < (tiny_object_pct * img_width)) & np.logical_not(gt_exists))
    small_obejcts = (((label_width < (small_object_pct * img_width)) & (label_width > (tiny_object_pct * img_width))) & gt_exists) | (
        ((prd_width < (small_object_pct * img_width)) & (prd_width > (tiny_object_pct * img_width))) & np.logical_not(gt_exists))
    large_obejcts = ((label_width > (large_object_pct * img_width)) & gt_exists) | (
        (prd_width > (large_object_pct * img_width)) & np.logical_not(gt_exists))
    medium_objects = np.logical_not(
        (tiny_obejcts | small_obejcts | large_obejcts))

    size = {'possible partitions': [
        'large', 'medium', 'small', 'tiny'], 'masks': [large_obejcts, medium_objects, small_obejcts, tiny_obejcts]}
    is_tiny = {'possible partitions': [
        'valid_width', 'tiny_width'], 'masks': [np.logical_not(tiny_obejcts), tiny_obejcts]}
    valid_size = {'possible partitions': [
        'v_large', 'v_medium', 'v_small'], 'masks': [large_obejcts, medium_objects, small_obejcts]}

    # masking by x value
    prd_left_x = prd_x_center < img_width/2
    label_left_x = label_x_center < img_width/2
    prd_right_x = np.logical_not(prd_left_x)
    label_right_x = np.logical_not(label_left_x)
    right_mask = prd_right_x | (label_right_x & dataframe['x'].isnull())
    left_mask = prd_left_x | (label_left_x & dataframe['x'].isnull())
    x_position = {'possible partitions': ['right', 'left'], 'masks': [right_mask, left_mask]}

    # masking by y value
    prd_upper_y = prd_y_center < img_height/2  # upper because of how matplotlib shows the image - the y axis origin is at the top so the upper part has lower values
    label_upper_y = label_y_center < img_height/2
    prd_lower_y = np.logical_not(prd_upper_y)
    label_lower_y = np.logical_not(label_upper_y)
    lower_mask = prd_lower_y | (label_lower_y & dataframe['x'].isnull())
    upper_mask = prd_upper_y | (label_upper_y & dataframe['x'].isnull())
    y_position = {'possible partitions': ['up', 'down'], 'masks': [upper_mask, lower_mask]}
    
    desired_masks = {'size': size, 'is_tiny': is_tiny, 'valid_size': valid_size, 'x position': x_position, 'y position': y_position}

    # masking by iou
    bins = [-1, 0, 0.25, 0.5, 0.75, 1.1]
    labels = ['0', '0-0.25', '0.25-0.5', '0.5-0.75', '0.75-1']

    dataframe['iou_binned'] = pd.cut(
        dataframe['iou'], bins=bins, labels=labels)
    dataframe['iou_binned'] = dataframe['iou_binned'].values.add_categories(
        'missing iou')
    dataframe['iou_binned'].fillna('missing iou', inplace=True)
    labels = ['missing iou'] + labels
    masks = []
    for label in labels:
        curr_mask = (dataframe['iou_binned'] == label)
        masks.append(curr_mask)

    iou = {'possible partitions': labels[::-1], 'masks': masks[::-1]}
    desired_masks_iou = {'iou': iou}

    desired_masks.update(desired_masks_iou)


    # masking by bbox proximity to x axis edge
    fifth_width = 0.05 * img_width # 10
    prd_edge_mask = (prd_x < fifth_width)| (prd_x2 > img_width - fifth_width)
    label_edge_mask = (label_x < fifth_width) | (label_x2 > img_width - fifth_width)
    edge_mask = prd_edge_mask | (label_edge_mask & dataframe['x'].isnull())
    edge_mask_dict = {'possible partitions': ['centerX', 'edgeX'], 'masks': [np.logical_not(edge_mask), edge_mask]}
    desired_masks.update({"isEdgeX": edge_mask_dict})

    # masking by bbox center proximity to x axis edge
    prd_left_x = prd_x_center < img_width / 4
    prd_right_x = prd_x_center > img_width - img_width / 4
    label_left_x = label_x_center < img_width / 4
    label_right_x = label_x_center > img_width - img_width / 4
    centerBB_edgeX_mask = prd_right_x | prd_left_x | (label_right_x & dataframe['x'].isnull()) | (label_left_x & dataframe['x'].isnull())
    centerBB_edgeX_mask_dict = {'possible partitions': ['centerBB_CenterX', 'centerBB_EdgeX'], 'masks': [np.logical_not(centerBB_edgeX_mask), centerBB_edgeX_mask]}
    desired_masks.update({"isCenterEdgeX": centerBB_edgeX_mask_dict})
    
    # masking by bbox proximity to x axis edge
    fifth_height = 0.05 * img_height # 10
    prd_edge_mask = (prd_y < fifth_height) | (prd_y2 > img_height - fifth_height)
    label_edge_mask = (label_y < fifth_height) | (label_y2 > img_height - fifth_height)
    edge_mask = prd_edge_mask | (label_edge_mask & dataframe['x'].isnull())
    edge_mask_dict = {'possible partitions': ['edgeY', 'CenterY'], 'masks': [edge_mask, np.logical_not(edge_mask)]}
    desired_masks.update({"isEdgeY": edge_mask_dict})


    # person on edges
    # ---------------
    elongation_ratio_medium = 2
    elongation_ratio_high = 3
    margin_px = 20

    gt_bb_on_boundary = ((dataframe['x_gt'] < 0 + margin_px) | (
        dataframe['x_gt'] + dataframe['width_gt'] > img_width - margin_px))
    prd_bb_on_boundary = ((dataframe['x'] < 0 + margin_px) | (
        dataframe['x'] + dataframe['width'] > img_width - margin_px))

    gt_high_elongation = (
        (dataframe['height_gt'] / dataframe['width_gt']) > elongation_ratio_high) & gt_bb_on_boundary
    gt_medium_elongation = ((dataframe['height_gt'] / dataframe['width_gt']) > elongation_ratio_medium) & (
        (dataframe['height_gt'] / dataframe['width_gt']) <= elongation_ratio_high) & gt_bb_on_boundary
    gt_low_elongation = np.logical_not(
        (gt_high_elongation | gt_medium_elongation)) & gt_bb_on_boundary
    gt_inside = np.logical_not(gt_bb_on_boundary)

    prd_high_elongation = (
        (dataframe['height'] / dataframe['width']) > elongation_ratio_high) & prd_bb_on_boundary
    prd_medium_elongation = ((dataframe['height'] / dataframe['width']) > elongation_ratio_medium) & (
        (dataframe['height'] / dataframe['width']) <= elongation_ratio_high) & prd_bb_on_boundary
    prd_low_elongation = np.logical_not(
        (prd_high_elongation | prd_medium_elongation)) & prd_bb_on_boundary
    prd_inside = np.logical_not(prd_bb_on_boundary)

    high_elongation = (gt_exists & gt_high_elongation) | (
        np.logical_not(gt_exists) & prd_high_elongation)
    medium_elongation = (gt_exists & gt_medium_elongation) | (
        np.logical_not(gt_exists) & prd_medium_elongation)
    low_elongation = (gt_exists & gt_low_elongation) | (
        np.logical_not(gt_exists) & prd_low_elongation)
    inside = (gt_exists & gt_inside) | (np.logical_not(gt_exists) & prd_inside)

    boundary = {'possible partitions': ['inside', 'low_elongation_on_boundary', 'medium_elongation_on_boundary',
                                        'high_elongation_on_boundary'], 'masks': [inside, low_elongation, medium_elongation, high_elongation]}

    desired_masks_boundary = {'boundary': boundary}

    desired_masks.update(desired_masks_boundary)

    def get_annotation_dict(annotation_name, att_types=[], other_name='other'):
        frame_att_all = dataframe[annotation_name].values.astype(object)
        frame_atts = []
        for att_type in att_types:
            frame_att = np.full(np.shape(frame_att_all), False)
            frame_att[frame_att_all==att_type] = True
            frame_atts.append(frame_att)

        frame_att_other = np.full(np.shape(frame_att_all), True)
        for att_type in att_types:
            frame_att_other[frame_att_all==att_type] = False
        frame_atts.append(frame_att_other)
        
        keys = [str(att_type) for att_type in att_types]
        keys.append(other_name)
        frame_dict = {'possible partitions': keys, 'masks': frame_atts}
        return frame_dict
    

    # masking by bbox meta
    if "BB_Body_Orientation_gt" in dataframe.columns:
        frame_orientation_dict = get_annotation_dict("BB_Body_Orientation_gt", att_types=['Foward', 'Back', 'Partial', 'Side'], other_name='Other_orientation')
        desired_masks.update({"User Orientation": frame_orientation_dict})

    if "BB_Occluded_gt" in dataframe.columns:
        frame_occluded_dict = get_annotation_dict("BB_Occluded_gt", att_types=[0.0,25.0,50.0,75.0,100.0], other_name='Other_occlusion')
        desired_masks.update({"Occluded": frame_occluded_dict})


    if "BB_Body_InFrame_gt" in dataframe.columns:
        body_inframe_dict = get_annotation_dict("BB_Body_InFrame_gt", att_types=['FullBody','UpperBoddy','SideBody','MidBody','LowerBody','SideUpperBody','SideLowerBody'], other_name='Other_inframe')
        desired_masks.update({"Body_Inframe": body_inframe_dict})

    # making sure there is no same 'possible partitions' for different partitions
    all_the_options = []
    for key in desired_masks:
        for option_list in desired_masks[key]['possible partitions']:
            all_the_options.append(option_list)
    assert len(all_the_options) == len(np.unique(all_the_options)), 'two partition options cant have the same name'

    return desired_masks
