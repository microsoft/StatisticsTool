
import mimetypes

from flask_GUI.flask_server import server

from flask_GUI.flask_report_view import *
from flask_GUI.flask_create_report import *
from flask_GUI.flask_examples_list import *


@server.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('start_page.html', exp_ext = Constants.EXPERIMENT_EXTENSION, wiki_page = Constants.WIKI_URL)


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
   


if __name__=='__main__':
    server.debug = False
    server.run()
