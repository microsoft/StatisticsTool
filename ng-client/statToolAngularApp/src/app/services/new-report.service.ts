import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { SaveSuiteDialogComponent } from "../save-suite-dialog/save-suite-dialog.component";
import { GROUND_TRUTH_DIRECTORY, LocalStorgeHelper, OUTPUT_DIRECTORY, PREDICTION_DIRECTORY } from "./localStorageHelper";
import { Subject } from "rxjs";
import { read } from "@popperjs/core";

export const SELECTE_SUITE = '--- Select Suite ---';
export const NONE_GT_READING_CUNCTION = 'none';

export class NewReportResult {
    ok = true;
    errorMessage = '';
    link = '';
    files:string[] = [];
    num_success_files:string[] = [];
    reading_function_skipped:string[] = [];
    not_json_files:string[] = [];
    failed_with_error:string[] = [];
    skipped_not_in_lognames:string[] = [];
}

export namespace UDF {
    export enum ParamType {
        STRING = 0
    }

    export class Param {
        
        constructor(name:string,type:string) {
            this.name = name;
            if (type == 'string'){
                this.type = ParamType.STRING;
            }            
        }

        name = '';
        type = ParamType.STRING;
        value = '';
    }

    export class Item {

        constructor(funcName:string,params:Param[]){
            this.funcName = funcName;
            this.params = params;
        }

        funcName = '';
        params:Param[] = [];
    }
}

@Injectable({
    providedIn: 'root'
  })

export class NewReportService {

    FUNC_TYPES = ['reading_functions','evaluation_functions','overlap_functions','partitioning_functions','statistics_functions','transform_functions','confusion_functions','association_functions'];
    
    showConfigViewer = true;

    configs:string[]  = [];
    suites:string []  = [];
    configsSelections = new Map<string,boolean>();
    selectedSuite = '';

    prediction_reading_functions    :string[] = [];
    gt_reading_functions            :string[] = [];
    evaluation_functions            :string[] = [];
    overlap_functions               :string[] = [];
    partitioning_functions          :string[] = [];
    statistics_functions            :string[] = [];
    transform_functions             :string[] = [];
    confusion_functions             :string[] = [];
    association_functions           :string[] = [];
    
    selectedPredictionReadingFunction   = '';
    selectedGTReadingFunction           = '';
    selectedOverlapFunction             = '';
    selectedTransformFunction           = '';
    selectedPartitioningFunction        = '';
    selectedStatisticsFunction          = '';
    selectedEvaluationFunction          = '';
    selectedConfusionFunction           = '';
    selectedAssociationFunction         = '';

    configName = '';
    logName = '';
    treshold = '';

    predictionsDirectory = '';
    groundTruthDirectory = '';
    reporterOutputDirectory = '';

    newReportResult = new NewReportResult();

    creatingReport = false;

    last_prediction_directory   :string[] = [];
    last_ground_truth_directory :string[] = [];
    last_output_directory       :string[] = [];

    //gtReadingEnabled:    boolean = false;
    gtReadingSameAsPrediction:  boolean = true;
    overlapEnabled:             boolean = true;
    evaluateEnabled:            boolean = true;
    tresholdEnabled:            boolean = true;
    transformEnabled:           boolean = false;
    partitioningEnabled:        boolean = false;
    associationEnabled:         boolean = false;

    isPanelOpen = false;

    //map between udf type (foe example reading_function) to function names
    udf = new Map<string,UDF.Item[]>();

    showArgumentsEvent = new Subject<{'funcType':string,'funcName':string,'udfItem':UDF.Item,'title':string}>();
    showParams = false;
    argPanelTop = '';
    argPanelLeft = '';
    udfArgumentsMap:{ [key: string]: any } = {};

