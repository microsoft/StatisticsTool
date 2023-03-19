import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'pkl-view',
  templateUrl: './pkl-view.component.html',
  styleUrls: ['./pkl-view.component.css']
})
export class PklViewComponent {
  url = '/Reporter_new';
  subscribeGetSegment = new Subscription;

  constructor(private httpClient:HttpClient,
              private statToolService:StatisticsToolService) {
    this.url = '/Reporter_new';
    
    this.subscribeGetSegment = this.httpClient.post('/get_segmentations',{})
                        .subscribe(res => {
                            let arr = Object.entries(res);
                            let map = new Map<string,string[]>();
                            arr.forEach(x => { map.set(x[0],x[1]) });
                            this.statToolService.optionalSegmentations = map;
                            this.statToolService.segmentationsFetched.next(true);
                          }
                        )
   }

  ngOnDestroy(){
    if (this.subscribeGetSegment != null)
      this.subscribeGetSegment.unsubscribe();
  }

  onclick(){
    this.url = this.url + '?name=hagai';
  }
}
