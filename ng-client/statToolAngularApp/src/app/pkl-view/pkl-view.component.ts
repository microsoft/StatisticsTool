import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'pkl-view',
  templateUrl: './pkl-view.component.html',
  styleUrls: ['./pkl-view.component.css']
})
export class PklViewComponent implements OnInit {
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

  constructor(private httpClient:HttpClient,
              private statToolService:StatisticsToolService) {
    this.url = '/Reporter_new';
    
    /*this.subscribeGetSegment = this.httpClient.post('/get_segmentations',{})
                        .subscribe(res => {
                            let arr = Object.entries(res);
                            let map = new Map<string,string[]>();
                            arr.forEach(x => { map.set(x[0],x[1]) });
                            this.statToolService.optionalSegmentations = map;
                            this.statToolService.segmentationsFetched.next(true);
                          }
                        )*/
  }

  ngOnInit(): void {
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows;
  }

  ngOnDestroy(){
    //if (this.subscribeGetSegment != null)
    //  this.subscribeGetSegment.unsubscribe();
  }

  onclick(){
    this.url = this.url + '?name=hagai';
  }

  onColumnsChanged(items:{'item_id':string,'item_text':string}[]){
    this.selectedColumns = '';
    items.forEach(x => {
      this.selectedColumns += x.item_id + ","
    })

    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows;
    console.log('onColumnsChanged',items);
  }

  onRowsChanged(items:{'item_id':string,'item_text':string}[]){
    this.selectedRows = '';
    items.forEach(x => {
      this.selectedRows += x.item_id + ","
    })
    this.url = '/Reporter_new?cols=' + this.selectedColumns + "&rows=" + this.selectedRows;
    console.log('onRowsChanged',items);
  }
}
