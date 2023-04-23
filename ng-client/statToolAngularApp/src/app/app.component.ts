import { AfterContentInit, Component, HostListener, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { StatisticsToolService } from './services/statistics-tool.service';
import { MatDrawer, MatSidenav } from '@angular/material/sidenav';

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
export class AppComponent implements OnInit {

  @ViewChild(MatSidenav) public drawer: any;
  showFiller = false;

  @HostListener('document:keydown', ['$event']) onKeydownHandler(event: KeyboardEvent) {
    console.log('keydown',event.key)
    if (event.key === "Escape") {
        this.statToolSvc.showDrawer = false;
    }
  }

  @HostListener("window:message",["$event"])
  SampleFunction($event:MessageEvent) {
    //if (event!.origin !== "protocol://my-expected-domain.tdl:port")
     // return;
    //console.log('hagai',$event.data)// {foo:"foo"}
    
    this.statToolSvc.openDrawer.next($event.data);
    let o = $event.data as {'action':string, 'value':string};
    //let obj:{'update_list':string} = JSON.parse($event.data)
    console.log($event.data)
    if (o.action == 'update_list'){
      console.log('in update_list')
      this.statToolSvc.drawerUpdateListUrl = o.value;
    }
    if (o.action == 'show_image'){
      console.log('in show_image',o.value)
      this.statToolSvc.drawerShowImageUrl = o.value;
    }
    //console.log('hagai','going to open')// {foo:"foo"}
    
    //console.log('hagai','opened')// {foo:"foo"}
  }


  
  //title = 'statToolAngularApp';
    constructor(private httpClient:HttpClient,
                private router : Router,
                public statToolSvc:StatisticsToolService) {
  }

    ngOnInit(){
    }
  }
