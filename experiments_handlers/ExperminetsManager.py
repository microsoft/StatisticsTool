from glob import glob
import json
import pickle
from threading import Lock
import uuid,os
from app_config.constants import Constants, UserDefinedConstants
from experiment_engine.ParallelExperiment import ParallelExperiment
from experiment_engine.UserDefinedFunctionsHelper import load_function_object
from utils.report_metadata import CONFIG_TOKEN


class ExperimentsManager:

    '''
      experiments: a Map that holds PKLs
        Key   - PKL full path
        Value - PKL object
    
      results_tables: a Map that holds Results_table
        Key   - a couple: two entries in experiments dictionary (main & ref)
        Value - Results_table object
    '''
    def __init__(self):
        self.experiments     = dict()
        self.results_tables  = dict()


    def add_results_table(self,main_experiment_path,ref_experiment_path,res_table):
        if (main_experiment_path,ref_experiment_path) in self.results_tables.keys():
            return
        self.results_tables[(main_experiment_path,ref_experiment_path)] = res_table
    
    def get_results_table(self,main_experiment_path,ref_experiment_path):
        if (main_experiment_path,ref_experiment_path) in self.results_tables.keys():
            return self.results_tables[(main_experiment_path,ref_experiment_path)]
        return None
    
    def get_norm_experiments_paths(self,folder):
        
        files = []
        if not folder or not os.path.exists(folder):
            return []
        if os.path.isdir(folder) == False:
            files = [folder]
        else:
            files = glob(folder + '/**/*' + Constants.EXPERIMENT_EXTENSION, recursive=True)

        
        retval = [self.to_unix_path(f) for f in files]
        return retval

    def to_unix_path(self, name):
        norm_name = name.replace('\\','/')
        return norm_name
    
    load_experiment_lock = Lock()
    def get_or_load_experiment(self, exp, main_exp = None):
        if exp is None or exp == '':
                return None
        if exp not in self.experiments.keys():
            with ExperimentsManager.load_experiment_lock:
                if exp not in self.experiments.keys():      
                    partitioning_func = None
                    if main_exp:
                        metadata = ExperimentsManager.load_report_metadata(main_exp)
                    else:
                        metadata = ExperimentsManager.load_report_metadata(exp)

                    partitioning_func = ExperimentsManager.get_udf_from_config(UserDefinedConstants.PARTITIONING_FUNCTIONS_KEY, metadata=metadata)
                    confusion_func = ExperimentsManager.get_udf_from_config(UserDefinedConstants.CONFUSION_FUNCTIONS_KEY, metadata=metadata)
                    assert confusion_func is not None, f"Failed to load confusion function from config: {metadata}"
                    with open(exp, 'rb') as report_data:
                        comp_data = pickle.load(report_data)

                    experiment_object = ParallelExperiment(comp_data, partitioning_func, confusion_func=confusion_func)
                    self.experiments[exp] = experiment_object

        return self.experiments[exp]

    def add_experiments_folders(self, main_folder, ref_folder):
        if not main_folder:
            return ''
        
        added_main = []
        added_ref = []

        main_experiments_path_list = self.get_norm_experiments_paths(main_folder)
        ref_experiments_path_list = self.get_norm_experiments_paths(ref_folder)

        for exp in main_experiments_path_list:
            exp_name = os.path.split(exp)[-1]
            ref = None
            for cur_ref in ref_experiments_path_list:
                ref_name = os.path.split(cur_ref)[-1]
                if exp_name == ref_name:
                    ref = cur_ref
                    break
            
            self.get_or_load_experiment(exp)
            added_main.append(exp)
            if ref:
                self.get_or_load_experiment(ref, exp)
                added_ref.append(ref)   

        return added_main, added_ref        
      
    def get_item_segmentations(self,main_path):
        
        experiment = self.get_or_load_experiment(main_path)
        if experiment == None:
            return None
        
        segmentations = {seg_category:v['possible partitions'] for seg_category, v in experiment.get_segmentations_masks().items()}
        result = []
        for k, v in segmentations.items():
            result.append({'name':k,'values':v})
        return segmentations   

    @staticmethod
    def get_udf_from_config(udf_type, metadata):
        func_conf = metadata[CONFIG_TOKEN].get(udf_type)
        func = load_function_object(func_conf, udf_type)
        return func

    @staticmethod
    def get_experiment_udf(report_path):
        metadata = ExperimentsManager.load_report_metadata(report_path)
        statistics_func = ExperimentsManager.get_udf_from_config(UserDefinedConstants.STATISTICS_FUNCTIONS_KEY, metadata)
        association_func = ExperimentsManager.get_udf_from_config(UserDefinedConstants.ASSOCIATION_FUNCTIONS_KEY, metadata)
       
        return statistics_func, association_func

    @staticmethod
    def load_report_metadata(report_path):
        report_metadata = report_path.replace(Constants.EXPERIMENT_EXTENSION, Constants.METADATA_EXTENTION)
        if not os.path.exists(report_metadata):
            print(f"\n\n-------- Error -------")
            print(f"Can't find report metadat {report_metadata}. Failed To load report\n\n")
            assert(0)
        with open(report_metadata) as conf:
            metadata = json.load(conf)

        return metadata
    
    