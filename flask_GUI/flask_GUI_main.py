#region - inports
import mimetypes
import urllib.parse
import traceback
import os, sys
import re
from classes_and_utils.UpdateListManager import UpdateListManager
from classes_and_utils.configuration.ConfigurationHelper import ConfigurationHelper
from classes_and_utils.configuration.ConfigurationManager import ConfigurationManager
from flask_GUI.dash_apps.results_table import Results_table

#from flask_GUI.configuration_results import ConfigurationResults
# the absolute path for this file
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(current_file_directory, '..'), '..'))

from classes_and_utils.GUI_utils import *
from classes_and_utils.TemplatesFilesHelper import *
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory
#endregion

#region - init Flask server 
server = Flask(__name__)
server.secret_key = 'any random string'
configuration_manager = ConfigurationManager()

# getting the options for each type of necessary function
file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs = options_for_funcs()

#endregion - init Flask server

#region - Homepage Route
@server.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('start_page.html', exp_ext = EXPERIMENT_EXTENTION, wiki_page = WIKI_URL)
#endregion 

#region - Functions for REPORT CREATION

@server.route('/create_new_report', methods=['GET', 'POST'])
def new_report_func():
    possible_configs = manage_new_report_page(request)
    return render_template('new_report.html', possible_configs=possible_configs, wiki_page = WIKI_URL)

@server.route('/calculating_page', methods=['GET', 'POST'])
def calculating():
    # extract the user specified directories and names
    config_file_name, prd_dir, GT_dir, output_dir = unpack_calc_request(request)
    
    # making sure save_stats_dir is empty and opening the appropriate folders
    empty, save_stats_dir = folder_func(output_dir, os.path.basename(config_file_name))
    if empty == 'FileNotFound':
        return render_template('Not_found.html')
    # if the output folder is not empty a message is sent
    elif not empty:
        return render_template('Not_empty.html')
    
    # calculate the intermediate results for all the videos then combine them
    exp, results_text, report_file_name = manage_video_analysis(config_file_name, prd_dir, save_stats_dir, gt_dir=GT_dir)
   
    configuration_manager.add_experiment(report_file_name,exp)

    if exp == 'TypeError' or exp is None or report_file_name is None:
        link = 'None'
    else:
        link = "/Report_Viewer?use_cached_report=true&main=" +  urllib.parse.quote(report_file_name)

    results_text = results_text.split('\n')
    return render_template('message.html', link=link, text=results_text)

@server.route('/add_config', methods=['GET', 'POST'])
def new_task_func():
    return render_template('new_task_config.html', file_reading_funcs=file_reading_funcs, Evaluation_funcs=Evaluation_funcs, overlap_funcs=overlap_funcs, partition_funcs=partition_funcs, statistics_funcs=statistics_funcs,transformation_funcs=transformation_funcs)

@server.route('/Help', methods=['GET', 'POST'])
def show_help():
    return render_template('help.html')

@server.route('/show', methods=['GET', 'POST'])
def show_config():
    config_name = request.args.get('Configuration')
    path_to_wanted_config = os.path.join(get_configs_folder(), config_name)
    config_file = loading_json(path_to_wanted_config)
    config_dict = config_file[0]
    return render_template('show_config.html', config_dict=config_dict, config_name=config_name)
#endregion - Functions for REPORT CREATION

#region - Functions for REPORT VIEW
@server.route('/Report_Viewer', methods=['GET', 'POST'])
def Report_Viewer():

    try:
        main, ref = ConfigurationHelper.get_request_experiments_info(request)
        
        main_added_experiments = configuration_manager.add(main)
        ref_added_experiments  = configuration_manager.add(ref)
        js_pairs = ConfigurationHelper.build_main_ref_pairs(main_added_experiments,ref_added_experiments)
        return redirect(f'static/index.html?reports={js_pairs}')
    
    except Exception as ex:
        print (f"error: {ex}. Traceback: ")
        for a in traceback.format_tb(ex.__traceback__): print(a)
        print (f"exception message: {ex}.")

        return f'Failed to load report for request {request.values}'

@server.route('/static/<file_name>')
def send_static_file(file_name):
    mime = mimetypes.guess_type(file_name, strict=False)[0]
    sp= os.path.splitext(file_name)
    if len(sp)>1 and sp[1]=='.js':
        mime = 'text/javascript'
    return send_from_directory('static', file_name,mimetype=mime)

