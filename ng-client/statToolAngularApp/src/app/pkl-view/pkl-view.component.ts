import { HttpClient } from '@angular/common/http';
import {  Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';
import { Utils } from '../utils';

@Component({
  selector: 'pkl-view',
  templateUrl: './pkl-view.component.html',
  styleUrls: ['./pkl-view.component.css']
})
export class PklViewComponent implements OnInit  {

  @ViewChild('iframe') iframe: ElementRef|null = null;
  
  url = '/get_report_table';
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
  subscribeReportChanged = new Subscription;

  height:string = '';

  constructor(private httpClient:HttpClient,
              public statToolService:StatisticsToolService) {
    
    this.url = '/get_report_table?calc_unique=' + statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();

    
 }

  ngOnInit(): void {
                  
    this.fixSelectedString();
    this.url = '/get_report_table?cols=' + this.selectedColumns
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    this.loadCounter = 1;

    this.subscribeUniqueChange = this.statToolService.uniqueValueChanged.subscribe(res => {
      this.loadCounter = 1;
      this.url = '/get_report_table?cols=' + this.selectedColumns 
                                           + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                           + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    })

    this.subscribeReportChanged = this.statToolService.reportSelected.subscribe(res => {
      this.fixSelectedString();
      this.loadCounter = 1;
      let u = '/get_report_table?cols=' + this.selectedColumns 
              + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
              + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
      this.url = u;
    })

    
  }

   ngOnDestroy(){
    if (this.subscribeUniqueChange != null)
      this.subscribeUniqueChange.unsubscribe();
    if (this.subscribeReportChanged != null)
      this.subscribeReportChanged.unsubscribe();
  }

  onColumnAdded(item:{'item_id':string,'item_text':string}){
    if (this.selectedColumns.length == 0 )
      this.selectedColumns = item.item_id;
    else
      this.selectedColumns += "," + item.item_id;
    
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
  }

  onAllColumnsAdded(items:{'item_id':string,'item_text':string}[]){
    this.selectedColumns = '';
    items.forEach(x => {
      this.selectedColumns += x.item_id + ","
    })

    this.fixSelectedString();
    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
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
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
  }

  onAllColumnsRemoved(event:any){
    this.selectedColumns = '';
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
  }

  onRowAdded(item:{'item_id':string,'item_text':string}){
    if (this.selectedRows.length == 0 )
      this.selectedRows = item.item_id;
    else
      this.selectedRows += "," + item.item_id;
    
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
  }

  onAllRowsAdded(items:{'item_id':string,'item_text':string}[]){
    this.selectedRows = '';
    items.forEach(x => {
      this.selectedRows += x.item_id + ","
    })

    this.fixSelectedString();
    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
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
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
  }

  onAllRowsRemoved(event:any){
    this.selectedRows = '';
    this.fixSelectedString();

    this.statToolService.updateSegments(this.id,this.name,this.selectedColumns,this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns 
                                         + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique
                                         + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();;
  }

  fixSelectedString(){
    if (this.selectedColumns.slice(-1) == ",")  
      this.selectedColumns = this.selectedColumns.slice(0,-1);
    if (this.selectedRows.slice(-1) == ",")  
      this.selectedRows = this.selectedRows.slice(0,-1);

  }

  async onIframeLoad(){
    this.loadCounter = this.loadCounter - 1;
    
    if (this.iframe != null){
      let loop = true;
      while(loop){
        await Utils.sleep(100);
        let h = this.iframe.nativeElement.contentWindow.document.body.scrollHeight;
        if (h > 100){
          //console.log('frame:::',this.id,h);
          h += 100;
          this.height = h.toString() + 'px';
          this.statToolService.viewHeights.set(this.id,this.height);  
          loop = false;
        }
      }
    }
  }

  onViewNameChanged(event:any){
    this.statToolService.updateSegmentationName(this.name,this.id,event.target.value);
  }

  removeView(){
    this.statToolService.removeView(this.id);
  }
}
