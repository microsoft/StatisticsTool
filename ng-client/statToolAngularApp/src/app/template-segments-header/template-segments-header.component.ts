import { Component, OnInit } from '@angular/core';
import { StatisticsToolService } from '../services/statistics-tool.service';

@Component({
  selector: 'template-segments-header',
  templateUrl: './template-segments-header.component.html',
  styleUrls: ['./template-segments-header.component.css']
})
export class TemplateSegmentsHeaderComponent implements OnInit {

  constructor(public statToolService: StatisticsToolService) {
  }

  ngOnInit(): void {
    
  }

  ngDestroy(){
    
  }

}
