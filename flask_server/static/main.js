"use strict";
(self["webpackChunkstatToolAngularApp"] = self["webpackChunkstatToolAngularApp"] || []).push([["main"],{

/***/ 158:
/*!***************************************!*\
  !*** ./src/app/app-routing.module.ts ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AppRoutingModule": () => (/* binding */ AppRoutingModule)
/* harmony export */ });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ 124);
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./app.component */ 5041);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);




const routes = [{
  path: 'update_list',
  component: _app_component__WEBPACK_IMPORTED_MODULE_0__.AppComponent
}, {
  path: 'index.html',
  component: _app_component__WEBPACK_IMPORTED_MODULE_0__.AppComponent
}];
class AppRoutingModule {}
AppRoutingModule.ɵfac = function AppRoutingModule_Factory(t) {
  return new (t || AppRoutingModule)();
};
AppRoutingModule.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineNgModule"]({
  type: AppRoutingModule
});
AppRoutingModule.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjector"]({
  imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule.forRoot(routes), _angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule]
});
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsetNgModuleScope"](AppRoutingModule, {
    imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule],
    exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule]
  });
})();

/***/ }),

/***/ 5041:
/*!**********************************!*\
  !*** ./src/app/app.component.ts ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AppComponent": () => (/* binding */ AppComponent),
/* harmony export */   "SafePipe": () => (/* binding */ SafePipe)
/* harmony export */ });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/router */ 124);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/platform-browser */ 4497);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./services/statistics-tool.service */ 4204);
/* harmony import */ var _services_new_report_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./services/new-report.service */ 9167);
/* harmony import */ var _services_common_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./services/common.service */ 5620);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./template-segmentations/template-segmentations.component */ 2260);
/* harmony import */ var _drawer_drawer_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./drawer/drawer.component */ 5220);
/* harmony import */ var _new_report_new_report_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./new-report/new-report.component */ 6652);











function AppComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵelementStart"](0, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵelement"](1, "drawer")(2, "template-segmentations");
    _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵelementEnd"]();
  }
}
function AppComponent_div_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵelementStart"](0, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵelement"](1, "new-report");
    _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵelementEnd"]();
  }
}
class SafePipe {
  constructor(sanitizer) {
    this.sanitizer = sanitizer;
  }
  transform(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
SafePipe.ɵfac = function SafePipe_Factory(t) {
  return new (t || SafePipe)(_angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdirectiveInject"](_angular_platform_browser__WEBPACK_IMPORTED_MODULE_7__.DomSanitizer, 16));
};
SafePipe.ɵpipe = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdefinePipe"]({
  name: "safe",
  type: SafePipe,
  pure: true
});
class AppComponent {
  onDocumentClick(event) {
    this.commonSvc.onMouseClicked.next(event);
  }
  onKeydownHandler(event) {
    if (event.key === "Escape") {
      this.statToolSvc.showDrawer = false;
    }
  }
  SampleFunction($event) {
    let o = $event.data;
    if (o.action == 'viewer-mousedown') {
      console.log('viewer-mousedown');
      this.commonSvc.onMouseClicked.next(true);
      return;
    }
    this.statToolSvc.openDrawer.next($event.data);
    if (o.action == 'update_list') {
      let updateListUrl = o.value;
      console.log('update_list', updateListUrl);
      this.statToolSvc.drawerUpdateListUrl = updateListUrl;
    }
    if (o.action == 'show_image') {
      //check if path exists
      if (this.statToolSvc.activeLocalDataStore && this.statToolSvc.localDataStorePath.length > 0) {
        let url = o.value + "&local_path=" + this.statToolSvc.localDataStorePath;
        this.statToolSvc.drawerShowImageUrl = url;
      } else {
        this.statToolSvc.drawerShowImageUrl = o.value;
      }
    }
  }
  constructor(router, statToolSvc, newReportService, eltRef, commonSvc) {
    this.router = router;
    this.statToolSvc = statToolSvc;
    this.newReportService = newReportService;
    this.eltRef = eltRef;
    this.commonSvc = commonSvc;
    this.showFiller = false;
    this.isNewReport = false;
    this.config_key = '';
  }
  ngOnInit() {
    this.newReportService.initialize();
    this.router.events.subscribe(event => {
      if (event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_8__.NavigationStart) {
        let reports = new URLSearchParams(window.location.search).get('reports');
        if (reports == null) {
          this.isNewReport = true;
        } else {
          this.isNewReport = false;
          let reportsPairs = new URLSearchParams(window.location.search).get('reports')?.toString();
          this.statToolSvc.init(reportsPairs);
        }
      }
    });
  }
}
AppComponent.ɵfac = function AppComponent_Factory(t) {
  return new (t || AppComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_8__.Router), _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService), _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdirectiveInject"](_services_new_report_service__WEBPACK_IMPORTED_MODULE_1__.NewReportService), _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_6__.ElementRef), _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdirectiveInject"](_services_common_service__WEBPACK_IMPORTED_MODULE_2__.CommonService));
};
AppComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵdefineComponent"]({
  type: AppComponent,
  selectors: [["app-root"]],
  hostBindings: function AppComponent_HostBindings(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵlistener"]("click", function AppComponent_click_HostBindingHandler($event) {
        return ctx.onDocumentClick($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵresolveDocument"])("keydown", function AppComponent_keydown_HostBindingHandler($event) {
        return ctx.onKeydownHandler($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵresolveDocument"])("message", function AppComponent_message_HostBindingHandler($event) {
        return ctx.SampleFunction($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵresolveWindow"]);
    }
  },
  inputs: {
    config_key: "config_key"
  },
  decls: 2,
  vars: 2,
  consts: [[4, "ngIf"]],
  template: function AppComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵtemplate"](0, AppComponent_div_0_Template, 3, 0, "div", 0);
      _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵtemplate"](1, AppComponent_div_1_Template, 2, 0, "div", 0);
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵproperty"]("ngIf", !ctx.isNewReport);
      _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_6__["ɵɵproperty"]("ngIf", ctx.isNewReport);
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_9__.NgIf, _template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_3__.TemplateSegmentationsComponent, _drawer_drawer_component__WEBPACK_IMPORTED_MODULE_4__.DrawerComponent, _new_report_new_report_component__WEBPACK_IMPORTED_MODULE_5__.NewReportComponent],
  styles: [".MyDrawer[_ngcontent-%COMP%]{\r\n    position: absolute;\r\n    left: 0;\r\n    background: rgb(240,240,240,0.4);\r\n  }\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvYXBwLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7SUFDSSxrQkFBa0I7SUFDbEIsT0FBTztJQUNQLGdDQUFnQztFQUNsQyIsInNvdXJjZXNDb250ZW50IjpbIi5NeURyYXdlcntcclxuICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcclxuICAgIGxlZnQ6IDA7XHJcbiAgICBiYWNrZ3JvdW5kOiByZ2IoMjQwLDI0MCwyNDAsMC40KTtcclxuICB9XHJcblxyXG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
});

/***/ }),

/***/ 6747:
/*!*******************************!*\
  !*** ./src/app/app.module.ts ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AppModule": () => (/* binding */ AppModule)
/* harmony export */ });
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/material/select */ 7371);
/* harmony import */ var _angular_material_grid_list__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @angular/material/grid-list */ 2642);
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @angular/material/radio */ 2922);
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @angular/material/button */ 4522);
/* harmony import */ var _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! @angular/material/progress-spinner */ 1708);
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! @angular/platform-browser */ 4497);
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./app-routing.module */ 158);
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./app.component */ 5041);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _segmentations_segmentations_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./segmentations/segmentations.component */ 3696);
/* harmony import */ var _pkl_view_pkl_view_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./pkl-view/pkl-view.component */ 7092);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./services/statistics-tool.service */ 4204);
/* harmony import */ var ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ng-multiselect-dropdown */ 1664);
/* harmony import */ var _template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./template-segmentations/template-segmentations.component */ 2260);
/* harmony import */ var _template_segments_header_template_segments_header_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./template-segments-header/template-segments-header.component */ 8621);
/* harmony import */ var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! @angular/material/slide-toggle */ 4714);
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_30__ = __webpack_require__(/*! @angular/material/icon */ 7822);
/* harmony import */ var _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! @angular/material/sidenav */ 6643);
/* harmony import */ var _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_31__ = __webpack_require__(/*! @angular/material/toolbar */ 2543);
/* harmony import */ var _angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_34__ = __webpack_require__(/*! @angular/cdk/drag-drop */ 7727);
/* harmony import */ var _drawer_drawer_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./drawer/drawer.component */ 5220);
/* harmony import */ var _drawer_content_drawer_content_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./drawer-content/drawer-content.component */ 9765);
/* harmony import */ var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_32__ = __webpack_require__(/*! @angular/material/expansion */ 7591);
/* harmony import */ var _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_33__ = __webpack_require__(/*! @ng-bootstrap/ng-bootstrap */ 4534);
/* harmony import */ var _angular_localize_init__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/localize/init */ 6344);
/* harmony import */ var _save_template_dialog_save_template_dialog_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./save-template-dialog/save-template-dialog.component */ 7897);
/* harmony import */ var _new_report_new_report_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./new-report/new-report.component */ 6652);
/* harmony import */ var _save_suite_dialog_save_suite_dialog_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./save-suite-dialog/save-suite-dialog.component */ 7972);
/* harmony import */ var _configuration_viewer_configuration_viewer_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./configuration-viewer/configuration-viewer.component */ 3213);
/* harmony import */ var _new_report_new_report_result_new_report_result_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./new-report/new-report-result/new-report-result.component */ 3886);
/* harmony import */ var _click_outside_directive__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./click-outside.directive */ 9155);
/* harmony import */ var _services_common_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./services/common.service */ 5620);
/* harmony import */ var _configuration_viewer_udf_arguments_udf_arguments_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./configuration-viewer/udf-arguments/udf-arguments.component */ 1201);
/* harmony import */ var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_35__ = __webpack_require__(/*! @angular/platform-browser/animations */ 7146);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_36__ = __webpack_require__(/*! @angular/common */ 4666);

































 // Adjust the path to your directive


 // Import the BrowserAnimationsModule




class AppModule {}
AppModule.ɵfac = function AppModule_Factory(t) {
  return new (t || AppModule)();
};
AppModule.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_18__["ɵɵdefineNgModule"]({
  type: AppModule,
  bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_1__.AppComponent]
});
AppModule.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_18__["ɵɵdefineInjector"]({
  providers: [_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_4__.StatisticsToolService, _services_common_service__WEBPACK_IMPORTED_MODULE_16__.CommonService],
  imports: [ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_19__.NgMultiSelectDropDownModule.forRoot(), _angular_material_select__WEBPACK_IMPORTED_MODULE_20__.MatSelectModule, _angular_material_grid_list__WEBPACK_IMPORTED_MODULE_21__.MatGridListModule, _angular_material_radio__WEBPACK_IMPORTED_MODULE_22__.MatRadioModule, _angular_material_button__WEBPACK_IMPORTED_MODULE_23__.MatButtonModule, _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_24__.MatSlideToggleModule, _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_25__.MatProgressSpinnerModule, _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_26__.MatSidenavModule, _angular_platform_browser__WEBPACK_IMPORTED_MODULE_27__.BrowserModule, _app_routing_module__WEBPACK_IMPORTED_MODULE_0__.AppRoutingModule, _angular_common_http__WEBPACK_IMPORTED_MODULE_28__.HttpClientModule, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.FormsModule, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.ReactiveFormsModule, _angular_material_icon__WEBPACK_IMPORTED_MODULE_30__.MatIconModule, _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_31__.MatToolbarModule, _angular_material_expansion__WEBPACK_IMPORTED_MODULE_32__.MatExpansionModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_33__.NgbModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_33__.NgbTypeaheadModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_33__.NgbAlertModule, _angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_34__.DragDropModule, _angular_platform_browser__WEBPACK_IMPORTED_MODULE_27__.BrowserModule, _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_35__.BrowserAnimationsModule]
});
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_18__["ɵɵsetNgModuleScope"](AppModule, {
    declarations: [_app_component__WEBPACK_IMPORTED_MODULE_1__.AppComponent, _app_component__WEBPACK_IMPORTED_MODULE_1__.SafePipe, _segmentations_segmentations_component__WEBPACK_IMPORTED_MODULE_2__.SegmentationsComponent, _pkl_view_pkl_view_component__WEBPACK_IMPORTED_MODULE_3__.PklViewComponent, _template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_5__.TemplateSegmentationsComponent, _template_segments_header_template_segments_header_component__WEBPACK_IMPORTED_MODULE_6__.TemplateSegmentsHeaderComponent, _drawer_drawer_component__WEBPACK_IMPORTED_MODULE_7__.DrawerComponent, _drawer_content_drawer_content_component__WEBPACK_IMPORTED_MODULE_8__.DrawerContentComponent, _save_template_dialog_save_template_dialog_component__WEBPACK_IMPORTED_MODULE_10__.SaveTemplateDialogComponent, _new_report_new_report_component__WEBPACK_IMPORTED_MODULE_11__.NewReportComponent, _save_suite_dialog_save_suite_dialog_component__WEBPACK_IMPORTED_MODULE_12__.SaveSuiteDialogComponent, _configuration_viewer_configuration_viewer_component__WEBPACK_IMPORTED_MODULE_13__.ConfigurationViewerComponent, _new_report_new_report_result_new_report_result_component__WEBPACK_IMPORTED_MODULE_14__.NewReportResultComponent, _click_outside_directive__WEBPACK_IMPORTED_MODULE_15__.ClickOutsideDirective, _configuration_viewer_udf_arguments_udf_arguments_component__WEBPACK_IMPORTED_MODULE_17__.UdfArgumentsComponent],
    imports: [ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_19__.NgMultiSelectDropDownModule, _angular_material_select__WEBPACK_IMPORTED_MODULE_20__.MatSelectModule, _angular_material_grid_list__WEBPACK_IMPORTED_MODULE_21__.MatGridListModule, _angular_material_radio__WEBPACK_IMPORTED_MODULE_22__.MatRadioModule, _angular_material_button__WEBPACK_IMPORTED_MODULE_23__.MatButtonModule, _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_24__.MatSlideToggleModule, _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_25__.MatProgressSpinnerModule, _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_26__.MatSidenavModule, _angular_platform_browser__WEBPACK_IMPORTED_MODULE_27__.BrowserModule, _app_routing_module__WEBPACK_IMPORTED_MODULE_0__.AppRoutingModule, _angular_common_http__WEBPACK_IMPORTED_MODULE_28__.HttpClientModule, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.FormsModule, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.ReactiveFormsModule, _angular_material_icon__WEBPACK_IMPORTED_MODULE_30__.MatIconModule, _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_31__.MatToolbarModule, _angular_material_expansion__WEBPACK_IMPORTED_MODULE_32__.MatExpansionModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_33__.NgbModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_33__.NgbTypeaheadModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_33__.NgbAlertModule, _angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_34__.DragDropModule, _angular_platform_browser__WEBPACK_IMPORTED_MODULE_27__.BrowserModule, _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_35__.BrowserAnimationsModule]
  });
})();
_angular_core__WEBPACK_IMPORTED_MODULE_18__["ɵɵsetComponentScope"](_template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_5__.TemplateSegmentationsComponent, function () {
  return [_angular_common__WEBPACK_IMPORTED_MODULE_36__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_36__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_36__.NgStyle, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.NgSelectOption, _angular_forms__WEBPACK_IMPORTED_MODULE_29__["ɵNgSelectMultipleOption"], _angular_forms__WEBPACK_IMPORTED_MODULE_29__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.CheckboxControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.SelectControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_29__.NgModel, _pkl_view_pkl_view_component__WEBPACK_IMPORTED_MODULE_3__.PklViewComponent];
}, []);
_angular_core__WEBPACK_IMPORTED_MODULE_18__["ɵɵsetComponentScope"](_drawer_content_drawer_content_component__WEBPACK_IMPORTED_MODULE_8__.DrawerContentComponent, [], function () {
  return [_app_component__WEBPACK_IMPORTED_MODULE_1__.SafePipe];
});

/***/ }),

/***/ 9155:
/*!********************************************!*\
  !*** ./src/app/click-outside.directive.ts ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ClickOutsideDirective": () => (/* binding */ ClickOutsideDirective)
/* harmony export */ });
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_common_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./services/common.service */ 5620);




class ClickOutsideDirective {
  constructor(elementRef, renderer, statSvc, commonSvc) {
    this.elementRef = elementRef;
    this.renderer = renderer;
    this.statSvc = statSvc;
    this.commonSvc = commonSvc;
    this.viewId = 0;
    this.viewguid = '';
    this.segmentName = '';
  }
  ngOnInit() {
    this.commonSvc.onMouseClicked.subscribe(event => {
      let name = this.elementRef.nativeElement.parentNode.parentNode.attributes['name'].value;
      const dropdownPanel = this.elementRef.nativeElement.querySelector('.dropdown-list');
      //const caretIcon = this.elementRef.nativeElement.querySelector('.dropdown-multiselect__caret');
      if (this.statSvc.getDropdownState(this.viewguid, name) == _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.States.Opened) {
        this.statSvc.setDropdownState(this.viewguid, name, _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.States.Open);
        return;
      }
      if (this.statSvc.getDropdownState(this.viewguid, name) == _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.States.Open) {
        dropdownPanel.hidden = true;
        /*if (caretIcon instanceof HTMLElement) {
          caretIcon.classList.add('rotate-180');
        }*/
      } else {
        /*caretIcon.classList.remove('rotate-180');*/
      }
    });
  }
}
ClickOutsideDirective.ɵfac = function ClickOutsideDirective_Factory(t) {
  return new (t || ClickOutsideDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_2__.ElementRef), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_2__.Renderer2), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_services_common_service__WEBPACK_IMPORTED_MODULE_1__.CommonService));
};
ClickOutsideDirective.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineDirective"]({
  type: ClickOutsideDirective,
  selectors: [["", "appClickOutside", ""]],
  inputs: {
    viewId: "viewId",
    viewguid: "viewguid",
    segmentName: "segmentName"
  }
});

/***/ }),

/***/ 5383:
/*!*********************************!*\
  !*** ./src/app/common/enums.ts ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "UDFConstants": () => (/* binding */ UDFConstants),
/* harmony export */   "UDFTitleEnum": () => (/* binding */ UDFTitleEnum),
/* harmony export */   "UDFTypeEnum": () => (/* binding */ UDFTypeEnum)
/* harmony export */ });
var UDFTitleEnum;
(function (UDFTitleEnum) {
  UDFTitleEnum["PREDICTION_READING_FUNCTION"] = "Prediction Reading Function";
  UDFTitleEnum["GT_READING_FUNCTION"] = "GT Reading Function";
  UDFTitleEnum["GT_READING_FUNCTION_SAME_AS_PREDICTION"] = "Same as prediction";
  UDFTitleEnum["GT_READING_FUNCTION_SEPARATE_FUNCTIONS"] = "Separate functions";
  UDFTitleEnum["ASSOCIATION_FUNCTION"] = "Association Function";
  UDFTitleEnum["TRANSFORM_FUNCTION"] = "Transform Function";
  UDFTitleEnum["PARTITIONING_FUNCTION"] = "Partitioning Function";
  UDFTitleEnum["CONFUSION_FUNCTION"] = "Confusion Function";
  UDFTitleEnum["STATISTICS_FUNCTION"] = "Statistics Function";
  UDFTitleEnum["EVALUATE_LOGS_FOLDER"] = "Evaluate Logs Folders";
  UDFTitleEnum["EVALUATE_LOGS_FILES"] = "Evaluate Logs Files";
})(UDFTitleEnum || (UDFTitleEnum = {}));
var UDFTypeEnum;
(function (UDFTypeEnum) {
  UDFTypeEnum["READING_FUNCTIONS"] = "reading_functions";
  UDFTypeEnum["GT_READING_FUNCTIONS"] = "gt_reading_functions";
  UDFTypeEnum["ASSOCIATION_FUNCTIONS"] = "association_functions";
  UDFTypeEnum["TRANSFORM_FUNCTIONS"] = "transform_functions";
  UDFTypeEnum["PARTITIONING_FUNCTIONS"] = "partitioning_functions";
  UDFTypeEnum["CONFUSION_FUNCTIONS"] = "confusion_functions";
  UDFTypeEnum["STATISTICS_FUNCTIONS"] = "statistics_functions";
  UDFTypeEnum["LOGS_NAME_TO_EVALUATE"] = "logs_file_names_to_evaluate";
  UDFTypeEnum["CONFIG_NAME"] = "configName";
  UDFTypeEnum["EVALUATE_FOLDERS"] = "evaluate_folders";
})(UDFTypeEnum || (UDFTypeEnum = {}));
var UDFConstants;
(function (UDFConstants) {
  UDFConstants["DEFAULT_LOG_FILTER"] = "*.json";
  UDFConstants["DEFAULT_FOLDER_FILTER"] = "*";
})(UDFConstants || (UDFConstants = {}));

/***/ }),

/***/ 3213:
/*!************************************************************************!*\
  !*** ./src/app/configuration-viewer/configuration-viewer.component.ts ***!
  \************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConfigurationViewerComponent": () => (/* binding */ ConfigurationViewerComponent)
/* harmony export */ });
/* harmony import */ var _common_enums__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../common/enums */ 5383);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_new_report_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../services/new-report.service */ 9167);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _udf_arguments_udf_arguments_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./udf-arguments/udf-arguments.component */ 1201);






