import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'template-segmentations',
  templateUrl: './template-segmentations.component.html',
  styleUrls: ['./template-segmentations.component.css']
})
export class TemplateSegmentationsComponent implements OnInit {
  
  radioChecked = 'create';
  templateNameCreated = '';

  constructor(private httpClient:HttpClient,
              public statService:StatisticsToolService) {
  }

  ngOnInit(): void {
    let sub = this.statService.segmentationsFetched.subscribe(res => {
      this.statService.addNewTemplate();
      sub.unsubscribe();
    })
  }

  ngOnDestroy(){
  }

  isChecked(radio:string){
    if (radio == this.radioChecked)
      return true;
    return false;
  }

  onChangeRadio(e:any) {
    console.log('onChangeRadio',e.target.value)
    if (e.target.value == 'Load Template')
      this.radioChecked = 'load';
    else {
      this.radioChecked = 'create';
      this.statService.templates = [];
      this.statService.addNewTemplate();
    }
  }

  onTemplateSelected(event:any){
    let tempalteId = event.target.value;
    let t = this.statService.templateNameOptions.find(x => x.key == +tempalteId);
    if (t != undefined){
      this.statService.onTemplateSelected(t.value);
    }
  }

  getTemplateName(){
    if (this.radioChecked == 'load' && this.statService.selectedTamplate > 0){
      return this.statService.templateNameOptions.find(x => x.key == this.statService.selectedTamplate)!.value;
    }

    if (this.radioChecked == 'create' && this.templateNameCreated.length > 0){
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
    if (this.radioChecked == 'create')
      this.statService.saveTemplate(true,this.templateNameCreated);
    else
      this.statService.saveTemplate(false);

  }
}
