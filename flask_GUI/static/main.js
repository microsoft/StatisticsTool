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
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ 124);
/* harmony import */ var _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/sidenav */ 6643);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/platform-browser */ 4497);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./services/statistics-tool.service */ 4204);







class SafePipe {
  constructor(sanitizer, httpClient) {
    this.sanitizer = sanitizer;
    this.httpClient = httpClient;
  }
  transform(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
SafePipe.ɵfac = function SafePipe_Factory(t) {
  return new (t || SafePipe)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_platform_browser__WEBPACK_IMPORTED_MODULE_2__.DomSanitizer, 16), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_3__.HttpClient, 16));
};
SafePipe.ɵpipe = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefinePipe"]({
  name: "safe",
  type: SafePipe,
  pure: true
});
class AppComponent {
  onKeydownHandler(event) {
    console.log('keydown', event.key);
    if (event.key === "Escape") {
      this.statToolSvc.showDrawer = false;
    }
  }
  SampleFunction($event) {
    this.statToolSvc.openDrawer.next($event.data);
    let o = $event.data;
    console.log($event.data);
    if (o.action == 'update_list') {
      console.log('in update_list');
      this.statToolSvc.drawerUpdateListUrl = o.value + "&key=" + this.statToolSvc.currentConfigKey + "&sub_key=" + this.statToolSvc.getSelectedSubKey();
    }
    if (o.action == 'show_image') {
      console.log('in show_image', o.value);
      //check if path exists
      if (this.statToolSvc.activeLocalDataStore && this.statToolSvc.localDataStorePath.length > 0) {
        let filepath = this.getFilePath(o.value);
        this.httpClient.post('/is_file_exists', {
          'file_path': filepath
        }).subscribe(res => {
          console.log('getFilePath', 'result', res);
          if (res.exists) {
            let url = o.value + "&local_path=" + this.statToolSvc.localDataStorePath + "&key=" + this.statToolSvc.currentConfigKey + "&sub_key=" + this.statToolSvc.getSelectedSubKey();
            this.statToolSvc.drawerShowImageUrl = url;
          } else {
            this.statToolSvc.showDrawer = false;
            this.statToolSvc.fileNotFoundError = 'File ' + filepath + " not found!";
          }
        });
      } else {
        this.statToolSvc.drawerShowImageUrl = o.value + "&key=" + this.statToolSvc.currentConfigKey + "&sub_key=" + this.statToolSvc.getSelectedSubKey();
      }
    }
  }
  constructor(httpClient, router, statToolSvc, eltRef, appRef) {
    this.httpClient = httpClient;
    this.router = router;
    this.statToolSvc = statToolSvc;
    this.eltRef = eltRef;
    this.appRef = appRef;
    this.showFiller = false;
    this.config_key = '';
  }
  ngOnInit() {
    this.router.events.subscribe(event => {
      if (event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__.NavigationStart) {
        let sub_keys = new URLSearchParams(window.location.search).get('sub_keys')?.toString();
        let key = new URLSearchParams(window.location.search).get('root_key')?.toString();
        if (sub_keys == undefined) sub_keys = '';
        if (key == undefined) key = '';
        this.statToolSvc.currentConfigKey = key;
        this.statToolSvc.loadSubKeys(sub_keys);
        console.log('loadSubKeys', 'loaded');
        this.statToolSvc.init();
        console.log('root key:', key);
        console.log('sub keys:', sub_keys);
      }
    });
  }
  getFilePath(str) {
    let startIdx = str.indexOf('[');
    let endIdx = str.indexOf('.mp4');
    let path = str.slice(startIdx + 2, endIdx);
    path = path += ".mp4";
    if (this.statToolSvc.activeLocalDataStore && this.statToolSvc.localDataStorePath.length > 0) {
      path = this.statToolSvc.localDataStorePath + "\\" + path;
    }
    return path;
  }
}
AppComponent.ɵfac = function AppComponent_Factory(t) {
  return new (t || AppComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_3__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_4__.Router), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_1__.ElementRef), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_1__.ApplicationRef));
};
AppComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: AppComponent,
  selectors: [["app-root"]],
  viewQuery: function AppComponent_Query(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵviewQuery"](_angular_material_sidenav__WEBPACK_IMPORTED_MODULE_5__.MatSidenav, 5);
    }
    if (rf & 2) {
      let _t;
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵloadQuery"]()) && (ctx.drawer = _t.first);
    }
  },
  hostBindings: function AppComponent_HostBindings(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("keydown", function AppComponent_keydown_HostBindingHandler($event) {
        return ctx.onKeydownHandler($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresolveDocument"])("message", function AppComponent_message_HostBindingHandler($event) {
        return ctx.SampleFunction($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresolveWindow"]);
    }
  },
  inputs: {
    config_key: "config_key"
  },
  decls: 2,
  vars: 0,
  template: function AppComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "drawer")(1, "template-segmentations");
    }
  },
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
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/select */ 7371);
/* harmony import */ var _angular_material_grid_list__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/grid-list */ 2642);
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/radio */ 2922);
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/button */ 4522);
/* harmony import */ var _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/progress-spinner */ 1708);
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/platform-browser */ 4497);
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./app-routing.module */ 158);
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./app.component */ 5041);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _segmentations_segmentations_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./segmentations/segmentations.component */ 3696);
/* harmony import */ var _pkl_view_pkl_view_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./pkl-view/pkl-view.component */ 7092);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./services/statistics-tool.service */ 4204);
/* harmony import */ var ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ng-multiselect-dropdown */ 1664);
/* harmony import */ var _template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./template-segmentations/template-segmentations.component */ 2260);
/* harmony import */ var _template_segments_header_template_segments_header_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./template-segments-header/template-segments-header.component */ 8621);
/* harmony import */ var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/slide-toggle */ 4714);
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @angular/material/icon */ 7822);
/* harmony import */ var _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/sidenav */ 6643);
/* harmony import */ var _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @angular/material/toolbar */ 2543);
/* harmony import */ var _drawer_drawer_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./drawer/drawer.component */ 5220);
/* harmony import */ var _drawer_content_drawer_content_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./drawer-content/drawer-content.component */ 9765);
/* harmony import */ var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! @angular/material/expansion */ 7591);
/* harmony import */ var _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! @ng-bootstrap/ng-bootstrap */ 4534);
/* harmony import */ var _angular_localize_init__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/localize/init */ 6344);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/core */ 2560);




























