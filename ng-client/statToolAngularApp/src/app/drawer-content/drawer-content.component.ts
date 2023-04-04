import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'drawer-content',
  templateUrl: './drawer-content.component.html',
  styleUrls: ['./drawer-content.component.css']
})
export class DrawerContentComponent implements OnInit {

  constructor(public statToolService:StatisticsToolService) {
  }

  ngOnInit(): void {
    
  }

  ngOnDestroy(){
  }

}
