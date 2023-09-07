
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

@server.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('start_page.html', exp_ext = Constants.EXPERIMENT_EXTENSION, wiki_page = Constants.WIKI_URL)

@server.route("/validate_path", methods=["POST"])
def validate_path():
    data = request.get_json()
    path = data.get("path")

    # Perform validation here (e.g., check if the path is a directory)
    is_directory = os.path.isdir(path)

    # Return the result as JSON
    return jsonify({"isValidDirectory": is_directory})

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
   

def process_command_line_args():
    parser = argparse.ArgumentParser(description='StatisticsTool')
    parser.add_argument("--azure_storage_id", help="azure storage id to access data container")
    parser.add_argument("--data_container_name", help="name of data container")
    parser.add_argument("--annotation_store_blobs_prefix", help="prefix in data container for the annotations files")
    parser.add_argument("--data_store_blobs_prefix", help="prefix in data container for the data files")
    parser.add_argument("--predictions_blobs_prefix", help="prefix in data container for predictions files")
    parser.add_argument("--external_lib_path", help="local path to the the external library")
    parser.add_argument("--config_file_path", help="path to the config file, default path is [repo_dir]/app_config/app_config.json")

    args = parser.parse_args()
    app_config = AppConfig.get_app_config()
    app_config.update_values_from_cmd_args(args, args.config_file_path)

if __name__=='__main__':
    process_command_line_args()
    server.debug = False
    server.run()
