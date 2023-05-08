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
    //filter only the existing rows
    let tmp:string[] = [];
    let keys = Array.from( this.statToolService.optionalSegmentations.keys() );
    rows.forEach(r => {
      let isExist = keys.find(x => x == r)
      if (isExist)
      tmp.push(r)
    })

    this.selectedRows = tmp.join(',');
  }
  @Input() selectedColumns = '';
  @Input() set selectedColumnsSet(cols:string[]){
        //filter only the existing columns
        let tmp:string[] = [];
        let keys = Array.from( this.statToolService.optionalSegmentations.keys() );
        cols.forEach(c => {
          let isExist = keys.find(x => x == c)
          if (isExist)
          tmp.push(c)
        })
    
        this.selectedColumns = tmp.join(',');
  }
  @Input() name = '';
  @Input() id = 0;
  loadCounter = 0;

  subscribeUniqueChange = new Subscription;

  @Input() height:string = '';

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

  onColumnAdded(item:{'item_id':string,'item_text':string}){
    if (this.selectedColumns.length == 0 )
      this.selectedColumns = item.item_id;
    else
      this.selectedColumns += "," + item.item_id;
    
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
  }

  onAllColumnsAdded(items:{'item_id':string,'item_text':string}[]){
    this.selectedColumns = '';
    items.forEach(x => {
      this.selectedColumns += x.item_id + ","
    })

    this.fixSelectedString();
    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
  }
  
  onColumnRemoved(item:{'item_id':string,'item_text':string}){
    let columns = this.selectedColumns.split(",");
    this.selectedColumns = '';
    columns.forEach(c => {
      if (c != item.item_text){
        this.selectedColumns += c + ","
      }
    })

    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
  }

  onAllColumnsRemoved(event:any){
    this.selectedColumns = '';
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
  }

  onRowAdded(item:{'item_id':string,'item_text':string}){
    if (this.selectedRows.length == 0 )
      this.selectedRows = item.item_id;
    else
      this.selectedRows += "," + item.item_id;
    
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
  }

  onAllRowsAdded(items:{'item_id':string,'item_text':string}[]){
    this.selectedRows = '';
    items.forEach(x => {
      this.selectedRows += x.item_id + ","
    })

    this.fixSelectedString();
    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
  }
  
  onRowRemoved(item:{'item_id':string,'item_text':string}){
    let columns = this.selectedRows.split(",");
    this.selectedRows = '';
    columns.forEach(c => {
      if (c != item.item_text){
        this.selectedRows += c + ","
      }
    })

    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
  }

  onAllRowsRemoved(event:any){
    this.selectedRows = '';
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique;
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
