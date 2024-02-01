import json
import os


default_secrets_file_name = r"blob_storage_config.json"
default_config_file_name = r"app_config.json"
class AppConfig():
    app_config = None
    def __init__(self, config_file = None, secrets_file = None):
        self.storage_id = ''
        self.data_container_name = ''
        self.annotation_store_blobs_prefix = ''
        self.data_store_blobs_prefix = ''
        self.predictions_blobs_prefix = ''
        self.storage_connection_string = ''
        self.external_lib_path = ''
        self.custom_storage_helper = ''
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

    def update_values_from_cmd_args(self, args, config_file = None, secrets_file_name = None):
        if config_file:
            AppConfig.app_config = AppConfig(config_file, secrets_file_name)
        for arg_name, arg_value in vars(args).items():
            if arg_value and hasattr(self, arg_name):
                 setattr(AppConfig.app_config, arg_name, arg_value)
        
    @staticmethod
    def get_app_config(config_file_name = default_config_file_name, storage_file_name = default_secrets_file_name):
        if not AppConfig.app_config:
            AppConfig.app_config = AppConfig(config_file_name, storage_file_name)
        return AppConfig.app_config