class AppModule {}
AppModule.ɵfac = function AppModule_Factory(t) {
  return new (t || AppModule)();
};
AppModule.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_10__["ɵɵdefineNgModule"]({
  type: AppModule,
  bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_1__.AppComponent]
});
AppModule.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_10__["ɵɵdefineInjector"]({
  providers: [_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_4__.StatisticsToolService],
  imports: [ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_11__.NgMultiSelectDropDownModule.forRoot(), _angular_material_select__WEBPACK_IMPORTED_MODULE_12__.MatSelectModule, _angular_material_grid_list__WEBPACK_IMPORTED_MODULE_13__.MatGridListModule, _angular_material_radio__WEBPACK_IMPORTED_MODULE_14__.MatRadioModule, _angular_material_button__WEBPACK_IMPORTED_MODULE_15__.MatButtonModule, _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_16__.MatSlideToggleModule, _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_17__.MatProgressSpinnerModule, _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_18__.MatSidenavModule, _angular_platform_browser__WEBPACK_IMPORTED_MODULE_19__.BrowserModule, _app_routing_module__WEBPACK_IMPORTED_MODULE_0__.AppRoutingModule, _angular_common_http__WEBPACK_IMPORTED_MODULE_20__.HttpClientModule, _angular_forms__WEBPACK_IMPORTED_MODULE_21__.FormsModule, _angular_forms__WEBPACK_IMPORTED_MODULE_21__.ReactiveFormsModule, _angular_material_icon__WEBPACK_IMPORTED_MODULE_22__.MatIconModule, _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_23__.MatToolbarModule, _angular_material_expansion__WEBPACK_IMPORTED_MODULE_24__.MatExpansionModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_25__.NgbModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_25__.NgbAlertModule]
});
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_10__["ɵɵsetNgModuleScope"](AppModule, {
    declarations: [_app_component__WEBPACK_IMPORTED_MODULE_1__.AppComponent, _app_component__WEBPACK_IMPORTED_MODULE_1__.SafePipe, _segmentations_segmentations_component__WEBPACK_IMPORTED_MODULE_2__.SegmentationsComponent, _pkl_view_pkl_view_component__WEBPACK_IMPORTED_MODULE_3__.PklViewComponent, _template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_5__.TemplateSegmentationsComponent, _template_segments_header_template_segments_header_component__WEBPACK_IMPORTED_MODULE_6__.TemplateSegmentsHeaderComponent, _drawer_drawer_component__WEBPACK_IMPORTED_MODULE_7__.DrawerComponent, _drawer_content_drawer_content_component__WEBPACK_IMPORTED_MODULE_8__.DrawerContentComponent],
    imports: [ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_11__.NgMultiSelectDropDownModule, _angular_material_select__WEBPACK_IMPORTED_MODULE_12__.MatSelectModule, _angular_material_grid_list__WEBPACK_IMPORTED_MODULE_13__.MatGridListModule, _angular_material_radio__WEBPACK_IMPORTED_MODULE_14__.MatRadioModule, _angular_material_button__WEBPACK_IMPORTED_MODULE_15__.MatButtonModule, _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_16__.MatSlideToggleModule, _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_17__.MatProgressSpinnerModule, _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_18__.MatSidenavModule, _angular_platform_browser__WEBPACK_IMPORTED_MODULE_19__.BrowserModule, _app_routing_module__WEBPACK_IMPORTED_MODULE_0__.AppRoutingModule, _angular_common_http__WEBPACK_IMPORTED_MODULE_20__.HttpClientModule, _angular_forms__WEBPACK_IMPORTED_MODULE_21__.FormsModule, _angular_forms__WEBPACK_IMPORTED_MODULE_21__.ReactiveFormsModule, _angular_material_icon__WEBPACK_IMPORTED_MODULE_22__.MatIconModule, _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_23__.MatToolbarModule, _angular_material_expansion__WEBPACK_IMPORTED_MODULE_24__.MatExpansionModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_25__.NgbModule, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_25__.NgbAlertModule]
  });
})();
_angular_core__WEBPACK_IMPORTED_MODULE_10__["ɵɵsetComponentScope"](_app_component__WEBPACK_IMPORTED_MODULE_1__.AppComponent, function () {
  return [_template_segmentations_template_segmentations_component__WEBPACK_IMPORTED_MODULE_5__.TemplateSegmentationsComponent, _drawer_drawer_component__WEBPACK_IMPORTED_MODULE_7__.DrawerComponent];
}, []);

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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../app.component */ 5041);



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
  return new (t || DrawerContentComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService));
};
DrawerContentComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineComponent"]({
  type: DrawerContentComponent,
  selectors: [["drawer-content"]],
  hostBindings: function DrawerContentComponent_HostBindings(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("keydown", function DrawerContentComponent_keydown_HostBindingHandler($event) {
        return ctx.onKeydownHandler($event);
      }, false, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresolveDocument"]);
    }
  },
  decls: 10,
  vars: 6,
  consts: [[2, "height", "40px", "width", "100%", "display", "flex", "justify-content", "space-between", "direction", "rtl"], [2, "margin", "5px"], ["src", "assets/cancel-icon.svg", "title", "Close Drawer", 2, "height", "33px", "width", "33px", "position", "relative", "cursor", "pointer", 3, "click"], [2, "height", "100vh", "width", "100%", "display", "flex"], [2, "width", "60%", "height", "92%"], [2, "display", "block", "width", "100%", "height", "85%", "margin-top", "0px", "border", "none", 3, "src"], [2, "width", "40%", "height", "100vh", "min-width", "600px"], [2, "display", "block", "width", "100%", "height", "100vh", "margin-top", "0px", "border", "none", 3, "src"]],
  template: function DrawerContentComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "div", 0)(1, "div", 1)(2, "img", 2);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("click", function DrawerContentComponent_Template_img_click_2_listener() {
        return ctx.closeDrawer();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](3, "div", 3)(4, "div", 4);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](5, "iframe", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipe"](6, "safe");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](7, "div", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](8, "iframe", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipe"](9, "safe");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("src", _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipeBind1"](6, 2, ctx.statToolService.getDrawerUpdateListUrl()), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsanitizeResourceUrl"]);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("src", _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipeBind1"](9, 4, ctx.statToolService.getDrawerShowImageUrl()), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsanitizeResourceUrl"]);
    }
  },
  dependencies: [_app_component__WEBPACK_IMPORTED_MODULE_1__.SafePipe],
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
    this.statToolSvc.showDrawer = false; //!this.statToolSvc.showDrawer;
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
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @ng-bootstrap/ng-bootstrap */ 4534);
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
  constructor(httpClient, statToolService) {
    this.httpClient = httpClient;
    this.statToolService = statToolService;
    this.iframe = null;
    this.url = '/get_report_table';
    //subscribeGetSegment = new Subscription;
    this.selectedRows = '';
    this.selectedColumns = '';
    this.name = '';
    this.id = 0;
    this.loadCounter = 0;
    this.subscribeUniqueChange = new rxjs__WEBPACK_IMPORTED_MODULE_6__.Subscription();
    this.subscribeReportChanged = new rxjs__WEBPACK_IMPORTED_MODULE_6__.Subscription();
    this.height = '';
    this.url = '/get_report_table?calc_unique=' + statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
  }
  ngOnInit() {
    this.fixSelectedString();
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    this.loadCounter = 1;
    this.subscribeUniqueChange = this.statToolService.uniqueValueChanged.subscribe(res => {
      this.loadCounter = 1;
      this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    });
    this.subscribeReportChanged = this.statToolService.reportSelected.subscribe(res => {
      this.fixSelectedString();
      this.loadCounter = 1;
      let u = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
      this.url = u;
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
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
  }
  onAllColumnsAdded(items) {
    this.selectedColumns = '';
    items.forEach(x => {
      this.selectedColumns += x.item_id + ",";
    });
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
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
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
  }
  onAllColumnsRemoved(event) {
    this.selectedColumns = '';
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
  }
  onRowAdded(item) {
    if (this.selectedRows.length == 0) this.selectedRows = item.item_id;else this.selectedRows += "," + item.item_id;
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
  }
  onAllRowsAdded(items) {
    this.selectedRows = '';
    items.forEach(x => {
      this.selectedRows += x.item_id + ",";
    });
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
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
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
  }
  onAllRowsRemoved(event) {
    this.selectedRows = '';
    this.fixSelectedString();
    this.statToolService.updateSegments(this.id, this.name, this.selectedColumns, this.selectedRows);
    this.loadCounter = 1;
    this.url = '/get_report_table?cols=' + this.selectedColumns + "&rows=" + this.selectedRows + "&calc_unique=" + this.statToolService.calculateUnique + "&key=" + this.statToolService.currentConfigKey + "&sub_key=" + this.statToolService.getSelectedSubKey();
    ;
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
            //console.log('frame:::',this.id,h);
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
    this.statToolService.removeView(this.id);
  }
}
PklViewComponent.ɵfac = function PklViewComponent_Factory(t) {
  return new (t || PklViewComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵdirectiveInject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_7__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_2__.StatisticsToolService));
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
    selectedColumns: "selectedColumns",
    selectedColumnsSet: "selectedColumnsSet",
    name: "name",
    id: "id"
  },
  decls: 19,
  vars: 11,
  consts: [[1, "parent", 2, "border", "1px solid lightgray", "padding", "3px"], [4, "ngIf"], [1, "pkl-view-header", 2, "width", "99.6%", "padding", "3px", "border", "solid 1px lightgray", "border-radius", "4x !important", "margin-top", "3px", "color", "#182a69", "background-color", "#fafafa"], [2, "width", "100%"], [2, "width", "20%"], ["type", "text", "placeholder", "View Name", 1, "view-name", 2, "padding-left", "5px", "height", "38px", "width", "96%", "border", "1px solid #adadad", "border-radius", "3px", 3, "ngModel", "change"], [2, "width", "38%"], ["name", "Select Rows", 2, "width", "95%", "background-color", "white", 3, "selectItems", "segmentAdded", "segmentRemoved", "allSegmentsAdded", "allSegmentsRemoved"], ["name", "Selct Columns", 2, "width", "95%", "background-color", "white", "margin-top", "2px", 3, "selectItems", "segmentAdded", "segmentRemoved", "allSegmentsAdded", "allSegmentsRemoved"], [2, "text-align", "right"], ["src", "assets/cancel-icon.svg", "title", "Remove View", 2, "height", "33px", "width", "33px", "position", "relative", "cursor", "pointer", 3, "click"], [2, "display", "block", "width", "100%", "margin-top", "3px", "border", "none", 3, "src", "ngStyle", "load"], ["iframe", ""], ["style", "position: sticky;bottom: 200px;z-index: 99999999;", 4, "ngIf"], ["src", "assets/spinner-90-ring-with-bg.svg", 2, "width", "40px", "height", "40x"], [2, "position", "sticky", "bottom", "200px", "z-index", "99999999"], ["type", "danger", 3, "closed"]],
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
        return ctx.onRowAdded($event);
      })("segmentRemoved", function PklViewComponent_Template_segmentations_segmentRemoved_9_listener($event) {
        return ctx.onRowRemoved($event);
      })("allSegmentsAdded", function PklViewComponent_Template_segmentations_allSegmentsAdded_9_listener($event) {
        return ctx.onAllRowsAdded($event);
      })("allSegmentsRemoved", function PklViewComponent_Template_segmentations_allSegmentsRemoved_9_listener($event) {
        return ctx.onAllRowsRemoved($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵelementStart"](10, "td", 6)(11, "segmentations", 8);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵlistener"]("segmentAdded", function PklViewComponent_Template_segmentations_segmentAdded_11_listener($event) {
        return ctx.onColumnAdded($event);
      })("segmentRemoved", function PklViewComponent_Template_segmentations_segmentRemoved_11_listener($event) {
        return ctx.onColumnRemoved($event);
      })("allSegmentsAdded", function PklViewComponent_Template_segmentations_allSegmentsAdded_11_listener($event) {
        return ctx.onAllColumnsAdded($event);
      })("allSegmentsRemoved", function PklViewComponent_Template_segmentations_allSegmentsRemoved_11_listener($event) {
        return ctx.onAllColumnsRemoved($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵtext"](12, " > ");
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
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("selectItems", ctx.selectedRows);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](2);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("selectItems", ctx.selectedColumns);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](4);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("src", _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵpipeBind1"](17, 7, ctx.url), _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵsanitizeResourceUrl"])("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵpureFunction1"](9, _c1, ctx.height));
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_5__["ɵɵproperty"]("ngIf", ctx.statToolService.showFileNotFoundError());
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_8__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_8__.NgStyle, _angular_forms__WEBPACK_IMPORTED_MODULE_9__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_9__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_9__.NgModel, _ng_bootstrap_ng_bootstrap__WEBPACK_IMPORTED_MODULE_10__.NgbAlert, _segmentations_segmentations_component__WEBPACK_IMPORTED_MODULE_3__.SegmentationsComponent, _app_component__WEBPACK_IMPORTED_MODULE_4__.SafePipe],
  styles: [".multiselect-dropdown[_ngcontent-%COMP%] {\r\n  width: 96% !important;\r\n  margin:2px !important;\r\n  background-color: white !important;\r\n  border-color: lightgray;\r\n}\r\n.parent[_ngcontent-%COMP%]{\r\n  \r\n}\r\n.parent[_ngcontent-%COMP%]   img[_ngcontent-%COMP%]{\r\n  position: absolute;\r\n  top: 0;       \r\n  bottom: 0;    \r\n  left: 0;\r\n  right: 0;\r\n  margin:auto;\r\n}\r\n\r\n  .pkl-view-header .mat-grid-tile-content {\r\n  justify-content: left !important;\r\n}\r\n\r\n.caption[_ngcontent-%COMP%] {\r\n  padding-left: 3px;\r\n  font-weight: bold;\r\n}\r\n\r\n.view-name[_ngcontent-%COMP%]:focus {\r\n  outline: none;\r\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvcGtsLXZpZXcvcGtsLXZpZXcuY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLHFCQUFxQjtFQUNyQixxQkFBcUI7RUFDckIsa0NBQWtDO0VBQ2xDLHVCQUF1QjtBQUN6QjtBQUNBO0VBQ0Usc0JBQXNCO0FBQ3hCO0FBQ0E7RUFDRSxrQkFBa0I7RUFDbEIsTUFBTTtFQUNOLFNBQVM7RUFDVCxPQUFPO0VBQ1AsUUFBUTtFQUNSLFdBQVc7QUFDYjs7QUFFQTtFQUNFLGdDQUFnQztBQUNsQzs7QUFFQTtFQUNFLGlCQUFpQjtFQUNqQixpQkFBaUI7QUFDbkI7O0FBRUE7RUFDRSxhQUFhO0FBQ2YiLCJzb3VyY2VzQ29udGVudCI6WyIubXVsdGlzZWxlY3QtZHJvcGRvd24ge1xyXG4gIHdpZHRoOiA5NiUgIWltcG9ydGFudDtcclxuICBtYXJnaW46MnB4ICFpbXBvcnRhbnQ7XHJcbiAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGUgIWltcG9ydGFudDtcclxuICBib3JkZXItY29sb3I6IGxpZ2h0Z3JheTtcclxufVxyXG4ucGFyZW50e1xyXG4gIC8qcG9zaXRpb246IHJlbGF0aXZlOyovXHJcbn1cclxuLnBhcmVudCBpbWd7XHJcbiAgcG9zaXRpb246IGFic29sdXRlO1xyXG4gIHRvcDogMDsgICAgICAgXHJcbiAgYm90dG9tOiAwOyAgICBcclxuICBsZWZ0OiAwO1xyXG4gIHJpZ2h0OiAwO1xyXG4gIG1hcmdpbjphdXRvO1xyXG59XHJcblxyXG46Om5nLWRlZXAgLnBrbC12aWV3LWhlYWRlciAubWF0LWdyaWQtdGlsZS1jb250ZW50IHtcclxuICBqdXN0aWZ5LWNvbnRlbnQ6IGxlZnQgIWltcG9ydGFudDtcclxufVxyXG5cclxuLmNhcHRpb24ge1xyXG4gIHBhZGRpbmctbGVmdDogM3B4O1xyXG4gIGZvbnQtd2VpZ2h0OiBib2xkO1xyXG59XHJcblxyXG4udmlldy1uYW1lOmZvY3VzIHtcclxuICBvdXRsaW5lOiBub25lO1xyXG59XHJcblxyXG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ 6078);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ng-multiselect-dropdown */ 1664);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/forms */ 2508);








function SegmentationsComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r2 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div")(1, "ng-multiselect-dropdown", 1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_ngModelChange_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r2);
      const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r1.selected = $event);
    })("onSelect", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onSelect_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r2);
      const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r3.onItemSelect($event));
    })("onSelectAll", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onSelectAll_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r2);
      const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r4.onSelectAll($event));
    })("onDeSelect", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onDeSelect_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r2);
      const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r5.onUnSelect($event));
    })("onDeSelectAll", function SegmentationsComponent_div_0_Template_ng_multiselect_dropdown_onDeSelectAll_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r2);
      const ctx_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r6.onUnSelectAll($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("placeholder", ctx_r0.name)("settings", ctx_r0.dropdownSettings)("data", ctx_r0.dropdownList)("ngModel", ctx_r0.selected);
  }
}
class SegmentationsComponent {
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
    console.log('foo', 'items:', JSON.stringify(arr), 'selected:', JSON.stringify(this.selected));
  }
  constructor(statToolService, httpClient) {
    this.statToolService = statToolService;
    this.httpClient = httpClient;
    this.name = '';
    this.dropdownList = [];
    this.selected = [];
    this.dropdownSettings = {};
    this.subscribeSegmentationsFetched = new rxjs__WEBPACK_IMPORTED_MODULE_2__.Subscription();
    this.segmentAdded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__.EventEmitter();
    this.segmentRemoved = new _angular_core__WEBPACK_IMPORTED_MODULE_1__.EventEmitter();
    this.allSegmentsAdded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__.EventEmitter();
    this.allSegmentsRemoved = new _angular_core__WEBPACK_IMPORTED_MODULE_1__.EventEmitter();
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
  ngOnDestroy() {
    if (this.subscribeSegmentationsFetched != null) this.subscribeSegmentationsFetched.unsubscribe();
  }
}
SegmentationsComponent.ɵfac = function SegmentationsComponent_Factory(t) {
  return new (t || SegmentationsComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_3__.HttpClient));
};
SegmentationsComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
  type: SegmentationsComponent,
  selectors: [["segmentations"]],
  inputs: {
    selectItems: "selectItems",
    name: "name"
  },
  outputs: {
    segmentAdded: "segmentAdded",
    segmentRemoved: "segmentRemoved",
    allSegmentsAdded: "allSegmentsAdded",
    allSegmentsRemoved: "allSegmentsRemoved"
  },
  decls: 1,
  vars: 1,
  consts: [[4, "ngIf"], [3, "placeholder", "settings", "data", "ngModel", "ngModelChange", "onSelect", "onSelectAll", "onDeSelect", "onDeSelectAll"]],
  template: function SegmentationsComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](0, SegmentationsComponent_div_0_Template, 2, 4, "div", 0);
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx.dropdownList.length > 0);
    }
  },
  dependencies: [ng_multiselect_dropdown__WEBPACK_IMPORTED_MODULE_4__.MultiSelectComponent, _angular_common__WEBPACK_IMPORTED_MODULE_5__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_6__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_6__.NgModel],
  styles: ["\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
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
/* harmony export */   "StatisticsToolService": () => (/* binding */ StatisticsToolService),
/* harmony export */   "TemplateInfo": () => (/* binding */ TemplateInfo)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ 228);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ 8987);



