import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { FormControl,ReactiveFormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'segmentations',
  templateUrl: './segmentations.component.html',
  styleUrls: ['./segmentations.component.css']
})
export class SegmentationsComponent implements OnInit{
  
  dropdownList : {'item_id':string,'item_text':string}[] = [];
  selected : {'item_id':string,'item_text':string}[] = [];
  
  dropdownSettings = {};

  subscribeSegmentationsFetched = new Subscription;

  @Input() optionalSegmentations:string[] = [];
  @Input() name = '';

  constructor(private statToolService:StatisticsToolService,
              private httpClient:HttpClient) {
  }

  ngOnInit(): void {

    this.subscribeSegmentationsFetched = this.statToolService.segmentationsFetched.subscribe(x => {
      if (this.optionalSegmentations.length == 0){
        let segmentations = this.statToolService.getSegmentations();
        segmentations.forEach(txt => {
          this.dropdownList.push({'item_id':txt,'item_text':txt})  
        })
      } else {
        this.optionalSegmentations.forEach(txt => {
          this.dropdownList.push({'item_id':txt,'item_text':txt})  
        })
      }

      this.dropdownSettings = {
        singleSelection: false,
        idField: 'item_id',
        textField: 'item_text',
        selectAllText: 'Select All',
        unSelectAllText: 'UnSelect All',
        itemsShowLimit: 100,
        allowSearchFilter: true
      };
    });
  }

  onItemSelect(item: any) {
    console.log(item);
  }
  onSelectAll(items: any) {
    console.log(items);
  }

ngOnDestroy(){
    if (this.subscribeSegmentationsFetched != null)
      this.subscribeSegmentationsFetched.unsubscribe();
  }
}