const _c0 = ["readingFunctionImg"];
const _c1 = ["gtReadingFunctionImg"];
const _c2 = ["associationFunctionImg"];
const _c3 = ["transformFunctionImg"];
const _c4 = ["partitioningFunctionImg"];
const _c5 = ["statisticsFunctionImg"];
const _c6 = ["confusionFunctionImg"];
function ConfigurationViewerComponent_div_0_option_39_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const func_r23 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("value", func_r23);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](func_r23);
  }
}
function ConfigurationViewerComponent_div_0_option_57_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const func_r24 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("value", func_r24);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](func_r24);
  }
}
function ConfigurationViewerComponent_div_0_option_70_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const func_r25 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("value", func_r25);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](func_r25);
  }
}
function ConfigurationViewerComponent_div_0_option_83_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const func_r26 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("value", func_r26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](func_r26);
  }
}
function ConfigurationViewerComponent_div_0_option_99_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const func_r27 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("value", func_r27);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](func_r27);
  }
}
function ConfigurationViewerComponent_div_0_option_110_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const func_r28 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("value", func_r28);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](func_r28);
  }
}
function ConfigurationViewerComponent_div_0_option_121_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const func_r29 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("value", func_r29);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](func_r29);
  }
}
const _c7 = function (a0, a1) {
  return {
    "is-invalid": a0,
    "is-valid": a1
  };
};
const _c8 = function (a0) {
  return {
    "pointer-events": a0
  };
};
const _c9 = function (a0, a1, a2, a3) {
  return {
    "is-invalid": a0,
    "is-valid": a1,
    "enable-user-defined-function": a2,
    "disable-user-defined-function": a3
  };
};
function ConfigurationViewerComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r31 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "div", 2)(1, "div", 3)(2, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_div_click_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r30 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r30.close());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](3, "X");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](4, "div", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](6, "div", 6)(7, "div", 7)(8, "div", 8)(9, "div", 9)(10, "label", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](11, "Configuration Name:");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](12, "input", 11, 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_12_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r32 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r32.newReportService.configName = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](14, "div", 13)(15, "div", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](16, "Report Creation");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](17, "div", 15)(18, "div", 8)(19, "div", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelement"](20, "div", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](21, "label", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](22, "Predictions files/folders filter:");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](23, "label", 18)(24, "input", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_24_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r33 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r33.newReportService.evaluate_folders = $event);
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_24_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r34 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r34.logsFolderRadioChanged(true));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](25);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](26, "label", 18)(27, "input", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_27_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r35 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r35.newReportService.evaluate_folders = $event);
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_27_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r36.logsFolderRadioChanged(false));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](28);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](29, "div", 16)(30, "input", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_30_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r37 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r37.newReportService.logsFilter = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](31, "div", 21)(32, "div", 8)(33, "div", 22)(34, "label", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](35);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](36, "div", 16)(37, "select", 24, 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("change", function ConfigurationViewerComponent_div_0_Template_select_change_37_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r38 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r38.onPredictionReadingFunctionChange($event));
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_select_ngModelChange_37_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r39 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r39.newReportService.selectedPredictionReadingFunction = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](39, ConfigurationViewerComponent_div_0_option_39_Template, 2, 2, "option", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](40, "img", 27, 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_img_click_40_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r40 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r40.showArgumentsPanel(ctx_r40.readingFunctionImgElement, ctx_r40.udfTypes.READING_FUNCTIONS, ctx_r40.udfTitles.PREDICTION_READING_FUNCTION, ctx_r40.newReportService.selectedPredictionReadingFunction));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](42, "div", 15)(43, "div", 8)(44, "div", 29)(45, "div", 16)(46, "label");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](47, " GT Reading function: ");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](48, "label", 18)(49, "input", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_49_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r41 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r41.newReportService.gtReadingSameAsPrediction = $event);
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_49_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r42 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r42.gtReadingRadioChanged(true));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](50);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](51, "label", 18)(52, "input", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_52_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r43 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r43.newReportService.gtReadingSameAsPrediction = $event);
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_52_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r44 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r44.gtReadingRadioChanged(false));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](53);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](54, "div", 16)(55, "select", 31, 32);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("change", function ConfigurationViewerComponent_div_0_Template_select_change_55_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r45 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r45.onGTReadingFunctionChange($event));
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_select_ngModelChange_55_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r46 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r46.newReportService.selectedGTReadingFunction = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](57, ConfigurationViewerComponent_div_0_option_57_Template, 2, 2, "option", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](58, "img", 27, 33);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_img_click_58_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r47 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r47.showArgumentsPanel(ctx_r47.gtReadingFunctionImgElement, ctx_r47.udfTypes.GT_READING_FUNCTIONS, ctx_r47.udfTitles.GT_READING_FUNCTION, ctx_r47.newReportService.selectedGTReadingFunction));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](60, "div", 15)(61, "div", 8)(62, "div", 29)(63, "div", 16)(64, "input", 34);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_64_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r48 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r48.newReportService.associationEnabled = $event);
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_64_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r49 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r49.checkboxChanged(ctx_r49.udfTypes.ASSOCIATION_FUNCTIONS));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](65, "label", 35);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](66);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](67, "div", 16)(68, "select", 36, 37);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("change", function ConfigurationViewerComponent_div_0_Template_select_change_68_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r50 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r50.onAssociationFunctionChange($event));
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_select_ngModelChange_68_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r51 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r51.newReportService.selectedAssociationFunction = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](70, ConfigurationViewerComponent_div_0_option_70_Template, 2, 2, "option", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](71, "img", 27, 38);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_img_click_71_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r52 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r52.showArgumentsPanel(ctx_r52.associationFunctionImgElement, ctx_r52.udfTypes.ASSOCIATION_FUNCTIONS, ctx_r52.udfTitles.ASSOCIATION_FUNCTION, ctx_r52.newReportService.selectedAssociationFunction));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](73, "div", 15)(74, "div", 8)(75, "div", 29)(76, "div", 16)(77, "input", 39);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_77_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r53 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r53.newReportService.transformEnabled = $event);
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_77_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r54 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r54.checkboxChanged(ctx_r54.udfTypes.TRANSFORM_FUNCTIONS));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](78, "label", 40);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](79);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](80, "div", 16)(81, "select", 41, 42);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_select_ngModelChange_81_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r55 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r55.newReportService.selectedTransformFunction = $event);
    })("change", function ConfigurationViewerComponent_div_0_Template_select_change_81_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r56 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r56.onTransformFunctionChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](83, ConfigurationViewerComponent_div_0_option_83_Template, 2, 2, "option", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](84, "img", 27, 43);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_img_click_84_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r57 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r57.showArgumentsPanel(ctx_r57.transformFunctionImgElement, ctx_r57.udfTypes.TRANSFORM_FUNCTIONS, ctx_r57.udfTitles.TRANSFORM_FUNCTION, ctx_r57.newReportService.selectedAssociationFunction));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](86, "div", 13)(87, "div", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](88, "Report View");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](89, "div", 15)(90, "div", 8)(91, "div", 29)(92, "div", 16)(93, "input", 39);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_93_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r58 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r58.newReportService.partitioningEnabled = $event);
    })("ngModelChange", function ConfigurationViewerComponent_div_0_Template_input_ngModelChange_93_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r59 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r59.checkboxChanged(ctx_r59.udfTypes.PARTITIONING_FUNCTIONS));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](94, "label", 44);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](95);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](96, "div", 16)(97, "select", 45, 46);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_select_ngModelChange_97_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r60 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r60.newReportService.selectedPartitioningFunction = $event);
    })("change", function ConfigurationViewerComponent_div_0_Template_select_change_97_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r61 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r61.onPartitioningFunctionChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](99, ConfigurationViewerComponent_div_0_option_99_Template, 2, 2, "option", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](100, "img", 27, 47);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_img_click_100_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r62 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r62.showArgumentsPanel(ctx_r62.partitioningFunctionImgElement, ctx_r62.udfTypes.PARTITIONING_FUNCTIONS, ctx_r62.udfTitles.PARTITIONING_FUNCTION, ctx_r62.newReportService.selectedPartitioningFunction));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](102, "div", 15)(103, "div", 8)(104, "div", 29)(105, "label", 48);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](106);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](107, "div", 16)(108, "select", 49, 50);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_select_ngModelChange_108_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r63 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r63.newReportService.selectedStatisticsFunction = $event);
    })("change", function ConfigurationViewerComponent_div_0_Template_select_change_108_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r64 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r64.onStatisticsFunctionChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](110, ConfigurationViewerComponent_div_0_option_110_Template, 2, 2, "option", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](111, "img", 27, 51);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_img_click_111_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r65 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r65.showArgumentsPanel(ctx_r65.statisticsFunctionImgElement, ctx_r65.udfTypes.STATISTICS_FUNCTIONS, ctx_r65.udfTitles.STATISTICS_FUNCTION, ctx_r65.newReportService.selectedStatisticsFunction));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](113, "div", 15)(114, "div", 8)(115, "div", 22)(116, "label", 52);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](117);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](118, "div", 16)(119, "select", 53, 54);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function ConfigurationViewerComponent_div_0_Template_select_ngModelChange_119_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r66 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r66.newReportService.selectedConfusionFunction = $event);
    })("change", function ConfigurationViewerComponent_div_0_Template_select_change_119_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r67 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r67.onConfusionFunctionChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](121, ConfigurationViewerComponent_div_0_option_121_Template, 2, 2, "option", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](122, "img", 27, 55);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_img_click_122_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r68 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r68.showArgumentsPanel(ctx_r68.confusionFunctionImgElement, ctx_r68.udfTypes.CONFUSION_FUNCTIONS, ctx_r68.udfTitles.CONFUSION_FUNCTION, ctx_r68.newReportService.selectedConfusionFunction));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](124, "div", 56)(125, "button", 57);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function ConfigurationViewerComponent_div_0_Template_button_click_125_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r31);
      const ctx_r69 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r69.newReportService.saveConfig());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](126, "Save");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](13);
    const _r2 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](38);
    const _r5 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](56);
    const _r8 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](69);
    const _r11 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](82);
    const _r14 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](98);
    const _r17 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](109);
    const _r20 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](120);
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](ctx_r0.getTitle());
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](7);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.configName)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction2"](65, _c7, _r1.invalid && _r1.touched, _r1.valid && _r1.touched));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](12);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.evaluate_folders)("value", false);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"](" ", ctx_r0.udfTitles.EVALUATE_LOGS_FILES, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.evaluate_folders)("value", true);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"](" ", ctx_r0.udfTitles.EVALUATE_LOGS_FOLDER, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.logsFilter);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"]("", ctx_r0.udfTitles.PREDICTION_READING_FUNCTION, ":");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.selectedPredictionReadingFunction)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction2"](68, _c7, _r2.invalid && _r2.touched, _r2.valid && _r2.touched));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx_r0.newReportService.prediction_reading_functions);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx_r0.getArgumentSvg(ctx_r0.udfTypes.READING_FUNCTIONS), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction1"](71, _c8, ctx_r0.enableArgumentsButton(ctx_r0.udfTypes.READING_FUNCTIONS) ? "all" : "none"));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](9);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.gtReadingSameAsPrediction)("value", true);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"](" ", ctx_r0.udfTitles.GT_READING_FUNCTION_SAME_AS_PREDICTION, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.gtReadingSameAsPrediction)("value", false);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"](" ", ctx_r0.udfTitles.GT_READING_FUNCTION_SEPARATE_FUNCTIONS, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.selectedGTReadingFunction)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction4"](73, _c9, _r5.invalid && _r5.touched, _r5.valid && _r5.touched, !ctx_r0.newReportService.gtReadingSameAsPrediction, ctx_r0.newReportService.gtReadingSameAsPrediction))("disabled", ctx_r0.newReportService.gtReadingSameAsPrediction);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx_r0.newReportService.gt_reading_functions);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx_r0.getArgumentSvg(ctx_r0.udfTypes.GT_READING_FUNCTIONS), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction1"](78, _c8, ctx_r0.enableArgumentsButton(ctx_r0.udfTypes.GT_READING_FUNCTIONS) ? "all" : "none"));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.associationEnabled);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"]("", ctx_r0.udfTitles.ASSOCIATION_FUNCTION, ":");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.selectedAssociationFunction)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction4"](80, _c9, _r8.invalid && _r8.touched, _r8.valid && _r8.touched, ctx_r0.newReportService.associationEnabled, !ctx_r0.newReportService.associationEnabled))("disabled", !ctx_r0.newReportService.associationEnabled);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx_r0.newReportService.association_functions);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx_r0.getArgumentSvg(ctx_r0.udfTypes.ASSOCIATION_FUNCTIONS), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction1"](85, _c8, ctx_r0.enableArgumentsButton(ctx_r0.udfTypes.ASSOCIATION_FUNCTIONS) ? "all" : "none"));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.transformEnabled);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"]("", ctx_r0.udfTitles.TRANSFORM_FUNCTION, ":");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.selectedTransformFunction)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction4"](87, _c9, _r11.invalid && _r11.touched, _r11.valid && _r11.touched, ctx_r0.newReportService.transformEnabled, !ctx_r0.newReportService.transformEnabled))("disabled", !ctx_r0.newReportService.transformEnabled);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx_r0.newReportService.transform_functions);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx_r0.getArgumentSvg(ctx_r0.udfTypes.TRANSFORM_FUNCTIONS), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction1"](92, _c8, ctx_r0.enableArgumentsButton(ctx_r0.udfTypes.TRANSFORM_FUNCTIONS) ? "all" : "none"));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](9);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.partitioningEnabled);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"]("", ctx_r0.udfTitles.PARTITIONING_FUNCTION, ":");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.selectedPartitioningFunction)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction4"](94, _c9, _r14.invalid && _r14.touched, _r14.valid && _r14.touched, ctx_r0.newReportService.partitioningEnabled, !ctx_r0.newReportService.partitioningEnabled))("disabled", !ctx_r0.newReportService.partitioningEnabled);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx_r0.newReportService.partitioning_functions);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx_r0.getArgumentSvg(ctx_r0.udfTypes.PARTITIONING_FUNCTIONS), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction1"](99, _c8, ctx_r0.enableArgumentsButton(ctx_r0.udfTypes.PARTITIONING_FUNCTIONS) ? "all" : "none"));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"]("", ctx_r0.udfTitles.STATISTICS_FUNCTION, ":");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.selectedStatisticsFunction)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction2"](101, _c7, _r17.invalid && _r17.touched, _r17.valid && _r17.touched));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx_r0.newReportService.statistics_functions);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx_r0.getArgumentSvg(ctx_r0.udfTypes.STATISTICS_FUNCTIONS), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction1"](104, _c8, ctx_r0.enableArgumentsButton(ctx_r0.udfTypes.STATISTICS_FUNCTIONS) ? "all" : "none"));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"]("", ctx_r0.udfTitles.CONFUSION_FUNCTION, ":");
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx_r0.newReportService.selectedConfusionFunction)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction2"](106, _c7, _r20.invalid && _r20.touched, _r20.valid && _r20.touched));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx_r0.newReportService.confusion_functions);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx_r0.getArgumentSvg(ctx_r0.udfTypes.CONFUSION_FUNCTIONS), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction1"](109, _c8, ctx_r0.enableArgumentsButton(ctx_r0.udfTypes.CONFUSION_FUNCTIONS) ? "all" : "none"));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("disabled", ctx_r0.disableSaveButton());
  }
}
class ConfigurationViewerComponent {
  constructor(newReportService) {
    this.newReportService = newReportService;
    this.readingFunctionImgElement = null;
    this.gtReadingFunctionImgElement = null;
    this.associationFunctionImgElement = null;
    this.transformFunctionImgElement = null;
    this.partitioningFunctionImgElement = null;
    this.statisticsFunctionImgElement = null;
    this.confusionFunctionImgElement = null;
    this.title = 'New Configuration';
    this.showPredictionAguments = false;
    this.functionOpenedArguments = '';
    this.udfTitles = _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTitleEnum;
    this.udfTypes = _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum;
    this.ARGUMENT_GRAY_ICON = 'assets/argument-gray-icon.svg';
    this.ARGUMENT_GREEN_ICON = 'assets/argument-green-icon.svg';
    this.ARGUMENT_RED_ICON = 'assets/argument-red-icon.svg';
  }
  ngOnInit() {}
  togglePanel() {
    this.newReportService.isPanelOpen = !this.newReportService.isPanelOpen;
  }
  close() {
    this.newReportService.showConfigViewer = false;
  }
  disableSaveButton() {
    if (this.newReportService.configName == '') return true;
    if (this.newReportService.selectedPredictionReadingFunction == '') return true;
    //else if (this.newReportService.selectedPredictionReadingFunction != '' && !this.paramsHaveValue(UDFTypeEnum.READING_FUNCTIONS)) return true;
    if (!this.newReportService.gtReadingSameAsPrediction && this.newReportService.selectedGTReadingFunction == '') return true;
    //else if (!this.newReportService.gtReadingSameAsPrediction && this.newReportService.selectedGTReadingFunction != '' && !this.paramsHaveValue(UDFTypeEnum.GT_READING_FUNCTIONS)) return true;
    if (this.newReportService.transformEnabled && this.newReportService.selectedTransformFunction == '') return true;
    //else if (this.newReportService.transformEnabled && this.newReportService.selectedTransformFunction != '' && !this.paramsHaveValue(UDFTypeEnum.TRANSFORM_FUNCTIONS)) return true;
    if (this.newReportService.selectedStatisticsFunction == '') return true;
    //else if (this.newReportService.selectedStatisticsFunction != '' && !this.paramsHaveValue(UDFTypeEnum.STATISTICS_FUNCTIONS)) return true;
    if (this.newReportService.partitioningEnabled && this.newReportService.selectedPartitioningFunction == '') return true;
    //else if (this.newReportService.partitioningEnabled && this.newReportService.selectedPartitioningFunction != ''  && !this.paramsHaveValue(UDFTypeEnum.PARTITIONING_FUNCTIONS)) return true;
    if (this.newReportService.selectedConfusionFunction == '') return true;
    //else if (this.newReportService.selectedConfusionFunction != '' && !this.paramsHaveValue(UDFTypeEnum.CONFUSION_FUNCTIONS)) return true;
    return false;
  }
  getTitle() {
    if (this.newReportService.configName != '') return this.newReportService.configName;
    return 'New Configuration';
  }
  onPredictionReadingFunctionChange(event) {
    this.newReportService.showParams = false;
    if (!this.functionHasArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.READING_FUNCTIONS, this.newReportService.selectedPredictionReadingFunction)) return;
    const selectedValue = event.target.value;
    this.newReportService.getUDFUserArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.READING_FUNCTIONS, selectedValue);
    this.showArgumentsPanel(this.readingFunctionImgElement, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.READING_FUNCTIONS, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTitleEnum.PREDICTION_READING_FUNCTION, this.newReportService.selectedPredictionReadingFunction, true);
  }
  onGTReadingFunctionChange(event) {
    this.newReportService.showParams = false;
    if (!this.functionHasArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.GT_READING_FUNCTIONS, this.newReportService.selectedGTReadingFunction)) return;
    const selectedValue = event.target.value;
    this.newReportService.getUDFUserArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.GT_READING_FUNCTIONS, selectedValue);
    this.showArgumentsPanel(this.gtReadingFunctionImgElement, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.GT_READING_FUNCTIONS, this.udfTitles.GT_READING_FUNCTION, this.newReportService.selectedGTReadingFunction, true);
  }
  onAssociationFunctionChange(event) {
    this.newReportService.showParams = false;
    if (!this.functionHasArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.ASSOCIATION_FUNCTIONS, this.newReportService.selectedAssociationFunction)) return;
    const selectedValue = event.target.value;
    this.newReportService.getUDFUserArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.ASSOCIATION_FUNCTIONS, selectedValue);
    this.showArgumentsPanel(this.gtReadingFunctionImgElement, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.ASSOCIATION_FUNCTIONS, this.udfTitles.ASSOCIATION_FUNCTION, this.newReportService.selectedAssociationFunction, true);
  }
  onStatisticsFunctionChange(event) {
    this.newReportService.showParams = false;
    if (!this.functionHasArguments(this.udfTypes.STATISTICS_FUNCTIONS, this.newReportService.selectedStatisticsFunction)) return;
    const selectedValue = event.target.value;
    this.newReportService.getUDFUserArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.STATISTICS_FUNCTIONS, selectedValue);
    this.showArgumentsPanel(this.statisticsFunctionImgElement, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.STATISTICS_FUNCTIONS, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTitleEnum.STATISTICS_FUNCTION, this.newReportService.selectedStatisticsFunction, true);
  }
  onConfusionFunctionChange(event) {
    this.newReportService.showParams = false;
    if (!this.functionHasArguments(this.udfTypes.CONFUSION_FUNCTIONS, this.newReportService.selectedConfusionFunction)) return;
    const selectedValue = event.target.value;
    this.newReportService.getUDFUserArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.CONFUSION_FUNCTIONS, selectedValue);
    this.showArgumentsPanel(this.confusionFunctionImgElement, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.CONFUSION_FUNCTIONS, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTitleEnum.CONFUSION_FUNCTION, this.newReportService.selectedConfusionFunction, true);
  }
  onTransformFunctionChange(event) {
    this.newReportService.showParams = false;
    if (!this.functionHasArguments(this.udfTypes.TRANSFORM_FUNCTIONS, this.newReportService.selectedTransformFunction)) return;
    const selectedValue = event.target.value;
    this.newReportService.getUDFUserArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.TRANSFORM_FUNCTIONS, selectedValue);
    this.showArgumentsPanel(this.transformFunctionImgElement, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.TRANSFORM_FUNCTIONS, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTitleEnum.TRANSFORM_FUNCTION, this.newReportService.selectedTransformFunction, true);
  }
  onPartitioningFunctionChange(event) {
    this.newReportService.showParams = false;
    if (!this.functionHasArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.PARTITIONING_FUNCTIONS, this.newReportService.selectedPartitioningFunction)) return;
    const selectedValue = event.target.value;
    this.newReportService.getUDFUserArguments(_common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.PARTITIONING_FUNCTIONS, selectedValue);
    this.showArgumentsPanel(this.partitioningFunctionImgElement, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.PARTITIONING_FUNCTIONS, _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTitleEnum.PARTITIONING_FUNCTION, this.newReportService.selectedPartitioningFunction, true);
  }
  getArgumentSVGType(funcType, selectedFunction, isEnabled = true) {
    if (selectedFunction == '') return this.ARGUMENT_GRAY_ICON;else {
      if (!this.functionHasArguments(funcType, selectedFunction)) return this.ARGUMENT_GRAY_ICON;
      if (this.paramsHaveValue(funcType)) {
        return this.ARGUMENT_GREEN_ICON;
      } else {
        return this.ARGUMENT_RED_ICON;
      }
    }
  }
  getArgumentSvg(funcType) {
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.READING_FUNCTIONS) {
      return this.getArgumentSVGType(funcType, this.newReportService.selectedPredictionReadingFunction);
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.GT_READING_FUNCTIONS) {
      return this.getArgumentSVGType(funcType, this.newReportService.selectedGTReadingFunction, !this.newReportService.gtReadingSameAsPrediction);
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.ASSOCIATION_FUNCTIONS) {
      return this.getArgumentSVGType(funcType, this.newReportService.selectedAssociationFunction, this.newReportService.associationEnabled);
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.TRANSFORM_FUNCTIONS) {
      return this.getArgumentSVGType(funcType, this.newReportService.selectedTransformFunction, this.newReportService.transformEnabled);
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.PARTITIONING_FUNCTIONS) {
      return this.getArgumentSVGType(funcType, this.newReportService.selectedPartitioningFunction, this.newReportService.partitioningEnabled);
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.CONFUSION_FUNCTIONS) {
      return this.getArgumentSVGType(funcType, this.newReportService.selectedConfusionFunction);
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.STATISTICS_FUNCTIONS) {
      return this.getArgumentSVGType(funcType, this.newReportService.selectedStatisticsFunction);
    }
    return this.ARGUMENT_RED_ICON;
  }
  showArgumentsPanel(elm, funcType, title, funcName, forceShow = false) {
    if (forceShow) {
      this.newReportService.showParams = true;
    } else {
      this.newReportService.showParams = !this.newReportService.showParams;
      if (!this.newReportService.showParams) return;
    }
    if (elm == null) return;
    const img = elm.nativeElement;
    const imgRect = img.getBoundingClientRect();
    this.newReportService.argPanelTop = `${imgRect.top - 40}px`;
    this.newReportService.argPanelLeft = `${imgRect.right + window.scrollX + 10}px`;
    this.newReportService.showArgumentsPanel(funcType, title, funcName);
    this.functionOpenedArguments = funcType;
  }
  enableArgumentsButton(funcType) {
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.READING_FUNCTIONS) {
      if (this.newReportService.selectedPredictionReadingFunction != '' && this.functionHasArguments(funcType, this.newReportService.selectedPredictionReadingFunction)) return true;
      return false;
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.GT_READING_FUNCTIONS) {
      if (this.newReportService.selectedGTReadingFunction != '' && !this.newReportService.gtReadingSameAsPrediction && this.functionHasArguments(funcType, this.newReportService.selectedGTReadingFunction)) return true;
      return false;
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.ASSOCIATION_FUNCTIONS) {
      if (this.newReportService.selectedAssociationFunction != '' && this.newReportService.associationEnabled && this.functionHasArguments(funcType, this.newReportService.selectedAssociationFunction)) return true;
      return false;
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.TRANSFORM_FUNCTIONS) {
      if (this.newReportService.selectedTransformFunction != '' && this.newReportService.transformEnabled && this.functionHasArguments(funcType, this.newReportService.selectedTransformFunction)) return true;
      return false;
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.PARTITIONING_FUNCTIONS) {
      if (this.newReportService.selectedPartitioningFunction != '' && this.newReportService.partitioningEnabled && this.functionHasArguments(funcType, this.newReportService.selectedPartitioningFunction)) return true;
      return false;
    }
    return false;
  }
  paramsHaveValue(funcType) {
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.READING_FUNCTIONS) {
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedPredictionReadingFunction);
      if (x == undefined || x.params == undefined) return false;
      let b = true;
      x.params.forEach(p => {
        if (p.value == '') b = false;
      });
      return b;
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.GT_READING_FUNCTIONS) {
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedGTReadingFunction);
      let b = true;
      x.params.forEach(p => {
        if (p.value == '') b = false;
      });
      return b;
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.ASSOCIATION_FUNCTIONS) {
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedAssociationFunction);
      let b = true;
      x.params.forEach(p => {
        if (p.value == '') b = false;
      });
      return b;
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.TRANSFORM_FUNCTIONS) {
      let x = this.newReportService.udf.get(funcType)?.find(x => x.funcName == this.newReportService.selectedTransformFunction);
      let b = true;
      x.params.forEach(p => {
        if (p.value == '') b = false;
      });
      return b;
    }
    return true;
  }
  checkboxChanged(funcType) {
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.GT_READING_FUNCTIONS) {
      if (this.newReportService.gtReadingSameAsPrediction && this.functionOpenedArguments == funcType) {
        this.newReportService.showParams = false;
      }
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.ASSOCIATION_FUNCTIONS) {
      if (this.newReportService.associationEnabled && this.functionOpenedArguments == funcType) {
        this.newReportService.showParams = false;
      }
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.TRANSFORM_FUNCTIONS) {
      if (this.newReportService.transformEnabled && this.functionOpenedArguments == funcType) {
        this.newReportService.showParams = false;
      }
    }
    if (funcType == _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFTypeEnum.PARTITIONING_FUNCTIONS) {
      if (this.newReportService.partitioningEnabled && this.functionOpenedArguments == funcType) {
        this.newReportService.showParams = false;
      }
    }
  }
  logsFolderRadioChanged(processLogsFolder) {
    if (processLogsFolder) {
      this.newReportService.logsFilter = _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFConstants.DEFAULT_LOG_FILTER;
    } else {
      this.newReportService.logsFilter = _common_enums__WEBPACK_IMPORTED_MODULE_0__.UDFConstants.DEFAULT_FOLDER_FILTER;
    }
  }
  gtReadingRadioChanged(sameAsPredicted) {
    if (sameAsPredicted) {
      this.newReportService.gtReadingSameAsPrediction = true;
      this.newReportService.showParams = false;
      this.newReportService.selectedGTReadingFunction = '';
    } else {
      this.newReportService.gtReadingSameAsPrediction = false;
      this.newReportService.showParams = false;
    }
  }
  functionHasArguments(funcType, funcName) {
    let funcs = this.newReportService.udf.get(funcType);
    if (funcs != undefined) {
      let f = funcs.find(x => x.funcName == funcName);
      if (f != undefined) {
        return f.params.length > 0;
      }
    }
    return false;
  }
}
ConfigurationViewerComponent.ɵfac = function ConfigurationViewerComponent_Factory(t) {
  return new (t || ConfigurationViewerComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdirectiveInject"](_services_new_report_service__WEBPACK_IMPORTED_MODULE_1__.NewReportService));
};
ConfigurationViewerComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineComponent"]({
  type: ConfigurationViewerComponent,
  selectors: [["configuration-viewer"]],
  viewQuery: function ConfigurationViewerComponent_Query(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c0, 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c1, 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c2, 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c3, 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c4, 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c5, 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c6, 5);
    }
    if (rf & 2) {
      let _t;
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.readingFunctionImgElement = _t.first);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.gtReadingFunctionImgElement = _t.first);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.associationFunctionImgElement = _t.first);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.transformFunctionImgElement = _t.first);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.partitioningFunctionImgElement = _t.first);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.statisticsFunctionImgElement = _t.first);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.confusionFunctionImgElement = _t.first);
    }
  },
  decls: 2,
  vars: 4,
  consts: [["class", "configuration-container", 4, "ngIf"], [3, "top", "left", "show"], [1, "configuration-container"], [1, "configuration-header"], [1, "closeButton", 3, "click"], [1, "titleText"], [1, "configuration-content"], [1, "row", 2, "width", "100%", "margin-bottom", "7px"], [1, "col"], [1, "form-group"], ["for", "config_name", 2, "font-weight", "bold"], ["type", "text", "id", "config_name", "placeholder", "", "name", "config_name", "minlength", "3", "required", "", "name", "config_name", "name", "config_name", 1, "form-control", "form-control-sm", 2, "min-height", "0px !important", "width", "100%", "padding-right", "10px", 3, "ngModel", "ngClass", "ngModelChange"], ["nameInput", "ngModel"], [1, "report-container"], [1, "report-caption"], [1, "row", 2, "width", "100%"], [2, "display", "flex", "align-items", "center"], ["for", "log_name", 2, "font-weight", "bold"], [2, "margin-left", "20px"], ["type", "radio", "name", "evaluate_logs_folder", 3, "ngModel", "value", "ngModelChange"], ["type", "text", "id", "log_name", "name", "logs_filter", "name", "logs_filter", 1, "form-control", "form-control-sm", 2, "min-height", "0px !important", 3, "ngModel", "ngModelChange"], [1, "row", 2, "width", "104.5%", "padding-right", "0px !important"], [1, "form-group", 2, "width", "100% !important"], ["for", "prediction_reading_function", 2, "font-weight", "bold"], ["id", "prediction_reading_function", "name", "prediction_reading_function", "required", "", 1, "form-select", "form-select-sm", 2, "padding-right", "10px", "width", "90%", 3, "ngModel", "ngClass", "change", "ngModelChange"], ["predictionReadingFunctionSelect", "ngModel"], [3, "value", 4, "ngFor", "ngForOf"], [2, "margin-left", "5px", "cursor", "pointer", 3, "src", "ngStyle", "click"], ["readingFunctionImg", ""], [1, "form-group", 2, "width", "101% !important"], ["type", "radio", "name", "gt_reading_function", 3, "ngModel", "value", "ngModelChange"], ["name", "gt_reading_function", "id", "gt_reading_function", "required", "", 1, "form-select", "form-select-sm", 2, "padding-right", "10px", "width", "100%", 3, "ngModel", "ngClass", "disabled", "change", "ngModelChange"], ["gtReadingFunctionSelect", "ngModel"], ["gtReadingFunctionImg", ""], ["type", "checkbox", "name", "association_functions", 2, "margin-right", "3px", 3, "ngModel", "ngModelChange"], ["for", "association_functions", 2, "font-weight", "bold"], ["id", "association_functions", "required", "", 1, "form-select", "form-select-sm", 2, "padding-right", "10px", "width", "100%", 3, "ngModel", "ngClass", "disabled", "change", "ngModelChange"], ["associationFunctionSelect", "ngModel"], ["associationFunctionImg", ""], ["type", "checkbox", 2, "margin-right", "3px", 3, "ngModel", "ngModelChange"], ["for", "transform_functions", 2, "font-weight", "bold"], ["id", "transform_functions", "required", "", "name", "transform_functions", 1, "form-select", "form-select-sm", 2, "padding-right", "10px", "width", "100%", 3, "ngModel", "ngClass", "disabled", "ngModelChange", "change"], ["transformFunctionSelect", "ngModel"], ["transformFunctionImg", ""], ["for", "partitioning_functions", 2, "font-weight", "bold"], ["id", "partitioning_functions", "name", "partitioning_functions", "required", "", 1, "form-select", "form-select-sm", 2, "padding-right", "10px", "width", "100%", 3, "ngModel", "ngClass", "disabled", "ngModelChange", "change"], ["partitFunctionSelect", "ngModel"], ["partitioningFunctionImg", ""], ["for", "statistics_function", 2, "font-weight", "bold"], ["id", "statistics_function", "name", "statistics_functions", "required", "", 1, "form-select", "form-select-sm", 2, "padding-right", "10px", "width", "100%", 3, "ngModel", "ngClass", "ngModelChange", "change"], ["statFunctionSelect", "ngModel"], ["statisticsFunctionImg", ""], ["for", "Confusion_function", 2, "font-weight", "bold"], ["id", "Confusion_function", "name", "confusion_functions", "required", "", 1, "form-select", "form-select-sm", 2, "padding-right", "10px", "width", "100%", 3, "ngModel", "ngClass", "ngModelChange", "change"], ["confFunctionSelect", "ngModel"], ["ConfusionFunctionImg", ""], [1, "form-footer"], ["type", "button", 1, "btn", "btn", "btn-primary", "btn-mdcd", 2, "margin-bottom", "5px", 3, "disabled", "click"], [3, "value"]],
  template: function ConfigurationViewerComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](0, ConfigurationViewerComponent_div_0_Template, 127, 111, "div", 0);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelement"](1, "udf-arguments", 1);
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngIf", ctx.newReportService.showConfigViewer);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("top", ctx.newReportService.argPanelTop)("left", ctx.newReportService.argPanelLeft)("show", ctx.newReportService.showParams);
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_4__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_4__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_4__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_4__.NgStyle, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.NgSelectOption, _angular_forms__WEBPACK_IMPORTED_MODULE_5__["ɵNgSelectMultipleOption"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.CheckboxControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.SelectControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.RadioControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.RequiredValidator, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.MinLengthValidator, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.NgModel, _udf_arguments_udf_arguments_component__WEBPACK_IMPORTED_MODULE_2__.UdfArgumentsComponent],
  styles: [".configuration-container[_ngcontent-%COMP%] {\r\n    width: 100%;\r\n    min-height: 580px;\r\n    padding: 0px;\r\n    display: flex;\r\n    flex-direction: column;\r\n    border: 1px solid lightgray;\r\n    background: #fafafa;\r\n  }\r\n\r\n  .closeButton[_ngcontent-%COMP%]{\r\n    margin-right: 0px;\r\n    position:absolute;\r\n    padding-left:2px;\r\n    cursor: pointer;\r\n    color: #182a69;\r\n  }\r\n\r\n  .titleText[_ngcontent-%COMP%]{\r\n    flex-grow: 1;\r\n    text-align: center;\r\n  }\r\n  \r\n  .configuration-header[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    text-align: center;\r\n    position: relative;\r\n    margin-bottom: 0px;\r\n    background-color: #E4F0F5;\r\n    border-bottom: 1px solid lightgray;\r\n    color: #182a69;\r\n    font-size: 18px;\r\n    font-weight: bold;\r\n  }\r\n\r\n  .configuration-content[_ngcontent-%COMP%] {\r\n    flex-grow: 1;\r\n    display: flex;\r\n    align-items: stretch;\r\n    padding:5px;\r\n    flex-direction: column;\r\n  }\r\n\r\n  .form-footer[_ngcontent-%COMP%] {\r\n    text-align: center;\r\n    margin-top: 0px;\r\n  }\r\n  \r\n  .enable-user-defined-function[_ngcontent-%COMP%] {\r\n    color: #182a69; \r\n  }\r\n  \r\n  .disable-user-defined-function[_ngcontent-%COMP%] {\r\n    color: lightgray; \r\n  }\r\n\r\n  .report-container[_ngcontent-%COMP%] {\r\n    border: 1px solid #ccc;\r\n    border-radius: 5px;\r\n    padding: 10px;\r\n    margin-bottom: 20px;\r\n  }\r\n  \r\n  .report-caption[_ngcontent-%COMP%] {\r\n    font-weight: bold;\r\n    margin-bottom: 10px;\r\n    color: #800080;\r\n  }\r\n\r\n \r\n.expandable-panel[_ngcontent-%COMP%] {\r\n  border: 1px solid #ccc;\r\n  border-radius: 5px;\r\n  margin-bottom: 20px;\r\n}\r\n\r\n.panel-header[_ngcontent-%COMP%] {\r\n  background-color: #006400; \r\n  color: #fff; \r\n  padding: 5px 10px; \r\n  cursor: pointer;\r\n  display: flex;\r\n  justify-content: space-between;\r\n  align-items: center;\r\n}\r\n\r\n.header-text[_ngcontent-%COMP%] {\r\n  font-weight: bold;\r\n  margin: 0;\r\n}\r\n\r\n.caret[_ngcontent-%COMP%] {\r\n  font-size: 16px; \r\n  transition: transform 0.3s;\r\n}\r\n\r\n.rotate[_ngcontent-%COMP%] {\r\n  transform: rotate(180deg);\r\n}\r\n\r\n.button-container[_ngcontent-%COMP%] {\r\n  position: relative;\r\n  \r\n}\r\n\r\n.dynamic-div[_ngcontent-%COMP%] {\r\n  position: absolute;\r\n  background-color: #fff;\r\n  border: 1px solid #ccc;\r\n  padding: 10px;\r\n  \r\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29uZmlndXJhdGlvbi12aWV3ZXIvY29uZmlndXJhdGlvbi12aWV3ZXIuY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLFdBQVc7SUFDWCxpQkFBaUI7SUFDakIsWUFBWTtJQUNaLGFBQWE7SUFDYixzQkFBc0I7SUFDdEIsMkJBQTJCO0lBQzNCLG1CQUFtQjtFQUNyQjs7RUFFQTtJQUNFLGlCQUFpQjtJQUNqQixpQkFBaUI7SUFDakIsZ0JBQWdCO0lBQ2hCLGVBQWU7SUFDZixjQUFjO0VBQ2hCOztFQUVBO0lBQ0UsWUFBWTtJQUNaLGtCQUFrQjtFQUNwQjs7RUFFQTtJQUNFLGFBQWE7SUFDYixrQkFBa0I7SUFDbEIsa0JBQWtCO0lBQ2xCLGtCQUFrQjtJQUNsQix5QkFBeUI7SUFDekIsa0NBQWtDO0lBQ2xDLGNBQWM7SUFDZCxlQUFlO0lBQ2YsaUJBQWlCO0VBQ25COztFQUVBO0lBQ0UsWUFBWTtJQUNaLGFBQWE7SUFDYixvQkFBb0I7SUFDcEIsV0FBVztJQUNYLHNCQUFzQjtFQUN4Qjs7RUFFQTtJQUNFLGtCQUFrQjtJQUNsQixlQUFlO0VBQ2pCOztFQUVBO0lBQ0UsY0FBYyxFQUFFLHVCQUF1QjtFQUN6Qzs7RUFFQTtJQUNFLGdCQUFnQixFQUFFLHdCQUF3QjtFQUM1Qzs7RUFFQTtJQUNFLHNCQUFzQjtJQUN0QixrQkFBa0I7SUFDbEIsYUFBYTtJQUNiLG1CQUFtQjtFQUNyQjs7RUFFQTtJQUNFLGlCQUFpQjtJQUNqQixtQkFBbUI7SUFDbkIsY0FBYztFQUNoQjs7Q0FFRCwwQ0FBMEM7QUFDM0M7RUFDRSxzQkFBc0I7RUFDdEIsa0JBQWtCO0VBQ2xCLG1CQUFtQjtBQUNyQjs7QUFFQTtFQUNFLHlCQUF5QixFQUFFLHlDQUF5QztFQUNwRSxXQUFXLEVBQUUsb0NBQW9DO0VBQ2pELGlCQUFpQixFQUFFLHdDQUF3QztFQUMzRCxlQUFlO0VBQ2YsYUFBYTtFQUNiLDhCQUE4QjtFQUM5QixtQkFBbUI7QUFDckI7O0FBRUE7RUFDRSxpQkFBaUI7RUFDakIsU0FBUztBQUNYOztBQUVBO0VBQ0UsZUFBZSxFQUFFLGlDQUFpQztFQUNsRCwwQkFBMEI7QUFDNUI7O0FBRUE7RUFDRSx5QkFBeUI7QUFDM0I7O0FBRUE7RUFDRSxrQkFBa0I7RUFDbEIsbUNBQW1DO0FBQ3JDOztBQUVBO0VBQ0Usa0JBQWtCO0VBQ2xCLHNCQUFzQjtFQUN0QixzQkFBc0I7RUFDdEIsYUFBYTtFQUNiLCtCQUErQjtBQUNqQyIsInNvdXJjZXNDb250ZW50IjpbIi5jb25maWd1cmF0aW9uLWNvbnRhaW5lciB7XHJcbiAgICB3aWR0aDogMTAwJTtcclxuICAgIG1pbi1oZWlnaHQ6IDU4MHB4O1xyXG4gICAgcGFkZGluZzogMHB4O1xyXG4gICAgZGlzcGxheTogZmxleDtcclxuICAgIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XHJcbiAgICBib3JkZXI6IDFweCBzb2xpZCBsaWdodGdyYXk7XHJcbiAgICBiYWNrZ3JvdW5kOiAjZmFmYWZhO1xyXG4gIH1cclxuXHJcbiAgLmNsb3NlQnV0dG9ue1xyXG4gICAgbWFyZ2luLXJpZ2h0OiAwcHg7XHJcbiAgICBwb3NpdGlvbjphYnNvbHV0ZTtcclxuICAgIHBhZGRpbmctbGVmdDoycHg7XHJcbiAgICBjdXJzb3I6IHBvaW50ZXI7XHJcbiAgICBjb2xvcjogIzE4MmE2OTtcclxuICB9XHJcblxyXG4gIC50aXRsZVRleHR7XHJcbiAgICBmbGV4LWdyb3c6IDE7XHJcbiAgICB0ZXh0LWFsaWduOiBjZW50ZXI7XHJcbiAgfVxyXG4gIFxyXG4gIC5jb25maWd1cmF0aW9uLWhlYWRlciB7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgdGV4dC1hbGlnbjogY2VudGVyO1xyXG4gICAgcG9zaXRpb246IHJlbGF0aXZlO1xyXG4gICAgbWFyZ2luLWJvdHRvbTogMHB4O1xyXG4gICAgYmFja2dyb3VuZC1jb2xvcjogI0U0RjBGNTtcclxuICAgIGJvcmRlci1ib3R0b206IDFweCBzb2xpZCBsaWdodGdyYXk7XHJcbiAgICBjb2xvcjogIzE4MmE2OTtcclxuICAgIGZvbnQtc2l6ZTogMThweDtcclxuICAgIGZvbnQtd2VpZ2h0OiBib2xkO1xyXG4gIH1cclxuXHJcbiAgLmNvbmZpZ3VyYXRpb24tY29udGVudCB7XHJcbiAgICBmbGV4LWdyb3c6IDE7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgYWxpZ24taXRlbXM6IHN0cmV0Y2g7XHJcbiAgICBwYWRkaW5nOjVweDtcclxuICAgIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XHJcbiAgfVxyXG5cclxuICAuZm9ybS1mb290ZXIge1xyXG4gICAgdGV4dC1hbGlnbjogY2VudGVyO1xyXG4gICAgbWFyZ2luLXRvcDogMHB4O1xyXG4gIH1cclxuICBcclxuICAuZW5hYmxlLXVzZXItZGVmaW5lZC1mdW5jdGlvbiB7XHJcbiAgICBjb2xvcjogIzE4MmE2OTsgLyogQ29sb3Igd2hlbiBlbmFibGVkICovXHJcbiAgfVxyXG4gIFxyXG4gIC5kaXNhYmxlLXVzZXItZGVmaW5lZC1mdW5jdGlvbiB7XHJcbiAgICBjb2xvcjogbGlnaHRncmF5OyAvKiBDb2xvciB3aGVuIGRpc2FibGVkICovXHJcbiAgfVxyXG5cclxuICAucmVwb3J0LWNvbnRhaW5lciB7XHJcbiAgICBib3JkZXI6IDFweCBzb2xpZCAjY2NjO1xyXG4gICAgYm9yZGVyLXJhZGl1czogNXB4O1xyXG4gICAgcGFkZGluZzogMTBweDtcclxuICAgIG1hcmdpbi1ib3R0b206IDIwcHg7XHJcbiAgfVxyXG4gIFxyXG4gIC5yZXBvcnQtY2FwdGlvbiB7XHJcbiAgICBmb250LXdlaWdodDogYm9sZDtcclxuICAgIG1hcmdpbi1ib3R0b206IDEwcHg7XHJcbiAgICBjb2xvcjogIzgwMDA4MDtcclxuICB9XHJcblxyXG4gLyogQWRkIHRoaXMgdG8geW91ciBjb21wb25lbnQncyBDU1MgZmlsZSAqL1xyXG4uZXhwYW5kYWJsZS1wYW5lbCB7XHJcbiAgYm9yZGVyOiAxcHggc29saWQgI2NjYztcclxuICBib3JkZXItcmFkaXVzOiA1cHg7XHJcbiAgbWFyZ2luLWJvdHRvbTogMjBweDtcclxufVxyXG5cclxuLnBhbmVsLWhlYWRlciB7XHJcbiAgYmFja2dyb3VuZC1jb2xvcjogIzAwNjQwMDsgLyogRGVlcCBHcmVlbiBiYWNrZ3JvdW5kIGZvciB0aGUgaGVhZGVyICovXHJcbiAgY29sb3I6ICNmZmY7IC8qIFdoaXRlIHRleHQgY29sb3IgZm9yIHRoZSBoZWFkZXIgKi9cclxuICBwYWRkaW5nOiA1cHggMTBweDsgLyogQWRqdXN0IHBhZGRpbmcgZm9yIGEgdGhpbm5lciBoZWFkZXIgKi9cclxuICBjdXJzb3I6IHBvaW50ZXI7XHJcbiAgZGlzcGxheTogZmxleDtcclxuICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47XHJcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcclxufVxyXG5cclxuLmhlYWRlci10ZXh0IHtcclxuICBmb250LXdlaWdodDogYm9sZDtcclxuICBtYXJnaW46IDA7XHJcbn1cclxuXHJcbi5jYXJldCB7XHJcbiAgZm9udC1zaXplOiAxNnB4OyAvKiBBZGp1c3QgdGhlIHNpemUgb2YgdGhlIGNhcmV0ICovXHJcbiAgdHJhbnNpdGlvbjogdHJhbnNmb3JtIDAuM3M7XHJcbn1cclxuXHJcbi5yb3RhdGUge1xyXG4gIHRyYW5zZm9ybTogcm90YXRlKDE4MGRlZyk7XHJcbn1cclxuXHJcbi5idXR0b24tY29udGFpbmVyIHtcclxuICBwb3NpdGlvbjogcmVsYXRpdmU7XHJcbiAgLyogQWRkIGFueSBvdGhlciBzdHlsZXMgYXMgbmVlZGVkICovXHJcbn1cclxuXHJcbi5keW5hbWljLWRpdiB7XHJcbiAgcG9zaXRpb246IGFic29sdXRlO1xyXG4gIGJhY2tncm91bmQtY29sb3I6ICNmZmY7XHJcbiAgYm9yZGVyOiAxcHggc29saWQgI2NjYztcclxuICBwYWRkaW5nOiAxMHB4O1xyXG4gIC8qIEFkZCBvdGhlciBzdHlsZXMgYXMgbmVlZGVkICovXHJcbn0iXSwic291cmNlUm9vdCI6IiJ9 */"]
});