class SegmentationItem {
  constructor() {
    this.name = '';
    this.columns = [];
    this.rows = [];
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
  constructor(httpClient) {
    this.httpClient = httpClient;
    this.optionalSegmentations = new Map();
    this.segmentationsFetched = new rxjs__WEBPACK_IMPORTED_MODULE_0__.Subject();
    this.openDrawer = new rxjs__WEBPACK_IMPORTED_MODULE_0__.Subject();
    this.uniqueValueChanged = new rxjs__WEBPACK_IMPORTED_MODULE_0__.Subject();
    this.viewHeights = new Map();
    this.reportSelected = new rxjs__WEBPACK_IMPORTED_MODULE_0__.Subject();
    this.templates = [];
    this.currentTemplate = new TemplateInfo();
    this.calculateUnique = false;
    this.fileNotFoundError = '';
    //templates = [{'key':0,'value':'--- select ---'},{'key':1,'value':'Template 1'},{'key':2,'value':'Template 2'},{'key':3,'value':'Template 3'}]
    this.templateNameOptions = [];
    this.selectedTamplate = 0;
    this.selectedSubKey = 0;
    this.showDrawer = false;
    this.drawerUpdateListUrl = '';
    this.drawerShowImageUrl = '';
    this.activeLocalDataStore = false;
    this.localDataStorePath = '';
    this.currentConfigKey = '';
    this.subKeys = [];
  }
  init(subKeySelected = 0) {
    this.templates = [];
    this.currentTemplate = new TemplateInfo();
    this.templateNameOptions = [];
    let url = '/get_all_templates';
    this.httpClient.post(url, {
      'key': this.currentConfigKey,
      'sub_key': this.getSelectedSubKey()
    }).subscribe(res => {
      this.processTemplates(res);
      this.updateTemplateNames();
      this.loadSegmentations(subKeySelected);
    });
    this.readLocalDataStoreInfoFromStorage();
  }
  loadSegmentations(subKeySelected = 0) {
    //get all optional segments
    this.optionalSegmentations = new Map();
    this.httpClient.post('/get_segmentations', {
      'key': this.currentConfigKey,
      'sub_key': this.subKeys[this.selectedSubKey].value
    }).subscribe(res => {
      res.forEach(x => {
        this.optionalSegmentations.set(x.name, x.values);
      });
      this.segmentationsFetched.next(subKeySelected);
    });
  }
  processTemplates(items) {
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
    this.templateNameOptions.push({
      'key': 0,
      'value': '--- New Template ---'
    });
    for (let i = 0; i < this.templates.length; i++) {
      if (this.templates[i].name != '') this.templateNameOptions.push({
        'key': i + 1,
        'value': this.templates[i].name
      });
    }
  }
  ngOnInit() {}
  getSegmentations() {
    /*let keys:string[] = [];
    this.optionalSegmentations.forEach((v,k) => {
      keys.push(k)
    });
          return keys;*/
    return '';
  }
  onTemplateSelected(templateName) {
    this.currentTemplate = this.templates.find(x => x.name == templateName);
  }
  getTemplateSegments(templateName, index, isRows) {
    /*let seg = this.mapTemplateSegments.get(templateName)!
    if (isRows)
      return seg[index].rows;
    else
      return seg[index].columns;*/
  }
  updateSegments(id, templateName, csvColumns, csvRows) {
    let cols = csvColumns.split(",");
    let rows = csvRows.split(",");
    this.currentTemplate.Segmentations[id].columns = cols;
    this.currentTemplate.Segmentations[id].rows = rows;
    //this.currentTemplate.wasChanged = true;
  }

  updateSegmentationName(templateName, id, segName) {
    this.currentTemplate.Segmentations[id].name = segName;
    //this.currentTemplate.wasChanged = true;
  }

  addNewTemplate() {
    let t = this.templates.find(x => x.name == "");
    if (t == undefined) {
      t = new TemplateInfo();
    }
    t.name = "";
    let s = new SegmentationItem();
    s.name = 'Total';
    s.columns = [];
    s.rows = [];
    t.Segmentations.push(s);
    t.SegmentationsClicked.push(true);
    this.templates.push(t);
    this.currentTemplate = t;
    console.log('addNewTemplate', JSON.stringify(this.templates), 'current:', JSON.stringify(this.currentTemplate));
  }
  addSegmentations() {
    //this.currentTemplate.wasChanged = true;
    this.currentTemplate.Segmentations.push(new SegmentationItem());
    this.currentTemplate.SegmentationsClicked.push(true);
  }
  saveTemplate(isNewTemplate, newTemplateName = '') {
    let template_name = this.currentTemplate.name;
    if (isNewTemplate) template_name = newTemplateName;
    let req = new SaveTemplateRequest();
    req.name = template_name;
    this.currentTemplate.Segmentations.forEach(s => {
      let seg = new SaveTemplate_SegmentItem();
      seg.columns = s.columns.join(",");
      seg.rows = s.rows.join(",");
      seg.name = s.name;
      req.segmentations.push(seg);
    });
    this.httpClient.post('/save_template', {
      'name': template_name,
      'content': JSON.stringify(req),
      'key': this.currentConfigKey,
      'sub_key': this.getSelectedSubKey()
    }).subscribe(res => {
      this.templates = [];
      this.processTemplates(res);
      this.updateTemplateNames();
      this.onTemplateSelected(template_name);
    });
  }
  removeView(viewId) {
    let segments = [];
    for (let i = 0; i < this.currentTemplate.Segmentations.length; i++) {
      let item = this.currentTemplate.Segmentations[i];
      if (i != viewId) {
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
  loadSubKeys(str) {
    this.subKeys = [];
    let items = str.split(",");
    let index = 0;
    items.forEach(s => {
      if (s != '') {
        this.subKeys.push({
          'key': index,
          'value': s
        });
        index++;
      }
    });
  }
  getSelectedSubKey() {
    return this.subKeys[this.selectedSubKey].value;
  }
}
StatisticsToolService.ɵfac = function StatisticsToolService_Factory(t) {
  return new (t || StatisticsToolService)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_2__.HttpClient));
};
StatisticsToolService.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"]({
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
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ 6078);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 2560);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ 8987);
/* harmony import */ var _services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../services/statistics-tool.service */ 4204);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common */ 4666);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ 124);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/forms */ 2508);
/* harmony import */ var _pkl_view_pkl_view_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../pkl-view/pkl-view.component */ 7092);








