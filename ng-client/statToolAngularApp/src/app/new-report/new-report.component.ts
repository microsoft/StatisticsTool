import { Component, OnDestroy, OnInit } from '@angular/core';
import {Location} from '@angular/common';
import { NewReportService, SELECTE_SUITE } from '../services/new-report.service';
import { Observable, OperatorFunction, debounceTime, distinctUntilChanged, map } from 'rxjs';
import { LocalStorgeHelper } from '../services/localStorageHelper';

@Component({
  selector: 'new-report',
  templateUrl: './new-report.component.html',
  styleUrls: ['./new-report.component.css']
})
export class NewReportComponent implements OnInit, OnDestroy {

  constructor(private location:Location,
              public  newReportService:NewReportService){

  }
  
  ngOnInit(): void {
  }
  
  ngOnDestroy(): void {
  }

  backImgSrc = 'assets/back-icon-blue.svg';
  formatter = (result: string) => result.toUpperCase();

  public onFocus(e: Event): void {
    e.stopPropagation();
    setTimeout(() => {
      const inputEvent: Event = new Event('input');
      e.target!.dispatchEvent(inputEvent);
    }, 0);
  }

  searchPredictionsDirectory: OperatorFunction<string, readonly string[]> = (
    text$: Observable<string>
  ) =>
    text$.pipe(
      debounceTime(200),
      distinctUntilChanged(),
      map((term) =>
        term === ''
          ? this.newReportService.last_prediction_directory.slice(0,10)
          : this.newReportService.last_prediction_directory
              .filter((v) => v.toLowerCase().indexOf(term.toLowerCase()) > -1)
              .slice(0, 10)
      )
    );

    searchGTDirectroy: OperatorFunction<string, readonly string[]> = (
      text$: Observable<string>
    ) =>
      text$.pipe(
        debounceTime(200),
        distinctUntilChanged(),
        map((term) =>
          term === ''
            ? this.newReportService.last_ground_truth_directory
            : this.newReportService.last_ground_truth_directory
                .filter((v) => v.toLowerCase().indexOf(term.toLowerCase()) > -1)
                .slice(0, 10)
        )
      );  

      searchOutputDirectroy: OperatorFunction<string, readonly string[]> = (
        text$: Observable<string>
      ) =>
        text$.pipe(
          debounceTime(200),
          distinctUntilChanged(),
          map((term) =>
            term === ''
              ? this.newReportService.last_output_directory
              : this.newReportService.last_output_directory
                  .filter((v) => v.toLowerCase().indexOf(term.toLowerCase()) > -1)
                  .slice(0, 10)
          )
        );  

  back(){
    let path = this.location.path();
    console.log('path',path)
    if (path.indexOf('/static/') > 0){
      path = path.replace('/static/','/');
      console.log('path-remove-static',path)
    }
    window.location.href = 'http://127.0.0.1:5000/';
  }

  isSelectSuiteValid(){
    if (this.newReportService.selectedSuite != SELECTE_SUITE)
      return true;
    return false;
  }

  disableCreateReportButton(){
    return (this.newReportService.groundTruthDirectory.length < 3) || 
           (this.newReportService.predictionsDirectory.length < 3) || 
           (this.newReportService.reporterOutputDirectory.length < 3) ||
           (this.newReportService.getNumConfigsSelected() == 0)            
  }
}