/***/ }),

/***/ 1201:
/*!*******************************************************************************!*\
  !*** ./src/app/configuration-viewer/udf-arguments/udf-arguments.component.ts ***!
  \*******************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "UdfArgumentsComponent": () => (/* binding */ UdfArgumentsComponent)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ 6078);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var src_app_services_new_report_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! src/app/services/new-report.service */ 9167);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ 2508);





function UdfArgumentsComponent_div_0_ng_container_12_Template(rf, ctx) {
  if (rf & 1) {
    const _r5 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "div", 11)(2, "div", 7)(3, "div", 8)(4, "label", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](6, "input", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function UdfArgumentsComponent_div_0_ng_container_12_Template_input_ngModelChange_6_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r5);
      const p_r2 = restoredCtx.$implicit;
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](p_r2.value = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const p_r2 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate1"]("", p_r2.name, ":");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpropertyInterpolate"]("name", p_r2.name);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", p_r2.value);
  }
}
function UdfArgumentsComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r7 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 1)(1, "div", 2)(2, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](4, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function UdfArgumentsComponent_div_0_Template_div_click_4_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r7);
      const ctx_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r6.close());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](5, "X");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](6, "div", 5)(7, "div", 6)(8, "div", 7)(9, "div", 8)(10, "label", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](11);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](12, UdfArgumentsComponent_div_0_ng_container_12_Template, 7, 3, "ng-container", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵstyleProp"]("top", ctx_r0.top)("left", ctx_r0.left);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate1"]("", ctx_r0.getTitle(), " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](8);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate1"]("Args of ", ctx_r0.func_name, "");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngForOf", ctx_r0.params);
  }
}
class UdfArgumentsComponent {
  constructor(newReportSvc) {
    this.newReportSvc = newReportSvc;
    this.subscribeOpenArgs = new rxjs__WEBPACK_IMPORTED_MODULE_2__.Subscription();
    this.top = '';
    this.left = '';
    this.show = false;
    this.func_name = '';
    this.params = [];
  }
  ngOnInit() {
    this.subscribeOpenArgs = this.newReportSvc.showArgumentsEvent.subscribe(data => {
      this.data = data;
      this.func_name = data ? data.funcName : '';
      this.params = data ? data.udfItem.params : [];
    });
  }
  ngOnDestroy() {
    if (this.subscribeOpenArgs) this.subscribeOpenArgs.unsubscribe();
  }
  close() {
    this.newReportSvc.showParams = false;
  }
  getTitle() {
    if (this.data != null) return this.data.title;
    return '';
  }
}
UdfArgumentsComponent.ɵfac = function UdfArgumentsComponent_Factory(t) {
  return new (t || UdfArgumentsComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](src_app_services_new_report_service__WEBPACK_IMPORTED_MODULE_0__.NewReportService));
};
UdfArgumentsComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: UdfArgumentsComponent,
  selectors: [["udf-arguments"]],
  inputs: {
    top: "top",
    left: "left",
    show: "show"
  },
  decls: 1,
  vars: 1,
  consts: [["class", "params-container", "style", "margin-left: 30px;", 3, "top", "left", 4, "ngIf"], [1, "params-container", 2, "margin-left", "30px"], [1, "params-header"], [1, "titleText"], [1, "closeButton", 3, "click"], [1, "params-content"], [1, "row", "text-center", 2, "width", "100%", "margin-bottom", "7px"], [1, "col"], [1, "form-group"], [2, "font-weight", "bold"], [4, "ngFor", "ngForOf"], [1, "row", 2, "width", "100%", "margin-bottom", "7px"], ["type", "text", 1, "form-control", "form-control-sm", 2, "min-height", "0px !important", "width", "100%", "padding-right", "10px", 3, "ngModel", "name", "ngModelChange"]],
  template: function UdfArgumentsComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](0, UdfArgumentsComponent_div_0_Template, 13, 7, "div", 0);
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx.show);
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_3__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_3__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.NgModel],
  styles: [".params-container[_ngcontent-%COMP%]{\r\n    position: absolute;\r\n    width: 350px;\r\n    padding: 0px;\r\n    display: flex;\r\n    flex-direction: column;\r\n    border: 1px solid lightgray;\r\n    background: white;\r\n    direction: rtl;\r\n}\r\n\r\n.closeButton[_ngcontent-%COMP%]{\r\n    margin-right: 0px;\r\n    position:absolute;\r\n    padding-right:5px;\r\n    cursor: pointer;\r\n    color: #182a69;\r\n  }\r\n\r\n.titleText[_ngcontent-%COMP%]{\r\n    flex-grow: 1;\r\n    text-align: center;\r\n}\r\n\r\n.params-header[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    text-align: center;\r\n    position: sticky;\r\n    margin-bottom: 0px;\r\n    background-color: #E4F0F5;\r\n    border-bottom: 1px solid lightgray;\r\n    color: #182a69;\r\n    font-size: 14px;\r\n    font-weight: bold;\r\n    z-index: 1;\r\n    top:0;\r\n}\r\n\r\n.params-content[_ngcontent-%COMP%] {\r\n    flex-grow: 1;\r\n    display: flex;\r\n    align-items: stretch;\r\n    padding:5px;\r\n    flex-direction: column;\r\n    direction: ltr !important;\r\n    max-height: 300px;\r\n    overflow-y: auto ;\r\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29uZmlndXJhdGlvbi12aWV3ZXIvdWRmLWFyZ3VtZW50cy91ZGYtYXJndW1lbnRzLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7SUFDSSxrQkFBa0I7SUFDbEIsWUFBWTtJQUNaLFlBQVk7SUFDWixhQUFhO0lBQ2Isc0JBQXNCO0lBQ3RCLDJCQUEyQjtJQUMzQixpQkFBaUI7SUFDakIsY0FBYztBQUNsQjs7QUFFQTtJQUNJLGlCQUFpQjtJQUNqQixpQkFBaUI7SUFDakIsaUJBQWlCO0lBQ2pCLGVBQWU7SUFDZixjQUFjO0VBQ2hCOztBQUVGO0lBQ0ksWUFBWTtJQUNaLGtCQUFrQjtBQUN0Qjs7QUFFQTtJQUNJLGFBQWE7SUFDYixrQkFBa0I7SUFDbEIsZ0JBQWdCO0lBQ2hCLGtCQUFrQjtJQUNsQix5QkFBeUI7SUFDekIsa0NBQWtDO0lBQ2xDLGNBQWM7SUFDZCxlQUFlO0lBQ2YsaUJBQWlCO0lBQ2pCLFVBQVU7SUFDVixLQUFLO0FBQ1Q7O0FBRUE7SUFDSSxZQUFZO0lBQ1osYUFBYTtJQUNiLG9CQUFvQjtJQUNwQixXQUFXO0lBQ1gsc0JBQXNCO0lBQ3RCLHlCQUF5QjtJQUN6QixpQkFBaUI7SUFDakIsaUJBQWlCO0FBQ3JCIiwic291cmNlc0NvbnRlbnQiOlsiLnBhcmFtcy1jb250YWluZXJ7XHJcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XHJcbiAgICB3aWR0aDogMzUwcHg7XHJcbiAgICBwYWRkaW5nOiAwcHg7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcclxuICAgIGJvcmRlcjogMXB4IHNvbGlkIGxpZ2h0Z3JheTtcclxuICAgIGJhY2tncm91bmQ6IHdoaXRlO1xyXG4gICAgZGlyZWN0aW9uOiBydGw7XHJcbn1cclxuXHJcbi5jbG9zZUJ1dHRvbntcclxuICAgIG1hcmdpbi1yaWdodDogMHB4O1xyXG4gICAgcG9zaXRpb246YWJzb2x1dGU7XHJcbiAgICBwYWRkaW5nLXJpZ2h0OjVweDtcclxuICAgIGN1cnNvcjogcG9pbnRlcjtcclxuICAgIGNvbG9yOiAjMTgyYTY5O1xyXG4gIH1cclxuXHJcbi50aXRsZVRleHR7XHJcbiAgICBmbGV4LWdyb3c6IDE7XHJcbiAgICB0ZXh0LWFsaWduOiBjZW50ZXI7XHJcbn1cclxuXHJcbi5wYXJhbXMtaGVhZGVyIHtcclxuICAgIGRpc3BsYXk6IGZsZXg7XHJcbiAgICB0ZXh0LWFsaWduOiBjZW50ZXI7XHJcbiAgICBwb3NpdGlvbjogc3RpY2t5O1xyXG4gICAgbWFyZ2luLWJvdHRvbTogMHB4O1xyXG4gICAgYmFja2dyb3VuZC1jb2xvcjogI0U0RjBGNTtcclxuICAgIGJvcmRlci1ib3R0b206IDFweCBzb2xpZCBsaWdodGdyYXk7XHJcbiAgICBjb2xvcjogIzE4MmE2OTtcclxuICAgIGZvbnQtc2l6ZTogMTRweDtcclxuICAgIGZvbnQtd2VpZ2h0OiBib2xkO1xyXG4gICAgei1pbmRleDogMTtcclxuICAgIHRvcDowO1xyXG59XHJcblxyXG4ucGFyYW1zLWNvbnRlbnQge1xyXG4gICAgZmxleC1ncm93OiAxO1xyXG4gICAgZGlzcGxheTogZmxleDtcclxuICAgIGFsaWduLWl0ZW1zOiBzdHJldGNoO1xyXG4gICAgcGFkZGluZzo1cHg7XHJcbiAgICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xyXG4gICAgZGlyZWN0aW9uOiBsdHIgIWltcG9ydGFudDtcclxuICAgIG1heC1oZWlnaHQ6IDMwMHB4O1xyXG4gICAgb3ZlcmZsb3cteTogYXV0byA7XHJcbn1cclxuXHJcbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
});

