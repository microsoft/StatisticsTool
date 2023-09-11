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
    this.newReportService.showConfigViewer = false;
  }

  disableSaveButton(){
    if (this.newReportService.configName == '') return true;
    if (this.newReportService.selectedPredictionReadingFunction == '') return true;
    if (this.newReportService.selectedPredictionReadingFunction == '') return true;
    if (this.newReportService.gtReadingEnabled && this.newReportService.selectedGTReadingFunction == '') return true;
    if (this.newReportService.overlapEnabled && this.newReportService.selectedOverlapFunction == '') return true;
    if (this.newReportService.evaluateEnabled && this.newReportService.selectedEvaluationFunction == '') return true;
    if (this.newReportService.tresholdEnabled && this.newReportService.treshold == '') return true;
    if (this.newReportService.transformEnabled && this.newReportService.selectedTransformFunction == '') return true;
    if (this.newReportService.selectedStatisticsFunction == '') return true;
    if (this.newReportService.partitioningEnabled && this.newReportService.selectedPartitioningFunction == '') return true;
    if (this.newReportService.selectedConfusionFunction == '') return true;

    return false
      
 }

 getTitle(){
    if (this.newReportService.configName != '')
      return this.newReportService.configName;
    return 'New Configuration';
 }

  
}
