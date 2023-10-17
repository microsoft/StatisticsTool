#region - inports
from threading import Lock
import traceback
import os, sys
from classes_and_utils.experiments.ExperminetsManager import ExperimentsManager

from flask_GUI.flask_server import server, experiments_manager

from classes_and_utils.experiments.ExperimentsHelper import ExperimentsHelper
from flask_GUI.dash_apps.results_table import Results_table
from app_config.constants import Constants, Tags, URLs
from urllib.parse import quote

#from flask_GUI.configuration_results import ConfigurationResults
# the absolute path for this file
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(current_file_directory, '..'), '..'))

from classes_and_utils.TemplatesFilesHelper import *
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory
#endregion

class ReportViewer_Routes:
    URL = '/viewer/Report_Viewer'
    MISSING_FILES_ALERT = 'missing_files_alert.html'
    ERROR_PAGE = 'error_page.html'
    GET_SEGMENTATIONS = '/viewer/get_segmentations'
    GET_REPORT_TABLE = '/viewer/get_report_table'
    GET_ALL_TEMPLATES = '/viewer/get_all_templates'
    SAVE_TEMPLATE = '/viewer/save_template'

class ReportViewer_Tags:
    REPORT_FILE_PATH = 'report_file_path'
    MAIN_PATH = 'main_path'
    REF_PATH = 'ref_path'
    NAME = 'name'
    VALUES = 'values'
    CALC_UNIQUE = 'calc_unique'
    NAME = 'name'
    CONTENT = 'content'

server.secret_key = 'any random string'

@server.route(ReportViewer_Routes.URL, methods=['GET', 'POST'])
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
            location = "{}?{}={}".format(URLs.INDEX_HTML,Tags.REPORTS,{quote(js_pairs)})
            #location = f'/static/index.html?reports={quote(js_pairs)}'
            return render_template(ReportViewer_Routes.MISSING_FILES_ALERT, 
                                   location=location, 
                                   missing_files_from_main = missing_files_from_main, 
                                   missing_files_from_ref = missing_files_from_ref)
        url = "{}?{}={}".format(URLs.INDEX_HTML,Tags.REPORTS,js_pairs)
        #return redirect(f'/static/index.html?reports={js_pairs}')
        return redirect(url)
    
    except Exception as ex:
        print (f"error: {ex}. Traceback: ")
        for a in traceback.format_tb(ex.__traceback__): print(a)
        print (f"exception message: {ex}.")
        error_message = f"We encountered an error while attempting to load the report for the request {request.values}."
        return render_template(ReportViewer_Routes.ERROR_PAGE, error_message=error_message)


@server.route(ReportViewer_Routes.GET_SEGMENTATIONS, methods=['POST'])    
def get_segmentations():
    main_path = request.json[ReportViewer_Tags.MAIN_PATH]
    
    segmentations = experiments_manager.get_item_segmentations(main_path)
    
    result = []
    for k, v in segmentations.items():
        result.append({ReportViewer_Tags.NAME:k,ReportViewer_Tags.VALUES:v})
    return jsonify(result)

'''
    returns the report table that generated by Dash
'''
table_lock = Lock()
@server.route(ReportViewer_Routes.GET_REPORT_TABLE, methods=['GET', 'POST'])
def get_report_table():
    
    main_path = request.args.get(ReportViewer_Tags.MAIN_PATH)
    ref_path = request.args.get(ReportViewer_Tags.REF_PATH)

    if experiments_manager.get_or_load_experiment(main_path) == None:
        return None

    main = experiments_manager.get_or_load_experiment(main_path)
    ref = experiments_manager.get_or_load_experiment(ref_path) if ref_path != '' else None

    calc_unique = True if ref and request.args.get(ReportViewer_Routes.CALC_UNIQUE) == 'true' else False
    
    
    res_table = experiments_manager.get_results_table(main_path,ref_path)
    
    if res_table == None:
        with table_lock:
            res_table = experiments_manager.get_results_table(main_path,ref_path)
            if res_table == None:
                segmentations = experiments_manager.get_item_segmentations(main_path)
                statistics_func, association_func = ExperimentsManager.get_experiment_udf(main_path)
                res_table = Results_table(server, main,ref, main_path, ref_path, segmentations, statistics_func, association_func)
                experiments_manager.add_results_table(main_path,ref_path,res_table)
    
    res_table.set_unique(calc_unique)
    
    wp = res_table.get_webpage()
    return wp

@server.route(ReportViewer_Routes.GET_ALL_TEMPLATES, methods=['POST'])
def get_all_templates():
    main = request.json[ReportViewer_Tags.MAIN_PATH]
    ref = request.json[ReportViewer_Tags.REF_PATH]
   
    helper = TemplatesFilesHelper()
    content = helper.get_all_templates_content(main,ref)
    return jsonify(content)

@server.route(ReportViewer_Routes.SAVE_TEMPLATE,methods=['POST'])
def save_template():
    data = request.json
    name = data[ReportViewer_Tags.NAME]
    content = data[ReportViewer_Tags.CONTENT]
    main_path = data[ReportViewer_Tags.MAIN_PATH]
    ref_path = data[ReportViewer_Tags.REF_PATH]
    helper = TemplatesFilesHelper()
    if not name:
        return 
    helper.save_template(name,content,main_path)
    result = helper.get_all_templates_content(main_path, ref_path)
    return jsonify(result)
 