import { Component } from '@angular/core';
import { NewReportService, SELECTE_SUITE } from '../services/new-report.service';

@Component({
  selector: 'save-suite-dialog',
  templateUrl: './save-suite-dialog.component.html',
  styleUrls: ['./save-suite-dialog.component.css']
})
export class SaveSuiteDialogComponent {
  
  suiteName = '';

  constructor(public newReportService:NewReportService) {
    
    let name = this.newReportService.getSelectedSuiteName();
    if (name == SELECTE_SUITE){
      this.suiteName = '';
    } else {
      this.suiteName = name;
    }
    
  }
  close(){
    this.newReportService.closeSaveSuiteDialog();
  }

  save(){
    if (this.suiteName == '')
      return;
    this.newReportService.saveSuite(this.suiteName)
    this.close();
  }

  disableSaveButton(){
    return false;
  }
}
