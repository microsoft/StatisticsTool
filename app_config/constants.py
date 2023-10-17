

class Constants:
    folder_prefix_for_blob = "blob:"
    log_header_video_name_token = "video_file_name"
    log_header_video_path_token = "data_path"
    blob_path_startwidth_token = "http"
    log_header_token = "header"
    TEMPLATE_EXTENSION   = ".template.json"
    EXPERIMENT_EXTENSION = ".pkl"
    JSON_EXTENSION = '.json'
    PNG_EXTENSION = '.png'
    REPORTS_TEMPLATES_FOLDER_NAME = "reports_templates"
    MAIN_REPORT_FILE_PATH   = 'report_file_path'
    MAIN_REPORT_CHOOSEFILE  = 'choose_report_file'
    REF_REPORT_FILE_PATH    = 'reference_file_path'
    REF_REPORT_CHOOSE_FILE  = 'choose_reference_file'
    WIKI_URL =  "https://www.deviceswiki.com/wiki/Statistics_Tool"
    METADATA_EXTENTION = '.metadata.json'
    INTERMEDIATE_RESULTS_DIR="intermediate resutls"
    CONFIG_FOLDER_NAME = "reports_configurations/configs"
    SUITES_FOLDER_NAME = "reports_configurations/suites"
    EXTERNAL_LIBRARY = 'statisticstool_external_library'
    USER_DEFINED_FUNCTIONS = 'user_defined_functions'
    UDF_USER_ARGUMENT_FUNCTION = 'get_function_arguments'
    CONFIG_FUNCTION_NAME_TOKEN = 'func_name'
    CONFIG_FUNCTION_PARAMS_TOKEN = 'params'

class UserDefinedConstants:
    READING_FUNCTIONS_KEY           = 'reading_functions'
    GT_READING_FUNCTIONS_KEY        = 'gt_reading_functions'
    PARTITIONING_FUNCTIONS_KEY      = 'partitioning_functions'
    STATISTICS_FUNCTIONS_KEY        = 'statistics_functions'
    TRANSFORM_FUNCTIONS_KEY         = 'transform_functions'
    CONFUSION_FUNCTIONS_KEY         = 'confusion_functions'
    ASSOCIATION_FUNCTIONS_KEY       = 'association_functions'
    LOGS_TO_EVALUATE_KEY            = 'logs_file_names_to_evaluate'

class URLs:
    #INDEX_HTML_NEW_REPORT = '/static/index.html?new_report='
    INDEX_HTML = '/static/index.html'

class Tags:
    NEW_REPORT = 'new_report'
    REPORTS = 'reports'

