import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { NewReportService } from '../services/new-report.service';
import { ignoreElements } from 'rxjs';
import { UDFTypeEnum, UDFTitleEnum } from '../common/enums';

@Component({
  selector: 'configuration-viewer',
  templateUrl: './configuration-viewer.component.html',
  styleUrls: ['./configuration-viewer.component.css']
})
export class ConfigurationViewerComponent implements OnInit {

  @ViewChild('readingFunctionImg',      { static: false }) readingFunctionImgElement: ElementRef|null = null;
  @ViewChild('gtReadingFunctionImg',    { static: false }) gtReadingFunctionImgElement: ElementRef|null = null;
  @ViewChild('associationFunctionImg',  { static: false }) associationFunctionImgElement: ElementRef|null = null;
  @ViewChild('transformFunctionImg',    { static: false }) transformFunctionImgElement: ElementRef|null = null;
  @ViewChild('partitioningFunctionImg', { static: false }) partitioningFunctionImgElement: ElementRef|null = null;

  readonly title = 'New Configuration';

  showPredictionAguments = false;
  functionOpenedArguments = '';

  udfTitles = UDFTitleEnum;
  udfTypes  = UDFTypeEnum;

  readonly ARGUMENT_GRAY_ICON   = 'assets/argument-gray-icon.svg';
  readonly ARGUMENT_GREEN_ICON = 'assets/argument-green-icon.svg';
  readonly ARGUMENT_RED_ICON    = 'assets/argument-red-icon.svg';

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
    else if (this.newReportService.selectedPredictionReadingFunction != '' && !this.paramsHaveValue(UDFTypeEnum.READING_FUNCTIONS)) return true;

    if (!this.newReportService.gtReadingSameAsPrediction && this.newReportService.selectedGTReadingFunction == '') return true;
    else if (!this.newReportService.gtReadingSameAsPrediction && this.newReportService.selectedGTReadingFunction != '' && !this.paramsHaveValue(UDFTypeEnum.GT_READING_FUNCTIONS)) return true;
    
    if (this.newReportService.transformEnabled && this.newReportService.selectedTransformFunction == '') return true;
    else if (this.newReportService.transformEnabled && this.newReportService.selectedTransformFunction != '' && !this.paramsHaveValue(UDFTypeEnum.TRANSFORM_FUNCTIONS)) return true;

    if (this.newReportService.selectedStatisticsFunction == '') return true;
    else if (this.newReportService.selectedStatisticsFunction != '' && !this.paramsHaveValue(UDFTypeEnum.STATISTICS_FUNCTIONS)) return true;

    if (this.newReportService.partitioningEnabled && this.newReportService.selectedPartitioningFunction == '') return true;
    else if (this.newReportService.partitioningEnabled && this.newReportService.selectedPartitioningFunction != ''  && !this.paramsHaveValue(UDFTypeEnum.PARTITIONING_FUNCTIONS)) return true;

    if (this.newReportService.selectedConfusionFunction == '') return true;
    else if (this.newReportService.selectedConfusionFunction != '' && !this.paramsHaveValue(UDFTypeEnum.CONFUSION_FUNCTIONS)) return true;

