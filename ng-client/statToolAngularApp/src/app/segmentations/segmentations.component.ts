import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, EventEmitter, HostListener, Input, OnInit, Output, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';
import { States, StatisticsToolService } from '../services/statistics-tool.service';
import { CommonService } from '../services/common.service';

@Component({
  selector: 'segmentations',
  templateUrl: './segmentations.component.html',
  styleUrls: ['./segmentations.component.css']
})
export class SegmentationsComponent implements OnInit{
  @ViewChild('dropdown', { static: false }) dropdown: ElementRef|undefined;
  isDropdownOpen = false;

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }
  
  @Input() set selectItems(items:string){
    if (items == "," || items == "" || items == ' ')
      return;
    let arr = items.split(',')
    this.selected = []
    arr.forEach(a => {
      this.selected.push({'item_id':a,'item_text':a})
    })
    
  }
  
  @Input() name = '';
  @Input() elementRef = '';
  dropdownList : {'item_id':string,'item_text':string}[] = [];
  selected     : {'item_id':string,'item_text':string}[] = [];
  
  dropdownSettings = {};
  subscribeSegmentationsFetched = new Subscription;
  
  @Output() segmentAdded        = new EventEmitter();
  @Output() segmentRemoved      = new EventEmitter();
  @Output() allSegmentsAdded    = new EventEmitter();
  @Output() allSegmentsRemoved  = new EventEmitter();

  constructor(private statToolService:StatisticsToolService,
              private httpClient:HttpClient,
              private commonSvc:CommonService) {
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
        allowSearchFilter: true,
      };

      /*this.commonSvc.onMouseClicked.subscribe(event => {
        this.isDropdownOpen = false;
        console.log(this.isDropdownOpen +"," + event.target)
        if (this.dropdown != undefined)
          if (!this.dropdown.nativeElement.contains(event.target)) {
            this.isDropdownOpen = false;
          }
      })*/
  }

  onItemSelect(item: any) {
    console.log('onItemSelect',item);
    this.segmentAdded.emit(item);
  }
  onSelectAll(items: any) {
    console.log('onSelectAll',items);
    this.allSegmentsAdded.emit(items);
  }
  onUnSelect(item: any) {
    console.log('onUnSelect',item);
    this.segmentRemoved.emit(item)
  }

  onUnSelectAll(item: any) {
    console.log('onUnSelectAll',item);
    this.allSegmentsRemoved.emit([])
  }

  onClick(){
    let name = this.dropdown?.nativeElement.parentElement.attributes['name'].value;

    if (!this.dropdown?.nativeElement.querySelectorAll('.dropdown-list')[0].hidden){
      if (name == "Horizontal Segmentation")
        this.statToolService.openHorizontalSegmentation = States.Opened;
      else   
        this.statToolService.openVerticalSegmentation = States.Opened;
      return;
    }
    if (name == "Horizontal Segmentation")
      this.statToolService.openHorizontalSegmentation = States.Close;
    else 
      this.statToolService.openVerticalSegmentation = States.Close;
  }

  ngOnDestroy(){
    if (this.subscribeSegmentationsFetched != null)
      this.subscribeSegmentationsFetched.unsubscribe();
  }
}
