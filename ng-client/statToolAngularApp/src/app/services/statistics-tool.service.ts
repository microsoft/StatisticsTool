import { HttpClient } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { connect, Subject } from 'rxjs';
import { SaveTemplateDialogComponent } from '../save-template-dialog/save-template-dialog.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';


export class SegmentationItem {
  name = '';
  columns:string[] = [];
  rows:string[] = [];
}

export class TemplateInfo {
  //wasChanged = false;
  Segmentations:SegmentationItem[] = [];
  SegmentationsClicked:boolean[] = [];
  name = '';
}

interface ISegmentation {
  columns:string;
  name:string;
  rows:string;
}
interface IContent {
  segmentations:ISegmentation[];
}

export class SaveTemplate_SegmentItem{
  name = '';
  rows = '';
  columns = '';
}
export class SaveTemplateRequest {
  name = '';
  segmentations:SaveTemplate_SegmentItem [] = [];
}

@Injectable({
  providedIn: 'root'
})
export class StatisticsToolService implements OnInit {

  optionalSegmentations = new Map<string,string[]>();
  segmentationsFetched = new Subject<number>();
  openDrawer = new Subject<string>();
  uniqueValueChanged = new Subject<boolean>();
  viewHeights = new Map<number,string>();
  reportSelected = new Subject();
    
  templates:TemplateInfo[] = [];
  currentTemplate:TemplateInfo = new TemplateInfo();
  calculateUnique = false;
  fileNotFoundError = '';

  templateNameOptions:{'key':number,'value':string}[] = [];
  selectedTamplate = 0;
  selectedReport = 0;

  showDrawer = false;

  drawerUpdateListUrl = '';
  drawerShowImageUrl = '';

  activeLocalDataStore = false;
  localDataStorePath = '';

  currentConfigKey = '';
  subKeys:{'key':number,'value':string}[] = [];
  ref_dir = '';

  mainRefPairs:{'main':string,'ref':string}[] = [];
  reportlistItems:{'key':number,'value':string}[] = []

  
  constructor(private httpClient:HttpClient,private modalService: NgbModal) { 
    
  }
  
  init(reportsPairs:string = '',selectedReport:number = 0){
    this.processReportsPairs(reportsPairs);
    this.templates = [];
    this.currentTemplate = new TemplateInfo();
    this.templateNameOptions = [];
    this.selectedTamplate = 0;
    
    let main = this.reportlistItems.find(x => x.key == selectedReport)!;
    let ref = this.mainRefPairs.find(x => x.main == main.value);

    let url = '/get_all_templates';
    this.httpClient.post<{'content':IContent,'name':string}[]>
      (url,{
        'main':main.value,
        'ref': ref!.ref,
      })
      .subscribe(res => {
        this.processTemplates(res);

        this.updateTemplateNames();       

        this.loadSegmentations(selectedReport);
      })

      this.readLocalDataStoreInfoFromStorage();
  }

  processReportsPairs(reportPairs:string){
    if (reportPairs == '')
      return;
    
      this.mainRefPairs = JSON.parse(reportPairs);
      this.reportlistItems = [];
      let index = 0;
      this.mainRefPairs.forEach(pair => {
        let parts = pair.main.split("\\");
        this.reportlistItems.push({'key':index,'value':pair.main})
        index++;
      })
  }

  getReportDesc(reportfileName:string){
    let parts = reportfileName.split("\\");
    let dir = parts[parts.length-2];
    let file = parts[parts.length-1];
    return dir + "\\" + file;
  }

  loadSegmentations(selectedReport:number = 0){
    //get all optional segments
    let main = this.reportlistItems.find(x => x.key == selectedReport)!;

    this.optionalSegmentations = new Map<string,string[]>();
    this.httpClient.post<{'name':string,'values':string[]}[]>
      ('/get_segmentations',
        {
          'main': main.value
        }
      )
      .subscribe(res => {
         res.forEach(x => {
          this.optionalSegmentations.set(x.name,x.values);
         })
         this.segmentationsFetched.next(selectedReport);
      }
    )
  }

  processTemplates(items:{'content':IContent,'name':string}[]){
    items.forEach(x => {
      let c:IContent = JSON.parse(JSON.stringify(x.content));
      let t = new TemplateInfo();
      t.name = x.name;
      c.segmentations.forEach(s => {
        let seg = new SegmentationItem();
        seg.columns = s.columns.split(',');
        seg.rows = s.rows.split(',');
        seg.name = s.name;
        t.Segmentations.push(seg);
        t.SegmentationsClicked.push(true)
      })  
      this.templates.push(t) ;
    })
  }

  updateTemplateNames(){
    this.templateNameOptions = [];
    this.templateNameOptions.push({'key':0,'value':'Default (Total)'});
    for(let i = 0;i< this.templates.length;i++){
      if (this.templates[i].name != '')
        this.templateNameOptions.push({'key':(i+1),'value':this.templates[i].name});
    }
  }

  ngOnInit(): void {
        
  }

  getSegmentations(){
    /*let keys:string[] = [];
    this.optionalSegmentations.forEach((v,k) => {
      keys.push(k)
    });

    return keys;*/
    return '';
  }

  onTemplateSelected(templateName:string){
    this.currentTemplate = this.templates.find(x => x.name == templateName)!;
    let find = this.templateNameOptions.find(x => x.value == templateName);
    this.selectedTamplate = find!.key;
  }

