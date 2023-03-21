import sys, os, json
from glob import glob
from pathlib import Path


USER_DEFINED_TEMPLATES_FOLDER_NAME = "user_defined_templates"


class TemplateItem:
    name = ''
    content = ''
    def __init__(self,name,content):
        self.name = name
        self.content = content        


class TemplatesFilesHelper:
    
    def __init__(self):
    
        pass

    def get_all_templates_names(self):
        templates = []
        path = str(os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), USER_DEFINED_TEMPLATES_FOLDER_NAME,'*'))
        files = glob(path)
        for fullname in files:
            filename = fullname.split(os.sep)[-1]
            file_parts = filename.split('.')
            if len(file_parts) == 2 and file_parts[1] == 'json':
                templates.append(file_parts[0])
        return templates
    
    def save_template(self,filename,content):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += ".json"

        path = os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), USER_DEFINED_TEMPLATES_FOLDER_NAME,filename)
        
        with open(path,'w') as f:
            f.write(content)

    def get_template_content(self,filename):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += ".json"

        path = os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), USER_DEFINED_TEMPLATES_FOLDER_NAME,filename)
        if os.path.exists(path) == False:
            return ''
        
        with open(path,'r') as f:
            data = json.load(f)            
            return data
        
    def get_all_templates_content(self):
        templates = []
        path = str(os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), USER_DEFINED_TEMPLATES_FOLDER_NAME,'*'))
        files = glob(path)
        for fullname in files:
            filename = fullname.split(os.sep)[-1]
            file_parts = filename.split('.')
            if len(file_parts) == 2 and file_parts[1] == 'json':
                templates.append({'name':file_parts[0],'content':self.get_template_content(file_parts[0])})
        return templates

       
