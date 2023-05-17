import mimetypes
import os, sys
from requests import Session

from flask_GUI.configuration_results import ConfigurationResults
# the absolute path for this file
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(current_file_directory, '..'), '..'))
from dash.dependencies import Input, Output, State
from dash import Dash, html

# from pyfladesk import init_gui
from classes_and_utils.GUI_utils import *
from classes_and_utils.TemplatesFilesHelper import *
from flask import Flask, jsonify, render_template, request,redirect, url_for,session, send_from_directory
from flask_GUI.rendering_functions import show_stats_render
from flask_GUI.dash_apps.results_table import Results_table


### init Flask server ###
#########################
server = Flask(__name__)
server.secret_key = 'any random string'
results_table = Results_table(server)
configuration_results = ConfigurationResults()

# getting the options for each type of necessary function
file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs = options_for_funcs()

#### Route for homepage ####
@server.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('start_page.html')

#region - Functions for REPORT CREATION

@server.route('/create_new_report', methods=['GET', 'POST'])
def new_report_func():
    possible_configs = manage_new_report_page(request, current_file_directory)
    return render_template('new_report.html', possible_configs=possible_configs)

@server.route('/calculating_page', methods=['GET', 'POST'])
def calculating():
    # extract the user specified directories and names
    config_file_name, prd_dir, GT_dir, output_dir, single_video_hash_saving_dir, config_dict = unpack_calc_request(request, current_file_directory)
    # making sure save_stats_dir is empty and opening the appropriate folders
    empty, save_stats_dir = folder_func(output_dir)
    if empty == 'FileNotFound':
        return render_template('Not_found.html')
    # if the output folder is not empty a message is sent
    elif not empty:
        return render_template('Not_empty.html')
    global exp
    # calculate the intermediate results for all the videos then combine them
    exp = manage_video_analysis(config_file_name, prd_dir, single_video_hash_saving_dir, save_stats_dir, config_dict, gt_dir=GT_dir)
    if exp is None:
        return "No logs to compare"
    if exp == 'TypeError':
        return render_template('Bad_format.html')
    return render_template('message.html')

@server.route('/add_config', methods=['GET', 'POST'])
def new_task_func():
    return render_template('new_task_config.html', file_reading_funcs=file_reading_funcs, Evaluation_funcs=Evaluation_funcs, overlap_funcs=overlap_funcs, partition_funcs=partition_funcs, statistics_funcs=statistics_funcs,transformation_funcs=transformation_funcs)

@server.route('/Help', methods=['GET', 'POST'])
def show_help():
    return render_template('help.html')

@server.route('/show', methods=['GET', 'POST'])
def show_config():
    config_name = request.args.get('Configuration')
    path_to_wanted_config = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI_main.py'), os.path.join('configs', config_name))
    config_file = loading_json(path_to_wanted_config)
    config_dict = config_file[0]
    return render_template('show_config.html', config_dict=config_dict, config_name=config_name)
#endregion - Functions for REPORT CREATION

#region - Functions for REPORT VIEW
@server.route('/Report_Viewer', methods=['GET', 'POST'])
def Report_Viewer():

    key = configuration_results.save_configuration(request,server)

    #use_cached_report = request.args.get('use_cached_report')
    #extract_data_request(request,use_cached_report)
    #session['error_message'] = ''

    return render_template('index.html',key=key)

def extract_data_request(request,use_cached_report):
    global exp
    global comp_exp

    comp_exp = []
    if not use_cached_report:
        exp,result,err_msg = load_experiment(request,False)

        if exp == None and result == False and err_msg != '':
            #return render_template("start_page.html",message=err_msg)
            session['error_message'] = err_msg
            return redirect(url_for("homepage"))
        cexp,_,_ = load_experiment(request,True)
        if cexp != None:
            comp_exp.append(cexp)

@server.route('/static/<file_name>')
def send_file(file_name):
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
    key = request.json['key']
    segmentations = configuration_results.get_item_segmentations(key)
    #segmentations = {seg_category:v['possible partitions'] for seg_category, v in exp.masks.items() if seg_category != 'total_stats'}

    result = []
    for k, v in segmentations.items():
        result.append({'name':k,'values':v})
    return jsonify(result)

'''
    returns the report table that generated by Dash
'''
@server.route('/get_report_table', methods=['GET', 'POST'])
def get_report_table():
    global exp
    global comp_exp

    calc_unique = True if request.args.get('calc_unique') == 'true' else False
    config_key = request.args.get('key')
    config_item = configuration_results.get_config_item(config_key)
    if config_item is None:
        return None
    
    columns = [] 
    rows = [] 
    argCols = request.args.get('cols')
    argRows = request.args.get('rows')
    if argCols != None and len(argCols) > 0:
        if argCols[-1] == ',':
            argCols = argCols[:-1]
        columns  = list(argCols.split(',') )
       
    if argRows != None and len(argRows) > 0:
        if argRows[-1] == ',':
            argRows = argRows[:-1]
        rows = list(argRows.split(','))
    #segmentations = {seg_category:v['possible partitions'] for seg_category, v in exp.masks.items() if seg_category != 'total_stats'}
    segmentations = configuration_results.get_item_segmentations(config_key)
    config_item.table_result.set_data(config_item, segmentations,calc_unique)
    config_item.table_result.dash_app.layout = config_item.table_result.get_layout_new(columns,rows)
    wp = config_item.table_result.get_webpage()

    return wp

