import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TemplateSegmentsHeaderComponent } from './template-segments-header.component';

describe('TemplateSegmentsHeaderComponent', () => {
  let component: TemplateSegmentsHeaderComponent;
  let fixture: ComponentFixture<TemplateSegmentsHeaderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TemplateSegmentsHeaderComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TemplateSegmentsHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
