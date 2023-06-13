import { Component } from '@angular/core';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'save-template-dialog',
  templateUrl: './save-template-dialog.component.html',
  styleUrls: ['./save-template-dialog.component.css']
})
export class SaveTemplateDialogComponent {

  templateName = '';

  constructor(public statService:StatisticsToolService) {
    let name = this.statService.getSelectedTemplateName();
    if (name == 'Default (Total)'){
      this.templateName = '';
    } else {
      this.templateName = name;
    }
    
  }
  close(){
    this.statService.closeSaveTempalteDialog();
  }

  save(){
    if (this.templateName == '')
      return;
    this.statService.saveTemplate(this.templateName)
    this.close();
  }

  disableSaveButton(){
    return false;
    return this.templateName == '';
  }
} 
