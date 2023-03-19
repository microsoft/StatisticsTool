import os, sys
from requests import Session
# the absolute path for this file
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(current_file_directory, '..'), '..'))
from dash.dependencies import Input, Output, State
from dash import Dash, html

# from pyfladesk import init_gui
from classes_and_utils.GUI_utils import *
from flask import Flask, jsonify, render_template, request,redirect, url_for,session
from flask_GUI.rendering_functions import show_stats_render
from flask_GUI.dash_apps.results_table import Results_table

### init Flask server ###
#########################
server = Flask(__name__)
server.secret_key = 'any random string'
results_table = Results_table(server)


# getting the options for each type of necessary function
file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs = options_for_funcs()


#### Route for homepage ####
@server.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('start_page.html')

#### The next functions are for *report creation* ==> ####
@server.route('/create_new_report', methods=['GET', 'POST'])
def new_report_func():
    possible_configs = manage_new_report_page(request, current_file_directory)
    return render_template('new_report.html', possible_configs=possible_configs)


@server.route('/calculating_page', methods=['GET', 'POST'])
def calculating():
    # extract the user specified directories and names
    config_file_name, prd_dir, GT_dir, output_dir, single_video_hash_saving_dir, save_stats_dir, config_dict = unpack_calc_request(request, current_file_directory)
    # making sure save_stats_dir is empty and opening the appropriate folders
    empty = folder_func(output_dir)
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
#### <<== The above functions are for *report creation* ####

#### The next functions are for *report view and analysis* ==> ####

@server.route('/Reporter_orig', methods=['GET', 'POST'])
def Report_orig():
    use_cached_report = request.args.get('use_cached_report')
    session['error_message'] = ''
    global report_type
    report_type = 'ORIG'
    return Report(use_cached_report)

@server.route('/Save_Report_Request', methods=['GET', 'POST'])
def Save_Report_Request():
    global report_type
    report_type = 'NEW'
    use_cached_report = request.args.get('use_cached_report')
    extract_data_request(request,use_cached_report)
    session['error_message'] = ''
    return render_template('index.html')

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

def Create_Report():
    global exp
    global comp_exp

    segmentations = {seg_category:v['possible partitions'] for seg_category, v in exp.masks.items() if seg_category != 'total_stats'}

    results_table.set_data({'main':exp, 'ref':comp_exp}, segmentations)
    return results_table.get_webpage()
    '''dashApp = Dash(__name__,server=server,url_base_pathname='/dash2/')# serve_locally = False)
    dashApp.layout = results_table.get_layout()
    @dashApp.callback(
        Output('table-div', 'children'),
        Input('cols_seg', 'value'),
        Input('rows_seg', 'value')
    )
    def update_output(cols_input ,rows_input):
        table_div = results_table.table.get_table(cols_input, rows_input)
        return table_div

    return dashApp.index()'''
@server.route('/get_segmentations', methods=['POST'])    
def get_segmentations():
    segmentations = {seg_category:v['possible partitions'] for seg_category, v in exp.masks.items() if seg_category != 'total_stats'}
    return jsonify(segmentations)

@server.route('/Reporter_new_wrapper', methods=['POST'])
def Reporter_new_wrapper():
    wp = Create_Report()
    return jsonify(wp), 201

@server.route('/Reporter_new', methods=['GET', 'POST'])
def Create_Report():
    global exp
    global comp_exp

    segmentations = {seg_category:v['possible partitions'] 
    for seg_category, v in exp.masks.items() if seg_category != 'total_stats'}

    results_table.set_data({'main':exp, 'ref':comp_exp}, segmentations)
    wp = results_table.get_webpage()
    return wp

@server.route('/Reporter_new_old', methods=['GET', 'POST'])
def Report_new():
    use_cached_report = request.args.get('use_cached_report')
    session['error_message'] = ''
    global report_type
    report_type = 'NEW'
    return Report(use_cached_report)

def Report(use_cached_report):
    # request to load a report
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

    # make a list of optional partitions which their bolean masks are available
    # list_of_seg_opt = ['N/A'] + [seg for seg in exp.masks.keys() if seg != 'total_stats']
    # partitions_names = ['Primary', 'Secondary', 'Tertiary']
    # return render_template('Reporter_page.html', opt=list_of_seg_opt, num_part=min(len(list_of_seg_opt)-1, 3), partitions_names=partitions_names, calc_unique_opt=len(comp_exp)>0)
    if report_type == 'NEW':
        segmentations = {seg_category:v['possible partitions'] 
        for seg_category, v in exp.masks.items() if seg_category != 'total_stats'}

        results_table.set_data({'main':exp, 'ref':comp_exp}, segmentations)
        return results_table.get_webpage()
    elif report_type == 'ORIG':
        # This is the deprecated reporter (before moving to Dash)
            # make a list of optional partitions which their bolean masks are available
        list_of_seg_opt = ['N/A'] + [seg for seg in exp.masks.keys() if seg != 'total_stats']
        partitions_names = ['Primary', 'Secondary', 'Tertiary']

    return render_template('Reporter_page.html', opt=list_of_seg_opt, num_part=min(len(list_of_seg_opt)-1, 3), partitions_names=partitions_names, calc_unique_opt=len(comp_exp)>0) #### TODO: check after merge



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
            ret_exp.main_ref_dict=None
            ret_exp.ref_main_dict=None
            return ret_exp,True,''
        else:
            #to do - if file not exist
            #return render_template("start_page.html")
            return None,False,"FILE " + report_filename.split(os.sep)[-1] + " NOT FOUND"
            

    if request.files and request.files[key_choose_file].filename != '':
        pckl_file = request.files[key_choose_file]
        
        report_filename = save_pkl_file(pckl_file,False)
        ret_exp = load_object(report_filename)
        ret_exp.main_ref_dict=None
        ret_exp.ref_main_dict=None
        return ret_exp,True,''
    
    return ret_exp, True, ''
#########################################################
#hagai-callback

@results_table.dash_app.callback(
    Output('table-div', 'children'),
    Input('cols_seg', 'value'),
    Input('rows_seg', 'value'))
def update_results_table(cols_input ,rows_input):
    table_div = results_table.table.get_table(cols_input, rows_input)

    return table_div


@server.route('/stats_pivot', methods=['GET', 'POST'])
def statistics_reporter_dash():
    return results_table.get_webpage()

@server.route('/stats_original', methods=['GET', 'POST'])
def show_stats():
    return show_stats_render(request, exp, comp_exp)			

#########################################################
@server.route('/update_list', methods=['GET', 'POST'])
def show_list():
    comp_index, unique, state, cl_and_choice, mytup, save_path, per_video_example_hash, saved_sheldon = manage_list_request(request, exp, comp_exp, report_type)
    return render_template('examples_list.html', state=state, cl_and_choice=cl_and_choice, mytup=mytup, save_path=save_path, per_video_example_hash=per_video_example_hash,saved_sheldon=saved_sheldon, comp_index=comp_index, unique = unique)

@server.route('/show_im', methods=['GET', 'POST'])
def show_image():
    data, save_path = manage_image_request(request, exp, comp_exp)
    return render_template('example_image.html', data=data, save_path=save_path)

@server.route('/show', methods=['GET', 'POST'])
def show_config():
    config_name = request.args.get('Configuration')
    path_to_wanted_config = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI_main.py'), os.path.join('configs', config_name))
    config_file = loading_json(path_to_wanted_config)
    config_dict = config_file[0]
    return render_template('show_config.html', config_dict=config_dict, config_name=config_name)


if __name__=='__main__':
    server.debug = False
    server.run()
    