/***/ }),

/***/ 9765:
/*!************************************************************!*\
  !*** ./src/app/drawer-content/drawer-content.component.ts ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DrawerContentComponent": () => (/* binding */ DrawerContentComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);


class DrawerContentComponent {
  onKeydownHandler(event) {
    if (event.key === "Escape") {
      this.closeDrawer();
    }
  }
  constructor(statToolService) {
    this.statToolService = statToolService;
  }
  ngOnInit() {}
  ngOnDestroy() {}
  closeDrawer() {
    this.statToolService.showDrawer = false;
  }
}
DrawerContentComponent.ɵfac = function DrawerContentComponent_Factory(t) {
  return new (t || DrawerContentComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService));
};
DrawerContentComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: DrawerContentComponent,
  selectors: [["drawer-content"]],
  hostBindings: function DrawerContentComponent_HostBindings(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("keydown", function DrawerContentComponent_keydown_HostBindingHandler($event) {
        return ctx.onKeydownHandler($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresolveDocument"]);
    }
  },
  decls: 10,
  vars: 6,
  consts: [[2, "height", "40px", "width", "100%", "display", "flex", "justify-content", "space-between", "direction", "rtl"], [2, "margin", "5px"], ["src", "assets/cancel-icon.svg", "title", "Close Drawer", 2, "height", "33px", "width", "33px", "position", "relative", "cursor", "pointer", 3, "click"], [2, "height", "100vh", "width", "100%", "display", "flex"], [2, "width", "60%", "height", "92%"], [2, "display", "block", "width", "100%", "height", "85%", "margin-top", "0px", "border", "none", 3, "src"], [2, "width", "40%", "height", "92%", "min-width", "600px"], [2, "display", "block", "width", "98%", "height", "95%", "margin-top", "0px", "border", "none", 3, "src"]],
  template: function DrawerContentComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 0)(1, "div", 1)(2, "img", 2);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function DrawerContentComponent_Template_img_click_2_listener() {
        return ctx.closeDrawer();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "div", 3)(4, "div", 4);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](5, "iframe", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](6, "safe");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](7, "div", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](8, "iframe", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](9, "safe");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("src", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind1"](6, 2, ctx.statToolService.getDrawerUpdateListUrl()), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeResourceUrl"]);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("src", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind1"](9, 4, ctx.statToolService.getDrawerShowImageUrl()), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeResourceUrl"]);
    }
  },
  styles: ["\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
});

/***/ }),

/***/ 5220:
/*!********************************************!*\
  !*** ./src/app/drawer/drawer.component.ts ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DrawerComponent": () => (/* binding */ DrawerComponent)
/* harmony export */ });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/animations */ 4851);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ 6078);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _drawer_content_drawer_content_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../drawer-content/drawer-content.component */ 9765);






function DrawerComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r2 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "div", 1)(1, "div", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("click", function DrawerComponent_div_0_Template_div_click_1_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r2);
      const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r1.clickDrawer());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](2, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](3, "drawer-content");
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("@widthGrow", ctx_r0.state);
  }
}
class DrawerComponent {
  onKeydownHandler(event) {
    console.log('keydown', event.key);
    if (event.key === "Escape") {
      this.statToolSvc.showDrawer = false;
    }
  }
  changeState() {
    this.state == "closed" ? this.state = "open" : this.state = "closed";
    console.log('Drawer state - ' + this.state);
  }
  constructor(statToolSvc) {
    this.statToolSvc = statToolSvc;
    this.state = "closed";
    this.subscribeOpenDrawer = new rxjs__WEBPACK_IMPORTED_MODULE_3__.Subscription();
    this.show = false;
  }
  ngOnInit() {
    this.subscribeOpenDrawer = this.statToolSvc.openDrawer.subscribe(msg => {
      this.statToolSvc.showDrawer = true;
      this.statToolSvc.drawerShowImageUrl = '';
      this.changeState();
    });
  }
  ngOnDestroy() {
    if (this.subscribeOpenDrawer != null) this.subscribeOpenDrawer.unsubscribe();
  }
  clickDrawer() {
    this.statToolSvc.showDrawer = false;
    this.changeState();
  }
}
DrawerComponent.ɵfac = function DrawerComponent_Factory(t) {
  return new (t || DrawerComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService));
};
DrawerComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineComponent"]({
  type: DrawerComponent,
  selectors: [["drawer"]],
  hostBindings: function DrawerComponent_HostBindings(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("keydown", function DrawerComponent_keydown_HostBindingHandler($event) {
        return ctx.onKeydownHandler($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresolveDocument"]);
    }
  },
  decls: 1,
  vars: 1,
  consts: [["style", "z-index: 1000;position: absolute; height: 100vh;width: 100%;display: flex;margin-top: 50px;", 4, "ngIf"], [2, "z-index", "1000", "position", "absolute", "height", "100vh", "width", "100%", "display", "flex", "margin-top", "50px"], [2, "width", "8%", "height", "100vh", "background-color", "transparent", "opacity", "0.5", "flex-grow", "1", 3, "click"], [2, "width", "92%", "height", "100vh", "background-color", "white", "position", "fixed", "box-shadow", "rgba(0, 0, 0, 0.24) 0px 3px 8px", "right", "0px"]],
  template: function DrawerComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](0, DrawerComponent_div_0_Template, 4, 1, "div", 0);
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", ctx.statToolSvc.showDrawer);
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_4__.NgIf, _drawer_content_drawer_content_component__WEBPACK_IMPORTED_MODULE_1__.DrawerContentComponent],
  styles: ["\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"],
  data: {
    animation: [(0,_angular_animations__WEBPACK_IMPORTED_MODULE_5__.trigger)('widthGrow', [(0,_angular_animations__WEBPACK_IMPORTED_MODULE_5__.state)('closed', (0,_angular_animations__WEBPACK_IMPORTED_MODULE_5__.style)({
      width: 0
    })), (0,_angular_animations__WEBPACK_IMPORTED_MODULE_5__.state)('open', (0,_angular_animations__WEBPACK_IMPORTED_MODULE_5__.style)({
      width: 400
    })), (0,_angular_animations__WEBPACK_IMPORTED_MODULE_5__.transition)('* => *', (0,_angular_animations__WEBPACK_IMPORTED_MODULE_5__.animate)(150))])]
  }
});

/***/ }),

/***/ 3886:
/*!*****************************************************************************!*\
  !*** ./src/app/new-report/new-report-result/new-report-result.component.ts ***!
  \*****************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NewReportResultComponent": () => (/* binding */ NewReportResultComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var src_app_services_new_report_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! src/app/services/new-report.service */ 9167);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ 4666);



function NewReportResultComponent_div_0_div_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4)(1, "a", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2, "Open Report");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpropertyInterpolate"]("href", ctx_r1.newReportService.newReportResult.link, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeUrl"]);
  }
}
function NewReportResultComponent_div_0_ng_container_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "div", 6)(2, "p")(3, "strong");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](4, "Report Creation Failed.");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
}
function NewReportResultComponent_div_0_ng_container_6_tr_19_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "tr")(1, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](5, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](7, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](8);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](9, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](10);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](11, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](12);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const file_r6 = ctx.$implicit;
    const i_r7 = ctx.index;
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](file_r6);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r5.newReportService.newReportResult.num_success_files[i_r7]);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r5.newReportService.newReportResult.reading_function_skipped[i_r7]);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r5.newReportService.newReportResult.not_json_files[i_r7]);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r5.newReportService.newReportResult.failed_with_error[i_r7]);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r5.newReportService.newReportResult.skipped_not_in_lognames[i_r7]);
  }
}
function NewReportResultComponent_div_0_ng_container_6_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "div", 7)(2, "div", 8)(3, "table", 9)(4, "thead")(5, "tr")(6, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](7, "Config");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](8, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](9, "# Success");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](10, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](11, "# Skipped");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](12, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](13, "Not Json");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](14, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](15, "# Failed");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](16, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](17, "Filtered");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](18, "tbody");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](19, NewReportResultComponent_div_0_ng_container_6_tr_19_Template, 13, 6, "tr", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](19);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngForOf", ctx_r3.newReportService.newReportResult.files);
  }
}
function NewReportResultComponent_div_0_ng_container_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "div", 6)(2, "p")(3, "strong");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r4.newReportService.newReportResult.errorMessage);
  }
}
function NewReportResultComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 1)(1, "h5");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2, "Execution Results");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](3, NewReportResultComponent_div_0_div_3_Template, 3, 1, "div", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, NewReportResultComponent_div_0_ng_container_4_Template, 5, 0, "ng-container", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](5, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](6, NewReportResultComponent_div_0_ng_container_6_Template, 20, 1, "ng-container", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](7, NewReportResultComponent_div_0_ng_container_7_Template, 5, 1, "ng-container", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r0.newReportService.newReportResult.link != "");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r0.newReportService.newReportResult.link == "");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r0.newReportService.newReportResult.ok == true);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", !(ctx_r0.newReportService.newReportResult.ok == true));
  }
}
class NewReportResultComponent {
  constructor(newReportService) {
    this.newReportService = newReportService;
  }
}
NewReportResultComponent.ɵfac = function NewReportResultComponent_Factory(t) {
  return new (t || NewReportResultComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](src_app_services_new_report_service__WEBPACK_IMPORTED_MODULE_0__.NewReportService));
};
NewReportResultComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: NewReportResultComponent,
  selectors: [["new-report-result"]],
  decls: 1,
  vars: 1,
  consts: [["class", "results", 4, "ngIf"], [1, "results"], ["class", "navigation", 4, "ngIf"], [4, "ngIf"], [1, "navigation"], [1, "link", 3, "href"], [1, "error-message"], [1, "key-value-pairs"], [1, "table-responsive"], [1, "table"], [4, "ngFor", "ngForOf"]],
  template: function NewReportResultComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](0, NewReportResultComponent_div_0_Template, 8, 4, "div", 0);
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx.newReportService.showResults());
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_2__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgIf],
  styles: [".results[_ngcontent-%COMP%] {\r\n    \r\n    \r\n  }\r\n  \r\n  h3[_ngcontent-%COMP%] {\r\n    margin-top: 0;\r\n  }\r\n  \r\n  .status[_ngcontent-%COMP%] {\r\n    background-color: green;\r\n    color: white;\r\n    padding: 5px 10px;\r\n    border-radius: 3px;\r\n    display: inline-block;\r\n    margin-bottom: 10px;\r\n  }\r\n  \r\n  .navigation[_ngcontent-%COMP%] {\r\n    margin-bottom: 10px;\r\n  }\r\n  \r\n  .link[_ngcontent-%COMP%] {\r\n    color: blue;\r\n    text-decoration: underline;\r\n    font-size: 18px;\r\n  }\r\n  \r\n  .key-value-pairs[_ngcontent-%COMP%]   p[_ngcontent-%COMP%] {\r\n    margin: 5px 0;\r\n  }\r\n  \r\n  .feedback[_ngcontent-%COMP%] {\r\n    margin-top: 20px;\r\n  }\r\n\r\n  .error-message[_ngcontent-%COMP%] {\r\n    margin: 5px 0;\r\n    color:red;\r\n    font-weight: bolder;\r\n  }\r\n\r\n  .table[_ngcontent-%COMP%] {\r\n    width: 100%;\r\n    border-collapse: collapse;\r\n  }\r\n  \r\n  .table[_ngcontent-%COMP%]   th[_ngcontent-%COMP%], .table[_ngcontent-%COMP%]   td[_ngcontent-%COMP%] {\r\n    padding: 4px;\r\n    text-align: left;\r\n    border-bottom: 1px solid #ddd;\r\n  }\r\n  \r\n  .table[_ngcontent-%COMP%]   th[_ngcontent-%COMP%] {\r\n    \r\n  }\r\n  \r\n  .table[_ngcontent-%COMP%]   tbody[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]:nth-child(even) {\r\n    \r\n  }\r\n  \r\n  .table-responsive[_ngcontent-%COMP%] {\r\n    overflow-x: auto;\r\n  }\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvbmV3LXJlcG9ydC9uZXctcmVwb3J0LXJlc3VsdC9uZXctcmVwb3J0LXJlc3VsdC5jb21wb25lbnQuY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOztJQUVJLGlCQUFpQjtFQUNuQjs7RUFFQTtJQUNFLGFBQWE7RUFDZjs7RUFFQTtJQUNFLHVCQUF1QjtJQUN2QixZQUFZO0lBQ1osaUJBQWlCO0lBQ2pCLGtCQUFrQjtJQUNsQixxQkFBcUI7SUFDckIsbUJBQW1CO0VBQ3JCOztFQUVBO0lBQ0UsbUJBQW1CO0VBQ3JCOztFQUVBO0lBQ0UsV0FBVztJQUNYLDBCQUEwQjtJQUMxQixlQUFlO0VBQ2pCOztFQUVBO0lBQ0UsYUFBYTtFQUNmOztFQUVBO0lBQ0UsZ0JBQWdCO0VBQ2xCOztFQUVBO0lBQ0UsYUFBYTtJQUNiLFNBQVM7SUFDVCxtQkFBbUI7RUFDckI7O0VBRUE7SUFDRSxXQUFXO0lBQ1gseUJBQXlCO0VBQzNCOztFQUVBOztJQUVFLFlBQVk7SUFDWixnQkFBZ0I7SUFDaEIsNkJBQTZCO0VBQy9COztFQUVBOztFQUVBOztFQUVBOztFQUVBOztFQUVBO0lBQ0UsZ0JBQWdCO0VBQ2xCIiwic291cmNlc0NvbnRlbnQiOlsiLnJlc3VsdHMge1xyXG4gICAgXHJcbiAgICAvKnBhZGRpbmc6IDIwcHg7Ki9cclxuICB9XHJcbiAgXHJcbiAgaDMge1xyXG4gICAgbWFyZ2luLXRvcDogMDtcclxuICB9XHJcbiAgXHJcbiAgLnN0YXR1cyB7XHJcbiAgICBiYWNrZ3JvdW5kLWNvbG9yOiBncmVlbjtcclxuICAgIGNvbG9yOiB3aGl0ZTtcclxuICAgIHBhZGRpbmc6IDVweCAxMHB4O1xyXG4gICAgYm9yZGVyLXJhZGl1czogM3B4O1xyXG4gICAgZGlzcGxheTogaW5saW5lLWJsb2NrO1xyXG4gICAgbWFyZ2luLWJvdHRvbTogMTBweDtcclxuICB9XHJcbiAgXHJcbiAgLm5hdmlnYXRpb24ge1xyXG4gICAgbWFyZ2luLWJvdHRvbTogMTBweDtcclxuICB9XHJcbiAgXHJcbiAgLmxpbmsge1xyXG4gICAgY29sb3I6IGJsdWU7XHJcbiAgICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcclxuICAgIGZvbnQtc2l6ZTogMThweDtcclxuICB9XHJcbiAgXHJcbiAgLmtleS12YWx1ZS1wYWlycyBwIHtcclxuICAgIG1hcmdpbjogNXB4IDA7XHJcbiAgfVxyXG4gIFxyXG4gIC5mZWVkYmFjayB7XHJcbiAgICBtYXJnaW4tdG9wOiAyMHB4O1xyXG4gIH1cclxuXHJcbiAgLmVycm9yLW1lc3NhZ2Uge1xyXG4gICAgbWFyZ2luOiA1cHggMDtcclxuICAgIGNvbG9yOnJlZDtcclxuICAgIGZvbnQtd2VpZ2h0OiBib2xkZXI7XHJcbiAgfVxyXG5cclxuICAudGFibGUge1xyXG4gICAgd2lkdGg6IDEwMCU7XHJcbiAgICBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlO1xyXG4gIH1cclxuICBcclxuICAudGFibGUgdGgsXHJcbiAgLnRhYmxlIHRkIHtcclxuICAgIHBhZGRpbmc6IDRweDtcclxuICAgIHRleHQtYWxpZ246IGxlZnQ7XHJcbiAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgI2RkZDtcclxuICB9XHJcbiAgXHJcbiAgLnRhYmxlIHRoIHtcclxuICAgIFxyXG4gIH1cclxuICBcclxuICAudGFibGUgdGJvZHkgdHI6bnRoLWNoaWxkKGV2ZW4pIHtcclxuICAgIFxyXG4gIH1cclxuICBcclxuICAudGFibGUtcmVzcG9uc2l2ZSB7XHJcbiAgICBvdmVyZmxvdy14OiBhdXRvO1xyXG4gIH0iXSwic291cmNlUm9vdCI6IiJ9 */"]
});

/***/ }),

/***/ 6652:
/*!****************************************************!*\
  !*** ./src/app/new-report/new-report.component.ts ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NewReportComponent": () => (/* binding */ NewReportComponent)
/* harmony export */ });
/* harmony import */ var _services_new_report_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/new-report.service */ 9167);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ 1989);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ 8977);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ 635);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _configuration_viewer_configuration_viewer_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../configuration-viewer/configuration-viewer.component */ 3213);
/* harmony import */ var _new_report_result_new_report_result_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./new-report-result/new-report-result.component */ 3886);








function NewReportComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "div", 41);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelement"](1, "img", 42);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
}
function NewReportComponent_option_22_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "option", 43);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const suite_r5 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpropertyInterpolate"]("value", suite_r5);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate1"]("", suite_r5, " ");
  }
}
function NewReportComponent_ng_container_31_Template(rf, ctx) {
  if (rf & 1) {
    const _r8 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](1, "div", 44)(2, "input", 45);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("change", function NewReportComponent_ng_container_31_Template_input_change_2_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r8);
      const config_r6 = restoredCtx.$implicit;
      const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r7.newReportService.configSelectionChanged($event, config_r6));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](3, "label", 46);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function NewReportComponent_ng_container_31_Template_label_click_3_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r8);
      const config_r6 = restoredCtx.$implicit;
      const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r9.newReportService.showConfig(config_r6));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const config_r6 = ctx.$implicit;
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("checked", ctx_r2.newReportService.isConfigSelected(config_r6));
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtextInterpolate"](config_r6);
  }
}
const _c0 = function (a0, a1) {
  return {
    "is-invalid": a0,
    "is-valid": a1
  };
};
class NewReportComponent {
  constructor(location, newReportService) {
    this.location = location;
    this.newReportService = newReportService;
    this.backImgSrc = 'assets/back-icon-blue.svg';
    this.formatter = result => result.toUpperCase();
    this.searchPredictionsDirectory = text$ => text$.pipe((0,rxjs__WEBPACK_IMPORTED_MODULE_4__.debounceTime)(200), (0,rxjs__WEBPACK_IMPORTED_MODULE_5__.distinctUntilChanged)(), (0,rxjs__WEBPACK_IMPORTED_MODULE_6__.map)(term => term === '' ? this.newReportService.last_prediction_directory.slice(0, 10) : this.newReportService.last_prediction_directory.filter(v => v.toLowerCase().indexOf(term.toLowerCase()) > -1).slice(0, 10)));
    this.searchGTDirectroy = text$ => text$.pipe((0,rxjs__WEBPACK_IMPORTED_MODULE_4__.debounceTime)(200), (0,rxjs__WEBPACK_IMPORTED_MODULE_5__.distinctUntilChanged)(), (0,rxjs__WEBPACK_IMPORTED_MODULE_6__.map)(term => term === '' ? this.newReportService.last_ground_truth_directory : this.newReportService.last_ground_truth_directory.filter(v => v.toLowerCase().indexOf(term.toLowerCase()) > -1).slice(0, 10)));
    this.searchOutputDirectroy = text$ => text$.pipe((0,rxjs__WEBPACK_IMPORTED_MODULE_4__.debounceTime)(200), (0,rxjs__WEBPACK_IMPORTED_MODULE_5__.distinctUntilChanged)(), (0,rxjs__WEBPACK_IMPORTED_MODULE_6__.map)(term => term === '' ? this.newReportService.last_output_directory : this.newReportService.last_output_directory.filter(v => v.toLowerCase().indexOf(term.toLowerCase()) > -1).slice(0, 10)));
  }
  ngOnInit() {}
  ngOnDestroy() {}
  onFocus(e) {
    e.stopPropagation();
    setTimeout(() => {
      const inputEvent = new Event('input');
      e.target.dispatchEvent(inputEvent);
    }, 0);
  }
  back() {
    let path = this.location.path();
    console.log('path', path);
    if (path.indexOf('/static/') > 0) {
      path = path.replace('/static/', '/');
      console.log('path-remove-static', path);
    }
    window.location.href = 'http://127.0.0.1:5000/';
  }
  isSelectSuiteValid() {
    if (this.newReportService.selectedSuite != _services_new_report_service__WEBPACK_IMPORTED_MODULE_0__.SELECTE_SUITE) return true;
    return false;
  }
  disableCreateReportButton() {
    return this.newReportService.predictionsDirectory.length < 3 || this.newReportService.reporterOutputDirectory.length < 3 || this.newReportService.getNumConfigsSelected() == 0;
  }
}
NewReportComponent.ɵfac = function NewReportComponent_Factory(t) {
  return new (t || NewReportComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_7__.Location), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdirectiveInject"](_services_new_report_service__WEBPACK_IMPORTED_MODULE_0__.NewReportService));
};
NewReportComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineComponent"]({
  type: NewReportComponent,
  selectors: [["new-report"]],
  decls: 54,
  vars: 19,
  consts: [["class", "centered-image", "style", "z-index:999999", 4, "ngIf"], [2, "height", "100%"], [2, "width", "100%", "height", "50px", "border", "1px solid lightgray", "border-radius", "4px", "color", "#182a69", "background-color", "#E4F0F5", "position", "absolute", "z-index", "0", "top", "0px"], [1, "template-selection", 2, "margin-left", "10px", "padding-top", "8px"], [2, "display", "flex", "width", "100%", "height", "40px"], [1, "back-icon", 2, "margin-top", "-2px", "width", "40px"], ["title", "Back", 1, "back", 2, "width", "33px", "height", "33px", "margin-top", "3px", "cursor", "pointer", 3, "src", "mouseover", "mouseout", "click"], [2, "margin-left", "5px"], [2, "font-weight", "bold"], ["autocomplete", "on", 2, "display", "flex", "position", "relative", "margin-right", "20px"], [1, "overlay"], [1, "form-container"], [1, "form-header"], [1, "form-content"], [1, "main-div"], [1, "input-label", 2, "display", "flex", "align-items", "center", "margin-top", "3px"], ["for", "reports_suites", 2, "font-weight", "bold", "margin-right", "5px"], [1, "select-input", 2, "flex-grow", "1"], ["id", "reports_suites", "name", "reports_suites", 1, "form-select", "form-select-sm", 3, "ngModel", "ngModelChange", "change"], [3, "value", 4, "ngFor", "ngForOf"], [1, "link-button", 2, "right", "5px !important", "position", "relative", "margin-right", "3px", "margin-left", "10px", "margin-top", "4px"], [1, "link-a-cls", 3, "click"], [1, "combined-section"], [1, "scrollable-div", 2, "border-bottom", "1px solid lightgray", "background", "white"], [1, "scrollable-content"], [2, "margin-left", "28px", "color", "#28a745", "text-decoration", "underline", "cursor", "pointer", 3, "click"], [4, "ngFor", "ngForOf"], [1, "text-inputs", "dropdown-wrapper"], [1, "input-sm"], ["for", "predictions_directory", 2, "width", "30%", "font-weight", "bold"], ["type", "text", "id", "predictions_directory", "placeholder", "Local directory or blob folder", "name", "predictions_directory", "minlength", "0", "required", "", 1, "form-control", "input-sm", 3, "ngModel", "ngClass", "focus", "ngModelChange"], ["predictionsDirectoryInput", "ngModel"], ["for", "ground_truth_directory", 2, "width", "30%", "font-weight", "bold"], ["type", "text", "id", "ground_truth_directory", "placeholder", "Leave blank if GT is from annotation store", "name", "ground_truth_directory", "minlength", "0", 1, "form-control", "input-sm", 3, "ngModel", "focus", "ngModelChange"], ["for", "output_directory", 2, "width", "30%", "font-weight", "bold"], ["type", "text", "id", "output_directory", "placeholder", "", "name", "output_directory", "minlength", "0", "required", "", 1, "form-control", "input-sm", 3, "ngModel", "ngClass", "focus", "ngModelChange"], ["reporterOutputDirectoryInput", "ngModel"], [1, "form-footer"], ["type", "submit", 1, "btn", "btn", "btn-primary", "btn-mdcd", 2, "margin-bottom", "5px", 3, "disabled", "click"], [2, "width", "30%", "margin-top", "10px"], [2, "width", "39.6%", "margin-top", "10px", "margin-left", "20px", "max-height", "25vh", "overflow-y", "auto", "overflow-x", "hidden"], [1, "centered-image", 2, "z-index", "999999"], ["src", "assets/spinner-90-ring-with-bg.svg", 2, "width", "40px", "height", "40x"], [3, "value"], [1, "form-check", 2, "margin-left", "4px"], ["type", "checkbox", 1, "form-check-input", 3, "checked", "change"], [1, "form-check-label", 2, "cursor", "pointer", "color", "blue", "text-decoration", "underline", 3, "click"]],
  template: function NewReportComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](0, NewReportComponent_div_0_Template, 2, 0, "div", 0);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](1, "div", 1)(2, "div", 2)(3, "div", 3)(4, "div", 4)(5, "div", 5)(6, "img", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("mouseover", function NewReportComponent_Template_img_mouseover_6_listener() {
        return ctx.backImgSrc = "assets/back-icon-orange.svg";
      })("mouseout", function NewReportComponent_Template_img_mouseout_6_listener() {
        return ctx.backImgSrc = "assets/back-icon-blue.svg";
      })("click", function NewReportComponent_Template_img_click_6_listener() {
        return ctx.back();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](7, "div", 7)(8, "h3", 8);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](9, "NEW REPORT");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](10, "div", 9);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelement"](11, "div", 10);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](12, "form", 11)(13, "div", 12);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](14, " Crate New Report ");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](15, "div", 13)(16, "div", 14)(17, "div", 15)(18, "label", 16);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](19, "Reports Suites:");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](20, "div", 17)(21, "select", 18);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function NewReportComponent_Template_select_ngModelChange_21_listener($event) {
        return ctx.newReportService.selectedSuite = $event;
      })("change", function NewReportComponent_Template_select_change_21_listener($event) {
        return ctx.newReportService.onSuiteSelected($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](22, NewReportComponent_option_22_Template, 2, 2, "option", 19);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](23, "div", 20)(24, "a", 21);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function NewReportComponent_Template_a_click_24_listener() {
        return ctx.newReportService.openSaveSuiteDialog();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](25, "Save Suite");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](26, "div", 22)(27, "div", 23)(28, "div", 24)(29, "a", 25);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function NewReportComponent_Template_a_click_29_listener() {
        return ctx.newReportService.clearConfigViewer();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](30, "Add new configuration");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](31, NewReportComponent_ng_container_31_Template, 5, 2, "ng-container", 26);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](32, "div", 27)(33, "div", 28)(34, "label", 29);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](35, "Predictions Directory:");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](36, "input", 30, 31);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("focus", function NewReportComponent_Template_input_focus_36_listener($event) {
        return ctx.onFocus($event);
      })("ngModelChange", function NewReportComponent_Template_input_ngModelChange_36_listener($event) {
        return ctx.newReportService.predictionsDirectory = $event;
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](38, "div", 28)(39, "label", 32);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](40, "Ground Truth Directory:");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](41, "input", 33);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("focus", function NewReportComponent_Template_input_focus_41_listener($event) {
        return ctx.onFocus($event);
      })("ngModelChange", function NewReportComponent_Template_input_ngModelChange_41_listener($event) {
        return ctx.newReportService.groundTruthDirectory = $event;
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](42, "div", 28)(43, "label", 34);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](44, "Output Directory:");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](45, "input", 35, 36);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("focus", function NewReportComponent_Template_input_focus_45_listener($event) {
        return ctx.onFocus($event);
      })("ngModelChange", function NewReportComponent_Template_input_ngModelChange_45_listener($event) {
        return ctx.newReportService.reporterOutputDirectory = $event;
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](47, "div", 37)(48, "button", 38);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("click", function NewReportComponent_Template_button_click_48_listener() {
        return ctx.newReportService.createReport();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtext"](49, "Create Report");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](50, "div", 39);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelement"](51, "configuration-viewer");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](52, "div", 40);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelement"](53, "new-report-result");
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()()();
    }
    if (rf & 2) {
      const _r3 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](37);
      const _r4 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵreference"](46);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngIf", ctx.newReportService.isBusy);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](6);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("src", ctx.backImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsanitizeUrl"]);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵclassProp"]("show", ctx.newReportService.isBusy);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](10);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx.newReportService.selectedSuite);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx.newReportService.suites);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](9);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngForOf", ctx.newReportService.configs);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx.newReportService.predictionsDirectory)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction2"](13, _c0, _r3.invalid && (_r3.dirty || _r3.touched), _r3.valid && (_r3.dirty || _r3.touched)));
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx.newReportService.groundTruthDirectory);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](4);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngModel", ctx.newReportService.reporterOutputDirectory)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵpureFunction2"](16, _c0, _r4.invalid && (_r4.dirty || _r4.touched), _r4.valid && (_r4.dirty || _r4.touched)));
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("disabled", ctx.disableCreateReportButton());
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_7__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_8__["ɵNgNoValidate"], _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgSelectOption, _angular_forms__WEBPACK_IMPORTED_MODULE_8__["ɵNgSelectMultipleOption"], _angular_forms__WEBPACK_IMPORTED_MODULE_8__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.SelectControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.RequiredValidator, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.MinLengthValidator, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgModel, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgForm, _configuration_viewer_configuration_viewer_component__WEBPACK_IMPORTED_MODULE_1__.ConfigurationViewerComponent, _new_report_result_new_report_result_component__WEBPACK_IMPORTED_MODULE_2__.NewReportResultComponent],
  styles: [".form-container[_ngcontent-%COMP%] {\r\n    height: 70vh;\r\n    min-height: 580px;\r\n    width: 40%;\r\n    margin-left: 20px;\r\n    margin-top: 10px;\r\n    margin-right: 20px !important;\r\n    padding: 0px;\r\n    display: flex;\r\n    flex-direction: column;\r\n    border: 1px solid lightgray;\r\n    background: #fafafa;\r\n  }\r\n  \r\n  .form-header[_ngcontent-%COMP%] {\r\n    text-align: center;\r\n    margin-bottom: 0px;\r\n    background-color: #E4F0F5;\r\n    border-bottom: 1px solid lightgray;\r\n    color: #182a69;\r\n    font-size: 18px;\r\n    font-weight: bold;\r\n  }\r\n  \r\n  .form-content[_ngcontent-%COMP%] {\r\n    flex-grow: 1;\r\n    display: flex;\r\n    align-items: stretch;\r\n    padding:5px;\r\n  }\r\n  \r\n  .main-div[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    flex-direction: column;\r\n    flex-grow: 1;\r\n  }\r\n  \r\n  .combined-section[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    flex-direction: column;\r\n    flex-grow: 20;\r\n  }\r\n  \r\n  .scrollable-div[_ngcontent-%COMP%] {\r\n    flex-grow: 1;\r\n    overflow-y: auto;\r\n    border: 1px solid #ccc;\r\n    padding: 10px;\r\n    height: 35vh;\r\n  }\r\n\r\n  .scrollable-content[_ngcontent-%COMP%] {\r\n    overflow-y: auto;\r\n  }\r\n  \r\n  .link-button[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    justify-content: flex-start;\r\n    margin-top: 10px;\r\n  }\r\n  \r\n  .link-button[_ngcontent-%COMP%]   a[_ngcontent-%COMP%] {\r\n    padding: 5px;\r\n  }\r\n\r\n  .text-inputs[_ngcontent-%COMP%] {\r\n    margin-top: 15px;\r\n    flex-grow: 1;\r\n    display: flex;\r\n    flex-direction: column;\r\n    gap: 0px;\r\n    overflow-y: auto;\r\n    \r\n  }\r\n  \r\n  .text-boxes[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    flex-direction: column;\r\n    gap: 10px;\r\n  }\r\n  \r\n  .form-footer[_ngcontent-%COMP%] {\r\n    text-align: center;\r\n    margin-top: 0px;\r\n  }\r\n  \r\n  .input-label[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    justify-content: left;\r\n  }\r\n  \r\n  .select-input[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    justify-content: center;\r\n    \r\n  }\r\n\r\n  \r\n.input-sm[_ngcontent-%COMP%] {\r\n    display: flex;\r\n    \r\n    width: 99.0%;\r\n    margin:2px;\r\n\r\n  }\r\n  \r\n  .input-sm[_ngcontent-%COMP%]   label[_ngcontent-%COMP%] {\r\n    margin-bottom: 5px;\r\n  }\r\n  \r\n  .input-sm[_ngcontent-%COMP%]   input[_ngcontent-%COMP%] {\r\n    padding: 5px;\r\n  }\r\n\r\n  .separator[_ngcontent-%COMP%] {\r\n    margin: 0 5px;\r\n    color: #999;\r\n    line-height: 2em;\r\n  }\r\n\r\n  .link-a-cls[_ngcontent-%COMP%]{\r\n    color: #0d6efd;\r\n    cursor: pointer;\r\n    text-decoration: underline;\r\n  }\r\n\r\n  .link-a-cls[_ngcontent-%COMP%]:hover {\r\n    color: #0a58ca;\r\n  }\r\n\r\n  .centered-image[_ngcontent-%COMP%] {\r\n    position: fixed;\r\n    top: 50%;\r\n    left: 50%;\r\n    transform: translate(-50%, -50%);\r\n  }\r\n\r\n  .overlay[_ngcontent-%COMP%] {\r\n    position: fixed;\r\n    top: 0;\r\n    left: 0;\r\n    width: 100%;\r\n    height: 100%;\r\n    background-color: rgba(0, 0, 0, 0.5); \r\n    z-index: 9999;\r\n    display: none;\r\n  }\r\n  \r\n  .overlay.show[_ngcontent-%COMP%] {\r\n    display: block;\r\n  }\r\n\r\n  .dropdown-wrapper[_ngcontent-%COMP%] {\r\n      width: 100%;\r\n    }\r\n\r\n  .dropdown-item.active[_ngcontent-%COMP%] {\r\n    width: 94.5%;\r\n  }\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvbmV3LXJlcG9ydC9uZXctcmVwb3J0LmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7RUFFRTtJQUNFLFlBQVk7SUFDWixpQkFBaUI7SUFDakIsVUFBVTtJQUNWLGlCQUFpQjtJQUNqQixnQkFBZ0I7SUFDaEIsNkJBQTZCO0lBQzdCLFlBQVk7SUFDWixhQUFhO0lBQ2Isc0JBQXNCO0lBQ3RCLDJCQUEyQjtJQUMzQixtQkFBbUI7RUFDckI7O0VBRUE7SUFDRSxrQkFBa0I7SUFDbEIsa0JBQWtCO0lBQ2xCLHlCQUF5QjtJQUN6QixrQ0FBa0M7SUFDbEMsY0FBYztJQUNkLGVBQWU7SUFDZixpQkFBaUI7RUFDbkI7O0VBRUE7SUFDRSxZQUFZO0lBQ1osYUFBYTtJQUNiLG9CQUFvQjtJQUNwQixXQUFXO0VBQ2I7O0VBRUE7SUFDRSxhQUFhO0lBQ2Isc0JBQXNCO0lBQ3RCLFlBQVk7RUFDZDs7RUFFQTtJQUNFLGFBQWE7SUFDYixzQkFBc0I7SUFDdEIsYUFBYTtFQUNmOztFQUVBO0lBQ0UsWUFBWTtJQUNaLGdCQUFnQjtJQUNoQixzQkFBc0I7SUFDdEIsYUFBYTtJQUNiLFlBQVk7RUFDZDs7RUFFQTtJQUNFLGdCQUFnQjtFQUNsQjs7RUFFQTtJQUNFLGFBQWE7SUFDYiwyQkFBMkI7SUFDM0IsZ0JBQWdCO0VBQ2xCOztFQUVBO0lBQ0UsWUFBWTtFQUNkOztFQUVBO0lBQ0UsZ0JBQWdCO0lBQ2hCLFlBQVk7SUFDWixhQUFhO0lBQ2Isc0JBQXNCO0lBQ3RCLFFBQVE7SUFDUixnQkFBZ0I7O0VBRWxCOztFQUVBO0lBQ0UsYUFBYTtJQUNiLHNCQUFzQjtJQUN0QixTQUFTO0VBQ1g7O0VBRUE7SUFDRSxrQkFBa0I7SUFDbEIsZUFBZTtFQUNqQjs7RUFFQTtJQUNFLGFBQWE7SUFDYixxQkFBcUI7RUFDdkI7O0VBRUE7SUFDRSxhQUFhO0lBQ2IsdUJBQXVCOztFQUV6Qjs7O0FBR0Y7SUFDSSxhQUFhOztJQUViLFlBQVk7SUFDWixVQUFVOztFQUVaOztFQUVBO0lBQ0Usa0JBQWtCO0VBQ3BCOztFQUVBO0lBQ0UsWUFBWTtFQUNkOztFQUVBO0lBQ0UsYUFBYTtJQUNiLFdBQVc7SUFDWCxnQkFBZ0I7RUFDbEI7O0VBRUE7SUFDRSxjQUFjO0lBQ2QsZUFBZTtJQUNmLDBCQUEwQjtFQUM1Qjs7RUFFQTtJQUNFLGNBQWM7RUFDaEI7O0VBRUE7SUFDRSxlQUFlO0lBQ2YsUUFBUTtJQUNSLFNBQVM7SUFDVCxnQ0FBZ0M7RUFDbEM7O0VBRUE7SUFDRSxlQUFlO0lBQ2YsTUFBTTtJQUNOLE9BQU87SUFDUCxXQUFXO0lBQ1gsWUFBWTtJQUNaLG9DQUFvQyxFQUFFLHNDQUFzQztJQUM1RSxhQUFhO0lBQ2IsYUFBYTtFQUNmOztFQUVBO0lBQ0UsY0FBYztFQUNoQjs7RUFFQTtNQUNJLFdBQVc7SUFDYjs7RUFFRjtJQUNFLFlBQVk7RUFDZCIsInNvdXJjZXNDb250ZW50IjpbIlxyXG4gIFxyXG4gIC5mb3JtLWNvbnRhaW5lciB7XHJcbiAgICBoZWlnaHQ6IDcwdmg7XHJcbiAgICBtaW4taGVpZ2h0OiA1ODBweDtcclxuICAgIHdpZHRoOiA0MCU7XHJcbiAgICBtYXJnaW4tbGVmdDogMjBweDtcclxuICAgIG1hcmdpbi10b3A6IDEwcHg7XHJcbiAgICBtYXJnaW4tcmlnaHQ6IDIwcHggIWltcG9ydGFudDtcclxuICAgIHBhZGRpbmc6IDBweDtcclxuICAgIGRpc3BsYXk6IGZsZXg7XHJcbiAgICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xyXG4gICAgYm9yZGVyOiAxcHggc29saWQgbGlnaHRncmF5O1xyXG4gICAgYmFja2dyb3VuZDogI2ZhZmFmYTtcclxuICB9XHJcbiAgXHJcbiAgLmZvcm0taGVhZGVyIHtcclxuICAgIHRleHQtYWxpZ246IGNlbnRlcjtcclxuICAgIG1hcmdpbi1ib3R0b206IDBweDtcclxuICAgIGJhY2tncm91bmQtY29sb3I6ICNFNEYwRjU7XHJcbiAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgbGlnaHRncmF5O1xyXG4gICAgY29sb3I6ICMxODJhNjk7XHJcbiAgICBmb250LXNpemU6IDE4cHg7XHJcbiAgICBmb250LXdlaWdodDogYm9sZDtcclxuICB9XHJcbiAgXHJcbiAgLmZvcm0tY29udGVudCB7XHJcbiAgICBmbGV4LWdyb3c6IDE7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgYWxpZ24taXRlbXM6IHN0cmV0Y2g7XHJcbiAgICBwYWRkaW5nOjVweDtcclxuICB9XHJcbiAgXHJcbiAgLm1haW4tZGl2IHtcclxuICAgIGRpc3BsYXk6IGZsZXg7XHJcbiAgICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xyXG4gICAgZmxleC1ncm93OiAxO1xyXG4gIH1cclxuICBcclxuICAuY29tYmluZWQtc2VjdGlvbiB7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcclxuICAgIGZsZXgtZ3JvdzogMjA7XHJcbiAgfVxyXG4gIFxyXG4gIC5zY3JvbGxhYmxlLWRpdiB7XHJcbiAgICBmbGV4LWdyb3c6IDE7XHJcbiAgICBvdmVyZmxvdy15OiBhdXRvO1xyXG4gICAgYm9yZGVyOiAxcHggc29saWQgI2NjYztcclxuICAgIHBhZGRpbmc6IDEwcHg7XHJcbiAgICBoZWlnaHQ6IDM1dmg7XHJcbiAgfVxyXG5cclxuICAuc2Nyb2xsYWJsZS1jb250ZW50IHtcclxuICAgIG92ZXJmbG93LXk6IGF1dG87XHJcbiAgfVxyXG4gIFxyXG4gIC5saW5rLWJ1dHRvbiB7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAganVzdGlmeS1jb250ZW50OiBmbGV4LXN0YXJ0O1xyXG4gICAgbWFyZ2luLXRvcDogMTBweDtcclxuICB9XHJcbiAgXHJcbiAgLmxpbmstYnV0dG9uIGEge1xyXG4gICAgcGFkZGluZzogNXB4O1xyXG4gIH1cclxuXHJcbiAgLnRleHQtaW5wdXRzIHtcclxuICAgIG1hcmdpbi10b3A6IDE1cHg7XHJcbiAgICBmbGV4LWdyb3c6IDE7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcclxuICAgIGdhcDogMHB4O1xyXG4gICAgb3ZlcmZsb3cteTogYXV0bztcclxuICAgIFxyXG4gIH1cclxuICBcclxuICAudGV4dC1ib3hlcyB7XHJcbiAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcclxuICAgIGdhcDogMTBweDtcclxuICB9XHJcbiAgXHJcbiAgLmZvcm0tZm9vdGVyIHtcclxuICAgIHRleHQtYWxpZ246IGNlbnRlcjtcclxuICAgIG1hcmdpbi10b3A6IDBweDtcclxuICB9XHJcbiAgXHJcbiAgLmlucHV0LWxhYmVsIHtcclxuICAgIGRpc3BsYXk6IGZsZXg7XHJcbiAgICBqdXN0aWZ5LWNvbnRlbnQ6IGxlZnQ7XHJcbiAgfVxyXG4gIFxyXG4gIC5zZWxlY3QtaW5wdXQge1xyXG4gICAgZGlzcGxheTogZmxleDtcclxuICAgIGp1c3RpZnktY29udGVudDogY2VudGVyO1xyXG4gICAgXHJcbiAgfVxyXG5cclxuICBcclxuLmlucHV0LXNtIHtcclxuICAgIGRpc3BsYXk6IGZsZXg7XHJcbiAgICBcclxuICAgIHdpZHRoOiA5OS4wJTtcclxuICAgIG1hcmdpbjoycHg7XHJcblxyXG4gIH1cclxuICBcclxuICAuaW5wdXQtc20gbGFiZWwge1xyXG4gICAgbWFyZ2luLWJvdHRvbTogNXB4O1xyXG4gIH1cclxuICBcclxuICAuaW5wdXQtc20gaW5wdXQge1xyXG4gICAgcGFkZGluZzogNXB4O1xyXG4gIH1cclxuXHJcbiAgLnNlcGFyYXRvciB7XHJcbiAgICBtYXJnaW46IDAgNXB4O1xyXG4gICAgY29sb3I6ICM5OTk7XHJcbiAgICBsaW5lLWhlaWdodDogMmVtO1xyXG4gIH1cclxuXHJcbiAgLmxpbmstYS1jbHN7XHJcbiAgICBjb2xvcjogIzBkNmVmZDtcclxuICAgIGN1cnNvcjogcG9pbnRlcjtcclxuICAgIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xyXG4gIH1cclxuXHJcbiAgLmxpbmstYS1jbHM6aG92ZXIge1xyXG4gICAgY29sb3I6ICMwYTU4Y2E7XHJcbiAgfVxyXG5cclxuICAuY2VudGVyZWQtaW1hZ2Uge1xyXG4gICAgcG9zaXRpb246IGZpeGVkO1xyXG4gICAgdG9wOiA1MCU7XHJcbiAgICBsZWZ0OiA1MCU7XHJcbiAgICB0cmFuc2Zvcm06IHRyYW5zbGF0ZSgtNTAlLCAtNTAlKTtcclxuICB9XHJcblxyXG4gIC5vdmVybGF5IHtcclxuICAgIHBvc2l0aW9uOiBmaXhlZDtcclxuICAgIHRvcDogMDtcclxuICAgIGxlZnQ6IDA7XHJcbiAgICB3aWR0aDogMTAwJTtcclxuICAgIGhlaWdodDogMTAwJTtcclxuICAgIGJhY2tncm91bmQtY29sb3I6IHJnYmEoMCwgMCwgMCwgMC41KTsgLyogQWRqdXN0IHRoZSB0cmFuc3BhcmVuY3kgYXMgbmVlZGVkICovXHJcbiAgICB6LWluZGV4OiA5OTk5O1xyXG4gICAgZGlzcGxheTogbm9uZTtcclxuICB9XHJcbiAgXHJcbiAgLm92ZXJsYXkuc2hvdyB7XHJcbiAgICBkaXNwbGF5OiBibG9jaztcclxuICB9XHJcblxyXG4gIC5kcm9wZG93bi13cmFwcGVyIHtcclxuICAgICAgd2lkdGg6IDEwMCU7XHJcbiAgICB9XHJcblxyXG4gIC5kcm9wZG93bi1pdGVtLmFjdGl2ZSB7XHJcbiAgICB3aWR0aDogOTQuNSU7XHJcbiAgfVxyXG4gICJdLCJzb3VyY2VSb290IjoiIn0= */"]
});

/***/ }),

/***/ 7092:
/*!************************************************!*\
  !*** ./src/app/pkl-view/pkl-view.component.ts ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PklViewComponent": () => (/* binding */ PklViewComponent)
/* harmony export */ });
/* harmony import */ var C_Users_v_nrosenberg_Documents_Sources_StatisticsTool_ng_client_statToolAngularApp_node_modules_babel_runtime_helpers_esm_asyncToGenerator_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./node_modules/@babel/runtime/helpers/esm/asyncToGenerator.js */ 1670);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ 6078);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils */ 7225);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @ng-bootstrap/ng-bootstrap */ 4534);
/* harmony import */ var _segmentations_segmentations_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../segmentations/segmentations.component */ 3696);
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../app.component */ 5041);










