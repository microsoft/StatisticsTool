import numpy as np
def transform_bb_size(bb_object, emulation_matrix):
    '''
    Transforms the bounding box size according to the emulation matrix
    :bb_object: dictionary with the bounding box information, fields: 'Left', 'Top', 'Width', 'Height'
    :emulation_matrix: 3x3 matrix
    '''
    # if emulation matrix is a unit matrix, then no transformation is needed
    if np.array_equal(emulation_matrix, np.identity(3)):
        return bb_object
    else:
        cord = np.array([bb_object['Left'], bb_object['Top'], 1])
        cord = emulation_matrix.dot(cord)
        width_hight = np.array([bb_object['Width'], bb_object['Height'], 0])
        width_hight = emulation_matrix.dot(width_hight)
        return {'Left':cord[0],'Top':cord[1],'Width':width_hight[0],'Height':width_hight[1]}