  getTemplateSegments(templateName:string,index:number,isRows:boolean){
    /*let seg = this.mapTemplateSegments.get(templateName)!
    if (isRows)
      return seg[index].rows;
    else
      return seg[index].columns;*/
  }

  updateSegments(id:number,templateName:string,csvColumns:string,csvRows:string){
    let cols = csvColumns.split(",");
    let rows = csvRows.split(",");
    this.currentTemplate.Segmentations[id].columns = cols;
    this.currentTemplate.Segmentations[id].rows = rows;
    //this.currentTemplate.wasChanged = true;
  }

  updateSegmentationName(templateName:string,id:number,segName:string){
    this.currentTemplate.Segmentations[id].name = segName;
    //this.currentTemplate.wasChanged = true;
  }
  
  addDefaultTemplate(){
    let t = this.templates.find(x => x.name == "")
    if (t == undefined){
      t = new TemplateInfo();
    }
    t.name = "Default (Total)";
    let s = new SegmentationItem();
    s.name = 'Total';
    s.columns = [];
    s.rows = [];
    t.Segmentations.push(s);
    t.SegmentationsClicked.push(true);
    this.templates.push(t);
    this.currentTemplate = t;
  }

  addSegmentations(){
    //this.currentTemplate.wasChanged = true;
    this.currentTemplate.Segmentations.push(new SegmentationItem());
    this.currentTemplate.SegmentationsClicked.push(true);
  }

  saveTemplate(templateName:string){

    let req = new SaveTemplateRequest();
    req.name = templateName;
    this.currentTemplate.Segmentations.forEach(s => {
      let seg = new SaveTemplate_SegmentItem();
      seg.columns = s.columns.join(",");
      seg.rows = s.rows.join(",");
      seg.name = s.name;
      req.segmentations.push(seg);
    })
    
    this.httpClient.post<any>('/save_template',{
      'name':templateName,
      'content':JSON.stringify(req),
      'key': this.currentConfigKey,
      'sub_key': this.getSelectedMainReport(),
      'ref_dir':this.ref_dir
    }).subscribe(res => {

      this.templates = [];
      this.processTemplates(res);
      this.updateTemplateNames();       
      this.onTemplateSelected(templateName);
    })
  }

  saveTemplate_old(isNewTemplate:boolean,newTemplateName:string = ''){
    let template_name = this.currentTemplate.name;
    if (isNewTemplate)
      template_name = newTemplateName;

    let req = new SaveTemplateRequest();
    req.name = template_name;
    this.currentTemplate.Segmentations.forEach(s => {
      let seg = new SaveTemplate_SegmentItem();
      seg.columns = s.columns.join(",");
      seg.rows = s.rows.join(",");
      seg.name = s.name;
      req.segmentations.push(seg);
    })
    
    this.httpClient.post<any>('/save_template',{
      'name':template_name,
      'content':JSON.stringify(req),
      'key': this.currentConfigKey,
      'sub_key': this.getSelectedMainReport()
    }).subscribe(res => {

      this.templates = [];
      this.processTemplates(res);
      this.updateTemplateNames();       
      this.onTemplateSelected(template_name);
    })
  }

  removeView(viewId:number) {
    let segments:SegmentationItem[] = [];
    for(let i = 0; i< this.currentTemplate.Segmentations.length;i++){
      let item = this.currentTemplate.Segmentations[i];
      if (i != viewId){
        segments.push(item);
      } 
    }

    this.currentTemplate.Segmentations = segments;
  }

  getDrawerUpdateListUrl(){
    return this.drawerUpdateListUrl;
  }

  getDrawerShowImageUrl(){
    return this.drawerShowImageUrl;
  }

  readLocalDataStoreInfoFromStorage(){
    this.localDataStorePath = localStorage.getItem('LOCAL_DATA_STORE')!;
    this.activeLocalDataStore = localStorage.getItem('ACTIVATE_LOCAL_DATA_STORE')! == "true" ? true : false;
  }

  saveLocalDataStoreInfoInStorage(){
    localStorage.setItem('LOCAL_DATA_STORE',this.localDataStorePath);
    localStorage.setItem('ACTIVATE_LOCAL_DATA_STORE',this.activeLocalDataStore ? 'true' : 'false');
  }

  showFileNotFoundError(){
    return this.fileNotFoundError.length > 0;
  }

  loadSubKeys(str:string){
    this.subKeys = [];
    let items = str.split(",");
    let index = 0;
    items.forEach(s => {
      if (s != ''){
        this.subKeys.push({'key':index,'value':s});
        index++;
      }
    })
  }

  getSelectedMainReport(){
    let main = this.reportlistItems[this.selectedReport];
    return main.value;
  }

  getSelectedRefReport(){
    let main = this.reportlistItems[this.selectedReport];
    let ref = this.mainRefPairs.find(x => x.main == main.value);
    if (ref != undefined)
      return ref.ref;
    return '';
  }

  

  openSaveTemplateDialog(){
    this.modalService.open(SaveTemplateDialogComponent,{ centered: true }).result.then(res => {
    });    
  }

  closeSaveTempalteDialog(){
    this.modalService.dismissAll();
  }

  getSelectedTemplateName(){
    return this.templateNameOptions[this.selectedTamplate].value;
  }
}