const _c0 = ["iframe"];
function PklViewComponent_div_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](0, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelement"](1, "img", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]();
  }
}
function PklViewComponent_div_18_Template(rf, ctx) {
  if (rf & 1) {
    const _r4 = _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](0, "div", 15)(1, "ngb-alert", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵlistener"]("closed", function PklViewComponent_div_18_Template_ngb_alert_closed_1_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵrestoreView"](_r4);
      const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵresetView"](ctx_r3.statToolService.fileNotFoundError = "");
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵtextInterpolate"](ctx_r2.statToolService.fileNotFoundError);
  }
}
const _c1 = function (a0) {
  return {
    "height": a0
  };
};
class PklViewComponent {
  set selectedRowsSet(rows) {
    //filter only the existing rows
    let tmp = [];
    let keys = Array.from(this.statToolService.optionalSegmentations.keys());
    rows.forEach(r => {
      let isExist = keys.find(x => x == r);
      if (isExist) tmp.push(r);
    });
    this.selectedRows = tmp.join(',');
  }
  set selectedColumnsSet(cols) {
    //filter only the existing columns
    let tmp = [];
    let keys = Array.from(this.statToolService.optionalSegmentations.keys());
    cols.forEach(c => {
      let isExist = keys.find(x => x == c);
      if (isExist) tmp.push(c);
    });
    this.selectedColumns = tmp.join(',');
  }
  constructor(statToolService) {
    this.statToolService = statToolService;
    this.iframe = null;
    this.url = '/viewer/get_report_table';
    this.selectedRows = '';
    this.viewguid = '';
    this.selectedColumns = '';
    this.name = '';
    this.id = 0;
    this.loadCounter = 0;
    this.subscribeUniqueChange = new rxjs__WEBPACK_IMPORTED_MODULE_6__.Subscription();
    this.subscribeReportChanged = new rxjs__WEBPACK_IMPORTED_MODULE_6__.Subscription();
    this.height = '';
    this.url = '/viewer/get_report_table?calc_unique=' + statToolService.calculateUnique + "&main_path=" + this.statToolService.getSelectedMainReport() + "&ref_path=" + this.statToolService.getSelectedRefReport();
  }
  setUrl() {
    this.url = '/viewer/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&main_path=" + this.statToolService.getSelectedMainReport() + "&ref_path=" + this.statToolService.getSelectedRefReport();
  }
  ngOnInit() {
    this.fixSelectedString();
    this.setUrl();
    this.loadCounter = 1;
    this.subscribeUniqueChange = this.statToolService.uniqueValueChanged.subscribe(res => {
      this.loadCounter = 1;
      this.setUrl();
    });
    this.subscribeReportChanged = this.statToolService.reportSelected.subscribe(res => {
      this.fixSelectedString();
      this.loadCounter = 1;
      this.setUrl();
    });
  }
  ngOnDestroy() {
    if (this.subscribeUniqueChange != null) this.subscribeUniqueChange.unsubscribe();
    if (this.subscribeReportChanged != null) this.subscribeReportChanged.unsubscribe();
  }
  onColumnAdded(item) {
    if (this.selectedColumns.length == 0) this.selectedColumns = item.item_id;else this.selectedColumns += "," + item.item_id;
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  onAllColumnsAdded(items) {
    this.selectedColumns = '';
    items.forEach(x => {
      this.selectedColumns += x.item_id + ",";
    });
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  onColumnRemoved(item) {
    let columns = this.selectedColumns.split(",");
    this.selectedColumns = '';
    columns.forEach(c => {
      if (c != item.item_text) {
        this.selectedColumns += c + ",";
      }
    });
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  onAllColumnsRemoved(event) {
    this.selectedColumns = '';
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  onRowAdded(item) {
    if (this.selectedRows.length == 0) this.selectedRows = item.item_id;else this.selectedRows += "," + item.item_id;
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  onAllRowsAdded(items) {
    this.selectedRows = '';
    items.forEach(x => {
      this.selectedRows += x.item_id + ",";
    });
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  onRowRemoved(item) {
    let columns = this.selectedRows.split(",");
    this.selectedRows = '';
    columns.forEach(c => {
      if (c != item.item_text) {
        this.selectedRows += c + ",";
      }
    });
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  onAllRowsRemoved(event) {
    this.selectedRows = '';
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.setUrl();
  }
  fixSelectedString() {
    if (this.selectedColumns.slice(-1) == ",") this.selectedColumns = this.selectedColumns.slice(0, -1);
    if (this.selectedRows.slice(-1) == ",") this.selectedRows = this.selectedRows.slice(0, -1);
  }
  onIframeLoad() {
    var _this = this;
    return (0,C_Users_v_nrosenberg_Documents_Sources_StatisticsTool_ng_client_statToolAngularApp_node_modules_babel_runtime_helpers_esm_asyncToGenerator_js__WEBPACK_IMPORTED_MODULE_0__["default"])(function* () {
      _this.loadCounter = _this.loadCounter - 1;
      if (_this.iframe != null) {
        let loop = true;
        while (loop) {
          yield _utils__WEBPACK_IMPORTED_MODULE_1__.Utils.sleep(100);
          let h = _this.iframe.nativeElement.contentWindow.document.body.scrollHeight;
          if (h > 100) {
            h += 100;
            _this.height = h.toString() + 'px';
            _this.statToolService.viewHeights.set(_this.id, _this.height);
            loop = false;
          }
        }
      }
    })();
  }
  onViewNameChanged(event) {
    this.statToolService.updateSegmentationName(this.name, this.id, event.target.value);
  }
  removeView() {
    this.statToolService.removeView(this.viewguid);
  }
}
PklViewComponent.ɵfac = function PklViewComponent_Factory(t) {
  return new (t || PklViewComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_2__.StatisticsToolService));
};
PklViewComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵdefineComponent"]({
  type: PklViewComponent,
  selectors: [["pkl-view"]],
  viewQuery: function PklViewComponent_Query(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵviewQuery"](_c0, 5);
    }
    if (rf & 2) {
      let _t;
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵloadQuery"]()) && (ctx.iframe = _t.first);
    }
  },
  inputs: {
    selectedRowsSet: "selectedRowsSet",
    viewguid: "viewguid",
    selectedColumns: "selectedColumns",
    selectedColumnsSet: "selectedColumnsSet",
    name: "name",
    id: "id"
  },
  decls: 19,
  vars: 15,
  consts: [[1, "parent", 2, "border", "1px solid lightgray", "padding", "3px"], [4, "ngIf"], [1, "pkl-view-header", 2, "width", "99.6%", "padding", "3px", "border", "solid 1px lightgray", "border-radius", "4x !important", "margin-top", "3px", "color", "#182a69", "background-color", "#fafafa"], [2, "width", "100%"], [2, "width", "20%"], ["type", "text", "placeholder", "View Name", 1, "view-name", 2, "padding-left", "5px", "height", "38px", "width", "96%", "border", "1px solid #adadad", "border-radius", "3px", 3, "ngModel", "change"], [2, "width", "38%"], ["name", "Horizontal Segmentation", "elementRef", "Horizontal_Segmentation", 2, "width", "95%", "background-color", "white", "margin-top", "2px", 3, "viewId", "viewguid", "selectItems", "segmentAdded", "segmentRemoved", "allSegmentsAdded", "allSegmentsRemoved"], ["name", "Vertical Segmentation", "elementRef", "Vertical_Segmentation", 2, "width", "95%", "background-color", "white", 3, "viewId", "viewguid", "selectItems", "segmentAdded", "segmentRemoved", "allSegmentsAdded", "allSegmentsRemoved"], [2, "text-align", "right"], ["src", "assets/cancel-icon.svg", "title", "Remove View", 2, "height", "33px", "width", "33px", "position", "relative", "cursor", "pointer", 3, "click"], [2, "display", "block", "width", "100%", "margin-top", "3px", "border", "none", 3, "src", "ngStyle", "load"], ["iframe", ""], ["style", "position: sticky;bottom: 200px;z-index: 99999999;", 4, "ngIf"], ["src", "assets/spinner-90-ring-with-bg.svg", 2, "width", "40px", "height", "40x"], [2, "position", "sticky", "bottom", "200px", "z-index", "99999999"], ["type", "danger", 3, "closed"]],
  template: function PklViewComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](0, "div", 0);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵtemplate"](1, PklViewComponent_div_1_Template, 2, 0, "div", 1);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](2, "div", 2)(3, "div", 3)(4, "table", 3)(5, "tr")(6, "td", 4)(7, "input", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵlistener"]("change", function PklViewComponent_Template_input_change_7_listener($event) {
        return ctx.onViewNameChanged($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](8, "td", 6)(9, "segmentations", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵlistener"]("segmentAdded", function PklViewComponent_Template_segmentations_segmentAdded_9_listener($event) {
        return ctx.onColumnAdded($event);
      })("segmentRemoved", function PklViewComponent_Template_segmentations_segmentRemoved_9_listener($event) {
        return ctx.onColumnRemoved($event);
      })("allSegmentsAdded", function PklViewComponent_Template_segmentations_allSegmentsAdded_9_listener($event) {
        return ctx.onAllColumnsAdded($event);
      })("allSegmentsRemoved", function PklViewComponent_Template_segmentations_allSegmentsRemoved_9_listener($event) {
        return ctx.onAllColumnsRemoved($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵtext"](10, " > ");
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](11, "td", 6)(12, "segmentations", 8);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵlistener"]("segmentAdded", function PklViewComponent_Template_segmentations_segmentAdded_12_listener($event) {
        return ctx.onRowAdded($event);
      })("segmentRemoved", function PklViewComponent_Template_segmentations_segmentRemoved_12_listener($event) {
        return ctx.onRowRemoved($event);
      })("allSegmentsAdded", function PklViewComponent_Template_segmentations_allSegmentsAdded_12_listener($event) {
        return ctx.onAllRowsAdded($event);
      })("allSegmentsRemoved", function PklViewComponent_Template_segmentations_allSegmentsRemoved_12_listener($event) {
        return ctx.onAllRowsRemoved($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](13, "td", 9)(14, "img", 10);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵlistener"]("click", function PklViewComponent_Template_img_click_14_listener() {
        return ctx.removeView();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]()()()()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](15, "iframe", 11, 12);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵlistener"]("load", function PklViewComponent_Template_iframe_load_15_listener() {
        return ctx.onIframeLoad();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵpipe"](17, "safe");
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵtemplate"](18, PklViewComponent_div_18_Template, 3, 1, "div", 13);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("ngIf", ctx.loadCounter > 0);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](6);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("ngModel", ctx.name);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](2);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("viewId", ctx.id)("viewguid", ctx.viewguid)("selectItems", ctx.selectedColumns);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("viewId", ctx.id)("viewguid", ctx.viewguid)("selectItems", ctx.selectedRows);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("src", _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵpipeBind1"](17, 11, ctx.url), _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵsanitizeResourceUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵpureFunction1"](13, _c1, ctx.height));
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("ngIf", ctx.statToolService.showFileNotFoundError());
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_7__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgStyle, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgModel, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_9__.NgbAlert, _segmentations_segmentations_component__WEBPACK_IMPORTED_MODULE_3__.SegmentationsComponent, _app_component__WEBPACK_IMPORTED_MODULE_4__.SafePipe],
  styles: [".multiselect-dropdown[_ngcontent-%COMP%] {\r\n  width: 96% !important;\r\n  margin:2px !important;\r\n  background-color: white !important;\r\n  border-color: lightgray;\r\n}\r\n.parent[_ngcontent-%COMP%]{\r\n  \r\n}\r\n.parent[_ngcontent-%COMP%]   img[_ngcontent-%COMP%]{\r\n  position: absolute;\r\n  top: 0;       \r\n  bottom: 0;    \r\n  left: 0;\r\n  right: 0;\r\n  margin:auto;\r\n}\r\n\r\n  .pkl-view-header .mat-grid-tile-content {\r\n  justify-content: left !important;\r\n}\r\n\r\n.caption[_ngcontent-%COMP%] {\r\n  padding-left: 3px;\r\n  font-weight: bold;\r\n}\r\n\r\n.view-name[_ngcontent-%COMP%]:focus {\r\n  outline: none;\r\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvcGtsLXZpZXcvcGtsLXZpZXcuY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLHFCQUFxQjtFQUNyQixxQkFBcUI7RUFDckIsa0NBQWtDO0VBQ2xDLHVCQUF1QjtBQUN6QjtBQUNBO0VBQ0Usc0JBQXNCO0FBQ3hCO0FBQ0E7RUFDRSxrQkFBa0I7RUFDbEIsTUFBTTtFQUNOLFNBQVM7RUFDVCxPQUFPO0VBQ1AsUUFBUTtFQUNSLFdBQVc7QUFDYjs7QUFFQTtFQUNFLGdDQUFnQztBQUNsQzs7QUFFQTtFQUNFLGlCQUFpQjtFQUNqQixpQkFBaUI7QUFDbkI7O0FBRUE7RUFDRSxhQUFhO0FBQ2YiLCJzb3VyY2VzQ29udGVudCI6WyIubXVsdGlzZWxlY3QtZHJvcGRvd24ge1xyXG4gIHdpZHRoOiA5NiUgIWltcG9ydGFudDtcclxuICBtYXJnaW46MnB4ICFpbXBvcnRhbnQ7XHJcbiAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGUgIWltcG9ydGFudDtcclxuICBib3JkZXItY29sb3I6IGxpZ2h0Z3JheTtcclxufVxyXG4ucGFyZW50e1xyXG4gIC8qcG9zaXRpb246IHJlbGF0aXZlOyovXHJcbn1cclxuLnBhcmVudCBpbWd7XHJcbiAgcG9zaXRpb246IGFic29sdXRlO1xyXG4gIHRvcDogMDsgICAgICAgXHJcbiAgYm90dG9tOiAwOyAgICBcclxuICBsZWZ0OiAwO1xyXG4gIHJpZ2h0OiAwO1xyXG4gIG1hcmdpbjphdXRvO1xyXG59XHJcblxyXG46Om5nLWRlZXAgLnBrbC12aWV3LWhlYWRlciAubWF0LWdyaWQtdGlsZS1jb250ZW50IHtcclxuICBqdXN0aWZ5LWNvbnRlbnQ6IGxlZnQgIWltcG9ydGFudDtcclxufVxyXG5cclxuLmNhcHRpb24ge1xyXG4gIHBhZGRpbmctbGVmdDogM3B4O1xyXG4gIGZvbnQtd2VpZ2h0OiBib2xkO1xyXG59XHJcblxyXG4udmlldy1uYW1lOmZvY3VzIHtcclxuICBvdXRsaW5lOiBub25lO1xyXG59Il0sInNvdXJjZVJvb3QiOiIifQ== */"]
});

/***/ }),

/***/ 7972:
/*!******************************************************************!*\
  !*** ./src/app/save-suite-dialog/save-suite-dialog.component.ts ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SaveSuiteDialogComponent": () => (/* binding */ SaveSuiteDialogComponent)
/* harmony export */ });
/* harmony import */ var _services_new_report_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/new-report.service */ 9167);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ 2508);




class SaveSuiteDialogComponent {
  constructor(newReportService) {
    this.newReportService = newReportService;
    this.suiteName = '';
    let name = this.newReportService.getSelectedSuiteName();
    if (name == _services_new_report_service__WEBPACK_IMPORTED_MODULE_0__.SELECTE_SUITE) {
      this.suiteName = '';
    } else {
      this.suiteName = name;
    }
  }
  close() {
    this.newReportService.closeSaveSuiteDialog();
  }
  save() {
    if (this.suiteName == '') return;
    this.newReportService.saveSuite(this.suiteName);
    this.close();
  }
  disableSaveButton() {
    return false;
  }
}
SaveSuiteDialogComponent.ɵfac = function SaveSuiteDialogComponent_Factory(t) {
  return new (t || SaveSuiteDialogComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_new_report_service__WEBPACK_IMPORTED_MODULE_0__.NewReportService));
};
SaveSuiteDialogComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: SaveSuiteDialogComponent,
  selectors: [["save-suite-dialog"]],
  decls: 14,
  vars: 1,
  consts: [[1, "modal-header"], ["id", "modal-basic-title", 1, "modal-title"], ["type", "button", "aria-label", "Close", 1, "btn-close", 3, "click"], [1, "modal-body"], [1, "mb-3"], ["for", "name"], [1, "input-group"], ["id", "suiteName", "placeholder", "Suite Name", "name", "suiteName", 1, "form-control", 3, "ngModel", "ngModelChange"], [1, "modal-footer"], ["type", "button", 1, "btn", "btn-outline-dark", 3, "click"]],
  template: function SaveSuiteDialogComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 0)(1, "h4", 1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2, "Save Suite");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "button", 2);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function SaveSuiteDialogComponent_Template_button_click_3_listener() {
        return ctx.close();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](4, "div", 3)(5, "form")(6, "div", 4)(7, "label", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](8, "Suite Name");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](9, "div", 6)(10, "input", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function SaveSuiteDialogComponent_Template_input_ngModelChange_10_listener($event) {
        return ctx.suiteName = $event;
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](11, "div", 8)(12, "button", 9);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function SaveSuiteDialogComponent_Template_button_click_12_listener() {
        return ctx.save();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](13, "Save");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](10);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx.suiteName);
    }
  },
  dependencies: [_angular_forms__WEBPACK_IMPORTED_MODULE_2__["ɵNgNoValidate"], _angular_forms__WEBPACK_IMPORTED_MODULE_2__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgModel, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgForm],
  styles: ["\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
});

/***/ }),

/***/ 7897:
/*!************************************************************************!*\
  !*** ./src/app/save-template-dialog/save-template-dialog.component.ts ***!
  \************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SaveTemplateDialogComponent": () => (/* binding */ SaveTemplateDialogComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ 2508);



class SaveTemplateDialogComponent {
  constructor(statService) {
    this.statService = statService;
    this.templateName = '';
    let name = this.statService.getSelectedTemplateName();
    if (name == 'Default (Total)') {
      this.templateName = '';
    } else {
      this.templateName = name;
    }
  }
  close() {
    this.statService.closeSaveTempalteDialog();
  }
  save() {
    if (this.templateName == '') return;
    this.statService.saveTemplate(this.templateName);
    this.close();
  }
  disableSaveButton() {
    return false;
  }
}
SaveTemplateDialogComponent.ɵfac = function SaveTemplateDialogComponent_Factory(t) {
  return new (t || SaveTemplateDialogComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService));
};
SaveTemplateDialogComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: SaveTemplateDialogComponent,
  selectors: [["save-template-dialog"]],
  decls: 14,
  vars: 1,
  consts: [[1, "modal-header"], ["id", "modal-basic-title", 1, "modal-title"], ["type", "button", "aria-label", "Close", 1, "btn-close", 3, "click"], [1, "modal-body"], [1, "mb-3"], ["for", "name"], [1, "input-group"], ["id", "templateName", "placeholder", "Tempalte Name", "name", "templateName", 1, "form-control", 3, "ngModel", "ngModelChange"], [1, "modal-footer"], ["type", "button", 1, "btn", "btn-outline-dark", 3, "click"]],
  template: function SaveTemplateDialogComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 0)(1, "h4", 1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2, "Save Template");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "button", 2);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function SaveTemplateDialogComponent_Template_button_click_3_listener() {
        return ctx.close();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](4, "div", 3)(5, "form")(6, "div", 4)(7, "label", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](8, "Template Name");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](9, "div", 6)(10, "input", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function SaveTemplateDialogComponent_Template_input_ngModelChange_10_listener($event) {
        return ctx.templateName = $event;
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](11, "div", 8)(12, "button", 9);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function SaveTemplateDialogComponent_Template_button_click_12_listener() {
        return ctx.save();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](13, "Save");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](10);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx.templateName);
    }
  },
  dependencies: [_angular_forms__WEBPACK_IMPORTED_MODULE_2__["ɵNgNoValidate"], _angular_forms__WEBPACK_IMPORTED_MODULE_2__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgModel, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgForm],
  styles: ["\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
});

/***/ }),

/***/ 3696:
/*!**********************************************************!*\
  !*** ./src/app/segmentations/segmentations.component.ts ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SegmentationsComponent": () => (/* binding */ SegmentationsComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ 6078);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _services_common_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../services/common.service */ 5620);
/* harmony import */ var ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ng-multiselect-dropdown */ 1664);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _click_outside_directive__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../click-outside.directive */ 9155);











const _c0 = ["dropdown"];
function SegmentationsComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r3 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementStart"](0, "div", 1, 2)(2, "ng-multiselect-dropdown", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵlistener"]("ngModelChange", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_ngModelChange_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r3);
      const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r2.selected = $event);
    })("onSelect", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onSelect_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r3);
      const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r4.onItemSelect($event));
    })("onSelectAll", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onSelectAll_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r3);
      const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r5.onSelectAll($event));
    })("onDeSelect", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onDeSelect_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r3);
      const ctx_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r6.onUnSelect($event));
    })("onDeSelectAll", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onDeSelectAll_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r3);
      const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r7.onUnSelectAll($event));
    })("click", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_click_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵrestoreView"](_r3);
      const ctx_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵresetView"](ctx_r8.onClick($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵclassProp"]("dropdown-open", ctx_r0.isDropdownOpen);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("viewguid", ctx_r0.viewguid)("viewId", ctx_r0.viewId)("segmentName", ctx_r0.name)("placeholder", ctx_r0.name)("settings", ctx_r0.dropdownSettings)("data", ctx_r0.dropdownList)("ngModel", ctx_r0.selected);
  }
}
class SegmentationsComponent {
  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }
  set selectItems(items) {
    if (items == "," || items == "" || items == ' ') return;
    let arr = items.split(',');
    this.selected = [];
    arr.forEach(a => {
      this.selected.push({
        'item_id': a,
        'item_text': a
      });
    });
  }
  constructor(statToolService, httpClient, commonSvc) {
    this.statToolService = statToolService;
    this.httpClient = httpClient;
    this.commonSvc = commonSvc;
    this.isDropdownOpen = false;
    this.viewId = 0;
    this.name = '';
    this.elementRef = '';
    this.viewguid = '';
    this.dropdownList = [];
    this.selected = [];
    this.dropdownSettings = {};
    this.subscribeSegmentationsFetched = new rxjs__WEBPACK_IMPORTED_MODULE_4__.Subscription();
    this.segmentAdded = new _angular_core__WEBPACK_IMPORTED_MODULE_3__.EventEmitter();
    this.segmentRemoved = new _angular_core__WEBPACK_IMPORTED_MODULE_3__.EventEmitter();
    this.allSegmentsAdded = new _angular_core__WEBPACK_IMPORTED_MODULE_3__.EventEmitter();
    this.allSegmentsRemoved = new _angular_core__WEBPACK_IMPORTED_MODULE_3__.EventEmitter();
  }
  ngOnInit() {
    for (let [key, value] of this.statToolService.optionalSegmentations) {
      this.dropdownList.push({
        'item_id': key,
        'item_text': key
      });
    }
    this.dropdownSettings = {
      singleSelection: false,
      idField: 'item_id',
      textField: 'item_text',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      itemsShowLimit: 100,
      allowSearchFilter: true
    };
    /*this.commonSvc.onMouseClicked.subscribe(event => {
      this.isDropdownOpen = false;
      console.log(this.isDropdownOpen +"," + event.target)
      if (this.dropdown != undefined)
        if (!this.dropdown.nativeElement.contains(event.target)) {
          this.isDropdownOpen = false;
        }
    })*/
  }

  onItemSelect(item) {
    console.log('onItemSelect', item);
    this.segmentAdded.emit(item);
  }
  onSelectAll(items) {
    console.log('onSelectAll', items);
    this.allSegmentsAdded.emit(items);
  }
  onUnSelect(item) {
    console.log('onUnSelect', item);
    this.segmentRemoved.emit(item);
  }
  onUnSelectAll(item) {
    console.log('onUnSelectAll', item);
    this.allSegmentsRemoved.emit([]);
  }
  onClick(event) {
    let name = this.dropdown?.nativeElement.parentElement.attributes['name'].value;
    if (!this.dropdown?.nativeElement.querySelectorAll('.dropdown-list')[0].hidden) {
      this.statToolService.setDropdownState(this.viewguid, name, _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.States.Opened);
      return;
    }
    this.statToolService.setDropdownState(this.viewguid, name, _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.States.Close);
  }
  ngOnDestroy() {
    if (this.subscribeSegmentationsFetched != null) this.subscribeSegmentationsFetched.unsubscribe();
  }
}
SegmentationsComponent.ɵfac = function SegmentationsComponent_Factory(t) {
  return new (t || SegmentationsComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdirectiveInject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_5__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdirectiveInject"](_services_common_service__WEBPACK_IMPORTED_MODULE_1__.CommonService));
};
SegmentationsComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineComponent"]({
  type: SegmentationsComponent,
  selectors: [["segmentations"]],
  viewQuery: function SegmentationsComponent_Query(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵviewQuery"](_c0, 5);
    }
    if (rf & 2) {
      let _t;
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵloadQuery"]()) && (ctx.dropdown = _t.first);
    }
  },
  inputs: {
    selectItems: "selectItems",
    viewId: "viewId",
    name: "name",
    elementRef: "elementRef",
    viewguid: "viewguid"
  },
  outputs: {
    segmentAdded: "segmentAdded",
    segmentRemoved: "segmentRemoved",
    allSegmentsAdded: "allSegmentsAdded",
    allSegmentsRemoved: "allSegmentsRemoved"
  },
  decls: 1,
  vars: 1,
  consts: [["class", "dropdown-wrapper", 3, "dropdown-open", 4, "ngIf"], [1, "dropdown-wrapper"], ["dropdown", ""], ["appClickOutside", "", 3, "viewguid", "viewId", "segmentName", "placeholder", "settings", "data", "ngModel", "ngModelChange", "onSelect", "onSelectAll", "onDeSelect", "onDeSelectAll", "click"]],
  template: function SegmentationsComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵtemplate"](0, SegmentationsComponent_div_0_Template, 3, 9, "div", 0);
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵproperty"]("ngIf", ctx.dropdownList.length > 0);
    }
  },
  dependencies: [ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_6__.MultiSelectComponent, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgModel, _click_outside_directive__WEBPACK_IMPORTED_MODULE_2__.ClickOutsideDirective],
  styles: [".dropdown-open[_ngcontent-%COMP%]   .ng-dropdown-panel[_ngcontent-%COMP%] {\r\n    display: block !important;\r\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvc2VnbWVudGF0aW9ucy9zZWdtZW50YXRpb25zLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUNBO0lBQ0kseUJBQXlCO0FBQzdCIiwic291cmNlc0NvbnRlbnQiOlsiXHJcbi5kcm9wZG93bi1vcGVuIC5uZy1kcm9wZG93bi1wYW5lbCB7XHJcbiAgICBkaXNwbGF5OiBibG9jayAhaW1wb3J0YW50O1xyXG59XHJcblxyXG4gICJdLCJzb3VyY2VSb290IjoiIn0= */"]
});

/***/ }),

/***/ 5620:
/*!********************************************!*\
  !*** ./src/app/services/common.service.ts ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommonService": () => (/* binding */ CommonService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ 228);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);


class CommonService {
  constructor() {
    this.onMouseClicked = new rxjs__WEBPACK_IMPORTED_MODULE_0__.Subject();
  }
}
CommonService.ɵfac = function CommonService_Factory(t) {
  return new (t || CommonService)();
};
CommonService.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"]({
  token: CommonService,
  factory: CommonService.ɵfac,
  providedIn: 'root'
});

/***/ }),

/***/ 9167:
/*!************************************************!*\
  !*** ./src/app/services/new-report.service.ts ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NONE_GT_READING_CUNCTION": () => (/* binding */ NONE_GT_READING_CUNCTION),
/* harmony export */   "NewReportResult": () => (/* binding */ NewReportResult),
/* harmony export */   "NewReportService": () => (/* binding */ NewReportService),
/* harmony export */   "SELECTE_SUITE": () => (/* binding */ SELECTE_SUITE),
/* harmony export */   "UDF": () => (/* binding */ UDF)
/* harmony export */ });
/* harmony import */ var C_Users_v_nrosenberg_Documents_Sources_StatisticsTool_ng_client_statToolAngularApp_node_modules_babel_runtime_helpers_esm_asyncToGenerator_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./node_modules/@babel/runtime/helpers/esm/asyncToGenerator.js */ 1670);
/* harmony import */ var _save_suite_dialog_save_suite_dialog_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../save-suite-dialog/save-suite-dialog.component */ 7972);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ 228);
/* harmony import */ var _common_enums__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../common/enums */ 5383);
/* harmony import */ var sweetalert2__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! sweetalert2 */ 598);
/* harmony import */ var sweetalert2__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(sweetalert2__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @ng-bootstrap/ng-bootstrap */ 4534);








