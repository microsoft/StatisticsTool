from glob import glob
import uuid,os
from flask_GUI.dash_apps.results_table import Results_table

from classes_and_utils.GUI_utils import *

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
        self.experiments[experiment_path] = experiment_object

    def add_results_table(self,main_experiment_path,ref_experiment_path,server):
        res_table = Results_table(server)
        self.results_tables[(main_experiment_path,ref_experiment_path)] = res_table
        return res_table

    def get_experiment(self,experiment_path):
        if experiment_path is None or experiment_path == '':
            return None
        return self.experiments[experiment_path]
    
    def get_results_table(self,main_experiment_path,ref_experiment_path):
        if (main_experiment_path,ref_experiment_path) in self.results_tables.keys():
            return self.results_tables[(main_experiment_path,ref_experiment_path)]
        return None
    
    def add_experiments_in_folder(self,folder):
        if os.path.isdir(folder) == False:
            return ''
        
        experiments_added = ''
        files = glob(folder + '/**/*.pkl', recursive=True)
        for v in files:
            experiment = load_object(v)
            self.add_experiment(v,experiment)
            if len(experiments_added) > 0:
                experiments_added += ","
            experiments_added += str(v)

        return experiments_added

    def add_experiment_object(self,experiment_object):
        key = str(uuid.uuid4()) + "\\" + "Upload" + "\\" + experiment_object.filename
        experiment_object = load_object(experiment_object)
        self.add_experiment(key,experiment_object)
        return key
    
    def add(self,value):
        if value == None:
            return ''
        
        if type(value) == str:
            return self.add_experiments_in_folder(value)
        else:
            return self.add_experiment_object(value)
        
    def get_item_segmentations(self,main_path):
        
        experiment = self.get_experiment(main_path)
        if experiment == None:
            return None
        
        segmentations = {seg_category:v['possible partitions'] for seg_category, v in experiment.masks.items() if seg_category != 'total_stats'}
        result = []
        for k, v in segmentations.items():
            result.append({'name':k,'values':v})
        return segmentations    