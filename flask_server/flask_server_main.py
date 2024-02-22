
import argparse
import mimetypes

import sys, os

path = os.path.abspath(os.path.join(os.path.join(os.path.realpath(__file__), '..'), '..'))
if path not in sys.path:
    sys.path.append(path)

from flask_server.flask_server import server

from flask_server.flask_report_view import *
from flask_server.flask_create_report import *
from flask_server.flask_examples_list import *
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
    parser.add_argument('--storage_id', help="azure storage id to access data container")
    parser.add_argument('--data_container_name', help="name of data container")
    parser.add_argument('--annotation_store_blobs_prefix', help="prefix in data container for the annotations files")
    parser.add_argument('--data_store_blobs_prefix', help="prefix in data container for the data files")
    parser.add_argument('--predictions_blobs_prefix', help="prefix in data container for predictions files")
    parser.add_argument('--external_lib_path', help="local path to the the external library")
    parser.add_argument('--config_file_path', help="path to the config file, default path is [repo_dir]/app_config/app_config.json")
    parser.add_argument('--storage_config_path', help="path to the config file, default path is [repo_dir]/app_config/blob_storage_config.json")
    args = parser.parse_args()
    app_config = AppConfig.get_app_config()
    app_config.update_values_from_cmd_args(args, args.config_file_path, args.storage_config_path)

if __name__=='__main__':
    process_command_line_args()
    server.debug = False
    server.run()
