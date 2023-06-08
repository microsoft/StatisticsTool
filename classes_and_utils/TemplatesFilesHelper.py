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
    
    def save_template(self,filename,content,main_path,ref_path,returnAllTemplates = True):
        
        _, file_extension = os.path.splitext(filename)
        if file_extension == '' or file_extension == None:
            filename += Constants.TEMPLATE_EXTENSION

        path = ''

        dir_main,_ = os.path.split(main_path)
        path = os.path.join(dir_main,filename)
        
        if os.path.exists(dir_main):
            with open(path,'w') as f:
                f.write(content)

        dir_ref,_ = os.path.split(ref_path)

        if returnAllTemplates:
            return self.get_all_templates_content(dir_main,dir_ref)

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
    def get_all_templates_content(self,main_dir,ref_dir):
        
        templates = self.get_all_templates_content_inner(main_dir)        

        if len(templates) > 0:
            return templates
        
        #search in REF directory
        templates = self.get_all_templates_content_inner(ref_dir,True)        
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
                except jsonschema.exceptions.ValidationError as err:
                    print(err)
                      
        return templates