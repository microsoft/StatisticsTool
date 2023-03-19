import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent, SafePipe } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { SegmentationsComponent } from './segmentations/segmentations.component';
import { PklViewComponent } from './pkl-view/pkl-view.component';
import { StatisticsToolService } from './services/statistics-tool.service';

import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
@NgModule({
  declarations: [
    AppComponent,SafePipe, SegmentationsComponent, PklViewComponent 
  ],
  imports: [
    NgMultiSelectDropDownModule.forRoot(),
    MatSelectModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [StatisticsToolService],
  bootstrap: [AppComponent]
})
export class AppModule { }
