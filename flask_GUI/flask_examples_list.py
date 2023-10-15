
import base64
import os
from app_config.constants import Constants
from classes_and_utils.UpdateListManager import UpdateListManager
from flask import render_template, request, Markup
from flask_GUI.flask_server import server, experiments_manager

from utils.image_util import draw_detection_on_figure, read_frame_from_video

class ExamplesList_Routes:
    UPDATE_LIST = '/example_list/update_list'
    EXAMPLE_LIST_HTML = 'examples_list.html'
    SHOW_IMAGE = '/show_im'
    EXAMPLE_IMAGE_HTML = 'example_image.html'

class ExampleList_Tags:
    MAIN_PATH = 'main_path'
    REF_PATH = 'ref_path'
    CELL_NAME = 'cell_name'
    STAT = 'stat'
    UNIQUE = 'unique'
    REF = 'ref'
    COMP_INDEX = 'comp_index'
    LOCAL_PATH = 'local_path'
    EXAMPLE_VID = 'example_vid'
    EXAMPLE_INDEX = 'example_index'
    EXAMPLE_FRAME = 'example_frame'
    SAVE_IMAGE = 'save_image'
    SAVED_IMAGES = 'saved images'

@server.route(ExamplesList_Routes.UPDATE_LIST, methods=['GET', 'POST'])
def show_list():
    main_path = request.args.get(ExampleList_Tags.MAIN_PATH)
    ref_path  = request.args.get(ExampleList_Tags.REF_PATH)
    list_ref_report  = ExampleList_Tags.REF in request.args
    cell_name = request.args.get(ExampleList_Tags.CELL_NAME) if ExampleList_Tags.CELL_NAME in request.args else None
    stat = request.args.get(ExampleList_Tags.STAT) if ExampleList_Tags.STAT in request.args else None  #This is a string contain 'TP' / 'FP' / 'FN
    show_unique = ExampleList_Tags.UNIQUE in request.args

    results_table = experiments_manager.get_results_table(main_path, ref_path)
    list_html, saved_file = UpdateListManager.manage_list_request(results_table, main_path, ref_path, cell_name, stat, show_unique, list_ref_report, 'save_json' in request.args)

    retval= render_template(ExamplesList_Routes.EXAMPLE_LIST_HTML, 
                            state=stat, 
                            cell_name=cell_name,
                            saved_json = saved_file,
                            comp_index = 0 if list_ref_report else -1,
                            unique = show_unique,
                            main_path = main_path,
                            ref_path = ref_path,
                            list_html = Markup(list_html)
    )
    return retval

@server.route(ExamplesList_Routes.SHOW_IMAGE, methods=['GET', 'POST'])
def show_image():
    main_path = request.args.get(ExampleList_Tags.MAIN_PATH)
    ref_path = request.args.get(ExampleList_Tags.REF_PATH)
    comp_index=eval(request.args.get(ExampleList_Tags.COMP_INDEX))
    
    local_path = None    
    if request.args.get(ExampleList_Tags.LOCAL_PATH):
        local_path = request.args.get(ExampleList_Tags.LOCAL_PATH)
    
    video_name = request.args.get(ExampleList_Tags.EXAMPLE_VID)
    example_index = int(request.args.get(ExampleList_Tags.EXAMPLE_INDEX))
    frame_num = int(request.args.get(ExampleList_Tags.EXAMPLE_FRAME))

    main_exp = experiments_manager.get_experiment(main_path)
    ref_exp = experiments_manager.get_experiment(ref_path)

    main_dir,_ = os.path.split(main_path)
    
    detection_text_list, data, save_path = manage_image_request(request,main_exp, ref_exp,main_dir, comp_index>-1, local_path, example_index, video_name, frame_num)

    return render_template(ExamplesList_Routes.EXAMPLE_IMAGE_HTML, 
                           data=data, 
                           save_path=save_path, 
                           detection_text_list=detection_text_list, 
                           video_name = video_name, 
                           example_index = example_index, 
                           frame_num = frame_num, 
                           main_path=main_path, 
                           ref_path=ref_path, 
                           comp_index = comp_index)


def manage_image_request(request, main_exp, ref_exp,main_directory, use_ref, local_path, bb_index, video, frame_id):
    """
    Accepts the requests to /show_im route and returns an encoded image and the path where the image was saved (if it was saved)

    :param request: request from either example_image (to save) or in examples_list.html
    :param exp: exp is an instance of ParallelExperiment
    :return: an encoded image and the path where the image was saved (if it was saved)
    """
    
    save_path = False
    data = None
    image = None
    try:
        image = read_frame_from_video(video, frame_id, local_path)
    except Exception as ex:
        print (f'failed to load image with exception: {ex}')
    
    exp = main_exp
    if use_ref:
        exp = ref_exp
    
    pred_bbs, label_bbs, selected_pred_index, selected_label_index = exp.get_detection_bounding_boxes(bb_index)
    detection_text_list = exp.get_detection_properties_text_list(bb_index)
    out_figure = draw_detection_on_figure(image, pred_bbs, label_bbs=label_bbs, selected_pred=selected_pred_index, selected_label=selected_label_index)
    if out_figure is not None:
        data = base64.b64encode(out_figure.getbuffer()).decode("ascii")
    
    if out_figure and ExampleList_Tags.SAVE_IMAGE in request.args:
        name = video.replace(Constants.JSON_EXTENSION, '')
        name = name.replace(':','')
        if name.startswith('/'):
            name = name[1:]
        
        save_path = os.path.join(os.path.join(main_directory, ExampleList_Tags.SAVED_IMAGES), name)
        save_path = os.path.normpath(save_path)
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        save_file = os.path.join(save_path,  str(bb_index) + Constants.PNG_EXTENSION)
        with open(save_file, "wb") as outfile:
            outfile.write(out_figure.getbuffer())
        
    return detection_text_list, data, save_path


