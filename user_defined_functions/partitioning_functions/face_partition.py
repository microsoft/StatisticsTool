import numpy as np

def face_partition(dataframe, from_file=False, img_width=1280, img_height=720):
    type_ = float if from_file else object
    score = dataframe['Score'].values.astype(type_)
    

    # masking by the area of the bounding box
    prd_00 = (score > 0) & (score < 0.2)
    prd_02 = (score > 0.2) & (score < 0.4)
    prd_04 = (score > 0.4) & (score < 0.6)
    prd_06 = (score > 0.6) & (score < 0.8)
    prd_08 = (score > 0.8) & (score < 0.9)
    prd_09 = (score > 0.9) & (score < 0.95)
    prd_095 = score > 0.95 
    nan = (score == 'nan')

    score = {'possible partitions': ['>00', '>02','>04','>06','>0.8','>09','>0.95','nan'], 'masks': [prd_00, prd_02, prd_04, prd_06, prd_08, prd_09, prd_095, nan]}

    desired_masks = {'Score': score}

    return desired_masks
