import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent, SafePipe } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { SegmentationsComponent } from './segmentations/segmentations.component';
import { PklViewComponent } from './pkl-view/pkl-view.component';
import { StatisticsToolService } from './services/statistics-tool.service';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { TemplateSegmentationsComponent } from './template-segmentations/template-segmentations.component';
import { TemplateSegmentsHeaderComponent } from './template-segments-header/template-segments-header.component';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatIconModule} from '@angular/material/icon';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { DrawerComponent } from './drawer/drawer.component';
import { DrawerContentComponent } from './drawer-content/drawer-content.component';
import {MatExpansionModule} from '@angular/material/expansion';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgbTypeaheadModule } from '@ng-bootstrap/ng-bootstrap';
import { NgbAlertModule } from '@ng-bootstrap/ng-bootstrap';
import '@angular/localize/init';
import { SaveTemplateDialogComponent } from './save-template-dialog/save-template-dialog.component';
import { NewReportComponent } from './new-report/new-report.component';
import { SaveSuiteDialogComponent } from './save-suite-dialog/save-suite-dialog.component';
import { ConfigurationViewerComponent } from './configuration-viewer/configuration-viewer.component';
import { NewReportResultComponent } from './new-report/new-report-result/new-report-result.component';
import { ClickOutsideDirective } from './click-outside.directive'; // Adjust the path to your directive
import { CommonService } from './services/common.service';


@NgModule({
  declarations: [
    AppComponent,
    SafePipe,
    SegmentationsComponent,
    PklViewComponent,
    TemplateSegmentationsComponent,
    TemplateSegmentsHeaderComponent,
    DrawerComponent,
    DrawerContentComponent,
    SaveTemplateDialogComponent,
    NewReportComponent,
    SaveSuiteDialogComponent,
    ConfigurationViewerComponent,
    NewReportResultComponent,
    ClickOutsideDirective
  ],
  imports: [
    NgMultiSelectDropDownModule.forRoot(),
    MatSelectModule,
    MatGridListModule,
    MatRadioModule,
    MatButtonModule,
    MatSlideToggleModule,
    MatProgressSpinnerModule,
    MatSidenavModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatToolbarModule,
    MatExpansionModule,
    NgbModule,
    NgbTypeaheadModule,
    NgbAlertModule,
    DragDropModule
  ],
  providers: [StatisticsToolService,CommonService],
  bootstrap: [AppComponent]
})
export class AppModule { }
