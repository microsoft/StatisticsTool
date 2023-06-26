import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { SaveSuiteDialogComponent } from "../save-suite-dialog/save-suite-dialog.component";

export const SELECTE_SUITE = '--- Select Suite ---';

@Injectable({
    providedIn: 'root'
  })

export class NewReportService {
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
    }

    configs:string[]  = [];
    suites:string []  = [];
    configsSelections = new Map<string,boolean>();
    selectedSuite = '';

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

        this.http.post<any>('/new_report/save_suite',{
            'suite':suiteName,
            'configurations':JSON.stringify(configs)
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
}