const SELECTE_SUITE = '--- Select Suite ---';
const NONE_GT_READING_CUNCTION = 'none';
class NewReportResult {
  constructor() {
    this.ok = true;
    this.errorMessage = '';
    this.link = '';
    this.files = [];
    this.num_success_files = [];
    this.reading_function_skipped = [];
    this.not_json_files = [];
    this.failed_with_error = [];
    this.skipped_not_in_lognames = [];
  }
}
var UDF;
(function (UDF) {
  let ParamType;
  (function (ParamType) {
    ParamType[ParamType["STRING"] = 0] = "STRING";
  })(ParamType = UDF.ParamType || (UDF.ParamType = {}));
  class Param {
    constructor(name, type) {
      this.name = '';
      this.type = ParamType.STRING;
      this.value = '';
      this.name = name;
      if (type == 'string') {
        this.type = ParamType.STRING;
      }
    }
  }
  UDF.Param = Param;
  class Item {
    constructor(funcName, params) {
      this.funcName = '';
      this.params = [];
      this.funcName = funcName;
      this.params = params;
    }
  }
  UDF.Item = Item;
})(UDF || (UDF = {}));
class NewReportService {
  constructor(http, modalService) {
    this.http = http;
    this.modalService = modalService;
    this.showConfigViewer = true;
    this.configs = [];
    this.suites = [];
    this.configsSelections = new Map();
    this.selectedSuite = '';
    this.prediction_reading_functions = [];
    this.gt_reading_functions = [];
    this.evaluation_functions = [];
    this.overlap_functions = [];
    this.partitioning_functions = [];
    this.statistics_functions = [];
    this.transform_functions = [];
    this.confusion_functions = [];
    this.association_functions = [];
    this.selectedPredictionReadingFunction = '';
    this.selectedGTReadingFunction = '';
    this.selectedTransformFunction = '';
    this.selectedPartitioningFunction = '';
    this.selectedStatisticsFunction = '';
    this.selectedConfusionFunction = '';
    this.selectedAssociationFunction = '';
    this.configName = '';
    this.logsFilter = _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFConstants.DEFAULT_LOG_FILTER;
    this.evaluate_folders = false;
    this.predictionsDirectory = '';
    this.groundTruthDirectory = '';
    this.reporterOutputDirectory = '';
    this.newReportResult = new NewReportResult();
    this.isBusy = false;
    this.last_prediction_directory = [];
    this.last_ground_truth_directory = [];
    this.last_output_directory = [];
    this.gtReadingSameAsPrediction = true;
    this.transformEnabled = false;
    this.partitioningEnabled = false;
    this.associationEnabled = false;
    this.isPanelOpen = false;
    //map between udf type (for example reading_function) to function names
    this.udf = new Map();
    this.showArgumentsEvent = new rxjs__WEBPACK_IMPORTED_MODULE_4__.Subject();
    this.showParams = false;
    this.argPanelTop = '';
    this.argPanelLeft = '';
    this.udfArgumentsMap = {};
  }
  initialize() {
    var _this = this;
    return (0,C_Users_v_nrosenberg_Documents_Sources_StatisticsTool_ng_client_statToolAngularApp_node_modules_babel_runtime_helpers_esm_asyncToGenerator_js__WEBPACK_IMPORTED_MODULE_0__["default"])(function* () {
      _this.isBusy = true;
      yield _this.initUserDefinedFunction();
      yield _this.initSuitsAndConfigs();
      _this.isBusy = false;
    })();
  }
  initSuitsAndConfigs() {
    var _this2 = this;
    return (0,C_Users_v_nrosenberg_Documents_Sources_StatisticsTool_ng_client_statToolAngularApp_node_modules_babel_runtime_helpers_esm_asyncToGenerator_js__WEBPACK_IMPORTED_MODULE_0__["default"])(function* () {
      try {
        const url = '/new_report/get_all_configs_and_suits';
        const response = yield _this2.http.get(url).toPromise();
        let configs = response.configs;
        let suites = response.suites;
        _this2.parseConfigs(configs);
        _this2.initSuitesList(suites);
        _this2.selectedSuite = SELECTE_SUITE;
        _this2.initSelectedConfigs();
      } finally {}
    })();
  }
  initUserDefinedFunction() {
    var _this3 = this;
    return (0,C_Users_v_nrosenberg_Documents_Sources_StatisticsTool_ng_client_statToolAngularApp_node_modules_babel_runtime_helpers_esm_asyncToGenerator_js__WEBPACK_IMPORTED_MODULE_0__["default"])(function* () {
      try {
        const url = '/new_report/get_all_user_defined_functions';
        const response = yield _this3.http.get(url).toPromise();
        _this3.processUdfResponse(response);
        _this3.prediction_reading_functions = _this3.udf.get(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.READING_FUNCTIONS)?.map(o => o.funcName);
        _this3.prediction_reading_functions.sort((a, b) => a > b ? 1 : -1);
        _this3.gt_reading_functions = _this3.prediction_reading_functions;
        _this3.partitioning_functions = _this3.udf.get(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.PARTITIONING_FUNCTIONS)?.map(o => o.funcName);
        _this3.partitioning_functions.sort((a, b) => a > b ? 1 : -1);
        _this3.statistics_functions = _this3.udf.get(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.STATISTICS_FUNCTIONS)?.map(o => o.funcName);
        _this3.statistics_functions.sort((a, b) => a > b ? 1 : -1);
        _this3.transform_functions = _this3.udf.get(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.TRANSFORM_FUNCTIONS)?.map(o => o.funcName);
        _this3.transform_functions.sort((a, b) => a > b ? 1 : -1);
        _this3.confusion_functions = _this3.udf.get(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.CONFUSION_FUNCTIONS)?.map(o => o.funcName);
        _this3.confusion_functions.sort((a, b) => a > b ? 1 : -1);
        _this3.association_functions = _this3.udf.get(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.ASSOCIATION_FUNCTIONS)?.map(o => o.funcName);
        _this3.association_functions.sort((a, b) => a > b ? 1 : -1);
      } catch (error) {
        console.error('Error initializing user-defined functions:', error);
      }
    })();
  }
  processUdfResponse(udfResponse) {
    for (const value of Object.values(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum)) {
      if (value === _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.GT_READING_FUNCTIONS) {
        continue;
      }
      let funcs = this.processUdfItem(value, udfResponse);
      this.udf.set(value, funcs);
    }
    let readingFunc = this.udf.get(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.READING_FUNCTIONS);
    let gt = JSON.parse(JSON.stringify(readingFunc));
    this.udf.set(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.GT_READING_FUNCTIONS, gt);
  }
  processUdfItem(funcType, udfResponse) {
    let arrFuncs = [];
    let functions = udfResponse[funcType];
    if (functions == undefined || functions == null) return arrFuncs;
    for (const func of functions) {
      let funcName = func.func_name;
      let funcArguments = func.params;
      let params = [];
      for (const key in funcArguments) {
        if (funcArguments.hasOwnProperty(key)) {
          const argumentName = key;
          const argumentValue = funcArguments[key];
          params.push(new UDF.Param(argumentName, argumentValue));
        }
      }
      arrFuncs.push(new UDF.Item(funcName, params));
    }
    return arrFuncs;
  }
  parseConfigs(configs) {
    this.configs = configs;
    this.configs.sort((a, b) => a > b ? 1 : -1);
  }
  initSelectedConfigs() {
    this.configsSelections.clear();
    this.configs.forEach(c => {
      this.configsSelections.set(c.toLocaleLowerCase(), false);
    });
  }
  initSuitesList(suites) {
    this.suites = [];
    this.suites.push(SELECTE_SUITE);
    suites.forEach(s => {
      s = s.replace(".json", "");
      this.suites.push(s);
    });
    this.suites.sort((a, b) => a > b ? 1 : -1);
  }
  onSuiteSelected(event) {
    this.initSelectedConfigs();
    if (event.target.value == SELECTE_SUITE) {
      return;
    }
    let suite = event.target.value + ".json";
    let params = {
      'suite': suite
    };
    let url = '/new_report/get_suite';
    this.http.get(url, {
      params
    }).subscribe(configs => {
      configs.forEach(config => {
        config = config.toLocaleLowerCase();
        this.configsSelections.set(config, true);
      });
    });
  }
  isConfigSelected(config) {
    return this.configsSelections.get(config.toLocaleLowerCase());
  }
  configSelectionChanged(event, config) {
    this.configsSelections.set(config.toLocaleLowerCase(), event.target.checked);
    if (event.target.checked) this.showConfig(config);
  }
  saveSuite(suiteName) {
    let configs = [];
    this.configs.forEach(c => {
      let isChecked = this.configsSelections.get(c.toLocaleLowerCase());
      if (isChecked) configs.push(c);
    });
    let strConfigs = '';
    for (let i = 0; i < configs.length; i++) {
      if (strConfigs.length > 0) strConfigs += ",";
      strConfigs += configs[i];
    }
    this.http.post('/new_report/save_suite', {
      'suite': suiteName,
      'configurations': strConfigs
    }).subscribe(res => {
      this.initSuitesList(res);
      this.selectedSuite = suiteName;
    });
  }
  getSelectedSuiteName() {
    return this.selectedSuite;
  }
  openSaveSuiteDialog() {
    this.modalService.open(_save_suite_dialog_save_suite_dialog_component__WEBPACK_IMPORTED_MODULE_1__.SaveSuiteDialogComponent, {
      centered: true
    }).result.then(res => {});
  }
  closeSaveSuiteDialog() {
    this.modalService.dismissAll();
  }
  clearConfigViewer() {
    this.selectedPredictionReadingFunction = '';
    this.selectedGTReadingFunction = '';
    this.selectedTransformFunction = '';
    this.selectedPartitioningFunction = '';
    this.selectedStatisticsFunction = '';
    this.selectedConfusionFunction = '';
    this.selectedAssociationFunction = '';
    this.configName = '';
    this.logsFilter = _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFConstants.DEFAULT_LOG_FILTER;
    //clear param values
    this.udf.forEach((value, key) => {
      value.forEach(item => {
        item.params.forEach(p => {
          p.value = '';
        });
      });
    });
  }
  parseGetConfigResult(udfType, result) {
    if (result[udfType] != undefined) {
      let func = result[udfType].func_name;
      if (udfType == _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.READING_FUNCTIONS) this.selectedPredictionReadingFunction = func;
      if (udfType == _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.ASSOCIATION_FUNCTIONS) this.selectedAssociationFunction = func;
      if (udfType == _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.CONFUSION_FUNCTIONS) this.selectedConfusionFunction = func;
      if (udfType == _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.GT_READING_FUNCTIONS) this.selectedGTReadingFunction = func;
      if (udfType == _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.STATISTICS_FUNCTIONS) this.selectedStatisticsFunction = func;
      if (udfType == _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.TRANSFORM_FUNCTIONS) this.selectedTransformFunction = func;
      if (udfType == _common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.PARTITIONING_FUNCTIONS) this.selectedPartitioningFunction = func;
      let args = result[udfType].params;
      let udfItem = this.udf.get(udfType)?.find(x => x.funcName == func);
      if (udfItem != undefined) {
        udfItem.params.forEach(p => {
          p.value = args[p.name];
        });
      }
    }
  }
  showConfig(configName) {
    this.showParams = false;
    this.showConfigViewer = true;
    //get the confing from server
    let params = {
      'config': configName
    };
    let url = '/new_report/get_configuration';
    this.http.get(url, {
      params
    }).subscribe(config => {
      //clear the config viewer  
      this.clearConfigViewer();
      //show the new config in the viewer
      this.parseGetConfigResult(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.ASSOCIATION_FUNCTIONS, config);
      this.parseGetConfigResult(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.CONFUSION_FUNCTIONS, config);
      this.parseGetConfigResult(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.GT_READING_FUNCTIONS, config);
      this.parseGetConfigResult(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.PARTITIONING_FUNCTIONS, config);
      this.parseGetConfigResult(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.READING_FUNCTIONS, config);
      this.parseGetConfigResult(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.STATISTICS_FUNCTIONS, config);
      this.parseGetConfigResult(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.TRANSFORM_FUNCTIONS, config);
      this.configName = configName;
      this.logsFilter = config[_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.LOGS_NAME_TO_EVALUATE];
      this.evaluate_folders = config[_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.EVALUATE_FOLDERS];
      this.gtReadingSameAsPrediction = this.selectedGTReadingFunction == undefined || this.selectedGTReadingFunction == null || this.selectedGTReadingFunction == '' || this.selectedGTReadingFunction.toLowerCase() == 'none';
      this.transformEnabled = this.selectedTransformFunction != '' && this.selectedTransformFunction != undefined;
      this.partitioningEnabled = this.selectedPartitioningFunction != '' && this.selectedPartitioningFunction != undefined;
      this.associationEnabled = this.selectedAssociationFunction != '' && this.selectedAssociationFunction != undefined;
      this.isPanelOpen = false;
    });
  }
  addUdfToConfig(type, selectedFunc, dictionary) {
    let item = this.udf.get(type);
    let x = item?.find(x => x.funcName == selectedFunc);
    const paramsObj = {};
    if (x == undefined) return;
    for (let i = 0; i < x.params.length; i++) {
      let param = x.params[i];
      paramsObj[param.name] = param.value;
    }
    dictionary[type] = {
      'func_name': selectedFunc,
      'params': paramsObj
    };
  }
  saveConfig() {
    this.isBusy = true;
    this.showParams = false;
    this.newReportResult = new NewReportResult();
    const dictionary = {};
    this.addUdfToConfig(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.READING_FUNCTIONS, this.selectedPredictionReadingFunction, dictionary);
    if (!this.gtReadingSameAsPrediction && this.selectedGTReadingFunction.toLocaleLowerCase() != 'none') this.addUdfToConfig(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.GT_READING_FUNCTIONS, this.selectedGTReadingFunction, dictionary);
    if (this.transformEnabled) this.addUdfToConfig(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.TRANSFORM_FUNCTIONS, this.selectedTransformFunction, dictionary);
    if (this.partitioningEnabled) this.addUdfToConfig(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.PARTITIONING_FUNCTIONS, this.selectedPartitioningFunction, dictionary);
    this.addUdfToConfig(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.STATISTICS_FUNCTIONS, this.selectedStatisticsFunction, dictionary);
    this.addUdfToConfig(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.CONFUSION_FUNCTIONS, this.selectedConfusionFunction, dictionary);
    if (this.associationEnabled) this.addUdfToConfig(_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.ASSOCIATION_FUNCTIONS, this.selectedAssociationFunction, dictionary);
    dictionary[_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.CONFIG_NAME] = this.configName;
    dictionary[_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.LOGS_NAME_TO_EVALUATE] = this.logsFilter;
    dictionary[_common_enums__WEBPACK_IMPORTED_MODULE_2__.UDFTypeEnum.EVALUATE_FOLDERS] = this.evaluate_folders;
    const url = '/new_report/save_configuration';
    this.http.post(url, dictionary).subscribe(response => {
      this.isBusy = false;
      let configs;
      configs = response;
      this.configs = configs;
      this.configs.sort((a, b) => a > b ? 1 : -1);
      sweetalert2__WEBPACK_IMPORTED_MODULE_3___default().fire({
        text: 'Configuration saved successfully',
        timer: 3000,
        showConfirmButton: false,
        showCancelButton: false,
        backdrop: false,
        color: 'white',
        position: 'bottom',
        background: '#00CC00'
      });
    });
  }
  createReport() {
    this.isBusy = true;
    this.newReportResult = new NewReportResult();
    this.newReportResult.link = '';
    this.newReportResult.errorMessage = '';
    this.newReportResult.ok = false;
    let params = {
      'configurations': this.getSuiteConfigurations(this.selectedSuite),
      'suite_Name': this.selectedSuite == SELECTE_SUITE ? '' : this.selectedSuite,
      'predictions_directory': this.predictionsDirectory,
      'groundtruth_directory': this.groundTruthDirectory,
      'reporter_output_directory': this.reporterOutputDirectory
    };
    let url = '/new_report/calculating_page';
    this.http.get(url, {
      params
    }).subscribe(res => {
      this.isBusy = false;
      this.newReportResult.ok = res.ok;
      if (res.link != 'None' && res.link != undefined && res.link != null) this.newReportResult.link = res.link;else this.newReportResult.link = '';
      this.newReportResult.errorMessage = res.errorMessage;
      this.newReportResult.files = res.files;
      this.newReportResult.failed_with_error = res.failed_with_error;
      this.newReportResult.not_json_files = res.not_json_files;
      this.newReportResult.num_success_files = res.num_success_files;
      this.newReportResult.reading_function_skipped = res.reading_function_skipped;
      this.newReportResult.skipped_not_in_lognames = res.skipped_not_in_lognames;
    });
  }
  getSuiteConfigurations(suiteName) {
    let configs = [];
    for (let [key, value] of this.configsSelections) {
      if (value) {
        configs.push(key);
      }
    }
    return configs.join(",");
  }
  showResults() {
    if (this.newReportResult.ok && this.newReportResult.files.length > 0) return true;
    if (!this.newReportResult.ok && this.newReportResult.errorMessage != '') return true;
    return false;
  }
  getNumConfigsSelected() {
    //this.configsSelections
    let count = 0;
    for (const isSelected of this.configsSelections.values()) {
      if (isSelected) {
        count++;
      }
    }
    return count;
  }
  getUDFUserArguments(funcType, funcName) {
    let params = {
      'func_type': funcType,
      'func_name': funcName
    };
    let url = '/new_report/get_udf_user_arguments';
    this.http.get(url, {
      params
    }).subscribe(config => {
      this.udfArgumentsMap[funcType + "-" + funcName] = config;
      console.log('map', JSON.stringify(this.udfArgumentsMap));
    });
  }
  showArgumentsPanel(funcType, title, funcName) {
    let o = this.udf.get(funcType)?.find(x => x.funcName == funcName);
    if (o != undefined) {
      this.showArgumentsEvent.next({
        'funcType': funcType,
        'funcName': funcName,
        'udfItem': o,
        'title': title
      });
    }
  }
}
NewReportService.ɵfac = function NewReportService_Factory(t) {
  return new (t || NewReportService)(_angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_6__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵinject"](_ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_7__.NgbModal));
};
NewReportService.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵdefineInjectable"]({
  token: NewReportService,
  factory: NewReportService.ɵfac,
  providedIn: 'root'
});

/***/ }),

/***/ 4204:
/*!*****************************************************!*\
  !*** ./src/app/services/statistics-tool.service.ts ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SaveTemplateRequest": () => (/* binding */ SaveTemplateRequest),
/* harmony export */   "SaveTemplate_SegmentItem": () => (/* binding */ SaveTemplate_SegmentItem),
/* harmony export */   "SegmentationItem": () => (/* binding */ SegmentationItem),
/* harmony export */   "States": () => (/* binding */ States),
/* harmony export */   "StatisticsToolService": () => (/* binding */ StatisticsToolService),
/* harmony export */   "TemplateInfo": () => (/* binding */ TemplateInfo)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 228);
/* harmony import */ var _save_template_dialog_save_template_dialog_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../save-template-dialog/save-template-dialog.component */ 7897);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ng-bootstrap/ng-bootstrap */ 4534);





var States;
(function (States) {
  States[States["Close"] = 0] = "Close";
  States[States["Opened"] = 1] = "Opened";
  States[States["Open"] = 2] = "Open";
})(States || (States = {}));
class SegmentationItem {
  constructor() {
    this.name = '';
    this.columns = [];
    this.rows = [];
    this.openHorizontalSegmentation = States.Close;
    this.openVerticalSegmentation = States.Close;
    this.viewguid = StatisticsToolService.generateGUID();
  }
}
class TemplateInfo {
  constructor() {
    //wasChanged = false;
    this.Segmentations = [];
    this.SegmentationsClicked = [];
    this.name = '';
  }
}
class SaveTemplate_SegmentItem {
  constructor() {
    this.name = '';
    this.rows = '';
    this.columns = '';
  }
}
class SaveTemplateRequest {
  constructor() {
    this.name = '';
    this.segmentations = [];
  }
}
class StatisticsToolService {
  constructor(httpClient, modalService) {
    this.httpClient = httpClient;
    this.modalService = modalService;
    this.optionalSegmentations = new Map();
    this.segmentationsFetched = new rxjs__WEBPACK_IMPORTED_MODULE_1__.Subject();
    this.openDrawer = new rxjs__WEBPACK_IMPORTED_MODULE_1__.Subject();
    this.uniqueValueChanged = new rxjs__WEBPACK_IMPORTED_MODULE_1__.Subject();
    this.viewHeights = new Map();
    this.reportSelected = new rxjs__WEBPACK_IMPORTED_MODULE_1__.Subject();
    this.templates = [];
    this.currentTemplate = new TemplateInfo();
    this.calculateUnique = false;
    this.fileNotFoundError = '';
    this.templateNameOptions = [];
    this.selectedTamplate = 0;
    this.selectedReport = 0;
    this.showDrawer = false;
    this.drawerUpdateListUrl = '';
    this.drawerShowImageUrl = '';
    this.activeLocalDataStore = false;
    this.localDataStorePath = '';
    this.mainRefPairs = [];
    this.reportlistItems = [];
  }
  init(reportsPairs = '', selectedReport = 0) {
    if (reportsPairs != '') this.processReportsPairs(reportsPairs);
    this.templates = [];
    this.currentTemplate = new TemplateInfo();
    this.templateNameOptions = [];
    this.selectedTamplate = 0;
    let main = this.reportlistItems.find(x => x.key == selectedReport);
    let ref = this.mainRefPairs.find(x => x.main == main.value);
    let url = '/viewer/get_all_templates';
    this.httpClient.post(url, {
      'main_path': main.value,
      'ref_path': ref.ref
    }).subscribe(res => {
      this.processTemplates(res);
      this.updateTemplateNames();
      this.loadSegmentations(selectedReport);
    });
    this.readLocalDataStoreInfoFromStorage();
  }
  processReportsPairs(reportPairs) {
    if (reportPairs == '') return;
    this.mainRefPairs = JSON.parse(reportPairs);
    this.reportlistItems = [];
    let index = 0;
    this.mainRefPairs.forEach(pair => {
      this.reportlistItems.push({
        'key': index,
        'value': pair.main
      });
      index++;
    });
  }
  getReportDesc(reportfileName) {
    let parts = reportfileName.split(/[\\/]/);
    let dir = parts[parts.length - 2];
    let file = parts[parts.length - 1];
    return dir + "/" + file;
  }
  loadSegmentations(selectedReport = 0) {
    //get all optional segments
    let main = this.reportlistItems.find(x => x.key == selectedReport);
    this.optionalSegmentations = new Map();
    this.httpClient.post('/viewer/get_segmentations', {
      'main_path': main.value
    }).subscribe(res => {
      res.forEach(x => {
        this.optionalSegmentations.set(x.name, x.values);
      });
      this.segmentationsFetched.next(selectedReport);
    });
  }
  processTemplates(items) {
    this.addDefaultTemplate();
    items.forEach(x => {
      let c = JSON.parse(JSON.stringify(x.content));
      let t = new TemplateInfo();
      t.name = x.name;
      c.segmentations.forEach(s => {
        let seg = new SegmentationItem();
        seg.columns = s.columns.split(',');
        seg.rows = s.rows.split(',');
        seg.name = s.name;
        t.Segmentations.push(seg);
        t.SegmentationsClicked.push(true);
      });
      this.templates.push(t);
    });
  }
  updateTemplateNames() {
    this.templateNameOptions = [];
    for (let i = 0; i < this.templates.length; i++) {
      if (this.templates[i].name != '') this.templateNameOptions.push({
        'key': i,
        'value': this.templates[i].name
      });
    }
  }
  ngOnInit() {}
  onTemplateSelected(templateName) {
    this.currentTemplate = this.templates.find(x => x.name == templateName);
    let find = this.templateNameOptions.find(x => x.value == templateName);
    this.selectedTamplate = find.key;
  }
  updateSegments(id, templateName, csvColumns, csvRows) {
    let cols = csvColumns.split(",");
    let rows = csvRows.split(",");
    this.currentTemplate.Segmentations[id].columns = cols;
    this.currentTemplate.Segmentations[id].rows = rows;
  }
  updateSegmentationName(templateName, id, segName) {
    this.currentTemplate.Segmentations[id].name = segName;
  }
  addDefaultTemplate() {
    let t = this.templates.find(x => x.name == "");
    if (t == undefined) {
      t = new TemplateInfo();
    }
    t.name = "Default (Total)";
    let s = new SegmentationItem();
    s.name = 'Total';
    s.columns = [];
    s.rows = [];
    t.Segmentations.push(s);
    t.SegmentationsClicked.push(true);
    this.templates.push(t);
    this.currentTemplate = t;
  }
  addSegmentations() {
    //this.currentTemplate.wasChanged = true;
    this.currentTemplate.Segmentations.push(new SegmentationItem());
    this.currentTemplate.SegmentationsClicked.push(true);
  }
  saveTemplate(templateName) {
    let req = new SaveTemplateRequest();
    req.name = templateName;
    this.currentTemplate.Segmentations.forEach(s => {
      let seg = new SaveTemplate_SegmentItem();
      seg.columns = s.columns.join(",");
      seg.rows = s.rows.join(",");
      seg.name = s.name;
      req.segmentations.push(seg);
    });
    this.httpClient.post('/viewer/save_template', {
      'name': templateName,
      'content': JSON.stringify(req),
      'main_path': this.getSelectedMainReport(),
      'ref_path': this.getSelectedRefReport()
    }).subscribe(res => {
      this.templates = [];
      this.processTemplates(res);
      this.updateTemplateNames();
      this.onTemplateSelected(templateName);
    });
  }
  removeView(viewGuid) {
    let segments = [];
    for (let i = 0; i < this.currentTemplate.Segmentations.length; i++) {
      let item = this.currentTemplate.Segmentations[i];
      if (item.viewguid != viewGuid) {
        segments.push(item);
      }
    }
    this.currentTemplate.Segmentations = segments;
  }
  getDrawerUpdateListUrl() {
    return this.drawerUpdateListUrl;
  }
  getDrawerShowImageUrl() {
    return this.drawerShowImageUrl;
  }
  readLocalDataStoreInfoFromStorage() {
    this.localDataStorePath = localStorage.getItem('LOCAL_DATA_STORE');
    this.activeLocalDataStore = localStorage.getItem('ACTIVATE_LOCAL_DATA_STORE') == "true" ? true : false;
  }
  saveLocalDataStoreInfoInStorage() {
    localStorage.setItem('LOCAL_DATA_STORE', this.localDataStorePath);
    localStorage.setItem('ACTIVATE_LOCAL_DATA_STORE', this.activeLocalDataStore ? 'true' : 'false');
  }
  showFileNotFoundError() {
    return this.fileNotFoundError.length > 0;
  }
  getSelectedMainReport() {
    let main = this.reportlistItems[this.selectedReport];
    return main.value;
  }
  getSelectedRefReport() {
    let main = this.reportlistItems[this.selectedReport];
    let ref = this.mainRefPairs.find(x => x.main == main.value);
    if (ref != undefined) return ref.ref;
    return '';
  }
  openSaveTemplateDialog() {
    this.modalService.open(_save_template_dialog_save_template_dialog_component__WEBPACK_IMPORTED_MODULE_0__.SaveTemplateDialogComponent, {
      centered: true
    }).result.then(res => {});
  }
  closeSaveTempalteDialog() {
    this.modalService.dismissAll();
  }
  getSelectedTemplateName() {
    return this.templateNameOptions[this.selectedTamplate].value;
  }
  getView(guid) {
    for (let i = 0; i < this.currentTemplate.Segmentations.length; i++) {
      let v = this.currentTemplate.Segmentations[i];
      if (v.viewguid == guid) return v;
    }
    return null;
  }
  getDropdownState(viewGuid, segmentName) {
    let view = this.getView(viewGuid);
    if (view == null) return null;
    if (segmentName == "Horizontal Segmentation") {
      return view.openHorizontalSegmentation;
    } else {
      return view.openVerticalSegmentation;
    }
  }
  setDropdownState(viewGuid, segmentName, state) {
    let view = this.getView(viewGuid);
    if (view == null) return;
    if (segmentName == "Horizontal Segmentation") {
      view.openHorizontalSegmentation = state;
    } else {
      view.openVerticalSegmentation = state;
    }
  }
  static generateGUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : r & 0x3 | 0x8;
      return v.toString(16);
    });
  }
}
StatisticsToolService.ɵfac = function StatisticsToolService_Factory(t) {
  return new (t || StatisticsToolService)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_3__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵinject"](_ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_4__.NgbModal));
};
StatisticsToolService.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineInjectable"]({
  token: StatisticsToolService,
  factory: StatisticsToolService.ɵfac,
  providedIn: 'root'
});

