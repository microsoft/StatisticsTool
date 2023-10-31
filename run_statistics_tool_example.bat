cd "/d %~dp0"
python -m flask_server.flask_server_main --external_lib_path ".\running_example\st_external_lib" %*
