import { Component } from '@angular/core';
import { NewReportService } from 'src/app/services/new-report.service';

@Component({
  selector: 'new-report-result',
  templateUrl: './new-report-result.component.html',
  styleUrls: ['./new-report-result.component.css']
})
export class NewReportResultComponent {
  
  constructor(public newReportService:NewReportService) {
    
  }
}