    return false
      
  }

  getTitle(){
    if (this.newReportService.configName != '')
      return this.newReportService.configName;
    return 'New Configuration';
  }

  onPredictionReadingFunctionChange(event: Event) {

    this.newReportService.showParams = false;

    if (!this.functionHasArguments(UDFTypeEnum.READING_FUNCTIONS,this.newReportService.selectedPredictionReadingFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments(UDFTypeEnum.READING_FUNCTIONS,selectedValue);
    this.showArgumentsPanel(this.readingFunctionImgElement,
                            UDFTypeEnum.READING_FUNCTIONS,
                            UDFTitleEnum.PREDICTION_READING_FUNCTION,
                            this.newReportService.selectedPredictionReadingFunction,
                            true);
  }

  onGTReadingFunctionChange(event: Event) {

    this.newReportService.showParams = false;

    if (!this.functionHasArguments(UDFTypeEnum.GT_READING_FUNCTIONS,this.newReportService.selectedGTReadingFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments(UDFTypeEnum.GT_READING_FUNCTIONS,selectedValue);
    this.showArgumentsPanel(this.gtReadingFunctionImgElement,
                            UDFTypeEnum.GT_READING_FUNCTIONS,
                            this.udfTitles.GT_READING_FUNCTION,
                            this.newReportService.selectedGTReadingFunction,
                            true);

  }

  onAssociationFunctionChange(event: Event) {

    this.newReportService.showParams = false;

    if (!this.functionHasArguments(UDFTypeEnum.ASSOCIATION_FUNCTIONS,this.newReportService.selectedAssociationFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments(UDFTypeEnum.ASSOCIATION_FUNCTIONS,selectedValue);
    this.showArgumentsPanel(this.gtReadingFunctionImgElement,
      UDFTypeEnum.ASSOCIATION_FUNCTIONS,
      this.udfTitles.ASSOCIATION_FUNCTION,
      this.newReportService.selectedAssociationFunction,
      true);
  }

  onTransformFunctionChange(event: Event) {

    this.newReportService.showParams = false;

    if (!this.functionHasArguments(this.udfTypes.TRANSFORM_FUNCTIONS,this.newReportService.selectedTransformFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments(UDFTypeEnum.TRANSFORM_FUNCTIONS,selectedValue);
    this.showArgumentsPanel(this.transformFunctionImgElement,
      UDFTypeEnum.TRANSFORM_FUNCTIONS,
      UDFTitleEnum.TRANSFORM_FUNCTION,
      this.newReportService.selectedTransformFunction,
      true);
  }

  onPartitioningFunctionChange(event: Event) {

    this.newReportService.showParams = false;
    
    if (!this.functionHasArguments(UDFTypeEnum.PARTITIONING_FUNCTIONS,this.newReportService.selectedPartitioningFunction))
      return;

    const selectedValue = (event.target as HTMLSelectElement).value;
    this.newReportService.getUDFUserArguments(UDFTypeEnum.PARTITIONING_FUNCTIONS,selectedValue);
    this.showArgumentsPanel(this.partitioningFunctionImgElement,
      UDFTypeEnum.PARTITIONING_FUNCTIONS,
      UDFTitleEnum.PARTITIONING_FUNCTION,
      this.newReportService.selectedPartitioningFunction,
      true);
  }

  getArgumentSvg(funcType:UDFTypeEnum){
    if (funcType == UDFTypeEnum.READING_FUNCTIONS){
      if(this.newReportService.selectedPredictionReadingFunction == '')
        return this.ARGUMENT_GRAY_ICON;
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedPredictionReadingFunction))
          return this.ARGUMENT_GRAY_ICON;
        if (this.paramsHaveValue(this.udfTypes.READING_FUNCTIONS)){
          return this.ARGUMENT_GREEN_ICON;
        } else {
          return this.ARGUMENT_RED_ICON;
        }
      }
    }

    if (funcType == UDFTypeEnum.GT_READING_FUNCTIONS){
      if(this.newReportService.selectedGTReadingFunction == '' || this.newReportService.gtReadingSameAsPrediction)
        return this.ARGUMENT_GRAY_ICON;
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedGTReadingFunction))
          return this.ARGUMENT_GRAY_ICON;
        if (this.paramsHaveValue(UDFTypeEnum.GT_READING_FUNCTIONS)){
          return this.ARGUMENT_GREEN_ICON;
        } else {
          return this.ARGUMENT_RED_ICON;
        }
      }
    }

    if (funcType == UDFTypeEnum.ASSOCIATION_FUNCTIONS){
      if (this.newReportService.selectedAssociationFunction == '' || !this.newReportService.associationEnabled)
        return this.ARGUMENT_GRAY_ICON;
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedAssociationFunction))
          return this.ARGUMENT_GRAY_ICON;
        if (this.paramsHaveValue(this.udfTypes.ASSOCIATION_FUNCTIONS)){
          return this.ARGUMENT_GREEN_ICON;
        } else {
          return this.ARGUMENT_RED_ICON;
        }
      }
    }

    if (funcType == UDFTypeEnum.TRANSFORM_FUNCTIONS){
      if (this.newReportService.selectedTransformFunction == '' || !this.newReportService.transformEnabled)
        return this.ARGUMENT_GRAY_ICON;
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedTransformFunction))
          return this.ARGUMENT_GRAY_ICON;
        if (this.paramsHaveValue(UDFTypeEnum.TRANSFORM_FUNCTIONS)){
          return this.ARGUMENT_GREEN_ICON;
        } else {
          return this.ARGUMENT_RED_ICON;
        }
      }
    }

    if (funcType == UDFTypeEnum.PARTITIONING_FUNCTIONS){
      if (this.newReportService.selectedPartitioningFunction == '' || !this.newReportService.partitioningEnabled)
        return this.ARGUMENT_GRAY_ICON;
      else {
        if (!this.functionHasArguments(funcType,this.newReportService.selectedPartitioningFunction))
          return this.ARGUMENT_GRAY_ICON;
        if (this.paramsHaveValue(this.udfTypes.PARTITIONING_FUNCTIONS)){
          return this.ARGUMENT_GREEN_ICON;
        } else {
          return this.ARGUMENT_RED_ICON;
        }
      }
    }

    return this.ARGUMENT_RED_ICON;
  }

  showArgumentsPanel(elm:ElementRef|null,
                     funcType:UDFTypeEnum,
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
    this.newReportService.argPanelLeft = `${imgRect.right + window.scrollX + 10}px`;
    this.newReportService.showArgumentsPanel(funcType,title,funcName);  
    this.functionOpenedArguments = funcType;
  }

  enableArgumentsButton(funcType:UDFTypeEnum){
    if (funcType == UDFTypeEnum.READING_FUNCTIONS){
      if (this.newReportService.selectedPredictionReadingFunction != '' && 
          this.functionHasArguments(funcType,this.newReportService.selectedPredictionReadingFunction))
        return true;
      return false;
    }

    if (funcType == UDFTypeEnum.GT_READING_FUNCTIONS){
      if (this.newReportService.selectedGTReadingFunction != '' && !this.newReportService.gtReadingSameAsPrediction && 
          this.functionHasArguments(funcType,this.newReportService.selectedGTReadingFunction))
        return true;
      return false;
    }

    if (funcType == UDFTypeEnum.ASSOCIATION_FUNCTIONS){
      if (this.newReportService.selectedAssociationFunction != '' && this.newReportService.associationEnabled 
          && this.functionHasArguments(funcType,this.newReportService.selectedAssociationFunction))
        return true;
      return false;
    }

    if (funcType == UDFTypeEnum.TRANSFORM_FUNCTIONS){
      if (this.newReportService.selectedTransformFunction != '' && this.newReportService.transformEnabled 
          && this.functionHasArguments(funcType,this.newReportService.selectedTransformFunction))
        return true;
      return false;
    }

    if (funcType == UDFTypeEnum.PARTITIONING_FUNCTIONS  ){
      if (this.newReportService.selectedPartitioningFunction != '' && this.newReportService.partitioningEnabled 
          && this.functionHasArguments(funcType,this.newReportService.selectedPartitioningFunction))
        return true;
      return false;
    }

    return false;
  }

  paramsHaveValue(funcType:UDFTypeEnum){
    if (funcType == UDFTypeEnum.READING_FUNCTIONS){
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedPredictionReadingFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    if (funcType == UDFTypeEnum.GT_READING_FUNCTIONS){
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedGTReadingFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    if (funcType == UDFTypeEnum.ASSOCIATION_FUNCTIONS){
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedAssociationFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    if (funcType == UDFTypeEnum.TRANSFORM_FUNCTIONS){
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedTransformFunction)!;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '')
          b = false;
      })
      return b;
    } 

    return true;
  }

  checkboxChanged(funcType:UDFTypeEnum){
    if (funcType == UDFTypeEnum.GT_READING_FUNCTIONS){
      if (this.newReportService.gtReadingSameAsPrediction && this.functionOpenedArguments == funcType){
        this.newReportService.showParams = false;
      }
    }

    if (funcType == UDFTypeEnum.ASSOCIATION_FUNCTIONS){
      if (this.newReportService.associationEnabled && this.functionOpenedArguments == funcType){
        this.newReportService.showParams = false;
      }
    }

    if (funcType == UDFTypeEnum.TRANSFORM_FUNCTIONS){
      if (this.newReportService.transformEnabled && this.functionOpenedArguments == funcType){
        this.newReportService.showParams = false;
      }
    }

    if (funcType == UDFTypeEnum.PARTITIONING_FUNCTIONS){
      if (this.newReportService.partitioningEnabled && this.functionOpenedArguments == funcType){
          this.newReportService.showParams = false;
      }
    }
  }

  gtReadingRadioChanged(sameAsPredicted:boolean){

    if (sameAsPredicted){ 
      this.newReportService.gtReadingSameAsPrediction = true;
      this.newReportService.showParams = false;
    } else {
      this.newReportService.gtReadingSameAsPrediction = false;
      if (this.newReportService.selectedGTReadingFunction != '')
        this.newReportService.showParams = true;
      else 
        this.newReportService.showParams = false;
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

