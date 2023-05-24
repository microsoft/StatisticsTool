import sys, os, json
from glob import glob
from pathlib import Path


REPORTS_TEMPLATES_FOLDER_NAME = "reports_templates"


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
        path = str(os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), REPORTS_TEMPLATES_FOLDER_NAME,'*'))
        files = glob(path)
        for fullname in files:
            filename = fullname.split(os.sep)[-1]
            file_parts = filename.split('.')
            if len(file_parts) == 2 and file_parts[1] == 'json':
                templates.append(file_parts[0])
        return templates
    
    def save_template(self,filename,content,key,sub_key,returnAllTemplates = True):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += ".json"

        #path = os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), REPORTS_TEMPLATES_FOLDER_NAME,filename)
        path = ''
        if os.path.exists(os.path.join(key,sub_key)):
            path = os.path.join(key,sub_key,filename)
        else:
            path = os.path.join(key,filename)
        
        with open(path,'w') as f:
            f.write(content)

        if returnAllTemplates:
            return self.get_all_templates_content(key,sub_key);            

    def get_template_content(self,filename):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += ".json"

        path = os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), REPORTS_TEMPLATES_FOLDER_NAME,filename)
        if os.path.exists(path) == False:
            return ''
        
        with open(path,'r') as f:
            data = json.load(f)            
            return data
        
    def get_all_templates_content(self,root_key,sub_key):
        templates = []
        #path = str(os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), REPORTS_TEMPLATES_FOLDER_NAME,'*'))
        path = os.path.join(root_key,sub_key)
        if os.path.exists(path) == False:
            path = os.path.join(root_key,'*')
        else:    
            path = os.path.join(root_key,sub_key,'*')

        files = glob(path)
        for fullname in files:
            filename = fullname.split(os.sep)[-1]
            file_parts = filename.split('.')
            if len(file_parts) == 2 and file_parts[1] == 'json':
                with open(fullname,'r') as f:
                    content = json.load(f)  
                    #templates.append({'name':file_parts[0],'content':self.get_template_content(file_parts[0])})
                    templates.append({'name':file_parts[0],'content':content})
        return templates

       
