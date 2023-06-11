from glob import glob
import uuid,os
from flask_GUI.dash_apps.results_table import Results_table
from classes_and_utils.GUI_utils import *
from classes_and_utils.consts import Constants

class ConfigurationManager:

    '''
      experiments: a Map that holds PKLs
        Key   - PKL full path
        Value - PKL object
    
      results_tables: a Map that holds Results_table
        Key   - a couple: two entries in experiments dictionary (main & ref)
        Value - Results_table object
    '''
    experiments     = dict()
    results_tables  = dict()

    def add_experiment(self,experiment_path,experiment_object):
        norm_path = self.norm_exp_name(experiment_path)
        if norm_path not in self.experiments.keys():
            self.experiments[norm_path] = experiment_object

        return norm_path

    def add_results_table(self,main_experiment_path,ref_experiment_path,res_table):
        if (main_experiment_path,ref_experiment_path) in self.results_tables.keys():
            return
        self.results_tables[(main_experiment_path,ref_experiment_path)] = res_table
        return res_table

    def get_experiment(self,experiment_path):
        if experiment_path is None or experiment_path == '' or experiment_path not in self.experiments.keys():
            return None
        return self.experiments[experiment_path]
    
    def get_results_table(self,main_experiment_path,ref_experiment_path):
        if (main_experiment_path,ref_experiment_path) in self.results_tables.keys():
            return self.results_tables[(main_experiment_path,ref_experiment_path)]
        return None
    
    def add_experiments_in_folder(self,folder):
        total = []
        if folder and os.path.isdir(folder) == False:
            experiment = load_object(folder)
            exp_key = self.add_experiment(folder,experiment)
            total.append(exp_key)
        else:        
        
            files = glob(folder + '/**/*' + Constants.EXPERIMENT_EXTENSION, recursive=True)
            for v in files:
                experiment = load_object(v)
                exp_key = self.add_experiment(v,experiment)
                total.append(exp_key)
        
        return total

    def add_experiment_object(self,experiment_object):
        key = str(uuid.uuid4()) + "/" + "Upload" + "/" + experiment_object.filename
        experiment_object = load_object(experiment_object)
        self.add_experiment(key,experiment_object)
        return key
    
    def norm_exp_name(self, name):
        norm_name = name.replace('\\','/')
        return norm_name
    
    def add(self, value):
        if not value:
            return ''
        
        return self.add_experiments_in_folder(value)
        
    def get_item_segmentations(self,main_path):
        
        experiment = self.get_experiment(main_path)
        if experiment == None:
            return None
        
        segmentations = {seg_category:v['possible partitions'] for seg_category, v in experiment.masks.items() if seg_category != 'total_stats'}
        result = []
        for k, v in segmentations.items():
            result.append({'name':k,'values':v})
        return segmentations    