function TemplateSegmentationsComponent_ng_container_6_option_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "option", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const s_r10 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpropertyInterpolate"]("value", s_r10.key);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtextInterpolate1"]("Report - ", s_r10.value, "");
  }
}
function TemplateSegmentationsComponent_ng_container_6_Template(rf, ctx) {
  if (rf & 1) {
    const _r12 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "div", 22)(2, "select", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_ng_container_6_Template_select_ngModelChange_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r12);
      const ctx_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r11.statService.selectedSubKey = $event);
    })("change", function TemplateSegmentationsComponent_ng_container_6_Template_select_change_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r12);
      const ctx_r13 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r13.onSubKeySelected($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](3, TemplateSegmentationsComponent_ng_container_6_option_3_Template, 2, 2, "option", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx_r0.statService.selectedSubKey);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngForOf", ctx_r0.statService.subKeys);
  }
}
function TemplateSegmentationsComponent_ng_container_7_option_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "option", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const s_r15 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpropertyInterpolate"]("value", s_r15.key);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtextInterpolate1"]("Report - ", s_r15.value, "");
  }
}
function TemplateSegmentationsComponent_ng_container_7_Template(rf, ctx) {
  if (rf & 1) {
    const _r17 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "div", 24)(2, "select", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_ng_container_7_Template_select_ngModelChange_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r17);
      const ctx_r16 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r16.statService.selectedSubKey = $event);
    })("change", function TemplateSegmentationsComponent_ng_container_7_Template_select_change_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r17);
      const ctx_r18 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r18.onSubKeySelected($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](3, TemplateSegmentationsComponent_ng_container_7_option_3_Template, 2, 2, "option", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx_r1.statService.selectedSubKey);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngForOf", ctx_r1.statService.subKeys);
  }
}
function TemplateSegmentationsComponent_option_11_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "option", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const t_r19 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpropertyInterpolate"]("value", t_r19.key);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtextInterpolate"](t_r19.value);
  }
}
function TemplateSegmentationsComponent_ng_container_12_input_2_Template(rf, ctx) {
  if (rf & 1) {
    const _r23 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "input", 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_ng_container_12_input_2_Template_input_ngModelChange_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r23);
      const ctx_r22 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r22.templateNameCreated = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r20 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx_r20.templateNameCreated);
  }
}
function TemplateSegmentationsComponent_ng_container_12_input_3_Template(rf, ctx) {
  if (rf & 1) {
    const _r25 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "input", 29);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_ng_container_12_input_3_Template_input_ngModelChange_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r25);
      const ctx_r24 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r24.templateNameCreated = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r21 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx_r21.templateNameCreated);
  }
}
function TemplateSegmentationsComponent_ng_container_12_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "div", 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](2, TemplateSegmentationsComponent_ng_container_12_input_2_Template, 1, 1, "input", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](3, TemplateSegmentationsComponent_ng_container_12_input_3_Template, 1, 1, "input", 27);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", !ctx_r3.isFireFox());
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", ctx_r3.isFireFox());
  }
}
function TemplateSegmentationsComponent_ng_container_13_Template(rf, ctx) {
  if (rf & 1) {
    const _r27 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "div", 30)(2, "img", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_ng_container_13_Template_img_mouseover_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r27);
      const ctx_r26 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r26.addGridImgSrc = "assets/grid-add-orange.svg");
    })("mouseout", function TemplateSegmentationsComponent_ng_container_13_Template_img_mouseout_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r27);
      const ctx_r28 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r28.addGridImgSrc = "assets/grid-add-blue.svg");
    })("click", function TemplateSegmentationsComponent_ng_container_13_Template_img_click_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r27);
      const ctx_r29 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r29.addView());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("src", ctx_r4.addGridImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsanitizeUrl"]);
  }
}
function TemplateSegmentationsComponent_ng_container_14_Template(rf, ctx) {
  if (rf & 1) {
    const _r31 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "div", 32)(2, "img", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_ng_container_14_Template_img_mouseover_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r31);
      const ctx_r30 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r30.addGridImgSrc = "assets/grid-add-orange.svg");
    })("mouseout", function TemplateSegmentationsComponent_ng_container_14_Template_img_mouseout_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r31);
      const ctx_r32 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r32.addGridImgSrc = "assets/grid-add-blue.svg");
    })("click", function TemplateSegmentationsComponent_ng_container_14_Template_img_click_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r31);
      const ctx_r33 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r33.addView());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("src", ctx_r5.addGridImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsanitizeUrl"]);
  }
}
function TemplateSegmentationsComponent_ng_container_15_Template(rf, ctx) {
  if (rf & 1) {
    const _r35 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "div", 33)(2, "img", 34);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_ng_container_15_Template_img_mouseover_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r35);
      const ctx_r34 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r34.saveImgSrc = "assets/save-icon-orange.svg");
    })("mouseout", function TemplateSegmentationsComponent_ng_container_15_Template_img_mouseout_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r35);
      const ctx_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r36.saveImgSrc = "assets/save-icon-blue.svg");
    })("click", function TemplateSegmentationsComponent_ng_container_15_Template_img_click_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r35);
      const ctx_r37 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r37.saveTemplate());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngClass", ctx_r6.getDisabledClass());
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("src", ctx_r6.saveImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsanitizeUrl"]);
  }
}
function TemplateSegmentationsComponent_ng_container_16_Template(rf, ctx) {
  if (rf & 1) {
    const _r39 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "div", 35)(2, "img", 34);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_ng_container_16_Template_img_mouseover_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r39);
      const ctx_r38 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r38.saveImgSrc = "assets/save-icon-orange.svg");
    })("mouseout", function TemplateSegmentationsComponent_ng_container_16_Template_img_mouseout_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r39);
      const ctx_r40 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r40.saveImgSrc = "assets/save-icon-blue.svg");
    })("click", function TemplateSegmentationsComponent_ng_container_16_Template_img_click_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r39);
      const ctx_r41 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r41.saveTemplate());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngClass", ctx_r7.getDisabledClass());
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("src", ctx_r7.saveImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsanitizeUrl"]);
  }
}
const _c0 = function (a0) {
  return {
    "min-height": a0
  };
};
function TemplateSegmentationsComponent_ng_container_37_Template(rf, ctx) {
  if (rf & 1) {
    const _r45 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](1, "button", 36);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("click", function TemplateSegmentationsComponent_ng_container_37_Template_button_click_1_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r45);
      const i_r43 = restoredCtx.index;
      const ctx_r44 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r44.clickPanel(i_r43));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](3, "div", 37);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](4, "pkl-view", 38);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const x_r42 = ctx.$implicit;
    const i_r43 = ctx.index;
    const ctx_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngClass", ctx_r8.getActiveCls(i_r43));
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtextInterpolate1"]("View - ", ctx_r8.getTitle(i_r43), " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpureFunction1"](7, _c0, ctx_r8.getViewHeight(i_r43)));
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("selectedRowsSet", x_r42.rows)("selectedColumnsSet", x_r42.columns)("name", x_r42.name)("id", i_r43);
  }
}
class TemplateSegmentationsComponent {
  constructor(httpClient, statService, location, router) {
    this.httpClient = httpClient;
    this.statService = statService;
    this.location = location;
    this.router = router;
    this.isNewTemplateMode = true;
    this.templateNameCreated = '';
    this.backImgSrc = 'assets/back-icon-blue.svg';
    this.saveImgSrc = 'assets/save-icon-blue.svg';
    this.addGridImgSrc = 'assets/grid-add-blue.svg';
    this.subscribeSegmentsReady = new rxjs__WEBPACK_IMPORTED_MODULE_3__.Subscription();
  }
  ngOnInit() {
    /*let sub = this.statService.segmentationsFetched.subscribe(res => {
      
      sub.unsubscribe();
    })*/
    this.subscribeSegmentsReady = this.statService.segmentationsFetched.subscribe(selectedSubKey => {
      this.statService.addNewTemplate();
      this.statService.selectedSubKey = selectedSubKey;
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
    if (tempalteId == 0) {
      //new temmplate
      this.isNewTemplateMode = true;
      //this.statService.templates = [];
      if (this.statService.templates.length == 0) this.statService.addNewTemplate();
      return;
    }
    this.isNewTemplateMode = false;
    this.templateNameCreated = '';
    let t = this.statService.templateNameOptions.find(x => x.key == +tempalteId);
    if (t != undefined) {
      this.statService.onTemplateSelected(t.value);
    }
  }
  onSubKeySelected(event) {
    this.statService.init(event.target.value);
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
    if (this.isNewTemplateMode) this.statService.saveTemplate(true, this.templateNameCreated);else this.statService.saveTemplate(false);
  }
  slideUniqueChange(event) {
    //console.log('slideUniqueChange',event.checked)
    //this.statService.calculateUnique = event.checked;
    //this.statService.uniqueValueChanged.next(event.checked);
    this.statService.uniqueValueChanged.next(this.statService.calculateUnique);
  }
  slideLocalDataStore(event) {
    this.statService.saveLocalDataStoreInfoInStorage();
  }
  clickPanel(i) {
    for (let x = 0; x < this.statService.currentTemplate.SegmentationsClicked.length; x++) {
      if (x == i) {
        this.statService.currentTemplate.SegmentationsClicked[x] = !this.statService.currentTemplate.SegmentationsClicked[x];
        /*console.log('view-clicked',
                    i,
                    this.statService.currentTemplate.SegmentationsClicked[x],
                    this.statService.viewHeights.get(x)
        );*/
      }
      //else
      //this.statService.currentTemplate.SegmentationsClicked[x] = false;
      //console.log('clicked - false',i,this.statService.currentTemplate.SegmentationsClicked[x]);
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
  getHeight_deprecated(i) {
    if (this.statService.currentTemplate.SegmentationsClicked[i] == true) {
      let segments = this.statService.currentTemplate.Segmentations[i];
      let numRows = 1;
      segments.rows.forEach(r => {
        if (r != '') {
          let values = this.statService.optionalSegmentations.get(r);
          numRows = numRows * values.length;
        }
      });
      let lineHeight = 22;
      let tableHeight = numRows * 8 * lineHeight;
      //if (this.statService.calculateUnique == false)
      //  tableHeight = numRows * 7 * 22; 
      let totalHeight = 0;
      const segmentRowHeight = 40;
      const segmentsFilterRowHeight = 70;
      const viewTitleHeight = 40;
      if (segments.columns.length == 0) totalHeight = tableHeight + segmentRowHeight + segmentsFilterRowHeight + viewTitleHeight;else totalHeight = tableHeight + segments.columns.length * segmentRowHeight + segmentsFilterRowHeight + viewTitleHeight;
      const bufferHeight = 20;
      let height = totalHeight + bufferHeight;
      return height;
    } else return 0;
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
  getDisabledClass() {
    if (this.isNewTemplateMode) {
      if (this.templateNameCreated.length == 0) return 'disabledImg';
    }
    return '';
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
}
TemplateSegmentationsComponent.ɵfac = function TemplateSegmentationsComponent_Factory(t) {
  return new (t || TemplateSegmentationsComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_services_statistics_tool_service__WEBPACK_IMPORTED_MODULE_0__.StatisticsToolService), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_5__.Location), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_6__.Router));
};
TemplateSegmentationsComponent.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineComponent"]({
  type: TemplateSegmentationsComponent,
  selectors: [["template-segmentations"]],
  decls: 38,
  vars: 16,
  consts: [[2, "width", "100%", "height", "50px", "border", "1px solid lightgray", "border-radius", "4px", "color", "#182a69", "background-color", "#E4F0F5", "position", "sticky", "z-index", "99999", "top", "0px"], [1, "template-selection", 2, "margin-left", "10px", "padding-top", "8px"], [2, "display", "flex", "width", "100%", "height", "40px"], [1, "back-icon", 2, "margin-top", "-2px", "width", "40px"], ["title", "Back", 1, "back", 2, "width", "33px", "height", "33px", "margin-top", "3px", "cursor", "pointer", 3, "src", "mouseover", "mouseout", "click"], [4, "ngIf"], [1, "pipe"], [2, "width", "10%", "padding-top", "2px", "margin-left", "3px"], [2, "height", "29px", "width", "100%", "border-color", "lightgray", "border-radius", "3px", 3, "ngModel", "ngModelChange", "change"], [3, "value", 4, "ngFor", "ngForOf"], [1, "pipe", 2, "margin-right", "5px", "margin-left", "7px"], [2, "display", "flex", "padding-right", "3px"], [2, "margin-bottom", "-10px", "margin-left", "3px", "padding-top", "10px"], [1, "switch"], ["type", "checkbox", 3, "ngModel", "ngModelChange", "change"], [1, "slider", "round"], [2, "margin-left", "5px", "padding-top", "5px"], [2, "font-weight", "bold", "color", "#182a69"], [2, "display", "flex", "margin-left", "3px"], ["type", "text", 2, "height", "27px", "margin", "5px", "margin-top", "3px !important", "width", "180px", "border", "1px solid lightgray", "border-radius", "3px", "outline", "none", 3, "ngModel", "ngClass", "readonly", "ngModelChange", "keyup"], [2, "margin-top", "0px"], [4, "ngFor", "ngForOf"], [2, "width", "10%", "padding-top", "2px", "margin-right", "5px"], [3, "value"], [2, "width", "10%", "padding-top", "2px", "margin-right", "15px"], [2, "width", "10%", "padding-top", "2px", "margin-left", "4px"], ["type", "text", "placeholder", "Template Name", "style", "height:27px;width:100%;border:1px solid lightgray;border-radius: 3px;padding-left: 3px;", 3, "ngModel", "ngModelChange", 4, "ngIf"], ["type", "text", "placeholder", "Template Name", "style", "height:30px;width:100%;border:1px solid lightgray;border-radius: 3px;padding-left: 3px;margin-left: 11px;", 3, "ngModel", "ngModelChange", 4, "ngIf"], ["type", "text", "placeholder", "Template Name", 2, "height", "27px", "width", "100%", "border", "1px solid lightgray", "border-radius", "3px", "padding-left", "3px", 3, "ngModel", "ngModelChange"], ["type", "text", "placeholder", "Template Name", 2, "height", "30px", "width", "100%", "border", "1px solid lightgray", "border-radius", "3px", "padding-left", "3px", "margin-left", "11px", 3, "ngModel", "ngModelChange"], [1, "save-icon", 2, "margin-left", "12px", "margin-top", "-1px"], ["title", "Add View", 2, "width", "40px", "height", "40px", "margin-top", "0px", "cursor", "pointer", 3, "src", "mouseover", "mouseout", "click"], [1, "save-icon", 2, "margin-left", "22px", "margin-top", "-1px"], [1, "save-icon", 2, "margin-left", "5px", "margin-top", "-1px", 3, "ngClass"], ["title", "Save Template", 2, "width", "33px", "height", "33px", "margin-top", "3px", "cursor", "pointer", 3, "src", "mouseover", "mouseout", "click"], [1, "save-icon", 2, "margin-top", "-1px", "margin-left", "10px", 3, "ngClass"], [1, "collapsible", 2, "font-weight", "bold", 3, "ngClass", "click"], [1, "content", 3, "ngStyle"], [3, "selectedRowsSet", "selectedColumnsSet", "name", "id"]],
  template: function TemplateSegmentationsComponent_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "div")(1, "div", 0)(2, "div", 1)(3, "div", 2)(4, "div", 3)(5, "img", 4);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("mouseover", function TemplateSegmentationsComponent_Template_img_mouseover_5_listener() {
        return ctx.backImgSrc = "assets/back-icon-orange.svg";
      })("mouseout", function TemplateSegmentationsComponent_Template_img_mouseout_5_listener() {
        return ctx.backImgSrc = "assets/back-icon-blue.svg";
      })("click", function TemplateSegmentationsComponent_Template_img_click_5_listener() {
        return ctx.back();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](6, TemplateSegmentationsComponent_ng_container_6_Template, 4, 2, "ng-container", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](7, TemplateSegmentationsComponent_ng_container_7_Template, 4, 2, "ng-container", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](8, "div", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](9, "div", 7)(10, "select", 8);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_select_ngModelChange_10_listener($event) {
        return ctx.statService.selectedTamplate = $event;
      })("change", function TemplateSegmentationsComponent_Template_select_change_10_listener($event) {
        return ctx.onTemplateSelected($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](11, TemplateSegmentationsComponent_option_11_Template, 2, 2, "option", 9);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](12, TemplateSegmentationsComponent_ng_container_12_Template, 4, 2, "ng-container", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](13, TemplateSegmentationsComponent_ng_container_13_Template, 3, 1, "ng-container", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](14, TemplateSegmentationsComponent_ng_container_14_Template, 3, 1, "ng-container", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](15, TemplateSegmentationsComponent_ng_container_15_Template, 3, 2, "ng-container", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](16, TemplateSegmentationsComponent_ng_container_16_Template, 3, 2, "ng-container", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](17, "div", 10);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](18, "div", 11)(19, "div", 12)(20, "label", 13)(21, "input", 14);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_input_ngModelChange_21_listener($event) {
        return ctx.statService.calculateUnique = $event;
      })("change", function TemplateSegmentationsComponent_Template_input_change_21_listener($event) {
        return ctx.slideUniqueChange($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](22, "span", 15);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](23, "div", 16)(24, "p", 17);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](25, "Unique");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](26, "div", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](27, "div", 18)(28, "div", 12)(29, "label", 13)(30, "input", 14);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_input_ngModelChange_30_listener($event) {
        return ctx.statService.activeLocalDataStore = $event;
      })("change", function TemplateSegmentationsComponent_Template_input_change_30_listener($event) {
        return ctx.slideLocalDataStore($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](31, "span", 15);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](32, "div", 16)(33, "p", 17);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](34, "Local Store");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](35, "input", 19);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ngModelChange", function TemplateSegmentationsComponent_Template_input_ngModelChange_35_listener($event) {
        return ctx.statService.localDataStorePath = $event;
      })("keyup", function TemplateSegmentationsComponent_Template_input_keyup_35_listener($event) {
        return ctx.localDataStoreChange($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()()()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](36, "div", 20);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](37, TemplateSegmentationsComponent_ng_container_37_Template, 5, 9, "ng-container", 21);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("src", ctx.backImgSrc, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsanitizeUrl"]);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", !ctx.isFireFox());
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", ctx.isFireFox());
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](3);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx.statService.selectedTamplate);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngForOf", ctx.statService.templateNameOptions);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", ctx.isNewTemplateMode);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", !ctx.isFireFox());
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", ctx.isFireFox());
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", !ctx.isFireFox());
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", ctx.isFireFox());
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx.statService.calculateUnique);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](9);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx.statService.activeLocalDataStore);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx.statService.localDataStorePath)("ngClass", ctx.getLocalDataStoreCls())("readonly", ctx.statService.activeLocalDataStore == false);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](2);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngForOf", ctx.statService.currentTemplate.Segmentations);
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_5__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_5__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_5__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_5__.NgStyle, _angular_forms__WEBPACK_IMPORTED_MODULE_7__.NgSelectOption, _angular_forms__WEBPACK_IMPORTED_MODULE_7__["ɵNgSelectMultipleOption"], _angular_forms__WEBPACK_IMPORTED_MODULE_7__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_7__.CheckboxControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_7__.SelectControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_7__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_7__.NgModel, _pkl_view_pkl_view_component__WEBPACK_IMPORTED_MODULE_1__.PklViewComponent],
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