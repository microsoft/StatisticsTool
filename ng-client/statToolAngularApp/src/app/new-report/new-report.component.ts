import { Component } from '@angular/core';
import {Location} from '@angular/common';

@Component({
  selector: 'new-report',
  templateUrl: './new-report.component.html',
  styleUrls: ['./new-report.component.css']
})
export class NewReportComponent {

  constructor(private location:Location){

  }

  backImgSrc = 'assets/back-icon-blue.svg';
  

  back(){
    let path = this.location.path();
    console.log('path',path)
    if (path.indexOf('/static/') > 0){
      path = path.replace('/static/','/');
      console.log('path-remove-static',path)
    }
    window.location.href = 'http://127.0.0.1:5000/';
  }

}