@server.route('/get_all_templates', methods=['POST'])
def get_all_templates():
    helper = TemplatesFilesHelper()
    content = helper.get_all_templates_content()
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
    helper = TemplatesFilesHelper()
    result = helper.save_template(name,content)
    return jsonify(result)
    
def save_pkl_file(pckl_file,is_reference):
        path_to_save = os.path.join(current_file_directory.replace('flask_GUI_main.py', 'static'),
                                    'reports',
                                    ("comp_" + pckl_file.filename) if is_reference else pckl_file.filename)
        # save the pickle file of the report (the instance of the ParallelExperiment class as a pickle file)
        if not os.path.exists(os.path.dirname(path_to_save)):
            os.makedirs(os.path.dirname(path_to_save))
        if os.path.exists(path_to_save):
            os.remove(path_to_save)
        pckl_file.save(path_to_save)
        return path_to_save

def load_experiment(request,is_reference):
    
    key_file_path = 'reference_file_path' if is_reference else 'report_file_path'
    key_choose_file = 'choose_reference_file' if is_reference else 'choose_report_file'
    ret_exp = None
    
    if key_file_path in request.values and request.values[key_file_path] != '':
        #check if file exist
        report_filename = request.values[key_file_path]
        if os.path.exists(report_filename):
            ret_exp = load_object(report_filename)

            return ret_exp,True,''
        else:
            #to do - if file not exist
            #return render_template("start_page.html")
            return None,False,"FILE " + report_filename.split(os.sep)[-1] + " NOT FOUND"
            

    if request.files and request.files[key_choose_file].filename != '':
        pckl_file = request.files[key_choose_file]
        
        report_filename = save_pkl_file(pckl_file,False)
        ret_exp = load_object(report_filename)

        return ret_exp,True,''
    
    return ret_exp, True, ''


#########################################################
#hagai-callback

@results_table.dash_app.callback(
    Output('table-div', 'children'),
    Input('cols_seg', 'value'),
    Input('rows_seg', 'value'))
def update_results_table(cols_input ,rows_input):
    table_div = results_table.table.get_report_table(cols_input, rows_input)

    return table_div


@server.route('/stats_pivot', methods=['GET', 'POST'])
def statistics_reporter_dash():
    return results_table.get_webpage()

@server.route('/stats_original', methods=['GET', 'POST'])
def show_stats():
    return show_stats_render(request, exp, comp_exp)			

#########################################################

global LM
LM = None
def get_list_manager():
    global LM
    if LM == None:
        LM = UpdateListManager()
    return LM

@server.route('/update_list', methods=['GET', 'POST'])
def show_list():
    listManager = get_list_manager()
    config_key = request.args.get('key')
    config_item = configuration_results.get_config_item(config_key)
    if config_item is None:
        return

    # global comp_index, unique, state, cell_name, save_path, per_video_example_hash
    listManager.manage_list_request(request, config_item.main_pkl, config_item.ref_pkl)

    return render_template('examples_list.html', 
                            state=listManager.state, 
                            cell_name=listManager.cell_name,
                            save_path=listManager.saved_list,
                            per_video_example_hash=listManager.per_video_example_hash,
                            saved_sheldon=listManager.saved_sheldon,
                            comp_index=listManager.comp_index,
                            unique = listManager.show_unique)

    # return render_template('examples_list.html', state=state, cl_and_choice=cl_and_choice, mytup=mytup, save_path=save_path, per_video_example_hash=per_video_example_hash,saved_sheldon=saved_sheldon, comp_index=comp_index, unique = unique)

@server.route('/is_file_exists',methods=['GET', 'POST'])
def is_file_exists():
    file_path = request.json['file_path']
    if True: #os.path.exists(file_path):
        return {
            'exists': True
        }
    else:
        return {
            'exists': False
        }

@server.route('/show_im', methods=['GET', 'POST'])
def show_image():
    config_key = request.args.get('key')
    config_item = configuration_results.get_config_item(config_key)
    if config_item is None:
        return None

    data, save_path = manage_image_request(request, config_item.main_pkl, config_item.ref_pkl)
    return render_template('example_image.html', data=data, save_path=save_path)

#endregion - Functions for REPORT CREATION

if __name__=='__main__':
    server.debug = False
    server.run()
