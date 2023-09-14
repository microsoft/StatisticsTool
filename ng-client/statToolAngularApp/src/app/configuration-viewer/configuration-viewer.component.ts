import { Component, OnInit } from '@angular/core';
import { NewReportService } from '../services/new-report.service';

@Component({
  selector: 'configuration-viewer',
  templateUrl: './configuration-viewer.component.html',
  styleUrls: ['./configuration-viewer.component.css']
})
export class ConfigurationViewerComponent implements OnInit {

  title = 'New Configuration'

  constructor(public newReportService:NewReportService) {
  }
  
  ngOnInit(): void {
  }

  togglePanel() {
    this.newReportService.isPanelOpen = !this.newReportService.isPanelOpen;
  }

  close(){
    this.newReportService.showConfigViewer = false;
  }

  disableSaveButton(){
    if (this.newReportService.configName == '') return true;
    if (this.newReportService.selectedPredictionReadingFunction == '') return true;
    if (this.newReportService.selectedPredictionReadingFunction == '') return true;
    if (!this.newReportService.gtReadingSameAsPrediction && this.newReportService.selectedGTReadingFunction == '') return true;
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

  getGtReadingLabel(){
    if (this.newReportService.gtReadingSameAsPrediction)
      return "GT Reading Function (same as prediction):";
    else
      return "GT Reading Function:";
  }

  onAssociationFunctionChange(event: Event) {
    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments('association_functions',selectedValue);
  }
}
