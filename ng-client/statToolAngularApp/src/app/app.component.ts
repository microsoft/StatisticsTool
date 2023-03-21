import { AfterContentInit, Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Pipe({
  name: 'safe'
})
export class SafePipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) { }
  transform(url:string) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit,AfterContentInit {
  title = 'statToolAngularApp';

  //data = ''

  url = '/Reporter_new';

  constructor(private httpClient:HttpClient,private router : Router) {
    this.url = '/Reporter_new';
    /*
    console.log('ctor')
    this.httpClient.post('/Reporter_new_wrapper',{})
                   .subscribe(res => {
                      console.log(res) 
                      this.data = res.toString();
                   })*/
    /*this.httpClient.post('/get_segmentations',{})
                   .subscribe(res => {
                      console.log(res) 
                      //this.data = res.toString();
                    }
                   )*/
  }

  onclick(){
    this.url = this.url + '?name=hagai';
  }


  ngOnInit(){
    //console.log('ngOnInit')
    this.router.events.subscribe(val => {
      console.log('router:',val)
    })
  }

  ngAfterContentInit(){
    //console.log('ngAfterContentInit')
  }
}
