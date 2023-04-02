import * as tslib_1 from "tslib";
import { Pipe } from '@angular/core';
var ListFilterPipe = /** @class */ (function () {
    function ListFilterPipe() {
    }
    ListFilterPipe.prototype.transform = function (items, filter) {
        var _this = this;
        if (!items || !filter) {
            return items;
        }
        return items.filter(function (item) { return _this.applyFilter(item, filter); });
    };
    ListFilterPipe.prototype.applyFilter = function (item, filter) {
        if (typeof item.text === 'string' && typeof filter.text === 'string') {
            return !(filter.text && item.text && item.text.toLowerCase().indexOf(filter.text.toLowerCase()) === -1);
        }
        else {
            return !(filter.text && item.text && item.text.toString().toLowerCase().indexOf(filter.text.toString().toLowerCase()) === -1);
        }
    };
    ListFilterPipe = tslib_1.__decorate([
        Pipe({
            name: 'multiSelectFilter',
            pure: false
        })
    ], ListFilterPipe);
    return ListFilterPipe;
}());
export { ListFilterPipe };
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibGlzdC1maWx0ZXIucGlwZS5qcyIsInNvdXJjZVJvb3QiOiJuZzovL25nLW11bHRpc2VsZWN0LWRyb3Bkb3duLyIsInNvdXJjZXMiOlsibGlzdC1maWx0ZXIucGlwZS50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUEsT0FBTyxFQUFFLElBQUksRUFBaUIsTUFBTSxlQUFlLENBQUM7QUFRcEQ7SUFBQTtJQWVBLENBQUM7SUFkRyxrQ0FBUyxHQUFULFVBQVUsS0FBaUIsRUFBRSxNQUFnQjtRQUE3QyxpQkFLQztRQUpHLElBQUksQ0FBQyxLQUFLLElBQUksQ0FBQyxNQUFNLEVBQUU7WUFDbkIsT0FBTyxLQUFLLENBQUM7U0FDaEI7UUFDRCxPQUFPLEtBQUssQ0FBQyxNQUFNLENBQUMsVUFBQyxJQUFjLElBQUssT0FBQSxLQUFJLENBQUMsV0FBVyxDQUFDLElBQUksRUFBRSxNQUFNLENBQUMsRUFBOUIsQ0FBOEIsQ0FBQyxDQUFDO0lBQzVFLENBQUM7SUFFRCxvQ0FBVyxHQUFYLFVBQVksSUFBYyxFQUFFLE1BQWdCO1FBQ3hDLElBQUksT0FBTyxJQUFJLENBQUMsSUFBSSxLQUFLLFFBQVEsSUFBSSxPQUFPLE1BQU0sQ0FBQyxJQUFJLEtBQUssUUFBUSxFQUFFO1lBQ2xFLE9BQU8sQ0FBQyxDQUFDLE1BQU0sQ0FBQyxJQUFJLElBQUksSUFBSSxDQUFDLElBQUksSUFBSSxJQUFJLENBQUMsSUFBSSxDQUFDLFdBQVcsRUFBRSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsSUFBSSxDQUFDLFdBQVcsRUFBRSxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQztTQUMzRzthQUFNO1lBQ0gsT0FBTyxDQUFDLENBQUMsTUFBTSxDQUFDLElBQUksSUFBSSxJQUFJLENBQUMsSUFBSSxJQUFJLElBQUksQ0FBQyxJQUFJLENBQUMsUUFBUSxFQUFFLENBQUMsV0FBVyxFQUFFLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxJQUFJLENBQUMsUUFBUSxFQUFFLENBQUMsV0FBVyxFQUFFLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQyxDQUFDO1NBQ2pJO0lBQ0wsQ0FBQztJQWRRLGNBQWM7UUFKMUIsSUFBSSxDQUFDO1lBQ0YsSUFBSSxFQUFFLG1CQUFtQjtZQUN6QixJQUFJLEVBQUUsS0FBSztTQUNkLENBQUM7T0FDVyxjQUFjLENBZTFCO0lBQUQscUJBQUM7Q0FBQSxBQWZELElBZUM7U0FmWSxjQUFjIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgUGlwZSwgUGlwZVRyYW5zZm9ybSB9IGZyb20gJ0Bhbmd1bGFyL2NvcmUnO1xuXG5pbXBvcnQgeyBMaXN0SXRlbSB9IGZyb20gJy4vbXVsdGlzZWxlY3QubW9kZWwnO1xuXG5AUGlwZSh7XG4gICAgbmFtZTogJ211bHRpU2VsZWN0RmlsdGVyJyxcbiAgICBwdXJlOiBmYWxzZVxufSlcbmV4cG9ydCBjbGFzcyBMaXN0RmlsdGVyUGlwZSBpbXBsZW1lbnRzIFBpcGVUcmFuc2Zvcm0ge1xuICAgIHRyYW5zZm9ybShpdGVtczogTGlzdEl0ZW1bXSwgZmlsdGVyOiBMaXN0SXRlbSk6IExpc3RJdGVtW10ge1xuICAgICAgICBpZiAoIWl0ZW1zIHx8ICFmaWx0ZXIpIHtcbiAgICAgICAgICAgIHJldHVybiBpdGVtcztcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gaXRlbXMuZmlsdGVyKChpdGVtOiBMaXN0SXRlbSkgPT4gdGhpcy5hcHBseUZpbHRlcihpdGVtLCBmaWx0ZXIpKTtcbiAgICB9XG5cbiAgICBhcHBseUZpbHRlcihpdGVtOiBMaXN0SXRlbSwgZmlsdGVyOiBMaXN0SXRlbSk6IGJvb2xlYW4ge1xuICAgICAgICBpZiAodHlwZW9mIGl0ZW0udGV4dCA9PT0gJ3N0cmluZycgJiYgdHlwZW9mIGZpbHRlci50ZXh0ID09PSAnc3RyaW5nJykge1xuICAgICAgICAgICAgcmV0dXJuICEoZmlsdGVyLnRleHQgJiYgaXRlbS50ZXh0ICYmIGl0ZW0udGV4dC50b0xvd2VyQ2FzZSgpLmluZGV4T2YoZmlsdGVyLnRleHQudG9Mb3dlckNhc2UoKSkgPT09IC0xKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHJldHVybiAhKGZpbHRlci50ZXh0ICYmIGl0ZW0udGV4dCAmJiBpdGVtLnRleHQudG9TdHJpbmcoKS50b0xvd2VyQ2FzZSgpLmluZGV4T2YoZmlsdGVyLnRleHQudG9TdHJpbmcoKS50b0xvd2VyQ2FzZSgpKSA9PT0gLTEpO1xuICAgICAgICB9XG4gICAgfVxufVxuIl19