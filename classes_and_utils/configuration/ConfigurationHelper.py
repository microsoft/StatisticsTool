import os,json,urllib.parse
from classes_and_utils.consts import Constants
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
        
        if request.files and request.files[Constants.MAIN_REPORT_CHOOSEFILE].filename != '':
            main = request.files[Constants.MAIN_REPORT_CHOOSEFILE]
        else:
            main = request.values and request.values[Constants.MAIN_REPORT_FILE_PATH]

        if request.files and request.files[Constants.REF_REPORT_CHOOSE_FILE].filename != '':
            ref = request.files[Constants.REF_REPORT_CHOOSE_FILE]
        else:
            if Constants.REF_REPORT_FILE_PATH in request.values.keys():
                ref = request.values and request.values[Constants.REF_REPORT_FILE_PATH]            

        return main, ref  
    
    @staticmethod
    def build_main_ref_pairs(main_experiments,ref_experiments):

        list_main = list()
        list_ref  = list()
        if type(main_experiments).__name__ == 'str':
            list_main.append(main_experiments)
        else:
            list_main = list(main_experiments)    
        if type(ref_experiments).__name__ == 'str':
            list_ref.append(ref_experiments)
        else:
            list_ref = list(ref_experiments)    


        arr = []

        map_ref_exp = dict()
        for f in list_ref:
            _,file = os.path.split(f)
            map_ref_exp[str(file).lower()] = f

        for v in list_main:
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
        