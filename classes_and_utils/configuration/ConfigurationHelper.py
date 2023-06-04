import os,json,urllib.parse


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

        #"create report" case
        if request.args.get('use_cached_report') == 'true':
            main_path = request.args.get('main')
            main_path = urllib.parse.unquote_plus(main_path)
            
            return main_path, None

        main = None
        ref = None
        
        if request.files and request.files[MAIN_REPORT_CHOOSEFILE].filename != '':
            main = request.files[MAIN_REPORT_CHOOSEFILE] 
        else:
            main = request.values and request.values[MAIN_REPORT_FILE_PATH]
          

        if request.files and request.files[REF_REPORT_CHOOSE_FILE].filename != '':
            ref = request.files[REF_REPORT_CHOOSE_FILE]
        else:
            ref = request.values and request.values[REF_REPORT_FILE_PATH]            

        return main, ref  
    
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
    
    @staticmethod
    def parse_segmentations_csv(csv_segs):
        items = []
        if csv_segs != None and len(csv_segs) > 0:
            if csv_segs[-1] == ',':
                csv_segs = csv_segs[:-1]
            items  = list(csv_segs.split(',') )
        return items
        