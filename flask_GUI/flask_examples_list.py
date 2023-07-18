
import base64
import os
from classes_and_utils.UpdateListManager import UpdateListManager
from flask import render_template, request
from flask_GUI.flask_server import server, experiments_manager

from utils.image_util import draw_detection_on_figure, read_frame_from_video


@server.route('/example_list/update_list', methods=['GET', 'POST'])
def show_list():
    main_path = request.args.get('main_path')
    ref_path  = request.args.get('ref_path')
    list_ref_report  = 'ref' in request.args
    cell_name = request.args.get('cell_name') if "cell_name" in request.args else None
    stat = request.args.get('stat') if "stat" in request.args else None  #This is a string contain 'TP' / 'FP' / 'FN
    show_unique = 'unique' in request.args

    results_table = experiments_manager.get_results_table(main_path, ref_path)
    per_video_example_hash, saved_file = UpdateListManager.manage_list_request(results_table, main_path, cell_name, stat, show_unique, list_ref_report, 'save_json' in request.args)

    unique_flag = '' if show_unique is False else 'unique'
    return render_template('examples_list.html', 
                            state=stat, 
                            cell_name=cell_name,
                            per_video_example_hash = per_video_example_hash,
                            saved_json = saved_file,
                            comp_index = 0 if list_ref_report else -1,
                            unique = unique_flag,
                            main_path = main_path,
                            ref_path = ref_path
    )

@server.route('/show_im', methods=['GET', 'POST'])
def show_image():
    main_path = request.args.get('main_path')
    ref_path = request.args.get('ref_path')
    comp_index=eval(request.args.get('comp_index'))
    
    local_path = None    
    if request.args.get('local_path'):
        local_path = request.args.get('local_path')
    
    example_name = request.args.get('example_name')

    main_exp = experiments_manager.get_experiment(main_path)
    ref_exp = experiments_manager.get_experiment(ref_path)

    main_dir,_ = os.path.split(main_path)
    
    detection_text_list, data, save_path = manage_image_request(request,main_exp, ref_exp,main_dir, comp_index>-1, local_path, example_name)
    
    example_name = example_name.replace('\\','/')
    return render_template('example_image.html', data=data, save_path=save_path, detection_text_list=detection_text_list, example_name = example_name, main_path=main_path, ref_path=ref_path, comp_index = comp_index)


def manage_image_request(request, main_exp, ref_exp,main_directory, use_ref, local_path, example_name):
    """
    Accepts the requests to /show_im route and returns an encoded image and the path where the image was saved (if it was saved)

    :param request: request from either example_image (to save) or in examples_list.html
    :param exp: exp is an instance of ParallelExperiment
    :return: an encoded image and the path where the image was saved (if it was saved)
    """
    
    save_path = False
    data = None
    image = None
    # request came from examples_list.html to show an example image

    if example_name:
        example_id = eval(example_name.replace(" ", ","))
   
    video, bb_index,frame_id,_ = example_id
    if local_path:
        video = os.path.join(local_path,video)
    
    image = read_frame_from_video(video, frame_id)
    
    exp = main_exp
    if use_ref:
        exp = ref_exp
    
    pred_bbs, label_bbs, selected_pred_index, selected_label_index = exp.get_detection_bounding_boxes(bb_index)
    detection_text_list = exp.get_detection_properties_text_list(bb_index)
    out_figure = draw_detection_on_figure(image, pred_bbs, label_bbs=label_bbs, selected_pred=selected_pred_index, selected_label=selected_label_index)
    if out_figure is not None:
        data = base64.b64encode(out_figure.getbuffer()).decode("ascii")
    
    if out_figure and 'save_image' in request.args:
        name = example_id[0].replace('.json', '')
        name = name.replace(':','')
        if name.startswith('/'):
            name = name[1:]
        
        save_path = os.path.join(os.path.join(main_directory, 'saved images'), name)
        save_path = os.path.normpath(save_path)
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        save_file = os.path.join(save_path,  str(example_id[1]) + '.png')
        with open(save_file, "wb") as outfile:
            outfile.write(out_figure.getbuffer())
        
    return detection_text_list, data, save_path


