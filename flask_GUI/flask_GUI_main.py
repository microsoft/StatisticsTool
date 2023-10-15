
import argparse
import mimetypes

import sys, os
current_file_directory = os.path.realpath(__file__)
sys.path.append(os.path.join(os.path.join(current_file_directory, '..'), '..'))

from flask_GUI.flask_server import server

from flask_GUI.flask_report_view import *
from flask_GUI.flask_create_report import *
from flask_GUI.flask_examples_list import *
from app_config.config import AppConfig


from flask import render_template, send_from_directory

class GuiMain_Routes:
    START_PAGE_URL = '/'
    START_PAGE_HTML = 'start_page.html'
    VALIDATE_PATH = '/validate_path'
    FAV_ICON = '/favicon.ico'
    

class GuiMain_Tags:
    PATH = 'path'
    IS_VALID_DIRECTORY = 'isValidDirectory'
    STATIC = 'static'
    FAV_ICON_ICO = 'favicon.ico'
    MIME_TYPE = 'image/x-icon'
    AZURE_STORAGE_ID = '--azure_storage_id'
    DATA_CONTAINER_NAME = '--data_container_name'
    ANNOTATION_STORE_BLOBS_PREFIX = '--annotation_store_blobs_prefix'
    DATA_STORE_BLOBS_PREFIX = '--data_store_blobs_prefix'
    PREDICTIONS_BLOBS_PREFIX = '--predictions_blobs_prefix'
    EXTERNAL_LIB_PATH = '--external_lib_path'
    CONFIG_FILE_PATH = '--config_file_path'

@server.route(GuiMain_Routes.START_PAGE_URL, methods=['GET', 'POST'])
def homepage():
    return render_template (GuiMain_Routes.START_PAGE_HTML, exp_ext = Constants.EXPERIMENT_EXTENSION, wiki_page = Constants.WIKI_URL)

@server.route(GuiMain_Routes.VALIDATE_PATH, methods=["POST"])
def validate_path():
    data = request.get_json()
    path = data.get(GuiMain_Tags.PATH)

    # Perform validation here (e.g., check if the path is a directory)
    is_directory = os.path.isdir(path)

    # Return the result as JSON
    return jsonify({GuiMain_Tags.IS_VALID_DIRECTORY: is_directory})

@server.route('/static/<file_name>')
def send_static_file(file_name):
    mime = mimetypes.guess_type(file_name, strict=False)[0]
    sp= os.path.splitext(file_name)
    if len(sp)>1 and sp[1]=='.js':
        mime = 'text/javascript'
    return send_from_directory('static', file_name,mimetype=mime)


@server.route(GuiMain_Routes.FAV_ICON)
def favicon():
    return send_from_directory(GuiMain_Tags.STATIC,GuiMain_Tags.FAV_ICON_ICO,mimetype=GuiMain_Tags.MIME_TYPE)
   

def process_command_line_args():
    parser = argparse.ArgumentParser(description='StatisticsTool')
    parser.add_argument(GuiMain_Tags.AZURE_STORAGE_ID, help="azure storage id to access data container")
    parser.add_argument(GuiMain_Tags.DATA_CONTAINER_NAME, help="name of data container")
    parser.add_argument(GuiMain_Tags.ANNOTATION_STORE_BLOBS_PREFIX, help="prefix in data container for the annotations files")
    parser.add_argument(GuiMain_Tags.DATA_STORE_BLOBS_PREFIX, help="prefix in data container for the data files")
    parser.add_argument(GuiMain_Tags.PREDICTIONS_BLOBS_PREFIX, help="prefix in data container for predictions files")
    parser.add_argument(GuiMain_Tags.EXTERNAL_LIB_PATH, help="local path to the the external library")
    parser.add_argument(GuiMain_Tags.CONFIG_FILE_PATH, help="path to the config file, default path is [repo_dir]/app_config/app_config.json")

    args = parser.parse_args()
    app_config = AppConfig.get_app_config()
    app_config.update_values_from_cmd_args(args, args.config_file_path)

if __name__=='__main__':
    process_command_line_args()
    server.debug = False
    server.run()
