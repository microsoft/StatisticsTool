from glob import glob
import pickle
import uuid,os
from app_config.constants import Constants


class ExperimentsManager:

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
            experiment = ExperimentsManager.load_object(folder)
            exp_key = self.add_experiment(folder,experiment)
            total.append(exp_key)
        else:        
        
            files = glob(folder + '/**/*' + Constants.EXPERIMENT_EXTENSION, recursive=True)
            for v in files:
                experiment = ExperimentsManager.load_object(v)
                exp_key = self.add_experiment(v,experiment)
                total.append(exp_key)
        
        return total

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

    @staticmethod
    def load_object(file):
        """
        Loads a pickle file from a path
        :param filename: the path from which the function loads the pickle file
        :return: the loaded file
        """
        ret_exp = None
        ## Load  pickle
        if type(file).__name__ == 'str':
            with open(file, 'rb') as input:
                ret_exp = pickle.load(input)
        elif type(file).__name__ == 'FileStorage':
            ret_exp = pickle.load(file.stream)
        else:
            raise TypeError("Unable to load pickle")
        
        ## Update values
        ret_exp.main_ref_dict=None
        ret_exp.ref_main_dict=None

        return ret_exp
    