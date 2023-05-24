import { HttpClient } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { connect, Subject } from 'rxjs';


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

  //templates = [{'key':0,'value':'--- select ---'},{'key':1,'value':'Template 1'},{'key':2,'value':'Template 2'},{'key':3,'value':'Template 3'}]
  templateNameOptions:{'key':number,'value':string}[] = [];
  selectedTamplate = 0;
  selectedSubKey = 0;

  showDrawer = false;

  drawerUpdateListUrl = '';
  drawerShowImageUrl = '';

  activeLocalDataStore = false;
  localDataStorePath = '';

  currentConfigKey = '';
  subKeys:{'key':number,'value':string}[] = [];

  constructor(private httpClient:HttpClient) { 
    
  }
  
  init(subKeySelected:number = 0){

    this.templates = [];
    this.currentTemplate = new TemplateInfo();
    this.templateNameOptions = [];
    
    let url = '/get_all_templates' 
    this.httpClient.post<{'content':IContent,'name':string}[]>
      (url,{
        'key':this.currentConfigKey,
        'sub_key': this.getSelectedSubKey()
      })
      .subscribe(res => {
        this.processTemplates(res);

        this.updateTemplateNames();       

        this.loadSegmentations(subKeySelected);
      })

      this.readLocalDataStoreInfoFromStorage();
  }

  loadSegmentations(subKeySelected:number = 0){
    //get all optional segments
    this.optionalSegmentations = new Map<string,string[]>();
    this.httpClient.post<{'name':string,'values':string[]}[]>
      ('/get_segmentations',
        {
          'key':this.currentConfigKey,
          'sub_key': this.subKeys[this.selectedSubKey].value
        }
      )
      .subscribe(res => {
         res.forEach(x => {
          this.optionalSegmentations.set(x.name,x.values);
         })
         this.segmentationsFetched.next(subKeySelected);
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
    this.templateNameOptions.push({'key':0,'value':'--- New Template ---'});
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
  
  addNewTemplate(){
    let t = this.templates.find(x => x.name == "")
    if (t == undefined){
      t = new TemplateInfo();
    }
    t.name = "";
    let s = new SegmentationItem();
    s.name = 'Total';
    s.columns = [];
    s.rows = [];
    t.Segmentations.push(s);
    t.SegmentationsClicked.push(true);
    this.templates.push(t);
    this.currentTemplate = t;
    console.log('addNewTemplate',JSON.stringify(this.templates),'current:',JSON.stringify(this.currentTemplate));
  }

  addSegmentations(){
    //this.currentTemplate.wasChanged = true;
    this.currentTemplate.Segmentations.push(new SegmentationItem());
    this.currentTemplate.SegmentationsClicked.push(true);
  }

  saveTemplate(isNewTemplate:boolean,newTemplateName:string = ''){
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
      'sub_key': this.getSelectedSubKey()
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

  getSelectedSubKey(){
    return this.subKeys[this.selectedSubKey].value;
  }
}
