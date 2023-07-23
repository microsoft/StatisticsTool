from glob import glob
import json
import pickle
import uuid,os
from app_config.constants import Constants, UserDefinedConstants
from classes_and_utils.ParallelExperiment import ParallelExperiment
from classes_and_utils.UserDefinedFunctionsHelper import get_userdefined_function
from utils.report_metadata import CONFIG_TOKEN, EVALUATION_FUNC_TOKEN, OVERLAP_FUNC_TOKEN, PARTITIONING_FUNC_TOKEN, STATISTICS_FUNC_TOKEN, THRESHOLD_TOKEN


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

    def get_experiment(self,experiment_path):
        if experiment_path is None or experiment_path == '' or experiment_path not in self.experiments.keys():
            return None
        return self.experiments[experiment_path]
    
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
            
            if exp not in self.experiments.keys():
                experiment_object = self.load_experiments(exp)
                self.experiments[exp] = experiment_object
            added_main.append(exp)
            if ref:
                #get the partitioning function of the main report in order to compare same partitinings
                metadata = ExperimentsManager.load_report_metadata(exp)
                func_name = metadata[CONFIG_TOKEN][PARTITIONING_FUNC_TOKEN]
                partitioning_func = get_userdefined_function(UserDefinedConstants.PARTITIONING_FUNCTIONS, func_name)

                experiment_object = self.load_experiments(ref, partitioning_func)
                if ref not in self.experiments.keys():
                    self.experiments[ref] = experiment_object
                added_ref.append(ref)   

        return added_main, added_ref        

        
    def get_item_segmentations(self,main_path):
        
        experiment = self.get_experiment(main_path)
        if experiment == None:
            return None
        
        segmentations = {seg_category:v['possible partitions'] for seg_category, v in experiment.get_masks().items() if seg_category != 'total_stats'}
        result = []
        for k, v in segmentations.items():
            result.append({'name':k,'values':v})
        return segmentations   

    @staticmethod
    def get_user_defined_functions(report_path):
        metadata = ExperimentsManager.load_report_metadata(report_path)
        statistics_func = get_userdefined_function(UserDefinedConstants.STATISTICS_FUNCTIONS, func_name = metadata[CONFIG_TOKEN][STATISTICS_FUNC_TOKEN])
        overlap_func = get_userdefined_function(UserDefinedConstants.OVERLAP_FUNCTIONS, func_name = metadata[CONFIG_TOKEN][OVERLAP_FUNC_TOKEN])
        evaluation_func = get_userdefined_function(UserDefinedConstants.EVALUATION_FUNCTIONS, func_name = metadata[CONFIG_TOKEN][EVALUATION_FUNC_TOKEN])

        return statistics_func, evaluation_func, overlap_func


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
    
    @staticmethod
    def load_experiments(file_path, partitioning_func = None):
         
        if not os.path.exists(file_path):
            print(f"\n\n-------- Error -------")
            print(f"Can't find report file {file_path}. Failed To load report\n\n")
            assert(0)
        
        with open(file_path, 'rb') as report_data:
            comp_data = pickle.load(report_data)

        metadata = ExperimentsManager.load_report_metadata(file_path)
        func_name = metadata[CONFIG_TOKEN][PARTITIONING_FUNC_TOKEN]
        
        if not partitioning_func:
            partitioning_func = get_userdefined_function(UserDefinedConstants.PARTITIONING_FUNCTIONS, func_name)

        threshold = metadata[CONFIG_TOKEN][THRESHOLD_TOKEN]
        ret_exp = ParallelExperiment(comp_data, threshold, partitioning_func)
        return ret_exp
    