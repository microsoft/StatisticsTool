import os
current_file_directory = os.path.realpath(__file__)

class ConfigurationItem:
    main_pkl = None
    ref_pkl  = None
    table_result = None

class ConfigurationResults:
    '''
        dictionary to store Config Items
        key     - PKL absolute path
        value   - Config Item 
    '''
    items_dict = dict()
    
    def is_config_item_exist(self,key):
        if key in self.items_dict:
            return True
        else:
            return False
    
    def get_config_item(self,key):
        if key in self.items_dict:
            return self.items_dict[key]
        return None

    def add_config_item():
        pass

    def get_item_segmentations(self, key):
        if key in self.items_dict:
            item = self.items_dict[key]
            segmentations = {seg_category:v['possible partitions'] for seg_category, v in item.main_pkl.masks.items() if seg_category != 'total_stats'}
            result = []
            for k, v in segmentations.items():
                result.append({'name':k,'values':v})
            return segmentations
        else:
            return None

    def get_saved_files_directory_path(self):
        return os.path.join(current_file_directory.replace('flask_GUI_main.py', 'static'),'reports')

    def get_key_from_request(self,request):
        main_report_file_path = 'report_file_path'
        main_report_choose_file = 'choose_report_file'

        if main_report_file_path in request.values and request.values[main_report_file_path] != '':
            return request.values[main_report_file_path]
        else:
            if request.files and request.files[main_report_choose_file].filename != '':
                return os.path.join(self.get_saved_files_directory_path(),request.files[main_report_choose_file].filename)
            else:
                return ''    
    

    