import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'pkl-view',
  templateUrl: './pkl-view.component.html',
  styleUrls: ['./pkl-view.component.css']
})
export class PklViewComponent implements OnInit  {
    
  url = '/Reporter_new';
  //subscribeGetSegment = new Subscription;
  selectedRows = '';
  @Input() set selectedRowsSet(rows:string[]){
    this.selectedRows = rows.join(',');
  }
  @Input() selectedColumns = '';
  @Input() set selectedColumnsSet(cols:string[]){
    this.selectedColumns = cols.join(',');
  }
  @Input() name = '';
  @Input() id = 0;
  loadCounter = 0;

  subscribeUniqueChange = new Subscription;

  constructor(private httpClient:HttpClient,
              public statToolService:StatisticsToolService) {
    this.url = '/Reporter_new?calc_unique=' + statToolService.calculateUnique;
 }

  ngOnInit(): void {
    this.fixSelectedString();
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
    this.loadCounter = 1;

    this.subscribeUniqueChange = this.statToolService.uniqueValueChanged.subscribe(res => {
      this.loadCounter = 1;
      this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
    })
  }

   ngOnDestroy(){
    if (this.subscribeUniqueChange != null)
      this.subscribeUniqueChange.unsubscribe();
  }

  onColumnsChanged(items:{'item_id':string,'item_text':string}[]){
    this.selectedColumns = '';
    items.forEach(x => {
      this.selectedColumns += x.item_id + ","
    })

    this.fixSelectedString();
    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
   
    //console.log('url',this.url);
  }

  onRowsChanged(items:{'item_id':string,'item_text':string}[]){
    this.selectedRows = '';
    items.forEach(x => {
      this.selectedRows += x.item_id + ","
    })
    
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
    //console.log('url',this.url);
  }

  fixSelectedString(){
    if (this.selectedColumns.slice(-1) == ",")  
      this.selectedColumns = this.selectedColumns.slice(0,-1);
    if (this.selectedRows.slice(-1) == ",")  
      this.selectedRows = this.selectedRows.slice(0,-1);

  }

  onlaod(){
    //console.log('loaded...')
    this.loadCounter = this.loadCounter - 1;
  }

  onViewNameChanged(event:any){
    this.statToolService.updateSegmentationName(this.name,this.id,event.target.value);
  }

  removeView(){
    this.statToolService.removeView(this.id);
  }
}