    constructor(private http:HttpClient,private modalService: NgbModal){
        let url = '/new_report/get_all_user_defined_functions';
        this.http.get<any>(url).subscribe(response => {
            
            this.processUdfResponse(response);

            this.prediction_reading_functions = this.udf.get('reading_functions')?.map(o => o.funcName)!
            this.prediction_reading_functions.sort((a,b) =>  (a > b ? 1 : -1));
            
            this.gt_reading_functions = this.prediction_reading_functions;

            this.evaluation_functions = this.udf.get('evaluation_functions')?.map(o => o.funcName)!;
            this.evaluation_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.overlap_functions = this.udf.get('overlap_functions')?.map(o => o.funcName)!;
            this.overlap_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.partitioning_functions = this.udf.get('partitioning_functions')?.map(o => o.funcName)!;
            this.partitioning_functions.sort((a,b) =>  (a > b ? 1 : -1));
            
            this.statistics_functions = this.udf.get('statistics_functions')?.map(o => o.funcName)!;
            this.statistics_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.transform_functions = this.udf.get('transform_functions')?.map(o => o.funcName)!;
            this.transform_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.confusion_functions = this.udf.get('confusion_functions')?.map(o => o.funcName)!;
            this.confusion_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.association_functions = this.udf.get('association_functions')?.map(o => o.funcName)!;
            this.association_functions.sort((a,b) =>  (a > b ? 1 : -1));
            
        })
    }

    processUdfResponse(udfResponse:any){

        for (const f of this.FUNC_TYPES){
            let funcs = this.processUdfItem(f,udfResponse);
            this.udf.set(f,funcs);
        }

        let readingFunc = this.udf.get('reading_functions')
        let gt = JSON.parse(JSON.stringify(readingFunc));
        this.udf.set('gt_reading_functions',gt);
    }

    processUdfItem(funcType:string,udfResponse:any){
        let arrFuncs:UDF.Item[] = [];
        let functions = udfResponse[funcType];

        for (const func of functions){
            let funcName = func.func_name;
            let funcArguments = func.func_arguments;
            let params:UDF.Param[] = [];
            for (const key in funcArguments) {
                if (funcArguments.hasOwnProperty(key)) {
                  const argumentName = key;
                  const argumentValue = funcArguments[key];
                  params.push(new UDF.Param(argumentName,argumentValue))
                }
            }
            arrFuncs.push(new UDF.Item(funcName,params));
        }

        return arrFuncs;
    }

    initDataFromLocalStorage(){
        LocalStorgeHelper.loadAll();
        this.last_prediction_directory      = LocalStorgeHelper.getList(PREDICTION_DIRECTORY)!;
        this.last_ground_truth_directory    = LocalStorgeHelper.getList(GROUND_TRUTH_DIRECTORY)!;
        this.last_output_directory          = LocalStorgeHelper.getList(OUTPUT_DIRECTORY)!;
    }

    init(configs:string,suites:string){
        this.parseConfigs(configs);
        this.initSuitesList(JSON.parse(suites));    
        this.selectedSuite = SELECTE_SUITE;
        this.initSelectedConfigs();    
    }

    parseConfigs(configs:string){
        this.configs = JSON.parse(configs);
        this.configs.sort((a,b) =>  (a > b ? 1 : -1));
    }

    initSelectedConfigs(){
        this.configsSelections.clear();

        this.configs.forEach(c => {
            this.configsSelections.set(c.toLocaleLowerCase(),false);
        })
    }

    initSuitesList(suites:string[]){
        this.suites = [];
        this.suites.push(SELECTE_SUITE);
        
        suites.forEach(s => {
            s = s.replace(".json","")
            this.suites.push(s)
        })

        this.suites.sort((a,b) =>  (a > b ? 1 : -1));
    }

    onSuiteSelected(event:any){

        this.initSelectedConfigs();

        if (event.target.value == SELECTE_SUITE){
            return;
        }

        let suite = event.target.value + ".json";
        let params = { 'suite':suite };
        let url = '/new_report/get_suite';
        this.http.get<string[]>(url,{params}).subscribe(configs => {
            configs.forEach(config => {
                config = config.toLocaleLowerCase()
                this.configsSelections.set(config,true)
            })
        })
    }    

    isConfigSelected(config:string){
        return this.configsSelections.get(config.toLocaleLowerCase());
    }

    configSelectionChanged(event:any,config:string){
        this.configsSelections.set(config.toLocaleLowerCase(),event.target.checked);
        if (event.target.checked)
            this.showConfig(config.toLocaleLowerCase());
    }

