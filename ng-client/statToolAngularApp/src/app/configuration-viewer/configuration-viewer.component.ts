import { Component, OnInit } from '@angular/core';
import { NewReportService } from '../services/new-report.service';

@Component({
  selector: 'configuration-viewer',
  templateUrl: './configuration-viewer.component.html',
  styleUrls: ['./configuration-viewer.component.css']
})
export class ConfigurationViewerComponent implements OnInit {

  title = 'New Configuration';

  showPredictionAguments = false;

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

  onPredictionReadingFunctionChange(event: Event) {
    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments('reading_functions',selectedValue);
  }

  onAssociationFunctionChange(event: Event) {
    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments('association_functions',selectedValue);
  }

  getArgumentSvg(udf:string){
    return 'assets/argument-red-icon.svg'
  }

  showArgumentsPanel(event: MouseEvent,funcType:string,title:string,funcName:string){
    this.newReportService.showParams = !this.newReportService.showParams;
    if (!this.newReportService.showParams)
      return;

    const button = event.target as HTMLElement;
    const buttonRect = button.getBoundingClientRect();
    
    this.newReportService.argPanelTop = `${buttonRect.top-40}px`;
    this.newReportService.argPanelLeft = `${buttonRect.right + window.scrollX}px`;
    this.newReportService.showArgumentsPanel(funcType,title,funcName);  
    //this.showPredictionAguments = !this.showPredictionAguments;    

    //this.openDiv(event);
  }

  openDiv(event: MouseEvent) {
    //this.showDiv = true;
    
  }

  enableArgumentsButton(funcType:string){
    if (funcType == 'reading_functions'){
      if (this.newReportService.selectedPredictionReadingFunction != '')
        return true;
      return false;
    }

    return false;

  }
}