/***/ }),

/***/ 2260:
/*!****************************************************************************!*\
  !*** ./src/app/template-segmentations/template-segmentations.component.ts ***!
  \****************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TemplateSegmentationsComponent": () => (/* binding */ TemplateSegmentationsComponent)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ 6078);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ 4666);




function TemplateSegmentationsComponent_option_8_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "option", 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const s_r3 = ctx.$implicit;
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpropertyInterpolate"]("value", s_r3.key);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate1"]("Report - ", ctx_r0.statService.getReportDesc(s_r3.value), "");
  }
}
function TemplateSegmentationsComponent_option_12_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "option", 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const t_r4 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpropertyInterpolate"]("value", t_r4.key);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](t_r4.value);
  }
}
const _c0 = function (a0) {
  return {
    "min-height": a0
  };
};
function TemplateSegmentationsComponent_ng_container_37_Template(rf, ctx) {
  if (rf & 1) {
    const _r8 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "button", 29);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function TemplateSegmentationsComponent_ng_container_37_Template_button_click_1_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r8);
      const i_r6 = restoredCtx.index;
      const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r7.clickPanel(i_r6));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "div", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](4, "pkl-view", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const x_r5 = ctx.$implicit;
    const i_r6 = ctx.index;
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r2.getActiveCls(i_r6));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate1"]("View - ", ctx_r2.getTitle(i_r6), " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](8, _c0, ctx_r2.getViewHeight(i_r6)));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("viewguid", x_r5.viewguid)("selectedRowsSet", x_r5.rows)("selectedColumnsSet", x_r5.columns)("name", x_r5.name)("id", i_r6);
  }
}
const _c1 = function (a0) {
  return {
    "margin-right": a0
  };
};
const _c2 = function (a0) {
  return {
    "margin-left": a0
  };
};
const _c3 = function (a0) {
  return {
    "cursor": a0
  };
};
const _c4 = function (a0) {
  return {
    "color": a0
  };
};
class TemplateSegmentationsComponent {
  constructor(statService, location) {
    this.statService = statService;
    this.location = location;
    this.isNewTemplateMode = true;
    this.templateNameCreated = '';
    this.backImgSrc = 'assets/back-icon-blue.svg';
    this.saveImgSrc = 'assets/save-icon-blue.svg';
    this.addGridImgSrc = 'assets/grid-add-blue.svg';
    this.subscribeSegmentsReady = new rxjs__WEBPACK_IMPORTED_MODULE_2__.Subscription();
  }
  ngOnInit() {
    this.subscribeSegmentsReady = this.statService.segmentationsFetched.subscribe(selectedReport => {
      this.statService.addDefaultTemplate();
      this.statService.selectedReport = selectedReport;
      this.statService.reportSelected.next(true);
    });
  }
  ngOnDestroy() {
    if (this.subscribeSegmentsReady != null) this.subscribeSegmentsReady.unsubscribe();
  }
  getViewHeight(index) {
    var isViewPanelOpen = this.statService.currentTemplate.SegmentationsClicked[index];
    if (isViewPanelOpen) return this.statService.viewHeights.get(index);else return '0px';
  }
  onTemplateSelected(event) {
    let tempalteId = event.target.value;
    this.isNewTemplateMode = false;
    this.templateNameCreated = '';
    let t = this.statService.templateNameOptions.find(x => x.key == +tempalteId);
    if (t != undefined) {
      this.statService.onTemplateSelected(t.value);
    }
  }
  onReportSelected(event) {
    this.statService.init('', event.target.value);
  }
  getTemplateName() {
    if (!this.isNewTemplateMode && this.statService.selectedTamplate > 0) {
      return this.statService.templateNameOptions.find(x => x.key == this.statService.selectedTamplate).value;
    }
    if (this.isNewTemplateMode && this.templateNameCreated.length > 0) {
      return this.templateNameCreated;
    }
    return '';
  }
  getTemplateNameForTitle() {
    let t = this.getTemplateName();
    if (t.length > 0) {
      return " - " + t.toLocaleUpperCase();
    }
    return '';
  }
  addView() {
    this.statService.addSegmentations();
  }
  saveTemplate() {
    this.statService.openSaveTemplateDialog();
  }
  slideUniqueChange(event) {
    this.statService.uniqueValueChanged.next(this.statService.calculateUnique);
  }
  slideLocalDataStore(event) {
    this.statService.saveLocalDataStoreInfoInStorage();
  }
  clickPanel(i) {
    for (let x = 0; x < this.statService.currentTemplate.SegmentationsClicked.length; x++) {
      if (x == i) {
        this.statService.currentTemplate.SegmentationsClicked[x] = !this.statService.currentTemplate.SegmentationsClicked[x];
      }
    }
  }
  getActiveCls(i) {
    if (this.statService.currentTemplate.SegmentationsClicked[i] == true) {
      return 'active';
    } else return '';
  }
  agentHas(keyword) {
    return navigator.userAgent.toLowerCase().search(keyword.toLowerCase()) > -1;
  }
  isFireFox() {
    return this.agentHas("Firefox") || this.agentHas("FxiOS") || this.agentHas("Focus");
  }
  getTitle(i) {
    return this.statService.currentTemplate.Segmentations[i].name;
  }
  back() {
    let path = this.location.path();
    console.log('path', path);
    if (path.indexOf('/static/') > 0) {
      path = path.replace('/static/', '/');
      console.log('path-remove-static', path);
    }
    window.location.href = 'http://127.0.0.1:5000/';
  }
  localDataStoreChange(event) {
    this.statService.saveLocalDataStoreInfoInStorage();
  }
  getLocalDataStoreCls() {
    if (this.statService.activeLocalDataStore) {
      return '';
    } else {
      return 'disableLocalDataStore';
    }
  }
  getSelectedMainReportTooltip() {
    if (this.statService.reportlistItems && this.statService.selectedReport in this.statService.reportlistItems) return this.statService.reportlistItems[this.statService.selectedReport].value;else return '';
  }
  getSelectedTemplateTooltip() {
    if (this.statService.templateNameOptions && this.statService.selectedTamplate in this.statService.templateNameOptions) return this.statService.templateNameOptions[this.statService.selectedTamplate].value;else return '';
  }
  disableUnique() {
    if (this.statService.getSelectedRefReport() == '') return true;
    return false;
  }
}
TemplateSegmentationsComponent.ɵfac = function TemplateSegmentationsComponent_Factory(t) {
  return new (t || TemplateSegmentationsComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_3__.Location));
};
TemplateSegmentationsComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: TemplateSegmentationsComponent,
  selectors: [["template-segmentations"]],
  decls: 38,
  vars: 31,
  consts: [[2, "width", "100%", "height", "50px", "border", "1px solid lightgray", "border-radius", "4px", "color", "#182a69", "background-color", "#E4F0F5", "position", "sticky", "z-index", "99999", "top", "0px"], [1, "template-selection", 2, "margin-left", "10px", "padding-top", "8px"], [2, "display", "flex", "width", "100%", "height", "40px"], [1, "back-icon", 2, "margin-top", "-2px", "width", "40px"], ["title", "Back", 1, "back", 2, "width", "33px", "height", "33px", "margin-top", "3px", "cursor", "pointer", 3, "src", "mouseover", "mouseout", "click"], [2, "width", "10%", "padding-top", "2px", 3, "ngStyle"], [2, "height", "29px", "width", "100%", "border-color", "lightgray", "border-radius", "3px", 3, "title", "ngModel", "ngModelChange", "change"], [3, "value", 4, "ngFor", "ngForOf"], [1, "pipe"], [2, "width", "10%", "padding-top", "2px", "margin-left", "3px"], [1, "save-icon", 2, "margin-top", "-1px", 3, "ngStyle"], ["title", "Add View", 2, "width", "40px", "height", "40px", "margin-top", "0px", "cursor", "pointer", 3, "src", "mouseover", "mouseout", "click"], ["title", "Save Template", 2, "width", "33px", "height", "33px", "margin-top", "3px", "cursor", "pointer", 3, "src", "mouseover", "mouseout", "click"], [1, "pipe", 2, "margin-right", "5px", "margin-left", "7px"], [2, "display", "flex", "padding-right", "3px"], [2, "margin-bottom", "-10px", "margin-left", "3px", "padding-top", "10px"], [1, "switch"], ["type", "checkbox", 3, "disabled", "ngModel", "ngModelChange", "change"], [1, "slider", "round", 3, "ngStyle"], [2, "margin-left", "5px", "padding-top", "5px"], [2, "font-weight", "bold", 3, "ngStyle"], [2, "display", "flex", "margin-left", "3px"], ["type", "checkbox", 3, "ngModel", "ngModelChange", "change"], [1, "slider", "round"], [2, "font-weight", "bold", "color", "#182a69"], ["type", "text", 2, "height", "27px", "margin", "5px", "margin-top", "3px !important", "width", "180px", "border", "1px solid lightgray", "border-radius", "3px", "outline", "none", 3, "ngModel", "ngClass", "readonly", "ngModelChange", "keyup"], [2, "margin-top", "0px"], [4, "ngFor", "ngForOf"], [3, "value"], [1, "collapsible", 2, "font-weight", "bold", 3, "ngClass", "click"], [1, "content", 3, "ngStyle"], [3, "viewguid", "selectedRowsSet", "selectedColumnsSet", "name", "id"]],
  template: function TemplateSegmentationsComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div")(1, "div", 0)(2, "div", 1)(3, "div", 2)(4, "div", 3)(5, "img", 4);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_Template_img_mouseover_5_listener() {
        return ctx.backImgSrc = "assets/back-icon-orange.svg";
      })("mouseout", function TemplateSegmentationsComponent_Template_img_mouseout_5_listener() {
        return ctx.backImgSrc = "assets/back-icon-blue.svg";
      })("click", function TemplateSegmentationsComponent_Template_img_click_5_listener() {
        return ctx.back();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](6, "div", 5)(7, "select", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_select_ngModelChange_7_listener($event) {
        return ctx.statService.selectedReport = $event;
      })("change", function TemplateSegmentationsComponent_Template_select_change_7_listener($event) {
        return ctx.onReportSelected($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](8, TemplateSegmentationsComponent_option_8_Template, 2, 2, "option", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](9, "div", 8);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](10, "div", 9)(11, "select", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_select_ngModelChange_11_listener($event) {
        return ctx.statService.selectedTamplate = $event;
      })("change", function TemplateSegmentationsComponent_Template_select_change_11_listener($event) {
        return ctx.onTemplateSelected($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](12, TemplateSegmentationsComponent_option_12_Template, 2, 2, "option", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](13, "div", 10)(14, "img", 11);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_Template_img_mouseover_14_listener() {
        return ctx.addGridImgSrc = "assets/grid-add-orange.svg";
      })("mouseout", function TemplateSegmentationsComponent_Template_img_mouseout_14_listener() {
        return ctx.addGridImgSrc = "assets/grid-add-blue.svg";
      })("click", function TemplateSegmentationsComponent_Template_img_click_14_listener() {
        return ctx.addView();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](15, "div", 10)(16, "img", 12);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_Template_img_mouseover_16_listener() {
        return ctx.saveImgSrc = "assets/save-icon-orange.svg";
      })("mouseout", function TemplateSegmentationsComponent_Template_img_mouseout_16_listener() {
        return ctx.saveImgSrc = "assets/save-icon-blue.svg";
      })("click", function TemplateSegmentationsComponent_Template_img_click_16_listener() {
        return ctx.saveTemplate();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](17, "div", 13);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](18, "div", 14)(19, "div", 15)(20, "label", 16)(21, "input", 17);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_input_ngModelChange_21_listener($event) {
        return ctx.statService.calculateUnique = $event;
      })("change", function TemplateSegmentationsComponent_Template_input_change_21_listener($event) {
        return ctx.slideUniqueChange($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](22, "span", 18);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](23, "div", 19)(24, "p", 20);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](25, "Unique");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](26, "div", 8);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](27, "div", 21)(28, "div", 15)(29, "label", 16)(30, "input", 22);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_input_ngModelChange_30_listener($event) {
        return ctx.statService.activeLocalDataStore = $event;
      })("change", function TemplateSegmentationsComponent_Template_input_change_30_listener($event) {
        return ctx.slideLocalDataStore($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](31, "span", 23);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](32, "div", 19)(33, "p", 24);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](34, "Local Store");
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](35, "input", 25);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_input_ngModelChange_35_listener($event) {
        return ctx.statService.localDataStorePath = $event;
      })("keyup", function TemplateSegmentationsComponent_Template_input_keyup_35_listener($event) {
        return ctx.localDataStoreChange($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](36, "div", 26);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](37, TemplateSegmentationsComponent_ng_container_37_Template, 5, 10, "ng-container", 27);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("src", ctx.backImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeUrl"]);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](21, _c1, ctx.isFireFox() ? "15px" : "5px"));
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("title", ctx.getSelectedMainReportTooltip())("ngModel", ctx.statService.selectedReport);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngForOf", ctx.statService.reportlistItems);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("title", ctx.getSelectedTemplateTooltip())("ngModel", ctx.statService.selectedTamplate);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngForOf", ctx.statService.templateNameOptions);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](23, _c2, ctx.isFireFox() ? "22px" : "12px"));
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("src", ctx.addGridImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeUrl"]);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](25, _c2, ctx.isFireFox() ? "10px" : "5px"));
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("src", ctx.saveImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeUrl"]);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("disabled", ctx.disableUnique())("ngModel", ctx.statService.calculateUnique);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](27, _c3, ctx.disableUnique() ? "none" : "pointer"));
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](29, _c4, ctx.disableUnique() ? "lightgray" : "#182a69"));
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](6);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx.statService.activeLocalDataStore);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx.statService.localDataStorePath)("ngClass", ctx.getLocalDataStoreCls())("readonly", ctx.statService.activeLocalDataStore == false);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngForOf", ctx.statService.currentTemplate.Segmentations);
    }
  },
  styles: [".template-selection .mat-grid-tile-content {\r\n  justify-content: center !important;\r\n}\r\n\r\n  .save-template .mat-grid-tile-content {\r\n  justify-content: left !important;\r\n}\r\n\r\n  .save-icon .mat-grid-tile-content {\r\n  justify-content: left !important;\r\n}\r\n\r\n  .back-icon .mat-grid-tile-content {\r\njustify-content: left !important;\r\n}\r\n\r\nselect[_ngcontent-%COMP%]:focus { \r\n  outline: none !important;\r\n}\r\n\r\ninput[_ngcontent-%COMP%]:focus { \r\n  outline: none !important;\r\n}\r\n\r\n  .mat-slide-toggle.mat-checked:not(.mat-disabled) .mat-slide-toggle-bar {\r\n  background-color: #182a69 !important;\r\n}\r\n  .mat-slide-toggle.mat-checked:not(.mat-disabled) .mat-slide-toggle-thumb {\r\n  background-color: #182a69 !important;\r\n}\r\n\r\n.collapsible[_ngcontent-%COMP%] {\r\n  background-color: #777;\r\n  color: white;\r\n  cursor: pointer;\r\n  padding: 4px;\r\n  width: 100%;\r\n  border: none;\r\n  text-align: left;\r\n  outline: none;\r\n  font-size: 15px;\r\n}\r\n\r\n.active[_ngcontent-%COMP%], .collapsible[_ngcontent-%COMP%]:hover {\r\n  background-color: #555;\r\n}\r\n\r\n.collapsible[_ngcontent-%COMP%]:after {\r\n  content: '\\002B';\r\n  color: white;\r\n  font-weight: bold;\r\n  float: right;\r\n  right:10px;\r\n  position: absolute;\r\n}\r\n\r\n.active[_ngcontent-%COMP%]:after {\r\n  content: \"\\2212\";\r\n}\r\n\r\n.content[_ngcontent-%COMP%] {\r\n  padding: 0 0px;\r\n  max-height: 0;\r\n  overflow: hidden;\r\n  transition: max-height 0.2s ease-out;\r\n  background-color: #f1f1f1;\r\n}\r\n\r\n.disabledImg[_ngcontent-%COMP%] {\r\nopacity:0.1;\r\npointer-events: none !important;\r\n}\r\n\r\n.back[_ngcontent-%COMP%]:hover {\r\nfill: #182a69;\r\n}\r\n.pipe[_ngcontent-%COMP%] {\r\nwidth: 1px;\r\nborder-left: 2px solid lightgray;\r\nheight: 40px;\r\nmargin-top: -2px;\r\n}\r\n\r\n.disableLocalDataStore[_ngcontent-%COMP%]{\r\nbackground-color:lightgray;\r\ncolor:gray;\r\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvdGVtcGxhdGUtc2VnbWVudGF0aW9ucy90ZW1wbGF0ZS1zZWdtZW50YXRpb25zLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxrQ0FBa0M7QUFDcEM7O0FBRUE7RUFDRSxnQ0FBZ0M7QUFDbEM7O0FBRUE7RUFDRSxnQ0FBZ0M7QUFDbEM7O0FBRUE7QUFDQSxnQ0FBZ0M7QUFDaEM7O0FBRUE7RUFDRSx3QkFBd0I7QUFDMUI7O0FBRUE7RUFDRSx3QkFBd0I7QUFDMUI7O0FBRUE7RUFDRSxvQ0FBb0M7QUFDdEM7QUFDQTtFQUNFLG9DQUFvQztBQUN0Qzs7QUFFQTtFQUNFLHNCQUFzQjtFQUN0QixZQUFZO0VBQ1osZUFBZTtFQUNmLFlBQVk7RUFDWixXQUFXO0VBQ1gsWUFBWTtFQUNaLGdCQUFnQjtFQUNoQixhQUFhO0VBQ2IsZUFBZTtBQUNqQjs7QUFFQTtFQUNFLHNCQUFzQjtBQUN4Qjs7QUFFQTtFQUNFLGdCQUFnQjtFQUNoQixZQUFZO0VBQ1osaUJBQWlCO0VBQ2pCLFlBQVk7RUFDWixVQUFVO0VBQ1Ysa0JBQWtCO0FBQ3BCOztBQUVBO0VBQ0UsZ0JBQWdCO0FBQ2xCOztBQUVBO0VBQ0UsY0FBYztFQUNkLGFBQWE7RUFDYixnQkFBZ0I7RUFDaEIsb0NBQW9DO0VBQ3BDLHlCQUF5QjtBQUMzQjs7QUFFQTtBQUNBLFdBQVc7QUFDWCwrQkFBK0I7QUFDL0I7O0FBRUE7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBLFVBQVU7QUFDVixnQ0FBZ0M7QUFDaEMsWUFBWTtBQUNaLGdCQUFnQjtBQUNoQjs7QUFFQTtBQUNBLDBCQUEwQjtBQUMxQixVQUFVO0FBQ1YiLCJzb3VyY2VzQ29udGVudCI6WyI6Om5nLWRlZXAgLnRlbXBsYXRlLXNlbGVjdGlvbiAubWF0LWdyaWQtdGlsZS1jb250ZW50IHtcclxuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlciAhaW1wb3J0YW50O1xyXG59XHJcblxyXG46Om5nLWRlZXAgLnNhdmUtdGVtcGxhdGUgLm1hdC1ncmlkLXRpbGUtY29udGVudCB7XHJcbiAganVzdGlmeS1jb250ZW50OiBsZWZ0ICFpbXBvcnRhbnQ7XHJcbn1cclxuXHJcbjo6bmctZGVlcCAuc2F2ZS1pY29uIC5tYXQtZ3JpZC10aWxlLWNvbnRlbnQge1xyXG4gIGp1c3RpZnktY29udGVudDogbGVmdCAhaW1wb3J0YW50O1xyXG59XHJcblxyXG46Om5nLWRlZXAgLmJhY2staWNvbiAubWF0LWdyaWQtdGlsZS1jb250ZW50IHtcclxuanVzdGlmeS1jb250ZW50OiBsZWZ0ICFpbXBvcnRhbnQ7XHJcbn1cclxuXHJcbnNlbGVjdDpmb2N1cyB7IFxyXG4gIG91dGxpbmU6IG5vbmUgIWltcG9ydGFudDtcclxufVxyXG5cclxuaW5wdXQ6Zm9jdXMgeyBcclxuICBvdXRsaW5lOiBub25lICFpbXBvcnRhbnQ7XHJcbn1cclxuXHJcbjo6bmctZGVlcCAubWF0LXNsaWRlLXRvZ2dsZS5tYXQtY2hlY2tlZDpub3QoLm1hdC1kaXNhYmxlZCkgLm1hdC1zbGlkZS10b2dnbGUtYmFyIHtcclxuICBiYWNrZ3JvdW5kLWNvbG9yOiAjMTgyYTY5ICFpbXBvcnRhbnQ7XHJcbn1cclxuOjpuZy1kZWVwIC5tYXQtc2xpZGUtdG9nZ2xlLm1hdC1jaGVja2VkOm5vdCgubWF0LWRpc2FibGVkKSAubWF0LXNsaWRlLXRvZ2dsZS10aHVtYiB7XHJcbiAgYmFja2dyb3VuZC1jb2xvcjogIzE4MmE2OSAhaW1wb3J0YW50O1xyXG59XHJcblxyXG4uY29sbGFwc2libGUge1xyXG4gIGJhY2tncm91bmQtY29sb3I6ICM3Nzc7XHJcbiAgY29sb3I6IHdoaXRlO1xyXG4gIGN1cnNvcjogcG9pbnRlcjtcclxuICBwYWRkaW5nOiA0cHg7XHJcbiAgd2lkdGg6IDEwMCU7XHJcbiAgYm9yZGVyOiBub25lO1xyXG4gIHRleHQtYWxpZ246IGxlZnQ7XHJcbiAgb3V0bGluZTogbm9uZTtcclxuICBmb250LXNpemU6IDE1cHg7XHJcbn1cclxuXHJcbi5hY3RpdmUsIC5jb2xsYXBzaWJsZTpob3ZlciB7XHJcbiAgYmFja2dyb3VuZC1jb2xvcjogIzU1NTtcclxufVxyXG5cclxuLmNvbGxhcHNpYmxlOmFmdGVyIHtcclxuICBjb250ZW50OiAnXFwwMDJCJztcclxuICBjb2xvcjogd2hpdGU7XHJcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XHJcbiAgZmxvYXQ6IHJpZ2h0O1xyXG4gIHJpZ2h0OjEwcHg7XHJcbiAgcG9zaXRpb246IGFic29sdXRlO1xyXG59XHJcblxyXG4uYWN0aXZlOmFmdGVyIHtcclxuICBjb250ZW50OiBcIlxcMjIxMlwiO1xyXG59XHJcblxyXG4uY29udGVudCB7XHJcbiAgcGFkZGluZzogMCAwcHg7XHJcbiAgbWF4LWhlaWdodDogMDtcclxuICBvdmVyZmxvdzogaGlkZGVuO1xyXG4gIHRyYW5zaXRpb246IG1heC1oZWlnaHQgMC4ycyBlYXNlLW91dDtcclxuICBiYWNrZ3JvdW5kLWNvbG9yOiAjZjFmMWYxO1xyXG59XHJcblxyXG4uZGlzYWJsZWRJbWcge1xyXG5vcGFjaXR5OjAuMTtcclxucG9pbnRlci1ldmVudHM6IG5vbmUgIWltcG9ydGFudDtcclxufVxyXG5cclxuLmJhY2s6aG92ZXIge1xyXG5maWxsOiAjMTgyYTY5O1xyXG59XHJcbi5waXBlIHtcclxud2lkdGg6IDFweDtcclxuYm9yZGVyLWxlZnQ6IDJweCBzb2xpZCBsaWdodGdyYXk7XHJcbmhlaWdodDogNDBweDtcclxubWFyZ2luLXRvcDogLTJweDtcclxufVxyXG5cclxuLmRpc2FibGVMb2NhbERhdGFTdG9yZXtcclxuYmFja2dyb3VuZC1jb2xvcjpsaWdodGdyYXk7XHJcbmNvbG9yOmdyYXk7XHJcbn0iXSwic291cmNlUm9vdCI6IiJ9 */"]
});

/***/ }),

/***/ 8621:
/*!********************************************************************************!*\
  !*** ./src/app/template-segments-header/template-segments-header.component.ts ***!
  \********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TemplateSegmentsHeaderComponent": () => (/* binding */ TemplateSegmentsHeaderComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_material_grid_list__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material/grid-list */ 2642);



class TemplateSegmentsHeaderComponent {
  constructor(statToolService) {
    this.statToolService = statToolService;
  }
  ngOnInit() {}
  ngDestroy() {}
}
TemplateSegmentsHeaderComponent.ɵfac = function TemplateSegmentsHeaderComponent_Factory(t) {
  return new (t || TemplateSegmentsHeaderComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService));
};
TemplateSegmentsHeaderComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: TemplateSegmentsHeaderComponent,
  selectors: [["template-segments-header"]],
  decls: 3,
  vars: 0,
  consts: [[2, "width", "100%", "height", "195px", "border", "1px solid lightgray", "border-radius", "4px", "color", "#182a69", "background-color", "#fafafa"], [1, "template-selection", 2, "width", "600px"], ["cols", "2", "rowHeight", "40px"]],
  template: function TemplateSegmentsHeaderComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 0)(1, "div", 1);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](2, "mat-grid-list", 2);
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    }
  },
  dependencies: [_angular_material_grid_list__WEBPACK_IMPORTED_MODULE_2__.MatGridList],
  styles: ["\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
});

/***/ }),

/***/ 7225:
/*!**************************!*\
  !*** ./src/app/utils.ts ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Utils": () => (/* binding */ Utils)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 2560);

class Utils {
  static sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
Utils.ɵfac = function Utils_Factory(t) {
  return new (t || Utils)();
};
Utils.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({
  token: Utils,
  factory: Utils.ɵfac,
  providedIn: 'root'
});

/***/ }),

/***/ 4431:
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser */ 4497);
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./app/app.module */ 6747);


_angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__.platformBrowser().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_0__.AppModule).catch(err => console.error(err));

/***/ })

},
/******/ __webpack_require__ => { // webpackRuntimeModules
/******/ var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
/******/ __webpack_require__.O(0, ["vendor"], () => (__webpack_exec__(4431)));
/******/ var __webpack_exports__ = __webpack_require__.O();
/******/ }
]);
//# sourceMappingURL=main.js.map