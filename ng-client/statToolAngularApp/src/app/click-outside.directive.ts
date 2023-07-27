import { Directive, ElementRef, HostListener, Input, OnInit, Renderer2 } from '@angular/core';
import { CommonService } from './services/common.service';
import { States, StatisticsToolService } from './services/statistics-tool.service';

@Directive({
  selector: '[appClickOutside]'
})
export class ClickOutsideDirective implements OnInit {
  constructor(private elementRef: ElementRef, private renderer: Renderer2,private statSvc:StatisticsToolService,private commonSvc:CommonService) {}
  
  @Input() viewId:     number = 0;
  @Input() viewguid = '';
  @Input() segmentName:string = '';

  ngOnInit(): void {
    
    this.commonSvc.onMouseClicked.subscribe(event => {
        let name = this.elementRef.nativeElement.parentNode.parentNode.attributes['name'].value;
        const dropdownPanel = this.elementRef.nativeElement.querySelector('.dropdown-list');  
        //const caretIcon = this.elementRef.nativeElement.querySelector('.dropdown-multiselect__caret');
        
        if (this.statSvc.getDropdownState(this.viewguid,name) == States.Opened){
          this.statSvc.setDropdownState(this.viewguid,name,States.Open);
          
          return;
        }
        if (this.statSvc.getDropdownState(this.viewguid,name) == States.Open){
          dropdownPanel.hidden = true;
          /*if (caretIcon instanceof HTMLElement) {
            caretIcon.classList.add('rotate-180');
          }*/
        } else {
          /*caretIcon.classList.remove('rotate-180');*/
        }
    })
  }
}
