import { animate, state, style, transition, trigger } from '@angular/animations';
import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'drawer',
  templateUrl: './drawer.component.html',
  styleUrls: ['./drawer.component.css'],
  animations: [
        trigger('widthGrow', [
            state('closed', style({
                width: 0,
            })),
            state('open', style({
                width: 400
            })),
            transition('* => *', animate(150))
        ]),
    ]
})
export class DrawerComponent implements OnInit {

  state = "closed";
  subscribeOpenDrawer = new Subscription;

  changeState(): void {
    (this.state == "closed") ? this.state = "open" : this.state = "closed";
    console.log('Drawer state - ' + this.state);
  }

  constructor(public statToolSvc:StatisticsToolService) {
  }

  ngOnInit(): void {
    this.subscribeOpenDrawer = this.statToolSvc.openDrawer.subscribe(msg => {
      this.statToolSvc.showDrawer = true;
      this.changeState();
    })
  }

  ngOnDestroy(){
    if (this.subscribeOpenDrawer != null)
      this.subscribeOpenDrawer.unsubscribe();
  }

  show = false;

  clickDrawer(){
    this.statToolSvc.showDrawer = !this.statToolSvc.showDrawer;
    this.changeState();
  }
}
