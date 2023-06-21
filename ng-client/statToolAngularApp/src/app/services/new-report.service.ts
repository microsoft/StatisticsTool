import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { SaveSuiteDialogComponent } from "../save-suite-dialog/save-suite-dialog.component";

export const SELECTE_SUITE = '--- Select Suite ---';

@Injectable({
    providedIn: 'root'
  })

export class NewReportService {

    constructor(private http:HttpClient,private modalService: NgbModal){

    }

    configs:string[]  = [];
    suites:string []  = [];
    configsSelections = new Map<string,boolean>();
    selectedSuite = '';

    init(configs:string,suites:string){
        
        this.configs = JSON.parse(configs);
        this.configs.sort((a,b) =>  (a > b ? 1 : -1));
        this.initSuitesList(JSON.parse(suites));    
        this.selectedSuite = SELECTE_SUITE;
        this.initSelectedConfigs();    
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
 
      showConfig(config:string){
        alert(config)
      }
}