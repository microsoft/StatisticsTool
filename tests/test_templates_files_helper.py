from classes_and_utils.TemplatesFilesHelper import TemplatesFilesHelper
from flask import jsonify

class TestTemplatesFilesHelper:
    def __init__(self):
        pass

    def save_template(self,filename,content):
        helper = TemplatesFilesHelper()
        helper.save_template(filename,content)

    def get_all_template(self):
        helper = TemplatesFilesHelper()
        return helper.get_all_templates_names()

    def get_file_content(self,filename):
        helper = TemplatesFilesHelper()
        return helper.get_template_content(filename)
    
    def get_templates_content(self):
        helper = TemplatesFilesHelper()
        return helper.get_all_templates_content()

    def run_all_tests(self):
        #self.save_template('Template 1','this is template 1')
        #self.save_template('Template 2','this is template 2')
        #templates = self.get_all_template()
        #content = self.get_file_content('template 1')
        templates = self.get_templates_content()
        print(templates)

    
        


if __name__ == "__main__":
    test = TestTemplatesFilesHelper()   
    test.run_all_tests()        
    print("Everything passed")