    saveSuite(suiteName:string){    
        let configs:string[] = [];
        
        this.configs.forEach(c => {
            let isChecked = this.configsSelections.get(c.toLocaleLowerCase());
            if (isChecked)
                configs.push(c);
        })

        let strConfigs = '';
        for (let i=0;i<configs.length;i++){
            if (strConfigs.length > 0)
                strConfigs += ","
            strConfigs += configs[i]
        }

        this.http.post<any>('/new_report/save_suite',{
            'suite':suiteName,
            'configurations':strConfigs
        }).subscribe(res => {
            
            this.initSuitesList(res)
            this.selectedSuite = suiteName
        })
    }

    getSelectedSuiteName(){
        return this.selectedSuite;
    }

    openSaveSuiteDialog(){
        this.modalService.open(SaveSuiteDialogComponent,{ centered: true }).result.then(res => {
        });    
      }
    
    closeSaveSuiteDialog(){
        this.modalService.dismissAll();
    }
      
    clearConfigViewer(){
        this.selectedPredictionReadingFunction = '';
        this.selectedGTReadingFunction = '';
        this.selectedOverlapFunction = '';
        this.selectedTransformFunction = '';
        this.selectedPartitioningFunction = '';
        this.selectedStatisticsFunction = '';
        this.selectedEvaluationFunction = '';
        this.selectedConfusionFunction = '';    
        this.selectedAssociationFunction = '';

        this.configName = '';
        this.logName = '';
        this.treshold = '';
    }  

    showConfig(configName:string){
        this.showConfigViewer = true;    
        //get the confing from server
        let params = { 'config':configName };
        let url = '/new_report/get_configuration';
        this.http.get<any>(url,{params}).subscribe(config => {
            //clear the config viewer  
            this.clearConfigViewer();
            //show the new config in the viewer
            this.selectedPredictionReadingFunction = config['Prediction Reading Function']; 
            this.selectedGTReadingFunction = config['GT Reading Function'];

            this.selectedOverlapFunction = config['Overlap Function'];
            this.selectedTransformFunction = config['Transformation Function'];
            /*if (this.selectedTransformFunction == '' || this.selectedTransformFunction == null || this.selectedTransformFunction == undefined)
                this.selectedTransformFunction = 'None';*/
            this.selectedPartitioningFunction = config['Partitioning Functions'];
            this.selectedStatisticsFunction = config['Statistics Functions'];
            this.selectedEvaluationFunction = config['Evaluation Function'];
            this.selectedConfusionFunction = config['Confusion Functions'];
        
            this.configName = configName;
            this.logName = config['Log Names to Evaluate'];
            this.treshold = config['Threshold'];

            this.gtReadingSameAsPrediction = (this.selectedPredictionReadingFunction == this.selectedGTReadingFunction) || (this.selectedGTReadingFunction.toLowerCase() == 'none');

            this.overlapEnabled = this.selectedOverlapFunction != '' && this.selectedOverlapFunction != undefined;
            this.evaluateEnabled = this.selectedEvaluationFunction != '' && this.selectedEvaluationFunction != undefined;
            this.tresholdEnabled = this.treshold != '' && this.treshold != undefined;
            this.transformEnabled = this.selectedTransformFunction != '' && this.selectedTransformFunction != undefined;
            this.partitioningEnabled = this.selectedPartitioningFunction != '' && this.selectedPartitioningFunction != undefined;

            if (this.overlapEnabled || this.evaluateEnabled || this.treshold){
                this.isPanelOpen = true;
            } else {
                this.isPanelOpen = false;
            }    
        })
    }

