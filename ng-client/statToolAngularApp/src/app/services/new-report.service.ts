import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { SaveSuiteDialogComponent } from "../save-suite-dialog/save-suite-dialog.component";
import { Subject } from "rxjs";
import { UDFConstants, UDFTypeEnum } from "../common/enums";
import Swal from 'sweetalert2';

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
    selectedTransformFunction           = '';
    selectedPartitioningFunction        = '';
    selectedStatisticsFunction          = '';
    selectedConfusionFunction           = '';
    selectedAssociationFunction         = '';

    configName = '';
    logsFilter = UDFConstants.DEFAULT_LOG_FILTER;
    evaluate_folders = false;

    predictionsDirectory = '';
    groundTruthDirectory = '';
    reporterOutputDirectory = '';

    newReportResult = new NewReportResult();

    isBusy = false;

    last_prediction_directory   :string[] = [];
    last_ground_truth_directory :string[] = [];
    last_output_directory       :string[] = [];

    gtReadingSameAsPrediction:  boolean = true;
    transformEnabled:           boolean = false;
    partitioningEnabled:        boolean = false;
    associationEnabled:         boolean = false;

    isPanelOpen = false;

    //map between udf type (for example reading_function) to function names
    udf = new Map<string,UDF.Item[]>();

    showArgumentsEvent = new Subject<{'funcType':string,'funcName':string,'udfItem':UDF.Item,'title':string}>();
    showParams = false;
    argPanelTop = '';
    argPanelLeft = '';
    udfArgumentsMap:{ [key: string]: any } = {};

    constructor(private http:HttpClient,private modalService: NgbModal){
    }

    async initialize(): Promise<void> {
        this.isBusy = true;
        await this.initUserDefinedFunction();
        await this.initSuitsAndConfigs();
        this.isBusy = false;
    }

    private async initSuitsAndConfigs(): Promise<void> {
        try {
            const url = '/new_report/get_all_configs_and_suits';
            const response = await this.http.get<any>(url).toPromise();
            let configs = response.configs;
            let suites = response.suites;
            this.parseConfigs(configs);
            this.initSuitesList(suites);    
            this.selectedSuite = SELECTE_SUITE;
            this.initSelectedConfigs();    
        }
        finally{

        }
    }

    private async initUserDefinedFunction(): Promise<void> {
        try {
          const url = '/new_report/get_all_user_defined_functions';
          const response = await this.http.get<any>(url).toPromise();
    
          this.processUdfResponse(response);
    
          this.prediction_reading_functions = this.udf.get(UDFTypeEnum.READING_FUNCTIONS)?.map((o) => o.funcName)!;
          this.prediction_reading_functions.sort((a, b) => (a > b ? 1 : -1));
    
          this.gt_reading_functions = this.prediction_reading_functions;
    
          this.partitioning_functions = this.udf.get(UDFTypeEnum.PARTITIONING_FUNCTIONS)?.map((o) => o.funcName)!;
          this.partitioning_functions.sort((a, b) => (a > b ? 1 : -1));
    
          this.statistics_functions = this.udf.get(UDFTypeEnum.STATISTICS_FUNCTIONS)?.map((o) => o.funcName)!;
          this.statistics_functions.sort((a, b) => (a > b ? 1 : -1));
    
          this.transform_functions = this.udf.get(UDFTypeEnum.TRANSFORM_FUNCTIONS)?.map((o) => o.funcName)!;
          this.transform_functions.sort((a, b) => (a > b ? 1 : -1));
    
          this.confusion_functions = this.udf.get(UDFTypeEnum.CONFUSION_FUNCTIONS)?.map((o) => o.funcName)!;
          this.confusion_functions.sort((a, b) => (a > b ? 1 : -1));
    
          this.association_functions = this.udf.get(UDFTypeEnum.ASSOCIATION_FUNCTIONS)?.map((o) => o.funcName)!;
          this.association_functions.sort((a, b) => (a > b ? 1 : -1));

        } catch (error) {
          console.error('Error initializing user-defined functions:', error);
        }
    }

    processUdfResponse(udfResponse:any){

        for (const value of Object.values(UDFTypeEnum)) {
            
            if (value === UDFTypeEnum.GT_READING_FUNCTIONS) {
              continue;
            }
            let funcs = this.processUdfItem(value, udfResponse);
            this.udf.set(value, funcs);
        }
          

        let readingFunc = this.udf.get(UDFTypeEnum.READING_FUNCTIONS)
        let gt = JSON.parse(JSON.stringify(readingFunc));
        this.udf.set(UDFTypeEnum.GT_READING_FUNCTIONS,gt);
    }

    processUdfItem(funcType:string,udfResponse:any){
        let arrFuncs:UDF.Item[] = [];
        let functions = udfResponse[funcType];
        
        if (functions == undefined || functions == null)
            return arrFuncs;

        for (const func of functions){
            let funcName = func.func_name;
            let funcArguments = func.params;
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

    parseConfigs(configs:any){
        this.configs = configs;
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
            this.showConfig(config);
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
        this.selectedTransformFunction = '';
        this.selectedPartitioningFunction = '';
        this.selectedStatisticsFunction = '';
        this.selectedConfusionFunction = '';    
        this.selectedAssociationFunction = '';

        this.configName = '';
        this.logsFilter = UDFConstants.DEFAULT_LOG_FILTER;

        //clear param values
        this.udf.forEach((value, key) => {
            value.forEach(item => {
                item.params.forEach(p => {
                    p.value = '';
                })
            });
        })

    }  

    parseGetConfigResult(udfType:UDFTypeEnum,result:any){
        
        if (result[udfType] != undefined){
            let func = result[udfType].func_name;
            if (udfType == UDFTypeEnum.READING_FUNCTIONS)
                this.selectedPredictionReadingFunction = func;
            if (udfType == UDFTypeEnum.ASSOCIATION_FUNCTIONS)
                this.selectedAssociationFunction = func;
            if (udfType == UDFTypeEnum.CONFUSION_FUNCTIONS)
                this.selectedConfusionFunction = func;
            if (udfType == UDFTypeEnum.GT_READING_FUNCTIONS)
                this.selectedGTReadingFunction = func;
            if (udfType == UDFTypeEnum.STATISTICS_FUNCTIONS)
                this.selectedStatisticsFunction = func;
            if (udfType == UDFTypeEnum.TRANSFORM_FUNCTIONS)
                this.selectedTransformFunction = func;
            if (udfType == UDFTypeEnum.PARTITIONING_FUNCTIONS)
                this.selectedPartitioningFunction = func;    

            let args = result[udfType].params;
            let udfItem = this.udf.get(udfType)?.find(x => x.funcName == func);
            if (udfItem != undefined){
                udfItem.params.forEach(p => {
                    p.value = args[p.name];
                })
            }
        }
    }

    showConfig(configName:string){
        this.showParams = false;
        this.showConfigViewer = true;    
        //get the confing from server
        let params = { 'config':configName };
        let url = '/new_report/get_configuration';
        this.http.get<any>(url,{params}).subscribe(config => {
            //clear the config viewer  
            
            this.clearConfigViewer();
            //show the new config in the viewer

            this.parseGetConfigResult(UDFTypeEnum.ASSOCIATION_FUNCTIONS,config);
            this.parseGetConfigResult(UDFTypeEnum.CONFUSION_FUNCTIONS,config);
            this.parseGetConfigResult(UDFTypeEnum.GT_READING_FUNCTIONS,config);
            this.parseGetConfigResult(UDFTypeEnum.PARTITIONING_FUNCTIONS,config);
            this.parseGetConfigResult(UDFTypeEnum.READING_FUNCTIONS,config);
            this.parseGetConfigResult(UDFTypeEnum.STATISTICS_FUNCTIONS,config);
            this.parseGetConfigResult(UDFTypeEnum.TRANSFORM_FUNCTIONS,config);
                    
            this.configName = configName;
            this.logsFilter = config[UDFTypeEnum.LOGS_NAME_TO_EVALUATE];
            this.evaluate_folders = config[UDFTypeEnum.EVALUATE_FOLDERS];

            this.gtReadingSameAsPrediction = (this.selectedGTReadingFunction == undefined || this.selectedGTReadingFunction == null || this.selectedGTReadingFunction == '') || (this.selectedGTReadingFunction.toLowerCase() == 'none');
            this.transformEnabled = this.selectedTransformFunction != '' && this.selectedTransformFunction != undefined;
            this.partitioningEnabled = this.selectedPartitioningFunction != '' && this.selectedPartitioningFunction != undefined;
            this.associationEnabled = this.selectedAssociationFunction != '' && this.selectedAssociationFunction != undefined;

            this.isPanelOpen = false;
        })
    }

    addUdfToConfig(type:UDFTypeEnum,selectedFunc:string,dictionary:{ [key: string]: any }){
        let item = this.udf.get(type);
        let x = item?.find(x => x.funcName == selectedFunc);
        const paramsObj: { [key: string]: any } = {};
        if (x == undefined)
            return
        for(let i = 0;i<x!.params.length;i++){
            let param = x!.params[i];
            paramsObj[param.name] = param.value;
        }

        dictionary[type] = {

            'func_name':selectedFunc,
            'params':paramsObj
        }
    }

    saveConfig(){
        this.isBusy = true;
        this.showParams = false
        this.newReportResult = new NewReportResult();
        const dictionary: { [key: string]: any } = {};
        this.addUdfToConfig(UDFTypeEnum.READING_FUNCTIONS,this.selectedPredictionReadingFunction,dictionary);
        if (!this.gtReadingSameAsPrediction && this.selectedGTReadingFunction.toLocaleLowerCase() != 'none')
            this.addUdfToConfig(UDFTypeEnum.GT_READING_FUNCTIONS,this.selectedGTReadingFunction,dictionary);
        if (this.transformEnabled)
            this.addUdfToConfig(UDFTypeEnum.TRANSFORM_FUNCTIONS,this.selectedTransformFunction,dictionary);
        if (this.partitioningEnabled)
            this.addUdfToConfig(UDFTypeEnum.PARTITIONING_FUNCTIONS,this.selectedPartitioningFunction,dictionary);
        this.addUdfToConfig(UDFTypeEnum.STATISTICS_FUNCTIONS,this.selectedStatisticsFunction,dictionary);
        this.addUdfToConfig(UDFTypeEnum.CONFUSION_FUNCTIONS,this.selectedConfusionFunction,dictionary);
        if (this.associationEnabled)
            this.addUdfToConfig(UDFTypeEnum.ASSOCIATION_FUNCTIONS,this.selectedAssociationFunction,dictionary);

        dictionary[UDFTypeEnum.CONFIG_NAME] = this.configName;
        dictionary[UDFTypeEnum.LOGS_NAME_TO_EVALUATE] = this.logsFilter;
        dictionary[UDFTypeEnum.EVALUATE_FOLDERS] = this.evaluate_folders;

        const url = '/new_report/save_configuration'; 

        this.http.post(url, dictionary).subscribe(response => {
            this.isBusy = false;
            let configs:any;
            configs = response;
            this.configs = configs;
            this.configs.sort((a,b) =>  (a > b ? 1 : -1));

            Swal.fire({
                text: 'Configuration saved successfully',
                timer:3000,
                showConfirmButton:false,
                showCancelButton:false,
                backdrop:false,
                color:'white',
                position:'bottom',
                background:'#00CC00',
              });
            })
    }


    createReport(){
        this.isBusy = true;
        this.newReportResult = new NewReportResult();
        this.newReportResult.link = '';
        
        this.newReportResult.errorMessage = '';
        this.newReportResult.ok = false;


        let params = { 
            'configurations':this.getSuiteConfigurations(this.selectedSuite),
            'suite_Name':this.selectedSuite == SELECTE_SUITE ? '' : this.selectedSuite,
            'predictions_directory': this.predictionsDirectory,
            'groundtruth_directory': this.groundTruthDirectory,
            'reporter_output_directory':this.reporterOutputDirectory
        };

        let url = '/new_report/calculating_page';
        this.http.get<any>(url,{params}).subscribe(res => {
            
            this.isBusy = false;
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