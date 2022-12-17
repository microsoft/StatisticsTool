import os, sys
# the absolute path for this file
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(current_file_directory, '..'), '..'))

# from pyfladesk import init_gui
from classes_and_utils.GUI_utils import *
from flask import Flask, render_template, request

### init Flask server ###
#########################
app = Flask(__name__)

# getting the options for each type of necessary function
file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs = options_for_funcs()

#### Route for homepage ####
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('start_page.html')

@app.route('/create_new_report', methods=['GET', 'POST'])
def new_report_func():
    possible_configs = manage_new_report_page(request, current_file_directory)
    return render_template('new_report.html', possible_configs=possible_configs)


@app.route('/calculating_page', methods=['GET', 'POST'])
def calculating():
    # extract the user specified directories and names
    config_file_name, prd_dir, GT_dir, output_dir, single_video_hash_saving_dir, save_stats_dir, images_dir, config_dict = unpack_calc_request(request, current_file_directory)
    # making sure save_stats_dir is empty and opening the appropriate folders
    empty = folder_func(output_dir)
    if empty == 'FileNotFound':
        return render_template('Not_found.html')
    # if the output folder is not empty a message is sent
    elif not empty:
        return render_template('Not_empty.html')
    global exp
    # calculate the intermediate results for all the videos then combine them
    exp = manage_video_analysis(config_file_name, prd_dir, GT_dir, single_video_hash_saving_dir, save_stats_dir, images_dir, config_dict)
    if exp == 'TypeError':
        return render_template('Bad_format.html')
    return render_template('message.html')

@app.route('/add_config', methods=['GET', 'POST'])
def new_task_func():
    return render_template('new_task_config.html', file_reading_funcs=file_reading_funcs, Evaluation_funcs=Evaluation_funcs, overlap_funcs=overlap_funcs, partition_funcs=partition_funcs, statistics_funcs=statistics_funcs,transformation_funcs=transformation_funcs)

@app.route('/Reporter', methods=['GET', 'POST'])
def Report():
    # request to load a report
    if request.files:
        pckl_file = request.files['myFile']
        path_to_save = current_file_directory.replace('flask_GUI.py', 'static')
        path_to_save = os.path.join(path_to_save, 'reports')
        path_to_save = os.path.join(path_to_save, pckl_file.filename)
        # save the pickle file of the report (the instance of the ParallelExperiment class as a pickle file)
        if not os.path.exists(os.path.dirname(path_to_save)):
            os.makedirs(os.path.dirname(path_to_save))
        if os.path.exists(path_to_save):
            os.remove(path_to_save)
        pckl_file.save(path_to_save)
        global exp
        exp = load_object(path_to_save)
        exp.main_ref_dict=None
        exp.ref_main_dict=None
    global comp_exp
    comp_exp = []
    if 'myFile2' in request.files and request.files['myFile2'].filename:
        pckl_file = request.files['myFile2']
        path_to_save = current_file_directory.replace('flask_GUI.py', 'static')
        path_to_save = os.path.join(path_to_save, 'reports')
        path_to_save = os.path.join(path_to_save, "comp_"+pckl_file.filename)
        # save the pickle file of the report (the instance of the ParallelExperiment class as a pickle file)
        if not os.path.exists(os.path.dirname(path_to_save)):
            os.makedirs(os.path.dirname(path_to_save))
        if os.path.exists(path_to_save):
            os.remove(path_to_save)
        pckl_file.save(path_to_save)
        comp_exp.append(load_object(path_to_save))
        
    # make a list of optional partitions which their bolean masks are available
    list_of_seg_opt = ['N/A'] + [seg for seg in exp.masks.keys() if seg != 'total_stats']
    partitions_names = ['Primary', 'Secondary', 'Tertiary']
    return render_template('Reporter_page.html', opt=list_of_seg_opt, num_part=min(len(list_of_seg_opt)-1, 3), partitions_names=partitions_names, calc_unique_opt=len(comp_exp)>0)


@app.route('/stats', methods=['GET', 'POST'])
def show_stats():
    statistics_dict, wanted_seg, seg_num, wanted_statistics_names, columns, sub_rows, rows, primary, secondary, tertiary, save_path,_ = manage_stats_request(request, exp)
    cur_stats = None
    exp.unique = None
    unique_stats = None
    unique_stats_ref = None
    if len(comp_exp) > 0:
        
        cur_exp = comp_exp[0]
        cur_stats, _, _, _, _, _, _, _, _, _, _, calc_unique = manage_stats_request(request, cur_exp)
        if calc_unique and exp.main_ref_dict == None:
            exp.main_ref_dict, exp.ref_main_dict = match_main_ref_detections(exp, comp_exp[0])
        
        if exp.main_ref_dict != None and exp.ref_main_dict != None:
            keys = [x for x in statistics_dict.keys()]
            unique, unique_ref, unique_stats, unique_stats_ref =calc_unique_detections(keys, exp, cur_exp, exp.main_ref_dict, exp.ref_main_dict)
            exp.unique = unique
            cur_exp.unique = unique_ref
    return render_template('table.html', stats=statistics_dict, stats_ref=cur_stats, 
                    wanted_seg=wanted_seg, seg_num=seg_num, 
                    statistics_names=wanted_statistics_names, 
                    columns=columns, sub_rows=sub_rows, rows=rows, 
                    primary=primary, 
                    secondary=secondary, tertiary=tertiary,
                    unique_stats = unique_stats,
                    unique_stats_ref = unique_stats_ref, 
                    save_path=save_path)


@app.route('/update_list', methods=['GET', 'POST'])
def show_list():
    comp_index, unique, state, cl_and_choice, mytup, save_path, per_video_example_hash, saved_sheldon = manage_list_request(request, exp, comp_exp)
    return render_template('examples_list.html', state=state, cl_and_choice=cl_and_choice, mytup=mytup, save_path=save_path, per_video_example_hash=per_video_example_hash,saved_sheldon=saved_sheldon, comp_index=comp_index, unique = unique)

@app.route('/show_im', methods=['GET', 'POST'])
def show_image():
    data, save_path = manage_image_request(request, exp, comp_exp)
    return render_template('example_image.html', data=data, save_path=save_path)

@app.route('/show', methods=['GET', 'POST'])
def show_config():
    config_name = request.args.get('Configuration')
    path_to_wanted_config = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI.py'), os.path.join('configs', config_name))
    config_file = loading_json(path_to_wanted_config)
    config_dict = config_file[0]
    return render_template('show_config.html', config_dict=config_dict, config_name=config_name)

@app.route('/Help', methods=['GET', 'POST'])
def show_help():
    return render_template('help.html')

if __name__=='__main__':
    # init_gui(app, width=1500, height=1000) ## Changed manually by Ben
    app.run()
    