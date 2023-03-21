import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
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

@NgModule({
  declarations: [
    AppComponent,
    SafePipe,
    SegmentationsComponent,
    PklViewComponent,
    TemplateSegmentationsComponent,
    TemplateSegmentsHeaderComponent,
  ],
  imports: [
    NgMultiSelectDropDownModule.forRoot(),
    MatSelectModule,
    MatGridListModule,
    MatRadioModule,
    MatButtonModule,
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
