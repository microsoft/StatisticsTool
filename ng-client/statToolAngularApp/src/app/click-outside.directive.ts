import { Directive, ElementRef, HostListener, OnInit, Renderer2 } from '@angular/core';
import { CommonService } from './services/common.service';
import { States, StatisticsToolService } from './services/statistics-tool.service';

@Directive({
  selector: '[appClickOutside]'
})
export class ClickOutsideDirective implements OnInit {
  constructor(private elementRef: ElementRef, private renderer: Renderer2,private statSvc:StatisticsToolService,private commonSvc:CommonService) {}
  
  ngOnInit(): void {
    this.commonSvc.onMouseClicked.subscribe(event => {
        let name = this.elementRef.nativeElement.parentNode.parentNode.attributes['name'].value;
        const dropdownPanel = this.elementRef.nativeElement.querySelector('.dropdown-list');  

        if (name == "Horizontal Segmentation"){
          if (this.statSvc.openHorizontalSegmentation == States.Opened){
            this.statSvc.openHorizontalSegmentation = States.Open;
            return;
          }
          if (this.statSvc.openHorizontalSegmentation == States.Open){
            dropdownPanel.hidden = true;
          }
        } else {
          if (this.statSvc.openVerticalSegmentation == States.Opened){
            this.statSvc.openVerticalSegmentation = States.Open;
            return;
          }
          if (this.statSvc.openVerticalSegmentation == States.Open){
            dropdownPanel.hidden = true;
          }
        }
    })
  }
}
