import pathlib
import cv2
import os
import pathlib
from io import BytesIO

from experiment_engine.file_storage_handler import StoreType, find_in_blob_by_video_name, get_file_on_local_storage

def prepare_example_image(image_file, frame_id, prd_bbs, label_bbs, selected_pred = -1, selected_label = -1):
 
    vid= cv2.VideoCapture(image_file)
    if is_video(image_file) and frame_id:
        vid.set(cv2.CAP_PROP_POS_FRAMES, int(frame_id))
    _, frame = vid.read()
    
    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        vid.release()
    else:
        print(f'Cant find frmae {frame_id} for: {image_file}')

    frame = draw_detections_on_figure(frame, prd_bbs, label_bbs, selected_pred, selected_label)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   
    _, buffer = cv2.imencode(".png", image)
    output = BytesIO(buffer)
    
    return output
        
def is_video(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '']:
        return True
    else:
        return False

def draw_rect_on_image(image, x, y, width, height, color, thickness):
    bb_x_top_left = x
    bb_y_top_left = y
    bb_x_bottom_right = (bb_x_top_left + width)
    bb_y_bottom_right = (bb_y_top_left + height)

    start_point = (int(bb_x_top_left), int(bb_y_top_left))
    end_point = (int(bb_x_bottom_right), int(bb_y_bottom_right))
   
    cv2.rectangle(image, start_point, end_point, color, thickness)

def draw_detections_on_figure(image_in, prd_bbs, label_bbs, selected_pred = -1, selected_label = -1):
    """
    Overlay a frame's bounding boxes on top of the frame

    :param prd_bbs: list of x,y,w,h arrays of a single frame's predicted bounding boxes
    :param label_bbs: list of x,y,w,h arrays of a frame's Ground Truth bounding boxes
    :param matched: list of 1 or 2 bounding boxes. the first is prediction the second is label if there is one.
    :param image: the frame of the selected bounding box
    :return: image
    """
    
    if image_in is None:
        return None
    
    image = image_in.copy()
    for index, bb in enumerate(prd_bbs):
        (bb_x_coordinate, bb_y_coordinate, bb_width, bb_height) = bb
        thikness =  1
        if index == selected_pred:
            thikness = 3
        draw_rect_on_image(image, bb_x_coordinate, bb_y_coordinate, bb_width, bb_height, (0, 0, 255), thikness)
    for index, bb in enumerate(label_bbs):
        (bb_x_coordinate, bb_y_coordinate, bb_width, bb_height) = bb
        thikness =  1
        if index == selected_label:
            thikness = 3
        draw_rect_on_image(image, bb_x_coordinate, bb_y_coordinate, bb_width, bb_height, (0, 255, 0), thikness)
    
 
    return image