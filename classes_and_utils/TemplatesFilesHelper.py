import sys, os, json
from glob import glob
from pathlib import Path
from jsonschema import validate
import jsonschema
from classes_and_utils.consts import Constants


schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "segmentations": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "rows": {
              "type": "string"
            },
            "columns": {
              "type": "string"
            }
          },
          "required": [
            "name",
            "rows",
            "columns"
          ]
        },
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "rows": {
              "type": "string"
            },
            "columns": {
              "type": "string"
            }
          },
          "required": [
            "name",
            "rows",
            "columns"
          ]
        }
      ]
    }
  },
  "required": [
    "name",
    "segmentations"
  ]
}

class TemplateItem:
    name = ''
    content = ''
    def __init__(self,name,content):
        self.name = name
        self.content = content        


class TemplatesFilesHelper:
    
    def save_template(self,filename,content,main_path):
        
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += Constants.TEMPLATE_EXTENSION

        path = ''

        dir_main,_ = os.path.split(main_path)
        path = os.path.join(dir_main,filename)
        
        if os.path.exists(dir_main):
            with open(path,'w') as f:
                f.write(content)


    def get_template_content(self,filename):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += Constants.TEMPLATE_EXTENSION

        path = os.path.join(str(Path(os.path.dirname(os.path.realpath(__file__))).parent), Constants.REPORTS_TEMPLATES_FOLDER_NAME,filename)
        if os.path.exists(path) == False:
            return ''
        
        with open(path,'r') as f:
            data = json.load(f)            
            return data
    '''
        if no templates under Main and REF has templates - take the REF templates
    '''    
    def get_all_templates_content(self,main_path,ref_path):
        main_dir,_ = os.path.split(main_path)
        ref_dir,_ = os.path.split(ref_path)

        templates = self.get_all_templates_content_inner(main_dir)        

        #search in REF directory
        templates_ref = self.get_all_templates_content_inner(ref_dir,True)  

        #load template from ref reprort that not exists in main reports and save them in main report folder
        for t in templates_ref:
            exitsts = False
            for loaded in templates:
                if loaded['name'] == t['name']:
                    exitsts = True
                    break
            if not exitsts:
                templates.append(t)
                self.save_template(t['name'], json.dumps(t['content']), main_path)
        return templates
       
    def get_all_templates_content_inner(self,folder,recursive=False):
        templates = []
        
        files = glob(folder + '\*' + Constants.TEMPLATE_EXTENSION, recursive=recursive)
        for fullname in files:
            with open(fullname,'r') as f:
                try:
                    content = json.load(f)
                    validate(instance=content, schema=schema)
                    templates.append({'name':str(os.path.basename(fullname)).replace(Constants.TEMPLATE_EXTENSION,''),'content':content})
                except Exception as err:
                    print ('Failed to load template file: '+f)
                    print(err)
                      
        return templates