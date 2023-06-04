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
    
    def save_template(self,filename,content,main_path,ref_path,returnAllTemplates = True):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += ".json"

        path = ''

        dir_main,_ = os.path.split(main_path)
        path = os.path.join(dir_main,filename)
        
        with open(path,'w') as f:
            f.write(content)

        dir_ref,_ = os.path.split(ref_path)

        if returnAllTemplates:
            return self.get_all_templates_content(dir_main,dir_ref)

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
    '''
        if no templates under Main and REF has templates - take the REF templates
    '''    
    def get_all_templates_content(self,main_dir,ref_dir):
        
        templates = self.get_all_templates_content_inner(main_dir)        

        if len(templates) > 0:
            return templates
        
        #search in REF directory
        templates = self.get_all_templates_content_inner(ref_dir,True)        
        return templates
       
    def get_all_templates_content_inner(self,folder,recursive=False):
        templates = []
        
        files = glob(folder + '\*.json', recursive=recursive)
        for fullname in files:
            with open(fullname,'r') as f:
                content = json.load(f)  
                    
            templates.append({'name':os.path.splitext(os.path.basename(fullname))[0],'content':content})
        return templates