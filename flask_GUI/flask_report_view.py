#region - inports
from threading import Lock
import traceback
import os, sys
from classes_and_utils.experiments.ExperminetsManager import ExperimentsManager

from flask_GUI.flask_server import server, experiments_manager

from classes_and_utils.UserDefinedFunctionsHelper import options_for_funcs
from classes_and_utils.experiments.ExperimentsHelper import ExperimentsHelper
from flask_GUI.dash_apps.results_table import Results_table
from app_config.constants import Constants, UserDefinedConstants
from urllib.parse import quote

#from flask_GUI.configuration_results import ConfigurationResults
# the absolute path for this file
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(current_file_directory, '..'), '..'))

from classes_and_utils.TemplatesFilesHelper import *
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory
#endregion

server.secret_key = 'any random string'

@server.route('/viewer/Report_Viewer', methods=['GET', 'POST'])
def Report_Viewer():

    try:
        #load_all_user_defined_functions()
        main = request.values and request.values[Constants.MAIN_REPORT_FILE_PATH]

        ref = None
        if Constants.REF_REPORT_FILE_PATH in request.values.keys():
            ref = request.values and request.values[Constants.REF_REPORT_FILE_PATH]            

        main_added_experiments, ref_added_experiments  = experiments_manager.add_experiments_folders(main, ref)
        js_pairs,  missing_files_from_main, missing_files_from_ref = ExperimentsHelper.build_main_ref_pairs(main_added_experiments,ref_added_experiments)
        if ref and (len(missing_files_from_main) > 0 or len(missing_files_from_ref) > 0):      
            location = f'/static/index.html?reports={quote(js_pairs)}'
            return render_template('missing_files_alert.html', 
                                   location=location, 
                                   missing_files_from_main = missing_files_from_main, 
                                   missing_files_from_ref = missing_files_from_ref)
        return redirect(f'/static/index.html?reports={js_pairs}')
    
    except Exception as ex:
        print (f"error: {ex}. Traceback: ")
        for a in traceback.format_tb(ex.__traceback__): print(a)
        print (f"exception message: {ex}.")
        error_message = f"We encountered an error while attempting to load the report for the request {request.values}."
        return render_template('error_page.html', error_message=error_message)


@server.route('/viewer/get_segmentations', methods=['POST'])    
def get_segmentations():
    main_path = request.json['main_path']
    
    segmentations = experiments_manager.get_item_segmentations(main_path)
    
    result = []
    for k, v in segmentations.items():
        result.append({'name':k,'values':v})
    return jsonify(result)

'''
    returns the report table that generated by Dash
'''
table_lock = Lock()
@server.route('/viewer/get_report_table', methods=['GET', 'POST'])
def get_report_table():
    
    main_path = request.args.get('main_path')
    ref_path = request.args.get('ref_path')

    if experiments_manager.get_experiment(main_path) == None:
        return None

    main = experiments_manager.get_experiment(main_path)
    ref = experiments_manager.get_experiment(ref_path) if ref_path != '' else None

    calc_unique = True if ref and request.args.get('calc_unique') == 'true' else False
    
    
    res_table = experiments_manager.get_results_table(main_path,ref_path)
    
    if res_table == None:
        with table_lock:
            res_table = experiments_manager.get_results_table(main_path,ref_path)
            if res_table == None:
                segmentations = experiments_manager.get_item_segmentations(main_path)
                statistics_func, evaluation_func, overlap_func = ExperimentsManager.get_experiment_udf(main_path)
                res_table = Results_table(server, main,ref, main_path, ref_path, segmentations, statistics_func, evaluation_func, overlap_func)
                experiments_manager.add_results_table(main_path,ref_path,res_table)
    
    res_table.set_unique(calc_unique)
    
    wp = res_table.get_webpage()
    return wp

@server.route('/viewer/get_all_templates', methods=['POST'])
def get_all_templates():
    main = request.json['main_path']
    ref = request.json['ref_path']
   
    helper = TemplatesFilesHelper()
    content = helper.get_all_templates_content(main,ref)
    return jsonify(content)

@server.route('/viewer/save_template',methods=['POST'])
def save_template():
    data = request.json
    name = data['name']
    content = data['content']
    main_path = data['main_path']
    ref_path = data['ref_path']
    helper = TemplatesFilesHelper()
    if not name:
        return 
    helper.save_template(name,content,main_path)
    result = helper.get_all_templates_content(main_path, ref_path)
    return jsonify(result)
 