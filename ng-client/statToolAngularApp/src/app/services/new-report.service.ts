import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { SaveSuiteDialogComponent } from "../save-suite-dialog/save-suite-dialog.component";
import { config } from "rxjs";

export const SELECTE_SUITE = '--- Select Suite ---';

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

@Injectable({
    providedIn: 'root'
  })

export class NewReportService {
    
    showConfigViewer = true;

    configs:string[]  = [];
    suites:string []  = [];
    configsSelections = new Map<string,boolean>();
    selectedSuite = '';


    reading_functions:string[] = [];
    evaluation_functions:string[] = [];
    overlap_functions:string[] = [];
    partitioning_functions:string[] = [];
    statistics_functions:string[] = [];
    transform_functions:string[] = [];
    
    selectedReadingFunction = '';
    selectedOverlapFunction = '';
    selectedTransformFunction = '';
    selectedPartitioningFunction = '';
    selectedStatisticsFunction = '';
    selectedEvaluationFunction = '';

    configName = '';
    logName = '';
    treshold = '';

    predictionsDirectory = '';
    groundTruthDirectory = '';
    reporterOutputDirectory = '';

    newReportResult = new NewReportResult();

    creatingReport = false;

    constructor(private http:HttpClient,private modalService: NgbModal){

        let url = '/new_report/get_all_user_defined_functions';
        this.http.get<string[]>(url).subscribe(functions => {
            
            let map:any;
            map = functions;
            this.reading_functions = map.reading_functions;
            this.reading_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.evaluation_functions = map.evaluation_functions;
            this.evaluation_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.overlap_functions = map.overlap_functions;
            this.overlap_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.partitioning_functions = map.partitioning_functions;
            this.partitioning_functions.sort((a,b) =>  (a > b ? 1 : -1));
            
            this.statistics_functions = map.statistics_functions;
            this.statistics_functions.sort((a,b) =>  (a > b ? 1 : -1));

            this.transform_functions = map.transform_functions;
            this.transform_functions.sort((a,b) =>  (a > b ? 1 : -1));
            let trans:string[] = [];
            trans.push('None');
            trans.concat(this.transform_functions)
            this.transform_functions = trans;
        })

        this.predictionsDirectory = localStorage.getItem('predictions_directory') != null ? localStorage.getItem('predictions_directory')! : '';
        this.groundTruthDirectory = localStorage.getItem('ground_truth_directory') != null ? this.groundTruthDirectory = localStorage.getItem('ground_truth_directory')! : '';
        this.reporterOutputDirectory = localStorage.getItem('reporter_output_directory') != null ? localStorage.getItem('reporter_output_directory')! : '';
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
        this.configsSelections.set(config.toLocaleLowerCase(),event.target.checked)
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
        this.selectedReadingFunction = '';
        this.selectedOverlapFunction = '';
        this.selectedTransformFunction = '';
        this.selectedPartitioningFunction = '';
        this.selectedStatisticsFunction = '';
        this.selectedEvaluationFunction = '';
    
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
            this.selectedReadingFunction = config['File Reading Function'];
            this.selectedOverlapFunction = config['Overlap Function'];
            this.selectedTransformFunction = config['Transformation Function'];
            this.selectedPartitioningFunction = config['Partitioning Functions'];
            this.selectedStatisticsFunction = config['Statistics Functions'];
            this.selectedEvaluationFunction = config['Evaluation Function'];
        
            this.configName = configName;
            this.logName = '';
            this.treshold = config['Threshold'];
        })
    }

    saveConfig(){
        const dictionary: { [key: string]: any } = {};

        dictionary['File Reading Function'] = this.selectedReadingFunction;
        dictionary['Overlap Function'] = this.selectedOverlapFunction;
        dictionary['Transformation Function'] = this.selectedTransformFunction;
        dictionary['Partitioning Functions'] = this.selectedPartitioningFunction;
        dictionary['Statistics Functions'] = this.selectedStatisticsFunction;
        dictionary['Evaluation Function'] = this.selectedEvaluationFunction;
        dictionary['configName'] = this.configName;
        dictionary['Log Names to Evaluate'] = this.logName;
        dictionary['Threshold'] = this.treshold;

        const url = '/new_report/save_configuration'; 

        this.http.post(url, dictionary).subscribe(response => {
            let configs:any;
            configs = response;
            ///this.parseConfigs(configs);
            this.configs = configs;
            this.configs.sort((a,b) =>  (a > b ? 1 : -1));
        })
    }

    createReport(){
        this.creatingReport = true;
        this.newReportResult = new NewReportResult();
        this.newReportResult.link = '';
        
        this.newReportResult.errorMessage = '';
        this.newReportResult.ok = false;

        localStorage.setItem('predictions_directory',this.predictionsDirectory);
        localStorage.setItem('ground_truth_directory',this.groundTruthDirectory);
        localStorage.setItem('reporter_output_directory',this.reporterOutputDirectory);

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
        if (this.newReportResult.files.length > 0)
            return true;
        if (this.newReportResult.errorMessage.length > 0)
            return true;

        return false;
    }
}