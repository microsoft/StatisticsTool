import { Component, ElementRef, HostListener, Input, OnInit } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { NavigationStart, Router } from '@angular/router';
import { StatisticsToolService } from './services/statistics-tool.service';

@Pipe({
  name: 'safe'
})
export class SafePipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) { 
  }

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

  showFiller = false;

  @Input() config_key = '';

  @HostListener('document:keydown', ['$event']) onKeydownHandler(event: KeyboardEvent) {
    if (event.key === "Escape") {
        this.statToolSvc.showDrawer = false;
    }
  }

  @HostListener("window:message",["$event"])
  SampleFunction($event:MessageEvent) {
    
    this.statToolSvc.openDrawer.next($event.data);
    let o = $event.data as {'action':string, 'value':string};

    if (o.action == 'update_list'){
      let updateListUrl = o.value + "&main_path=" + this.statToolSvc.getSelectedMainReport() + "&ref_path=" + this.statToolSvc.getSelectedRefReport();
      console.log('update_list',updateListUrl);
      this.statToolSvc.drawerUpdateListUrl = updateListUrl;
    }
    if (o.action == 'show_image'){
      
      //check if path exists
      if (this.statToolSvc.activeLocalDataStore && this.statToolSvc.localDataStorePath.length > 0){
          let url = o.value + "&local_path=" + this.statToolSvc.localDataStorePath + "&main_path=" + this.statToolSvc.getSelectedMainReport() + "&ref_path=" + this.statToolSvc.getSelectedRefReport();
          this.statToolSvc.drawerShowImageUrl = url;
      } else {
        this.statToolSvc.drawerShowImageUrl = o.value  + "&main_path=" + this.statToolSvc.getSelectedMainReport() + "&ref_path=" + this.statToolSvc.getSelectedRefReport();
      }
    }
  }

  constructor(private router : Router,
              public statToolSvc:StatisticsToolService,
              public eltRef: ElementRef) {
  }

  ngOnInit(){
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationStart){
        let reportsPairs = new URLSearchParams(window.location.search).get('reports')?.toString();
        this.statToolSvc.init(reportsPairs);
      }
    })
  }
}
