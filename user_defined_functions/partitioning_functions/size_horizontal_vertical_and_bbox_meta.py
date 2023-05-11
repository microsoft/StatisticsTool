import numpy as np

def size_horizontal_vertical_and_bbox_meta(dataframe, from_file=False, img_width=1920, img_height=1080):
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
    prd_large_mask = prd_width + prd_height >= (img_width + img_height)/1.3
    prd_medium_mask = (prd_width + prd_height < (img_width + img_height)/1.3) & (prd_width + prd_height >= (img_width + img_height)/3)
    prd_small_mask = np.logical_not(prd_large_mask | prd_medium_mask)

    label_large_mask = label_width + label_height >= (img_width + img_height)/1.3
    label_medium_mask = (label_width + label_height < (img_width + img_height)/1.3) & (label_width + label_height >= (img_width + img_height)/3)
    label_small_mask = np.logical_not(label_large_mask | label_medium_mask)

    large_mask = prd_large_mask | (label_large_mask & dataframe['x'].isnull())
    small_mask = prd_small_mask | (label_small_mask & dataframe['x'].isnull())
    medium_mask = prd_medium_mask | (label_medium_mask & dataframe['x'].isnull())


    size = {'possible partitions': ['large','medium', 'small'], 'masks': [large_mask, medium_mask, small_mask]}

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

    desired_masks = {'size': size, 'x position': x_position, 'y position': y_position}


    # masking by bbox proximity to x axis edge
    fifth_width = 0.05 * img_width # 10
    prd_edge_mask = (prd_x < fifth_width)| (prd_x2 > img_width - fifth_width)
    label_edge_mask = (label_x < fifth_width) | (label_x2 > img_width - fifth_width)
    edge_mask = prd_edge_mask | (label_edge_mask & dataframe['x'].isnull())
    edge_mask_dict = {'possible partitions': ['edgeX', 'not edgeX'], 'masks': [edge_mask, np.logical_not(edge_mask)]}
    desired_masks.update({"isEdgeX": edge_mask_dict})

    # masking by bbox center proximity to x axis edge
    prd_left_x = prd_x_center < img_width / 4
    prd_right_x = prd_x_center > img_width - img_width / 4
    label_left_x = label_x_center < img_width / 4
    label_right_x = label_x_center > img_width - img_width / 4
    centerBB_edgeX_mask = prd_right_x | prd_left_x | (label_right_x & dataframe['x'].isnull()) | (label_left_x & dataframe['x'].isnull())
    centerBB_edgeX_mask_dict = {'possible partitions': ['centerBB_EdgeX', 'not centerBB_EdgeX'], 'masks': [centerBB_edgeX_mask, np.logical_not(centerBB_edgeX_mask)]}
    desired_masks.update({"isCenterEdgeX": centerBB_edgeX_mask_dict})
    
    # masking by bbox proximity to x axis edge
    fifth_height = 0.05 * img_height # 10
    prd_edge_mask = (prd_y < fifth_height) | (prd_y2 > img_height - fifth_height)
    label_edge_mask = (label_y < fifth_height) | (label_y2 > img_height - fifth_height)
    edge_mask = prd_edge_mask | (label_edge_mask & dataframe['x'].isnull())
    edge_mask_dict = {'possible partitions': ['edgeY', 'not edgeY'], 'masks': [edge_mask, np.logical_not(edge_mask)]}
    desired_masks.update({"isEdgeY": edge_mask_dict})


    # masking by bbox meta
    if "BB_Body_Orientation_gt" in dataframe.columns:
        frame_orientation = dataframe['BB_Body_Orientation_gt'].values.astype(object)
        frame_orientation_foward  = np.full(np.shape(frame_orientation), False)
        frame_orientation_back  = np.full(np.shape(frame_orientation), False)
        frame_orientation_partial  = np.full(np.shape(frame_orientation), False)
        frame_orientation_side  = np.full(np.shape(frame_orientation), False)
        frame_orientation_other  = np.full(np.shape(frame_orientation), True)

        frame_orientation_foward[frame_orientation=='Foward'] = True
        frame_orientation_back[frame_orientation=='Back'] = True
        frame_orientation_partial[frame_orientation=='Partial'] = True
        frame_orientation_side[frame_orientation=='Side'] = True

        frame_orientation_other[frame_orientation=='Foward'] = False
        frame_orientation_other[frame_orientation=='Back'] = False
        frame_orientation_other[frame_orientation=='Partial'] = False
        frame_orientation_other[frame_orientation=='Side'] = False

        frame_orientation_dict = {'possible partitions': ['Foward','Back','Partial','Side','Other_orientation'], 'masks': [frame_orientation_foward,frame_orientation_back,frame_orientation_partial, frame_orientation_side, frame_orientation_other]}
        desired_masks.update({"User Orientation": frame_orientation_dict})

    if "BB_Occluded_gt" in dataframe.columns:
        frame_occluded = dataframe['BB_Occluded_gt'].values.astype(object)
        frame_occluded_0  = np.full(np.shape(frame_occluded), False)
        frame_occluded_25  = np.full(np.shape(frame_occluded), False)
        frame_occluded_50  = np.full(np.shape(frame_occluded), False)
        frame_occluded_75  = np.full(np.shape(frame_occluded), False)
        frame_occluded_100  = np.full(np.shape(frame_occluded), False)
        frame_occluded_other  = np.full(np.shape(frame_occluded), True)

        frame_occluded_0[frame_occluded==0.0] = True
        frame_occluded_25[frame_occluded==25.0] = True
        frame_occluded_50[frame_occluded==50.0] = True
        frame_occluded_75[frame_occluded==75.0] = True
        frame_occluded_100[frame_occluded==100.0] = True

        frame_occluded_other[frame_occluded==0.0] = False
        frame_occluded_other[frame_occluded==25.0] = False
        frame_occluded_other[frame_occluded==50.0] = False
        frame_occluded_other[frame_occluded==75.0] = False
        frame_occluded_other[frame_occluded==100.0] = False

        frame_occluded_dict = {'possible partitions': ['0.0','25.0','50.0','75.0','100.0','Other_occlusion'], 'masks': [frame_occluded_0,frame_occluded_25,frame_occluded_50, frame_occluded_75, frame_occluded_100, frame_occluded_other]}
        desired_masks.update({"Occluded": frame_occluded_dict})

    if "BB_Body_InFrame_gt" in dataframe.columns:
        body_inframe = dataframe['BB_Body_InFrame_gt'].values.astype(object)
        body_inframe_SideBody  = np.full(np.shape(body_inframe), False)
        body_inframe_FullBody  = np.full(np.shape(body_inframe), False)
        body_inframe_UpperBoddy  = np.full(np.shape(body_inframe), False)
        body_inframe_SideUpperBody  = np.full(np.shape(body_inframe), False)
        body_inframe_LowerBody  = np.full(np.shape(body_inframe), False)
        body_inframe_MidBody  = np.full(np.shape(body_inframe), False)
        body_inframe_SideLowerBody  = np.full(np.shape(body_inframe), False)
        body_inframe_Other  = np.full(np.shape(body_inframe), True)

        body_inframe_SideBody[body_inframe=='SideBody'] = True
        body_inframe_FullBody[body_inframe=='FullBody'] = True
        body_inframe_UpperBoddy[body_inframe=='UpperBoddy'] = True
        body_inframe_SideUpperBody[body_inframe=='SideUpperBody'] = True
        body_inframe_LowerBody[body_inframe=='LowerBody'] = True
        body_inframe_MidBody[body_inframe=='MidBody'] = True
        body_inframe_SideLowerBody[body_inframe=='SideLowerBody'] = True

        body_inframe_Other[body_inframe=='SideBody'] = False
        body_inframe_Other[body_inframe=='FullBody'] = False
        body_inframe_Other[body_inframe=='UpperBoddy'] = False
        body_inframe_Other[body_inframe=='SideUpperBody'] = False
        body_inframe_Other[body_inframe=='LowerBody'] = False
        body_inframe_Other[body_inframe=='MidBody'] = False
        body_inframe_Other[body_inframe=='SideLowerBody'] = False

        body_inframe_dict = {'possible partitions': ['SideBody','FullBody','UpperBoddy','SideUpperBody','LowerBody','MidBody','SideLowerBody','Other_inframe'], 'masks': [body_inframe_SideBody,body_inframe_FullBody,body_inframe_UpperBoddy, body_inframe_SideUpperBody, body_inframe_LowerBody, body_inframe_MidBody, body_inframe_SideLowerBody, body_inframe_Other]}
        desired_masks.update({"Body_Inframe": body_inframe_dict})

    

    # making sure there is no same 'possible partitions' for different partitions
    all_the_options = []
    for key in desired_masks:
        for option_list in desired_masks[key]['possible partitions']:
            all_the_options.append(option_list)
    assert len(all_the_options) == len(np.unique(all_the_options)), 'two partition options cant have the same name'

    return desired_masks
