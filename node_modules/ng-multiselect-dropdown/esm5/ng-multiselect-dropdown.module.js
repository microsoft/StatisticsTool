import * as tslib_1 from "tslib";
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MultiSelectComponent } from './multiselect.component';
import { ClickOutsideDirective } from './click-outside.directive';
import { ListFilterPipe } from './list-filter.pipe';
var NgMultiSelectDropDownModule = /** @class */ (function () {
    function NgMultiSelectDropDownModule() {
    }
    NgMultiSelectDropDownModule_1 = NgMultiSelectDropDownModule;
    NgMultiSelectDropDownModule.forRoot = function () {
        return {
            ngModule: NgMultiSelectDropDownModule_1
        };
    };
    var NgMultiSelectDropDownModule_1;
    NgMultiSelectDropDownModule = NgMultiSelectDropDownModule_1 = tslib_1.__decorate([
        NgModule({
            imports: [CommonModule, FormsModule],
            declarations: [MultiSelectComponent, ClickOutsideDirective, ListFilterPipe],
            providers: [ListFilterPipe],
            exports: [MultiSelectComponent]
        })
    ], NgMultiSelectDropDownModule);
    return NgMultiSelectDropDownModule;
}());
export { NgMultiSelectDropDownModule };
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibmctbXVsdGlzZWxlY3QtZHJvcGRvd24ubW9kdWxlLmpzIiwic291cmNlUm9vdCI6Im5nOi8vbmctbXVsdGlzZWxlY3QtZHJvcGRvd24vIiwic291cmNlcyI6WyJuZy1tdWx0aXNlbGVjdC1kcm9wZG93bi5tb2R1bGUudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sRUFBRSxRQUFRLEVBQXVCLE1BQU0sZUFBZSxDQUFDO0FBQzlELE9BQU8sRUFBRSxZQUFZLEVBQUUsTUFBTSxpQkFBaUIsQ0FBQztBQUMvQyxPQUFPLEVBQUUsV0FBVyxFQUFFLE1BQU0sZ0JBQWdCLENBQUM7QUFDN0MsT0FBTyxFQUFFLG9CQUFvQixFQUFFLE1BQU0seUJBQXlCLENBQUM7QUFDL0QsT0FBTyxFQUFFLHFCQUFxQixFQUFFLE1BQU0sMkJBQTJCLENBQUM7QUFDbEUsT0FBTyxFQUFFLGNBQWMsRUFBRSxNQUFNLG9CQUFvQixDQUFDO0FBU3BEO0lBQUE7SUFNQSxDQUFDO29DQU5ZLDJCQUEyQjtJQUM3QixtQ0FBTyxHQUFkO1FBQ0UsT0FBTztZQUNMLFFBQVEsRUFBRSw2QkFBMkI7U0FDdEMsQ0FBQztJQUNKLENBQUM7O0lBTFEsMkJBQTJCO1FBUHZDLFFBQVEsQ0FBQztZQUNSLE9BQU8sRUFBRSxDQUFDLFlBQVksRUFBRSxXQUFXLENBQUM7WUFDcEMsWUFBWSxFQUFFLENBQUMsb0JBQW9CLEVBQUUscUJBQXFCLEVBQUUsY0FBYyxDQUFDO1lBQzNFLFNBQVMsRUFBRSxDQUFDLGNBQWMsQ0FBQztZQUMzQixPQUFPLEVBQUUsQ0FBQyxvQkFBb0IsQ0FBQztTQUNoQyxDQUFDO09BRVcsMkJBQTJCLENBTXZDO0lBQUQsa0NBQUM7Q0FBQSxBQU5ELElBTUM7U0FOWSwyQkFBMkIiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBOZ01vZHVsZSwgTW9kdWxlV2l0aFByb3ZpZGVycyB9IGZyb20gJ0Bhbmd1bGFyL2NvcmUnO1xuaW1wb3J0IHsgQ29tbW9uTW9kdWxlIH0gZnJvbSAnQGFuZ3VsYXIvY29tbW9uJztcbmltcG9ydCB7IEZvcm1zTW9kdWxlIH0gZnJvbSAnQGFuZ3VsYXIvZm9ybXMnO1xuaW1wb3J0IHsgTXVsdGlTZWxlY3RDb21wb25lbnQgfSBmcm9tICcuL211bHRpc2VsZWN0LmNvbXBvbmVudCc7XG5pbXBvcnQgeyBDbGlja091dHNpZGVEaXJlY3RpdmUgfSBmcm9tICcuL2NsaWNrLW91dHNpZGUuZGlyZWN0aXZlJztcbmltcG9ydCB7IExpc3RGaWx0ZXJQaXBlIH0gZnJvbSAnLi9saXN0LWZpbHRlci5waXBlJztcblxuQE5nTW9kdWxlKHtcbiAgaW1wb3J0czogW0NvbW1vbk1vZHVsZSwgRm9ybXNNb2R1bGVdLFxuICBkZWNsYXJhdGlvbnM6IFtNdWx0aVNlbGVjdENvbXBvbmVudCwgQ2xpY2tPdXRzaWRlRGlyZWN0aXZlLCBMaXN0RmlsdGVyUGlwZV0sXG4gIHByb3ZpZGVyczogW0xpc3RGaWx0ZXJQaXBlXSxcbiAgZXhwb3J0czogW011bHRpU2VsZWN0Q29tcG9uZW50XVxufSlcblxuZXhwb3J0IGNsYXNzIE5nTXVsdGlTZWxlY3REcm9wRG93bk1vZHVsZSB7XG4gICAgc3RhdGljIGZvclJvb3QoKTogTW9kdWxlV2l0aFByb3ZpZGVyczxOZ011bHRpU2VsZWN0RHJvcERvd25Nb2R1bGU+IHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIG5nTW9kdWxlOiBOZ011bHRpU2VsZWN0RHJvcERvd25Nb2R1bGVcbiAgICAgIH07XG4gICAgfVxufVxuIl19