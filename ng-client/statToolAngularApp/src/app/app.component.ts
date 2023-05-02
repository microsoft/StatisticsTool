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

  constructor(private sanitizer: DomSanitizer,
              private httpClient:HttpClient) { }
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
      
      this.statToolSvc.openDrawer.next($event.data);
      let o = $event.data as {'action':string, 'value':string};
      
      console.log($event.data)
      if (o.action == 'update_list'){
        console.log('in update_list')
        this.statToolSvc.drawerUpdateListUrl = o.value;
      }
      if (o.action == 'show_image'){
        console.log('in show_image',o.value)
        
        //check if path exists
        if (this.statToolSvc.activeLocalDataStore && this.statToolSvc.localDataStorePath.length > 0){
          let filepath = this.getFilePath(o.value) 
          this.httpClient.post<{'exists':boolean}>('/is_file_exists',{
            'file_path':filepath
          }).subscribe(res => {
            console.log('getFilePath','result',res)
            if (res.exists){
              let url = o.value + "&local_path=" + this.statToolSvc.localDataStorePath
              this.statToolSvc.drawerShowImageUrl = url;
            } else {
              this.statToolSvc.showDrawer = false;
              this.statToolSvc.fileNotFoundError = 'File ' + filepath + " not found!"
            }
          })
        } else {
          this.statToolSvc.drawerShowImageUrl = o.value;
        }
      }
    }

    constructor(private httpClient:HttpClient,
                  private router : Router,
                  public statToolSvc:StatisticsToolService) {
    }

    ngOnInit(){
    }

    getFilePath(str:string){
      let startIdx = str.indexOf('[');
      let endIdx = str.indexOf('.mp4');
      let path = str.slice(startIdx+2,endIdx);
      path = path += ".mp4"
      if (this.statToolSvc.activeLocalDataStore && this.statToolSvc.localDataStorePath.length > 0){
        path = this.statToolSvc.localDataStorePath + "\\" + path;
      }

      return path;
    }
  }
