import json

LOG_FILE_NAME = 'log_file_name'
LOGS_PATH = 'logs_path'
PRIMARY_LOG = 'primary_report'
SECONDARY_LOG = 'secondary_report'

def create_sheldon_list_header(primary_path, primary_name, secondary_path, secondary_name) -> dict:
    header = {}
    header[PRIMARY_LOG] = {}
    header[SECONDARY_LOG] = {}
    header[PRIMARY_LOG][LOGS_PATH] = primary_path
    header[SECONDARY_LOG][LOGS_PATH] = secondary_path
    header[PRIMARY_LOG][LOG_FILE_NAME] = primary_name
    header[SECONDARY_LOG][LOG_FILE_NAME] = secondary_name
    return header


