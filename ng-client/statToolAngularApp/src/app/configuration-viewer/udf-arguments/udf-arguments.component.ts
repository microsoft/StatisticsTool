import { HttpClient } from '@angular/common/http';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { NewReportService, UDF } from 'src/app/services/new-report.service';

@Component({
  selector: 'udf-arguments',
  templateUrl: './udf-arguments.component.html',
  styleUrls: ['./udf-arguments.component.css']
})
export class UdfArgumentsComponent implements OnInit,OnDestroy {

  subscribeOpenArgs = new Subscription;
  
  @Input() top  = '';
  @Input() left = '';
  @Input() show = false;

  data:any;
  params:UDF.Param[] = [];
  
  constructor(public newReportSvc:NewReportService) {
  }

  ngOnInit() {
    this.subscribeOpenArgs = this.newReportSvc.showArgumentsEvent.subscribe(data => {
      this.data = data;
      this.params = data.udfItem.params;
    })
  }
  
  ngOnDestroy() {
    if (this.subscribeOpenArgs)
      this.subscribeOpenArgs.unsubscribe();
  }


  close(){
    this.newReportSvc.showParams = false;
  }
}
