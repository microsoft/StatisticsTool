
import base64
import os
from app_config.constants import Constants
from experiment_engine.ParallelExperiment import ParallelExperiment
from experiment_engine.UpdateListManager import UpdateListManager
from flask import render_template, request, Markup
from flask_server.flask_server import server, experiments_manager

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
    SAVE_LIST = 'save_json'

@server.route(ExamplesList_Routes.UPDATE_LIST, methods=['GET', 'POST'])
def show_list():
    main_path = request.args.get(ExampleList_Tags.MAIN_PATH)
    ref_path  = request.args.get(ExampleList_Tags.REF_PATH)
    list_ref_report  = ExampleList_Tags.REF in request.args
    cell_name = request.args.get(ExampleList_Tags.CELL_NAME) if ExampleList_Tags.CELL_NAME in request.args else None
    stat = request.args.get(ExampleList_Tags.STAT) if ExampleList_Tags.STAT in request.args else None  #This is a string contain 'TP' / 'FP' / 'FN
    show_unique = ExampleList_Tags.UNIQUE in request.args

    results_table = experiments_manager.get_results_table(main_path, ref_path)
    list_html, saved_file = UpdateListManager.manage_list_request(results_table, main_path, ref_path, cell_name, stat, show_unique, list_ref_report, ExampleList_Tags.SAVE_LIST in request.args)

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
    
    main_exp = experiments_manager.get_or_load_experiment(main_path)
    ref_exp = experiments_manager.get_or_load_experiment(ref_path)

    main_dir,_ = os.path.split(main_path)
    
    detection_text_list, images_list, save_path = manage_image_request(request,main_exp, ref_exp,main_dir, comp_index>-1, local_path, example_index, video_name)

    return render_template(ExamplesList_Routes.EXAMPLE_IMAGE_HTML, 
                           images_list=images_list, 
                           save_path=save_path, 
                           detection_text_list=detection_text_list, 
                           video_name = video_name, 
                           images_num = len(images_list),
                           example_index = example_index, 
                           main_path=main_path, 
                           ref_path=ref_path, 
                           comp_index = comp_index)


def manage_image_request(request, main_exp:ParallelExperiment, ref_exp:ParallelExperiment,main_directory, use_ref, local_path, sample_index, video):
    """
    Accepts the requests to /show_im route and returns an encoded image and the path where the image was saved (if it was saved)

    :param request: request from either example_image (to save) or in examples_list.html
    :param exp: exp is an instance of ParallelExperiment
    :return: an encoded image and the path where the image was saved (if it was saved)
    """
    
    save_path = False
    image = None
    encoded_images = {}
    exp = main_exp
    if use_ref:
        exp = ref_exp
    
    try:
       images = exp.get_example_images_local_path(sample_index, local_path)
    except Exception as ex:
        print (f'failed to load image with exception: {ex}')
        
    
    detection_text_list = exp.get_sample_properties_text_list(sample_index)
    
    for image in images:
        encoded_images[image] = base64.b64encode(images[image].getbuffer()).decode("ascii")
        if  ExampleList_Tags.SAVE_IMAGE in request.args:
            name = video.replace(Constants.JSON_EXTENSION, '')
            name = name.replace(':','')
            if name.startswith('/'):
                name = name[1:]
            name += f'_{image}'
            save_path = os.path.join(os.path.join(main_directory, ExampleList_Tags.SAVED_IMAGES), name)
            save_path = os.path.normpath(save_path)
            if os.path.exists(save_path) == False:
                os.makedirs(save_path)
            save_file = os.path.join(save_path,  str(sample_index) + Constants.PNG_EXTENSION)
            with open(save_file, "wb") as outfile:
                outfile.write(images[image].getbuffer())
        
    return detection_text_list, encoded_images, save_path