    saveConfig(){
        this.newReportResult = new NewReportResult();
        const dictionary: { [key: string]: any } = {};

        dictionary['Prediction Reading Function'] = this.selectedPredictionReadingFunction;
        if (!this.gtReadingSameAsPrediction)
            dictionary['GT Reading Function'] = this.selectedGTReadingFunction;
        
        if (this.overlapEnabled)
            dictionary['Overlap Function'] = this.selectedOverlapFunction;
        if (this.transformEnabled)
            dictionary['Transformation Function'] = this.selectedTransformFunction;
        if (this.partitioningEnabled)
            dictionary['Partitioning Functions'] = this.selectedPartitioningFunction;
        dictionary['Statistics Functions'] = this.selectedStatisticsFunction;
        if (this.evaluateEnabled)
            dictionary['Evaluation Function'] = this.selectedEvaluationFunction;
        dictionary['configName'] = this.configName;
        dictionary['Log Names to Evaluate'] = this.logName;
        if (this.tresholdEnabled)
            dictionary['Threshold'] = this.treshold;
        dictionary['Confusion Functions']= this.selectedConfusionFunction;

        const url = '/new_report/save_configuration'; 

        this.http.post(url, dictionary).subscribe(response => {
            let configs:any;
            configs = response;
            ///this.parseConfigs(configs);
            this.configs = configs;
            this.configs.sort((a,b) =>  (a > b ? 1 : -1));
        })
    }

    saveDataInLocalStorage(){
        LocalStorgeHelper.addToList(PREDICTION_DIRECTORY,this.predictionsDirectory);
        LocalStorgeHelper.addToList(GROUND_TRUTH_DIRECTORY,this.groundTruthDirectory);
        LocalStorgeHelper.addToList(OUTPUT_DIRECTORY,this.reporterOutputDirectory);
        LocalStorgeHelper.saveInLocaStorage();
        this.initDataFromLocalStorage();
    }

    createReport(){
        this.creatingReport = true;
        this.newReportResult = new NewReportResult();
        this.newReportResult.link = '';
        
        this.newReportResult.errorMessage = '';
        this.newReportResult.ok = false;

        this.saveDataInLocalStorage();

        let params = { 
            'Configurations':this.getSuiteConfigurations(this.selectedSuite),
            'Suite Name':this.selectedSuite == SELECTE_SUITE ? '' : this.selectedSuite,
            'Predictions Directory': this.predictionsDirectory,
            'Ground Truth Directory': this.groundTruthDirectory,
            'Reporter Output Directory':this.reporterOutputDirectory
        };

        let url = '/new_report/calculating_page';
        this.http.get<any>(url,{params}).subscribe(res => {
            
            this.creatingReport = false;
            this.newReportResult.ok = res.ok;
            if (res.link != 'None' && res.link != undefined && res.link != null)
                this.newReportResult.link = res.link;
            else
                this.newReportResult.link = '';
            this.newReportResult.errorMessage = res.errorMessage;
            this.newReportResult.files = res.files;
            this.newReportResult.failed_with_error = res.failed_with_error;
            this.newReportResult.not_json_files= res.not_json_files;
            this.newReportResult.num_success_files = res.num_success_files;
            this.newReportResult.reading_function_skipped = res.reading_function_skipped;
            this.newReportResult.skipped_not_in_lognames = res.skipped_not_in_lognames;
        })
    }

    getSuiteConfigurations(suiteName:string){
        let configs:string[] = [];
        for (let [key,value] of this.configsSelections){
            if (value){
                configs.push(key)
            }
        }

        return configs.join(",");
    }

    showResults(){
        if (this.newReportResult.ok && this.newReportResult.files.length > 0)
            return true;
        if (!this.newReportResult.ok && this.newReportResult.errorMessage != '')
            return true;

        return false;
    }

    getNumConfigsSelected(){
        //this.configsSelections
        let count = 0;
        for (const isSelected of this.configsSelections.values()) {
            if (isSelected) {
            count++;
            }
        }
        return count;
    }

    getUDFUserArguments(funcType:string,funcName:string){
        let params = { 'func_type':funcType,'func_name':funcName };
        let url = '/new_report/get_udf_user_arguments';

        this.http.get<any>(url,{params}).subscribe(config => {
            this.udfArgumentsMap[funcType + "-" + funcName] = config;       
            console.log('map',JSON.stringify(this.udfArgumentsMap))        
        });
    }

    showArgumentsPanel(funcType:string,title:string,funcName:string){
        let o = this.udf.get(funcType)?.find(x => x.funcName == funcName)
        if (o != undefined){
            this.showArgumentsEvent.next({'funcType':funcType,'funcName':funcName,'udfItem':o,'title':title});
        }
    }
}