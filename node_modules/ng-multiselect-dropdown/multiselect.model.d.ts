export interface IDropdownSettings {
    singleSelection?: boolean;
    idField?: string;
    textField?: string;
    tooltipField?: string;
    disabledField?: string;
    enableCheckAll?: boolean;
    selectAllText?: string;
    unSelectAllText?: string;
    allowSearchFilter?: boolean;
    clearSearchFilter?: boolean;
    maxHeight?: number;
    itemsShowLimit?: number;
    limitSelection?: number;
    searchPlaceholderText?: string;
    noDataAvailablePlaceholderText?: string;
    noFilteredDataAvailablePlaceholderText?: string;
    closeDropDownOnSelection?: boolean;
    showSelectedItemsAtTop?: boolean;
    defaultOpen?: boolean;
    allowRemoteDataSearch?: boolean;
}
export declare class ListItem {
    id: String | number;
    text: String | number;
    tooltip?: String | undefined;
    isDisabled?: boolean;
    constructor(source: any);
}
