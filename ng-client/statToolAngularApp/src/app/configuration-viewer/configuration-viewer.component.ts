import { Component } from '@angular/core';
import { NewReportService } from '../services/new-report.service';

@Component({
  selector: 'configuration-viewer',
  templateUrl: './configuration-viewer.component.html',
  styleUrls: ['./configuration-viewer.component.css']
})
export class ConfigurationViewerComponent {
 
  constructor(public newReportService:NewReportService) {
  }

  title = 'New Configuration'

  close(){

  }

  disableSaveButton(){

    return (this.newReportService.selectedReadingFunction == '') || 
            (this.newReportService.selectedOverlapFunction == '') || 
            (this.newReportService.selectedTransformFunction == '') ||             
            (this.newReportService.selectedPartitioningFunction == '') ||             
            (this.newReportService.selectedStatisticsFunction == '') ||
            (this.newReportService.selectedEvaluationFunction == '') ||             
            (this.newReportService.configName == '') ||             
            (this.newReportService.treshold == '')      
 }
}
