import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { NewReportService } from '../services/new-report.service';
import { ignoreElements } from 'rxjs';

@Component({
  selector: 'configuration-viewer',
  templateUrl: './configuration-viewer.component.html',
  styleUrls: ['./configuration-viewer.component.css']
})
export class ConfigurationViewerComponent implements OnInit {

  @ViewChild('readingFunctionImg', { static: false }) readingFunctionImgElement: ElementRef|null = null;

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

  getArgumentSvg(funcType:string){
    
    if (funcType == 'prediction_reading_functions'){
      if(this.newReportService.selectedPredictionReadingFunction == '')
        return 'assets/argument-gray-icon.svg'
      else {
        if (this.paramsHaveValue('prediction_reading_functions')){
          return 'assets/argument-green-icon.svg'
        } else {
          return 'assets/argument-red-icon.svg'
        }
      }
    }
    return 'assets/argument-red-icon.svg'
  }

  showArgumentsPanel(elm:ElementRef|null,
                     funcType:string,
                     title:string,
                     funcName:string){
                     
    this.newReportService.showParams = !this.newReportService.showParams;
    if (!this.newReportService.showParams)
      return;

    if (elm == null)
      return;                     

    const img: HTMLElement = elm.nativeElement;
    const imgRect = img.getBoundingClientRect();
    this.newReportService.argPanelTop  = `${imgRect.top-40}px`;
    this.newReportService.argPanelLeft = `${imgRect.right + window.scrollX}px`;
    this.newReportService.showArgumentsPanel(funcType,title,funcName);  
  }

  openDiv(event: MouseEvent) {
    //this.showDiv = true;
    
  }

  enableArgumentsButton(funcType:string){
    if (funcType == 'prediction_reading_functions'){
      if (this.newReportService.selectedPredictionReadingFunction != '')
        return true;
      return false;
    }

    return false;

  }

  paramsHaveValue(funcType:string){
    if (funcType == 'prediction_reading_functions'){
      let x = this.newReportService.udf.get('reading_functions')?.find(x => x.funcName == this.newReportService.selectedPredictionReadingFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    return true;
  }
}

