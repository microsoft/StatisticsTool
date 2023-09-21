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
  @ViewChild('gtReadingFunctionImg', { static: false }) gtReadingFunctionImgElement: ElementRef|null = null;
  @ViewChild('associationFunctionImg', { static: false }) associationFunctionImgElement: ElementRef|null = null;
  @ViewChild('transformFunctionImg', { static: false }) transformFunctionImgElement: ElementRef|null = null;

  title = 'New Configuration';

  showPredictionAguments = false;
  functionOpenedArguments = '';

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
    if (!this.functionHasArguments('reading_functions',this.newReportService.selectedPredictionReadingFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments('reading_functions',selectedValue);
    this.showArgumentsPanel(this.readingFunctionImgElement,
                            'reading_functions',
                            'Prediction Reading Function',
                            this.newReportService.selectedPredictionReadingFunction,
                            true);
  }

  onGTReadingFunctionChange(event: Event) {
    if (!this.functionHasArguments('gt_reading_functions',this.newReportService.selectedGTReadingFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments('gt_reading_functions',selectedValue);
    this.showArgumentsPanel(this.gtReadingFunctionImgElement,
                            'gt_reading_functions',
                            'GT Reading Function',
                            this.newReportService.selectedGTReadingFunction,
                            true);

  }

  onAssociationFunctionChange(event: Event) {
    if (!this.functionHasArguments('association_functions',this.newReportService.selectedAssociationFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments('association_functions',selectedValue);
    this.showArgumentsPanel(this.gtReadingFunctionImgElement,
      'association_functions',
      'Association Function',
      this.newReportService.selectedAssociationFunction,
      true);
  }

  onTransformFunctionChange(event: Event) {
    if (!this.functionHasArguments('transform_functions',this.newReportService.selectedTransformFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments('transform_functions',selectedValue);
    this.showArgumentsPanel(this.transformFunctionImgElement,
      'transform_functions',
      'Transform Function',
      this.newReportService.selectedTransformFunction,
      true);
  }

  getArgumentSvg(funcType:string){
    if (funcType == 'reading_functions'){
      if(this.newReportService.selectedPredictionReadingFunction == '')
        return 'assets/argument-gray-icon.svg'
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedPredictionReadingFunction))
          return 'assets/argument-gray-icon.svg'
        if (this.paramsHaveValue('reading_functions')){
          return 'assets/argument-green-icon.svg'
        } else {
          return 'assets/argument-red-icon.svg'
        }
      }
    }

    if (funcType == 'gt_reading_functions'){
      if(this.newReportService.selectedGTReadingFunction == '' || this.newReportService.gtReadingSameAsPrediction)
        return 'assets/argument-gray-icon.svg'
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedGTReadingFunction))
          return 'assets/argument-gray-icon.svg'
        if (this.paramsHaveValue('gt_reading_functions')){
          return 'assets/argument-green-icon.svg'
        } else {
          return 'assets/argument-red-icon.svg'
        }
      }
    }

    if (funcType == 'association_functions'){
      if (this.newReportService.selectedAssociationFunction == '' || !this.newReportService.associationEnabled)
        return 'assets/argument-gray-icon.svg';
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedAssociationFunction))
          return 'assets/argument-gray-icon.svg'
        if (this.paramsHaveValue('association_functions')){
          return 'assets/argument-green-icon.svg'
        } else {
          return 'assets/argument-red-icon.svg'
        }
      }
    }

    if (funcType == 'transform_functions'){
      if (this.newReportService.selectedTransformFunction == '' || !this.newReportService.transformEnabled)
        return 'assets/argument-gray-icon.svg';
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedTransformFunction))
          return 'assets/argument-gray-icon.svg'
        if (this.paramsHaveValue('transform_functions')){
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
                     funcName:string,
                     forceShow = false){
    if (forceShow){
      this.newReportService.showParams = true;
    } else {                     
      this.newReportService.showParams = !this.newReportService.showParams;
      if (!this.newReportService.showParams)
        return;
    }

    if (elm == null)
      return;                     

    const img: HTMLElement = elm.nativeElement;
    const imgRect = img.getBoundingClientRect();
    this.newReportService.argPanelTop  = `${imgRect.top-40}px`;
    this.newReportService.argPanelLeft = `${imgRect.right + window.scrollX}px`;
    this.newReportService.showArgumentsPanel(funcType,title,funcName);  
    this.functionOpenedArguments = funcType;
  }

  enableArgumentsButton(funcType:string){
    if (funcType == 'reading_functions'){
      if (this.newReportService.selectedPredictionReadingFunction != '' && 
          this.functionHasArguments(funcType,this.newReportService.selectedPredictionReadingFunction))
        return true;
      return false;
    }

    if (funcType == 'gt_reading_functions'){
      if (this.newReportService.selectedGTReadingFunction != '' && !this.newReportService.gtReadingSameAsPrediction && 
          this.functionHasArguments(funcType,this.newReportService.selectedGTReadingFunction))
        return true;
      return false;
    }

    if (funcType == 'association_functions'){
      if (this.newReportService.selectedAssociationFunction != '' && this.newReportService.associationEnabled 
          && this.functionHasArguments(funcType,this.newReportService.selectedAssociationFunction))
        return true;
      return false;
    }

    if (funcType == 'transform_functions'){
      if (this.newReportService.selectedTransformFunction != '' && this.newReportService.transformEnabled 
          && this.functionHasArguments(funcType,this.newReportService.selectedTransformFunction))
        return true;
      return false;
    }

    return false;
  }

  paramsHaveValue(funcType:string){
    if (funcType == 'reading_functions'){
      let x = this.newReportService.udf.get('reading_functions')?.find(x => x.funcName == this.newReportService.selectedPredictionReadingFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    if (funcType == 'gt_reading_functions'){
      let x = this.newReportService.udf.get('gt_reading_functions')?.find(x => x.funcName == this.newReportService.selectedGTReadingFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    if (funcType == 'association_functions'){
      let x = this.newReportService.udf.get('association_functions')?.find(x => x.funcName == this.newReportService.selectedAssociationFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    if (funcType == 'transform_functions'){
      let x = this.newReportService.udf.get('transform_functions')?.find(x => x.funcName == this.newReportService.selectedTransformFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    return true;
  }

  checkboxChanged(funcType:string){
    if (funcType == 'gt_reading_functions'){
      if (this.newReportService.gtReadingSameAsPrediction && this.functionOpenedArguments == 'gt_reading_functions'){
        this.newReportService.showParams = false;
      }
    }

    if (funcType == 'association_functions'){
      if (this.newReportService.associationEnabled && this.functionOpenedArguments == 'association_functions'){
        this.newReportService.showParams = false;
      }
    }

    if (funcType == 'transform_functions'){
      if (this.newReportService.transformEnabled && this.functionOpenedArguments == 'transform_functions'){
        this.newReportService.showParams = false;
      }
    }
  }

  functionHasArguments(funcType:string,funcName:string){
    let funcs = this.newReportService.udf.get(funcType);
    if (funcs != undefined){
      let f = funcs.find(x => x.funcName == funcName);
      if (f != undefined){
        return f.params.length > 0;
      }
    }

    return false;
  }
}

