import enum
import json

LOG_FILE_NAME = 'log_file_name'
LOGS_PATH = 'logs_path'
PRIMARY_LOG = 'primary_report'
SECONDARY_LOG = 'secondary_report'
VIDEO_INFO = 'video_location'
VIDEO_BASE_PATH = 'video_path'
VIDEO_SUFFIX = 'video_suffix'
RUN_INFO_TOKEN = 'run_info'
CONFIG_TOKEN = 'config'

READING_FUNCTION = "File Reading Function"
GT_READING_FUNCTION = "GT Reading Function"
PARTITIONING_FUNC_TOKEN = 'Partitioning Functions'
STATISTICS_FUNC_TOKEN = 'Statistics Functions'
EVALUATION_FUNC_TOKEN = 'Evaluation Function'
TRANSFORM_FUNC_TOKEN = 'Transformation Function'
OVERLAP_FUNC_TOKEN = 'Overlap Function'
THRESHOLD_TOKEN = 'Threshold'

def create_run_info(primary_path, primary_name, secondary_path, secondary_name, video_path) -> dict:
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

def create_metadata(metadata, config):
    report_metadata = {}
    report_metadata[RUN_INFO_TOKEN] = metadata
    report_metadata[CONFIG_TOKEN] = config
    return report_metadata

