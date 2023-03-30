import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
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
  saveImgSrc = 'assets/back-icon-gray.svg';

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
    this.statService.calculateUnique = event.checked;
    this.statService.uniqueValueChanged.next(event.checked);
  }

  clickPanel(i:number){
    for(let x=0;x < this.statService.currentTemplate.SegmentationsClicked.length;x++){
      if (x == i){
        this.statService.currentTemplate.SegmentationsClicked[x] = !this.statService.currentTemplate.SegmentationsClicked[x];
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

    getHeight(i:number){
      if (this.statService.currentTemplate.SegmentationsClicked[i] == true)
        return '100vh';
      else
        return '0px';
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
 }
