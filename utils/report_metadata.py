import json

LOG_FILE_NAME = 'log_file_name'
LOGS_PATH = 'logs_path'
PRIMARY_LOG = 'primary_report'
SECONDARY_LOG = 'secondary_report'
VIDEO_INFO = 'video_location'
VIDEO_BASE_PATH = 'video_path'
VIDEO_SUFFIX = 'video_suffix'

def create_report_metadata(primary_path, primary_name, secondary_path, secondary_name, video_path) -> dict:
    header = {}
    header[PRIMARY_LOG] = {}
    header[SECONDARY_LOG] = {}
    header[VIDEO_INFO] = {}

    header[PRIMARY_LOG][LOGS_PATH] = primary_path
    header[SECONDARY_LOG][LOGS_PATH] = secondary_path

    header[PRIMARY_LOG][LOG_FILE_NAME] = primary_name
    header[SECONDARY_LOG][LOG_FILE_NAME] = secondary_name

    header[VIDEO_INFO][VIDEO_BASE_PATH] = video_path
    header[VIDEO_INFO][VIDEO_SUFFIX] = '.mp4'

    return header

