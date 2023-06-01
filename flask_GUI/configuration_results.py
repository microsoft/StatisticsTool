import os
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
        value   - dictionary of Config Items
    '''
    items_dict = None

    def __init__(self):
        self.items_dict = dict()

    def insert_to_dictionary(self,key,value,ref_dir):
        self.items_dict[key] = value,ref_dir

    def get_from_dictionary(self,key):
        if key in self.items_dict.keys():
            v = self.items_dict[key]
            return v[0]
        else:
            return None
        
    '''
        Loads the configurations according to the request and store it in the dictionary.
        Each entry in the dictionary is a root-key - the base directory in the file system.
        The value of the rook-key is also a map (dictionary) where each entry in the map is a Configuration Item.
        root_key => (pointer to a map of Config Items - sub directories)
                   - sub directory 1 (contains a PKL and JSON of segmentations)
                   - sub directory 2 (contains a PKL and JSON of segmentations)
                   - etc...

        if the user choose a PKL object or he choose a path to a specific PKL (and not a PATH of directory)
        in that case the sub directory is the name of the PKL. for example, the user select the path "c:/temp/file1.PKL"
        the root-key is c:/temp
        and the value is a map where the entry is "file1"
    '''
    def load_configurations(self,request,server):
        
        
        main_pkl_type = self.get_pkl_type(request,True)
        ref_pkl_type  = self.get_pkl_type(request,False)
        ref_dir,pkl_ref_path = self.get_ref_info (request)
        
        if main_pkl_type == PklType.PKL_FILE_PATH:
            return self.load_configurations_in_directory(request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH],ref_dir,pkl_ref_path,server)
            
        if main_pkl_type == PklType.PKL_OBJECT:
            file_path = self.get_pkl_object_file_path(request.files[ConfigurationResults.MAIN_REPORT_CHOOSEFILE],True)
            ref_pkl_files = self.get_all_files_in_directory(ref_dir)
            root_key = os.path.dirname(file_path)

            basename_without_ext = os.path.splitext(os.path.basename(file_path))[0] 
            basename = os.path.basename(file_path)
            conf = ConfigurationItem()
            main_pkl_path = self.save_pkl_file(request.files[ConfigurationResults.MAIN_REPORT_CHOOSEFILE],True)
            conf.main_pkl = load_object(main_pkl_path)
            if ref_pkl_type == PklType.PKL_OBJECT:
                conf.ref_pkl = load_object(pkl_ref_path)
            if ref_pkl_type == PklType.PKL_FILE_PATH:
                if basename in ref_pkl_files.keys():
                    conf.ref_pkl = load_object(ref_pkl_files[basename])
            if server != None:
                conf.table_result = Results_table(server)
            dic = dict()
            dic[basename_without_ext] = conf
            self.insert_to_dictionary(root_key,dic,ref_dir)     

            return root_key,ref_dir
        else:
            return None,None

    def get_ref_info(self,request):
        pkl_ref_path = ''
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
        return ref_dir,pkl_ref_path    

    def save_configuration(self,request,server):
        root_key,ref_dir = self.load_configurations(request,server)
        sub_keys = ''
        v = self.get_from_dictionary(root_key)
        for k in v.keys():
            sub_keys += k + ","    
            
        return root_key,sub_keys,ref_dir

    def load_configurations_in_directory(self,dir_main,ref_dir,pkl_ref_path,server):
        root_key = ''
        
        '''
        if the user select path of directory - the root-key is the directory path
        otherwise, if the user select a path to a PKL file, the root path is the base driectory of that file.

        for example: 
        1. if dir_main is 'c:/temp/dirs' then root_key is 'c:/temp/dirs'
        2. if dir main is 'c:/temp/foo/file1.pkl' then root_key is 'c:/temp/foo'
        '''
        if os.path.isdir(dir_main):
            root_key = dir_main
        else:    
            root_key,_ = os.path.split(dir_main)   

        #all the PKL files exists in the reference directory
        ref_pkl_files = self.get_all_files_in_directory(ref_dir)

        sub_keys = dict()
        if os.path.isdir(dir_main):
            for v in next(os.walk(dir_main))[1]: # all the sub-directories (each v is sub-directory)
                conf = ConfigurationItem()
                # take files (PKLs) in the sub directory
                sub_dir_files = self.get_all_files_in_directory(os.path.join(dir_main,v))
                for k in sub_dir_files.keys():
                    if k.split(".")[1] == 'pkl':
                        conf.main_pkl = load_object(sub_dir_files[k])
                        if pkl_ref_path != '':
                            conf.ref_pkl = load_object(pkl_ref_path)
                        else:
                            if k in ref_pkl_files.keys():
                                conf.ref_pkl = load_object(ref_pkl_files[k])
                        if server != None:
                            conf.table_result = Results_table(server)                        
                        sub_keys[v + "/" + k.split(".")[0]] = conf

            self.insert_to_dictionary(root_key,sub_keys,ref_dir)

        else:
            if pathlib.Path(dir_main).suffix == '.pkl':
                '''
                for example - the dir_main is c:/temp/file1.pkl, then
                basename_without_ext : 'file1'
                basename : 'c:/temp/file1.pkl'
                '''
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
                self.insert_to_dictionary(root_key,dic,ref_dir)
                 
        return root_key,ref_dir

    def get_all_files_in_directory(self,dir):
        map = dict()
        for (dirpath, dirnames, filenames) in os.walk(dir):
            for f in filenames+dirnames:
                map[f] = os.path.join(dirpath,f)
        
        return map

    def get_config_item(self,root_key,sub_key):
        v = self.get_from_dictionary(root_key)
        if v == None:
            return None
        
        if sub_key in v.keys():
            return v[sub_key]
        return None
    
    def get_config_root_key_info(self,root_key):
        v = self.get_from_dictionary(root_key)
        if v == None:
            return None,None,None
        sub_keys = ''
        for s in v[0].keys():
            sub_keys += s + ","

        ref_dir = v[1]

        return root_key,sub_keys,ref_dir    

    def get_item_segmentations(self,root_key,sub_key):
        
        item = self.get_config_item(root_key,sub_key)
        if item == None:
            return None
        
        segmentations = {seg_category:v['possible partitions'] for seg_category, v in item.main_pkl.masks.items() if seg_category != 'total_stats'}
        result = []
        for k, v in segmentations.items():
            result.append({'name':k,'values':v})
        return segmentations
        

    def get_saved_files_directory_path(self):
        return os.path.join(current_file_directory.replace('flask_GUI_main.py', 'static'),'reports')

    def get_key_from_request(self,request,is_main_ref):
        pkl_type = self.get_pkl_type(request,is_main_ref)

        if pkl_type is PklType.PKL_FILE_PATH:
            return request.values[ConfigurationResults.MAIN_REPORT_FILE_PATH if is_main_ref else ConfigurationResults.REF_REPORT_FILE_PATH]
        if pkl_type is PklType.PKL_OBJECT:
            return os.path.join(self.get_saved_files_directory_path(),
                   request.files[ConfigurationResults.MAIN_REPORT_CHOOSEFILE if is_main_ref else ConfigurationResults.REF_REPORT_CHOOSE_FILE].filename)
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
    
    def add_exp(self,exp,key,sub_key,ref_dir,server):
        if key in self.items_dict.keys():
            v = self.items_dict[key]
            v[sub_key].main_pkl = exp
            v[sub_key].table_result = Results_table(server)
        else:
            conf = ConfigurationItem()
            conf.main_pkl = exp
            conf.table_result = Results_table(server)
            dic = dict()
            dic[sub_key] = conf
            self.items_dict[key] = dic,ref_dir