@server.route('/favicon.ico')
def favicon():
    return send_from_directory('static','favicon.ico',mimetype='image/x-icon')
   
@server.route('/get_segmentations', methods=['POST'])    
def get_segmentations():
    main_path = request.json['main_path']
    
    segmentations = configuration_manager.get_item_segmentations(main_path)
    
    result = []
    for k, v in segmentations.items():
        result.append({'name':k,'values':v})
    return jsonify(result)

'''
    returns the report table that generated by Dash
'''
@server.route('/get_report_table', methods=['GET', 'POST'])
def get_report_table():
    
    main_path = request.args.get('main_path')
    ref_path = request.args.get('ref_path')

    if configuration_manager.get_experiment(main_path) == None:
        return None

    main = configuration_manager.get_experiment(main_path)
    ref = configuration_manager.get_experiment(ref_path) if ref_path != '' else None

    calc_unique = True if ref and request.args.get('calc_unique') == 'true' else False
    

    columns = ConfigurationHelper.parse_segmentations_csv(request.args.get('cols'))
    rows    = ConfigurationHelper.parse_segmentations_csv(request.args.get('rows'))
    
    res_table = configuration_manager.get_results_table(main_path,ref_path)
    if res_table == None:
        res_table = Results_table(server)
        segmentations = configuration_manager.get_item_segmentations(main_path)
        res_table.set_data(main,ref, main_path, ref_path, segmentations,calc_unique)
        res_table = configuration_manager.add_results_table(main_path,ref_path,res_table)
    else:
        if ref is not None:
            res_table.set_unique(calc_unique)

    wp = res_table.get_webpage(columns,rows)

    return wp

@server.route('/get_all_templates', methods=['POST'])
def get_all_templates():
    main = request.json['main_path']
    ref = request.json['ref_path']
    main_dir,_ = os.path.split(main)
    ref_dir,_ = os.path.split(ref)
    
    helper = TemplatesFilesHelper()
    content = helper.get_all_templates_content(main_dir,ref_dir)
    return jsonify(content)

@server.route('/get_template_content', methods=['POST'])
def get_template_content():
    file_name = request.args.get('file_name')
    helper = TemplatesFilesHelper()
    content = helper.get_template_content(file_name)
    return jsonify(content)

@server.route('/save_template',methods=['POST'])
def save_template():
    data = request.json
    name = data['name']
    content = data['content']
    main_path = data['main_path']
    ref_path = data['ref_path']
    helper = TemplatesFilesHelper()
    if not name:
        return 
    result = helper.save_template(name,content,main_path,ref_path)
    return jsonify(result)
    
#########################################################

@server.route('/update_list', methods=['GET', 'POST'])
def show_list():
    main_path = request.args.get('main_path')
    ref_path  = request.args.get('ref_path')
    list_ref_report  = 'ref' in request.args
    cell_name = request.args.get('cell_name') if "cell_name" in request.args else None
    stat = request.args.get('stat') if "stat" in request.args else None  #This is a string contain 'TP' / 'FP' / 'FN
    show_unique = 'unique' in request.args

    results_table = configuration_manager.get_results_table(main_path, ref_path)
    per_video_example_hash, saved_file = UpdateListManager.manage_list_request(results_table, main_path, cell_name, stat, show_unique, list_ref_report, 'sheldon' in request.args)

    unique_flag = '' if show_unique is False else 'unique'
    return render_template('examples_list.html', 
                            state=stat, 
                            cell_name=cell_name,
                            per_video_example_hash = per_video_example_hash,
                            saved_sheldon = saved_file,
                            comp_index = 0 if ref_path else -1,
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

    main_exp = configuration_manager.get_experiment(main_path)
    ref_exp = configuration_manager.get_experiment(ref_path)

    main_dir,_ = os.path.split(main_path)
    
    detection_text_list, data, save_path = manage_image_request(request,main_exp, ref_exp,main_dir, comp_index>-1, local_path, example_name)
    
    example_name = example_name.replace('\\','/')
    return render_template('example_image.html', data=data, save_path=save_path, detection_text_list=detection_text_list, example_name = example_name, main_path=main_path, ref_path=ref_path, comp_index = comp_index)

#endregion - Functions for REPORT CREATION

#region - run server
if __name__=='__main__':
    server.debug = False
    server.run()
#endregion 
