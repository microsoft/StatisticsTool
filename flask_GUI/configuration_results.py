import os
import threading
from enum import Enum
from classes_and_utils.GUI_utils import *
from flask_GUI.dash_apps.results_table import Results_table
current_file_directory = os.path.realpath(__file__)

class PklType(Enum):
    NONE = 0
    PKL_OBJECT = 1
    PKL_FILE_PATH = 2

class ConfigurationItem:
    def __init__(self,main_pkl,ref_pkl,table_result):
        self.main_pkl = main_pkl
        self.ref_pkl = ref_pkl
        self.table_result = table_result
class ConfigurationResults:

    MAIN_REPORT_FILE_PATH   = 'report_file_path'
    MAIN_REPORT_CHOOSEFILE  = 'choose_report_file'
    REF_REPORT_FILE_PATH    = 'reference_file_path'
    REF_REPORT_CHOOSE_FILE  = 'choose_reference_file'

    '''
        dictionary to store Config Items
        key     - PKL absolute path
        value   - Config Item 
    '''
    items_dict = None

    def __init__(self):
        self.items_dict = dict()
        self.lock = threading.Lock()


    def save_configuration(self,request,server):
        self.lock.acquire()
        try:
            key = self.get_key_from_request(request)
            if self.is_config_item_exist(key):
                return key
            else:
                # create the configuration-item
                # - create the main and ref pkls
                # - create the table result
                main_exp     = self.load_experiment(request,True)
                ref_exp      = self.load_experiment(request,False)
                table_result = Results_table(server)
                self.items_dict[key] = ConfigurationItem(main_exp,ref_exp,table_result)
                return key
        finally:
            self.lock.release()
        
    def is_config_item_exist(self,key):
        if key in self.items_dict:
            return True
        else:
            return False
    
    def get_config_item(self,key):
        self.lock.acquire()
        try:
            if key in self.items_dict:
                return self.items_dict[key]
            return None
        finally:
            self.lock.release()

    def get_item_segmentations(self, key):
        self.lock.acquire()
        try:
            if key in self.items_dict:
                item = self.items_dict[key]
                segmentations = {seg_category:v['possible partitions'] for seg_category, v in item.main_pkl.masks.items() if seg_category != 'total_stats'}
                result = []
                for k, v in segmentations.items():
                    result.append({'name':k,'values':v})
                return segmentations
            else:
                return None
        finally:
            self.lock.release()

    def get_saved_files_directory_path(self):
        return os.path.join(current_file_directory.replace('flask_GUI_main.py', 'static'),'reports')

    def get_key_from_request(self,request):
        pkl_type = self.get_pkl_type(request,True)
        if pkl_type is PklType.PKL_FILE_PATH:
            return request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH]
        if pkl_type is PklType.PKL_OBJECT:
            return os.path.join(self.get_saved_files_directory_path(),request.files[ConfigurationResults.MAIN_REPORT_CHOOSEFILE].filename)
        return ''

    def get_pkl_type(self,request,is_main_pkl):
        if is_main_pkl:
            if ConfigurationResults.MAIN_REPORT_FILE_PATH in request.values and request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH] != '':
                return PklType.PKL_FILE_PATH
            if request.files and request.files[ConfigurationResults.MAIN_REPORT_CHOOSEFILE].filename != '':
                return PklType.PKL_OBJECT
        else:
            if ConfigurationResults.REF_REPORT_FILE_PATH in request.values and request.values[ConfigurationResults.REF_REPORT_FILE_PATH] != '':
                return PklType.PKL_FILE_PATH
            if request.files and request.files[ConfigurationResults.REF_REPORT_CHOOSE_FILE].filename != '':
                return PklType.PKL_OBJECT

        return PklType.NONE
    
    def load_experiment(self,request,is_main_pkl):
        key_file_path   = ConfigurationResults.REF_REPORT_FILE_PATH if not is_main_pkl else ConfigurationResults.MAIN_REPORT_FILE_PATH
        key_choose_file = ConfigurationResults.REF_REPORT_CHOOSE_FILE if not is_main_pkl else  ConfigurationResults.MAIN_REPORT_CHOOSEFILE
        pkl_type = self.get_pkl_type(request,is_main_pkl)
        exp = None
        
        if pkl_type == PklType.PKL_FILE_PATH:
            #check if file exist
            report_filename = request.values[key_file_path]
            if os.path.exists(report_filename):
                exp = load_object(report_filename)

        if pkl_type == PklType.PKL_OBJECT:
            pckl_file = request.files[key_choose_file]
            report_filename = self.save_pkl_file(pckl_file,False)
            exp = load_object(report_filename)
        
        return exp
    
    def save_pkl_file(self,pckl_file,is_main_pkl):
        path_to_save = os.path.join(current_file_directory.replace(os.path.basename(__file__), 'static'),
                                    'reports',
                                    ("comp_" + pckl_file.filename) if not is_main_pkl else pckl_file.filename)
        # save the pickle file of the report (the instance of the ParallelExperiment class as a pickle file)
        if not os.path.exists(os.path.dirname(path_to_save)):
            os.makedirs(os.path.dirname(path_to_save))
        if os.path.exists(path_to_save):
            os.remove(path_to_save)
        pckl_file.save(path_to_save)
        return path_to_save
