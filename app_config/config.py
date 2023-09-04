import json
import os


secrets_file_name = r"app_secrets.json"

class AppConfig():
    app_config = None
    def __init__(self, config_file = None, secrets_file = None):
        self.azure_storage_id = ''
        self.data_container_name = ''
        self.annotation_store_blobs_prefix = ''
        self.data_store_blobs_prefix = ''
        self.predictions_blobs_prefix = ''
        self.base_detections_folder = ''
        self.local_storage_cache_size_limit = 1000
        self.storage_connection_string = ''
        self.external_lib_path = ''
        if config_file:
            self.update_values_from_config(config_file)
        if secrets_file:
            self.update_values_from_config(secrets_file)

    def update_values_from_config(self, config_file):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),config_file), 'r') as f:
            loaded_config = json.loads(f.read())
        for key in loaded_config.keys():
            if hasattr(self, key):
                setattr(self, key, loaded_config[key])

    def update_values_from_cmd_args(self, args):
        AppConfig.app_config = AppConfig(args.external_config_path, secrets_file_name)
        for arg_name, arg_value in vars(args).items():
            if arg_value and hasattr(self, arg_name):
                 setattr(AppConfig.app_config, arg_name, arg_value)
        
    @staticmethod
    def get_app_config(config_file_name = r"app_config.json"):
        if not AppConfig.app_config:
            AppConfig.app_config = AppConfig(config_file_name, secrets_file_name)
        return AppConfig.app_config









