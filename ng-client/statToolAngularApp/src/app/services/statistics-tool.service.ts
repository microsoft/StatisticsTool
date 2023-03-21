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
  Segmentations:SegmentationItem[] = [];
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

@Injectable({
  providedIn: 'root'
})
export class StatisticsToolService implements OnInit {

  optionalSegmentations = new Map<string,string[]>();
  templatesFetched = new Subject();
  segmentationsFetched = new Subject();
  templates:TemplateInfo[] = [];
  currentTemplate:TemplateInfo = new TemplateInfo();
  
  //templates = [{'key':0,'value':'--- select ---'},{'key':1,'value':'Template 1'},{'key':2,'value':'Template 2'},{'key':3,'value':'Template 3'}]
  templateNameOptions:{'key':number,'value':string}[] = [];
  selectedTamplate = 0;
  //segmentOfTempateFetched = new Subject<{'template':string,'info':SegmentsInfo[]}>();

  //mapTemplateSegments = new Map<string,SegmentsInfo[]>();

  //dictonary of segmentations, for example: size => ['large','small','medium']
  

  //templates = new NS_GetAllTemplatesResponse.Response();

  constructor(private httpClient:HttpClient) { 
    this.httpClient.post<{'content':any,'name':string}[]>('/get_all_templates',{})
      .subscribe(res => {
        res.forEach(x => {
          let c:IContent = JSON.parse(JSON.stringify(x.content));
          let t = new TemplateInfo();
          t.name = x.name;
          c.segmentations.forEach(s => {
            let seg = new SegmentationItem();
            seg.columns = s.columns.split(',');
            seg.rows = s.rows.split(',');
            seg.name = s.name;
            t.Segmentations.push(seg);
          })  
          this.templates.push(t) ;
        })

        console.log('templates:',JSON.stringify(this.templates));

        //get all optional segments
        this.optionalSegmentations = new Map<string,string[]>();
        this.httpClient.post<{'name':string,'values':string[]}[]>('/get_segmentations',{})
          .subscribe(res => {
             res.forEach(x => {
              this.optionalSegmentations.set(x.name,x.values);
             })
          }
        )
        
        this.templateNameOptions = [];
        this.templateNameOptions.push({'key':0,'value':'--- select ---'});
        for(let i = 0;i< this.templates.length;i++){
          this.templateNameOptions.push({'key':(i+1),'value':this.templates[i].name});
        }
  
        this.templatesFetched.next(true);
      })
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
}
