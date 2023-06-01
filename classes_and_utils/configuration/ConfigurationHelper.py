import os,json

MAIN_REPORT_FILE_PATH   = 'report_file_path'
MAIN_REPORT_CHOOSEFILE  = 'choose_report_file'
REF_REPORT_FILE_PATH    = 'reference_file_path'
REF_REPORT_CHOOSE_FILE  = 'choose_reference_file'

class ConfigurationHelper:

    '''
        input:   request
        retruns: main object ,is main object a directory or experiment,ref object, is ref object a directory or experiment
    '''
    @staticmethod
    def get_request_experiments_info(request):
        main = None
        is_main_an_object = False
        ref = None
        is_ref_an_object = False
        
        if request.files and request.files[MAIN_REPORT_CHOOSEFILE].filename != '':
            is_main_an_object = True
            main = request.files[MAIN_REPORT_CHOOSEFILE]
        else:
            is_main_an_object = False
            main = request.values and request.values[MAIN_REPORT_FILE_PATH]

        if request.files and request.files[REF_REPORT_CHOOSE_FILE].filename != '':
            is_ref_an_object = True
            ref = request.files[REF_REPORT_CHOOSE_FILE]
        else:
            is_ref_an_object = False
            ref = request.values and request.values[REF_REPORT_FILE_PATH]            

        return main, is_main_an_object, ref, is_ref_an_object    
    
    @staticmethod
    def build_main_ref_pairs(main_experiments,ref_experiments):

        arr = []

        map_ref_exp = dict()
        for f in ref_experiments.split(","):
            _,file = os.path.split(f)
            map_ref_exp[str(file).lower()] = f

        for v in main_experiments.split(","):
            _, main_file = os.path.split(v)
            if str(main_file).lower() in map_ref_exp.keys():
                arr.append({'main':v,'ref':map_ref_exp[str(main_file).lower()]})
            else:
                arr.append({'main':v,'ref':''})

        json_res = json.dumps(arr)                
        return json_res                    