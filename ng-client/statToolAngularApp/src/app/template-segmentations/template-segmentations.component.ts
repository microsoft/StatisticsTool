import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { StatisticsToolService } from '../services/statistics-tool.service';
import {Location} from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'template-segmentations',
  templateUrl: './template-segmentations.component.html',
  styleUrls: ['./template-segmentations.component.css']
})
export class TemplateSegmentationsComponent implements OnInit {
  
  isNewTemplateMode = true;
  templateNameCreated = '';
  backImgSrc = 'assets/back-icon-blue.svg';
  saveImgSrc = 'assets/save-icon-blue.svg';


  constructor(private httpClient:HttpClient,
              public statService:StatisticsToolService,
              private location:Location,
              private router:Router) {
  }

  ngOnInit(): void {
    let sub = this.statService.segmentationsFetched.subscribe(res => {
      this.statService.addNewTemplate();
      sub.unsubscribe();
    })
  }

  ngOnDestroy(){
  }

  getViewHeight(index:number){
    
    var isViewPanelOpen = this.statService.currentTemplate.SegmentationsClicked[index];

    if (isViewPanelOpen)
      return this.statService.viewHeights.get(index);
    else
      return '0px';  
  }

  onTemplateSelected(event:any){
    let tempalteId = event.target.value;
    if (tempalteId == 0){ //new temmplate
      this.isNewTemplateMode = true;
      //this.statService.templates = [];
      if (this.statService.templates.length == 0)
        this.statService.addNewTemplate();
      return;
    }
    this.isNewTemplateMode = false;
    this.templateNameCreated = '';
    let t = this.statService.templateNameOptions.find(x => x.key == +tempalteId);
    if (t != undefined){
      this.statService.onTemplateSelected(t.value);
    }
  }

  getTemplateName(){
    if (!this.isNewTemplateMode && this.statService.selectedTamplate > 0){
      return this.statService.templateNameOptions.find(x => x.key == this.statService.selectedTamplate)!.value;
    }

    if (this.isNewTemplateMode && this.templateNameCreated.length > 0){
      return this.templateNameCreated;
    }

    return '';
  }

  getTemplateNameForTitle(){
    
    let t = this.getTemplateName();
    if (t.length > 0){
      return " - " + t.toLocaleUpperCase();
    }

    return '';
  }

  addView(){
    this.statService.addSegmentations();
  }

  saveTemplate(){
    if (this.isNewTemplateMode)
      this.statService.saveTemplate(true,this.templateNameCreated);
    else
      this.statService.saveTemplate(false);
  }

  slideUniqueChange(event:any){
    //console.log('slideUniqueChange',event.checked)
    //this.statService.calculateUnique = event.checked;
    //this.statService.uniqueValueChanged.next(event.checked);
    this.statService.uniqueValueChanged.next(this.statService.calculateUnique);
  }

  slideLocalDataStore(event:any){
    this.statService.saveLocalDataStoreInfoInStorage();      
  }

  clickPanel(i:number){
    for(let x=0;x < this.statService.currentTemplate.SegmentationsClicked.length;x++){
      if (x == i){
        this.statService.currentTemplate.SegmentationsClicked[x] = !this.statService.currentTemplate.SegmentationsClicked[x];
        /*console.log('view-clicked',
                    i,
                    this.statService.currentTemplate.SegmentationsClicked[x],
                    this.statService.viewHeights.get(x)
        );*/

      }
      //else
        //this.statService.currentTemplate.SegmentationsClicked[x] = false;
        //console.log('clicked - false',i,this.statService.currentTemplate.SegmentationsClicked[x]);
      }
    }

    getActiveCls(i:number) {
      if (this.statService.currentTemplate.SegmentationsClicked[i] == true){
        return 'active';
      }
      else
        return ''; 
    }

    agentHas(keyword:string) {
      return navigator.userAgent.toLowerCase().search(keyword.toLowerCase()) > -1;
    }

    isFireFox(){
      return this.agentHas("Firefox") || this.agentHas("FxiOS") || this.agentHas("Focus");
    }

    getHeight_deprecated(i:number):number{
      if (this.statService.currentTemplate.SegmentationsClicked[i] == true){
        let segments = this.statService.currentTemplate.Segmentations[i];
        
        let numRows = 1;
        segments.rows.forEach(r => {
          if (r != '') {
            let values = this.statService.optionalSegmentations.get(r);
            numRows = numRows*values!.length;
          }
        })
        let lineHeight = 22;
        let tableHeight = numRows * 8 * lineHeight;
        //if (this.statService.calculateUnique == false)
        //  tableHeight = numRows * 7 * 22; 

        let totalHeight = 0;
        const segmentRowHeight = 40;
        const segmentsFilterRowHeight = 70;
        const viewTitleHeight = 40;
        if (segments.columns.length == 0)
          totalHeight = tableHeight + segmentRowHeight + segmentsFilterRowHeight + viewTitleHeight;
        else
          totalHeight = tableHeight + (segments.columns.length * segmentRowHeight) + segmentsFilterRowHeight + viewTitleHeight;

        const bufferHeight = 20;  
        let height = (totalHeight + bufferHeight);
        
        return height;
      }
      else
        return 0;
    }

    getTitle(i:number){
      return this.statService.currentTemplate.Segmentations[i].name;
    }

    back(){
      let path = this.location.path();
      console.log('path',path)
      if (path.indexOf('/static/') > 0){
        path = path.replace('/static/','/');
        console.log('path-remove-static',path)
      }
      window.location.href = 'http://127.0.0.1:5000/';
    }

    getDisabledClass(){
      if (this.isNewTemplateMode){
        if (this.templateNameCreated.length == 0)
          return 'disabledImg';
      }

      return '';
    }

    localDataStoreChange(event:any){
      this.statService.saveLocalDataStoreInfoInStorage();
    }

    getLocalDataStoreCls(){
      if (this.statService.activeLocalDataStore){
        return '';
      } else {
        return 'disableLocalDataStore';
      }
    }
 }
