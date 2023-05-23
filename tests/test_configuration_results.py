from flask_GUI.configuration_results import ConfigurationResults

class TestConfigurationResults:
    def __init__(self):
        pass

    def test_load_configurations_in_directory(self,main_dir,ref_dir):
        conf = ConfigurationResults()
        conf.load_configurations_in_directory(main_dir,ref_dir,None)    

    def run_all_tests(self):
        self.test_load_configurations_in_directory('C:\\Users\\v-hagaicohen\\Downloads\\ver-1','C:\\Users\\v-hagaicohen\\Downloads\\ver-2')


if __name__ == "__main__":
    test = TestConfigurationResults()   
    test.run_all_tests()        
    print("Everything passed")