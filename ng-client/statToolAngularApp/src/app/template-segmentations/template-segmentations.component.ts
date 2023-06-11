import { HttpClient } from '@angular/common/http';
import { ApplicationRef, Component, ElementRef, OnInit } from '@angular/core';
import { StatisticsToolService } from '../services/statistics-tool.service';
import {Location} from '@angular/common';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';


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
  addGridImgSrc = 'assets/grid-add-blue.svg';

  subscribeSegmentsReady = new Subscription;

  constructor(
              public statService:StatisticsToolService,
              private location:Location) {
  }

  ngOnInit(): void {

    this.subscribeSegmentsReady = this.statService.segmentationsFetched.subscribe(selectedReport => {
      this.statService.addDefaultTemplate();
      this.statService.selectedReport = selectedReport;
      this.statService.reportSelected.next(true);
    })
  } 

  ngOnDestroy(){
    if (this.subscribeSegmentsReady != null)
      this.subscribeSegmentsReady.unsubscribe();
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
    
    this.isNewTemplateMode = false;
    this.templateNameCreated = '';
    let t = this.statService.templateNameOptions.find(x => x.key == +tempalteId);
    if (t != undefined){
      this.statService.onTemplateSelected(t.value);
    }
  }

  onReportSelected(event:any){
    this.statService.init('',event.target.value);
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
    this.statService.openSaveTemplateDialog();
  }

  slideUniqueChange(event:any){
    this.statService.uniqueValueChanged.next(this.statService.calculateUnique);
  }

  slideLocalDataStore(event:any){
    this.statService.saveLocalDataStoreInfoInStorage();      
  }

  clickPanel(i:number){
    for(let x=0;x < this.statService.currentTemplate.SegmentationsClicked.length;x++){
      if (x == i){
        this.statService.currentTemplate.SegmentationsClicked[x] = !this.statService.currentTemplate.SegmentationsClicked[x];
       }
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

    getSelectedMainReportTooltip(){
      if (this.statService.reportlistItems && this.statService.selectedReport in this.statService.reportlistItems)
        return this.statService.reportlistItems[this.statService.selectedReport].value;
      else
        return ''
    }

    getSelectedTemplateTooltip(){
      if (this.statService.templateNameOptions && this.statService.selectedTamplate in this.statService.templateNameOptions)
        return this.statService.templateNameOptions[this.statService.selectedTamplate].value;
      else
        return ''
    }

    disableUnique(){
      if (this.statService.getSelectedRefReport() == '')
        return true;
      return false;
    }
 }
