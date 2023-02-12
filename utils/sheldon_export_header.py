import json

LOG_FILE_NAME = 'log_file_name'
LOGS_PATH = 'logs_path'
PRIMARY_METADATA = 'primary_report'
SECONDARY_METADATA = 'secondary_report'

def create_sheldon_list_header(primary_path, primary_name, secondary_path, secondary_name) -> dict:
    header = {}
    header[PRIMARY_METADATA] = {}
    header[SECONDARY_METADATA] = {}
    header[PRIMARY_METADATA][LOGS_PATH] = primary_path
    header[SECONDARY_METADATA][LOGS_PATH] = secondary_path
    header[PRIMARY_METADATA][LOG_FILE_NAME] = primary_name
    header[SECONDARY_METADATA][LOG_FILE_NAME] = secondary_name
    return header


