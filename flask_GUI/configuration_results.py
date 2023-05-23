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
    def __init__(self,main_pkl = None,ref_pkl = None,table_result = None):
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

    def load_configurations(self,request,server):
        self.lock.acquire()
        try:
            main_pkl_type = self.get_pkl_type(request,True)
            ref_dir = self.get_ref_dir(request)
            
            if main_pkl_type == PklType.PKL_FILE_PATH:
                if os.path.isdir(request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH]):
                    root_key = self.load_configurations_in_directory(request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH],ref_dir,server)
                    return root_key
                else:
                    root_key = self.load_configurations_in_directory(request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH],ref_dir,server)
                    return root_key
            if main_pkl_type == PklType.PKL_OBJECT:
                file_path = self.get_pkl_object_file_path(request.files[ConfigurationResults.MAIN_REPORT_CHOOSEFILE],True)
                ref_pkl_files = self.get_all_files_in_directory(ref_dir)
                root_key = os.path.dirname(file_path)

                basename_without_ext = os.path.splitext(os.path.basename(file_path))[0] 
                basename = os.path.basename(file_path)
                conf = ConfigurationItem()
                main_pkl_path = self.save_pkl_file(request.files[ConfigurationResults.MAIN_REPORT_CHOOSEFILE],True)
                conf.main_pkl = load_object(main_pkl_path)
                if basename in ref_pkl_files.keys():
                    conf.ref_pkl = load_object(ref_pkl_files[basename])
                if server != None:
                    conf.table_result = Results_table(server)
                dic = dict()
                dic[basename_without_ext] = conf
                self.items_dict[root_key] = dic        

                return root_key
            else:
                return ''
        finally:
            self.lock.release()

    def get_ref_dir(self,request):
        ref_pkl_type  = self.get_pkl_type(request,False)
        ref_dir = ''
        if ref_pkl_type == PklType.PKL_FILE_PATH:
            if os.path.isdir(request.values[ConfigurationResults.REF_REPORT_FILE_PATH]):
                ref_dir = request.values[ConfigurationResults.REF_REPORT_FILE_PATH]
            if os.path.isfile(request.values[ConfigurationResults.REF_REPORT_FILE_PATH]): 
                ref_dir, _ = os.path.split(request.values[ConfigurationResults.REF_REPORT_FILE_PATH])   
        if ref_pkl_type == PklType.PKL_OBJECT:
            pkl_ref_path = self.save_pkl_file(request.files[ConfigurationResults.REF_REPORT_CHOOSE_FILE],False)
            ref_dir,_ = os.path.split(pkl_ref_path)
        return ref_dir    

    def save_configuration(self,request,server):
        root_key = self.load_configurations(request,server)
        sub_keys = ''
        for k in self.items_dict[root_key].keys():
            sub_keys += k + ","    
            
        return root_key,sub_keys
        self.lock.acquire()
        try:
            key = self.get_key_from_request(request)
            if self.is_config_item_exist(key):
                return key
            else:
                if self.get_pkl_type(request,True) == PklType.PKL_FILE_PATH and os.path.isdir(request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH]):
                    self.load_configurations_in_directory(request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH],
                                                          request.values[ConfigurationResults.REF_REPORT_FILE_PATH],server)
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

    def load_configurations_in_directory(self,dir_main,dir_ref,server):
        root_key = ''
        if os.path.isdir(dir_main):
            root_key = dir_main
        else:    
            root_key,_ = os.path.split(dir_main)   

        ref_pkl_files = self.get_all_files_in_directory(dir_ref)
        sub_keys = dict()
        if os.path.isdir(dir_main):
            for v in next(os.walk(dir_main))[1]:
                conf = ConfigurationItem()
                config_key = ''
                sub_dir_files = self.get_all_files_in_directory(os.path.join(dir_main,v))
                for k in sub_dir_files.keys():
                    if k.split(".")[1] == 'pkl':
                        conf.main_pkl = load_object(sub_dir_files[k])
                        config_key = sub_dir_files[k]
                        if k in ref_pkl_files.keys():
                            conf.ref_pkl = load_object(ref_pkl_files[k])
                if server != None:
                    conf.table_result = Results_table(server)                        
                sub_keys[v] = conf
            self.items_dict[root_key] = sub_keys
        else:
            if pathlib.Path(dir_main).suffix == '.pkl':
                basename_without_ext = os.path.splitext(os.path.basename(dir_main))[0] 
                basename = os.path.basename(dir_main)
                conf = ConfigurationItem()
                conf.main_pkl = load_object(dir_main)
                if basename in ref_pkl_files.keys():
                    conf.ref_pkl = load_object(ref_pkl_files[basename])
                if server != None:
                    conf.table_result = Results_table(server)
                dic = dict()
                dic[basename_without_ext] = conf
                self.items_dict[root_key] = dic                         
        return root_key

    def get_all_files_in_directory(self,dir):
        map = dict()
        for (dirpath, dirnames, filenames) in os.walk(dir):
            for f in filenames:
                map[f] = os.path.join(dirpath,f)
        
        return map

    def is_config_item_exist(self,key):
        if key in self.items_dict:
            return True
        else:
            return False
    
    def get_config_item(self,root_key,sub_key):
        self.lock.acquire()
        try:
            if root_key in self.items_dict:
                if sub_key in self.items_dict[root_key]:
                    return self.items_dict[root_key][sub_key]
            return None
        finally:
            self.lock.release()

    def get_item_segmentations(self, key,sub_key):
        self.lock.acquire()
        try:
            if key in self.items_dict:
                item = self.items_dict[key]
                if sub_key in item:
                    segmentations = {seg_category:v['possible partitions'] for seg_category, v in item[sub_key].main_pkl.masks.items() if seg_category != 'total_stats'}
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
                                    'reports','comp' if not is_main_pkl else "",pckl_file.filename)
        # save the pickle file of the report (the instance of the ParallelExperiment class as a pickle file)
        if not os.path.exists(os.path.dirname(path_to_save)):
            os.makedirs(os.path.dirname(path_to_save))
        if os.path.exists(path_to_save):
            os.remove(path_to_save)
        pckl_file.save(path_to_save)
        return path_to_save

    def get_pkl_object_file_path(self,pckl_file,is_main_pkl):
        path = os.path.join(current_file_directory.replace(os.path.basename(__file__), 'static'),
                                    'reports','comp' if not is_main_pkl else "",pckl_file.filename)
        return path 
