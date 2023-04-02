import os,sys

#sys.path.append(os.path.join(os.getcwd(),'classes_and_utils'))

from classes_and_utils.GUI_utils import load_object,match_main_ref_predictions
from classes_and_utils.unique_helper import UniqueHelper

class TestUniqueHelper:

    def __init__(self):
        pass
    
    def load_experiment(self,filename):
        path = os.path.join(os.getcwd(),'tests','files',filename)
        exp = load_object(path)
        exp.main_ref_dict=None
        exp.ref_main_dict=None
        return exp

    def test_find_fp_unique(self):

        #Arrage
        exp = self.load_experiment('report_unique_exp.pkl')
        ref = self.load_experiment('report_unique_ref.pkl')
        unique_helper = UniqueHelper(exp,ref)
        columns  = []
        rows = []
        columns.append({"None":"None"})
        rows.append({"None":"None"})
        
        #act
        unique_array,unique_array_ref,tup = unique_helper.calc_unique_detections(columns,rows,'FP')

        #assert
        assert len(unique_array_ref) == 5

    def run_all_tests(self):
        self.test_find_fp_unique()
    
if __name__ == "__main__":
    test = TestUniqueHelper()   
    test.run_all_tests()        
    print("Everything passed")
