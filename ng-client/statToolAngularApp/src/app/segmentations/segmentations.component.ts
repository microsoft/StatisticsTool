import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl,ReactiveFormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'segmentations',
  templateUrl: './segmentations.component.html',
  styleUrls: ['./segmentations.component.css']
})
export class SegmentationsComponent implements OnInit{

  @Input() set selectItems(items:string){
    if (items == "," || items == "" || items == ' ')
      return;
    let arr = items.split(',')
    this.selected = []
    arr.forEach(a => {
      this.selected.push({'item_id':a,'item_text':a})
    })
    console.log('foo','items:',JSON.stringify(arr),'selected:',JSON.stringify(this.selected));
  }
  
  @Input() name = '';
  dropdownList : {'item_id':string,'item_text':string}[] = [];
  selected     : {'item_id':string,'item_text':string}[] = [];
  
  dropdownSettings = {};
  subscribeSegmentationsFetched = new Subscription;
  
  @Output() segmentsChanged = new EventEmitter();

  constructor(private statToolService:StatisticsToolService,
              private httpClient:HttpClient) {
  }

  ngOnInit(): void {
      
      for (let [key, value] of this.statToolService.optionalSegmentations) {
        this.dropdownList.push({'item_id':key,'item_text':key})
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
  }

  onItemSelect(item: any) {
    this.segmentsChanged.emit(this.selected)
    //console.log('segments, select',item,this.selected);
  }
  onSelectAll(items: any) {
    this.segmentsChanged.emit(this.selected)
    //console.log('segments, select all',items,this.selected);
  }
  onItemUnSelect(item: any) {
    this.segmentsChanged.emit(this.selected)
    //console.log('segments,un select',item,this.selected);
  }

ngOnDestroy(){
    if (this.subscribeSegmentationsFetched != null)
      this.subscribeSegmentationsFetched.unsubscribe();
  }
}
