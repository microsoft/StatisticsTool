import { Component, ElementRef, HostListener, Input, OnInit } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { NavigationStart, Router } from '@angular/router';
import { StatisticsToolService } from './services/statistics-tool.service';
import { NewReportService } from './services/new-report.service';
import { CommonService } from './services/common.service';

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

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent) {
    this.commonSvc.onMouseClicked.next(event);
  }

  showFiller = false;
  isNewReport = false;

  @Input() config_key = '';

  @HostListener('document:keydown', ['$event']) onKeydownHandler(event: KeyboardEvent) {
    if (event.key === "Escape") {
        this.statToolSvc.showDrawer = false;
    }
  }

  @HostListener("window:message",["$event"])
  SampleFunction($event:MessageEvent) {
    
    let o = $event.data as {'action':string, 'value':string};
    
    if (o.action == 'viewer-mousedown'){
      console.log('viewer-mousedown')
      this.commonSvc.onMouseClicked.next(true);
      return;
    }
    
    this.statToolSvc.openDrawer.next($event.data);

    if (o.action == 'update_list'){
      let updateListUrl = o.value;
      console.log('update_list',updateListUrl);
      this.statToolSvc.drawerUpdateListUrl = updateListUrl;
    }
    if (o.action == 'show_image'){
      
      //check if path exists
      if (this.statToolSvc.activeLocalDataStore && this.statToolSvc.localDataStorePath.length > 0){
          let url = o.value + "&local_path=" + this.statToolSvc.localDataStorePath;
          this.statToolSvc.drawerShowImageUrl = url;
      } else {
        this.statToolSvc.drawerShowImageUrl = o.value;
      }
    }
  }

  constructor(private router : Router,
              public statToolSvc:StatisticsToolService,
              private newReportService:NewReportService,
              public eltRef: ElementRef,
              private commonSvc:CommonService) {
  }

  ngOnInit(){
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationStart){
        let reports = new URLSearchParams(window.location.search).get('reports');
        if (reports == null){
          this.isNewReport = true;
          let configs = new URLSearchParams(window.location.search).get('possible_configs');
          let suites = new URLSearchParams(window.location.search).get('possible_suites');
          this.newReportService.init(configs!,suites!);

        } else {
          this.isNewReport = false;
          let reportsPairs = new URLSearchParams(window.location.search).get('reports')?.toString();
          this.statToolSvc.init(reportsPairs);
        }
      }
    })
  }
}
