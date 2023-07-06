import { Injectable } from "@angular/core";

export const PREDICTION_DIRECTORY      = 'PREDICTION_DIRECTORY';
export const GROUND_TRUTH_DIRECTORY    = 'GROUND_TRUTH_DIRECTORY';
export const OUTPUT_DIRECTORY          = 'OUTPUT_DIRECTORY';

@Injectable({
    providedIn: 'root'
})

export class LocalStorgeHelper {

    static data = new Map<string,string[]>();

    static addToList(listName:string,value:string){
        
        let arr = LocalStorgeHelper.data.get(listName);
        
        if (arr == null || arr == undefined)
            return;
        const lowerCaseItem = value.toLowerCase(); 

        if (arr.some((str) => str.toLowerCase() === lowerCaseItem)) {
            return; // Item already exists, return the array as is
        }

        const updatedArr = [...arr, value]; // Add the item to the array
        updatedArr.sort((a, b) => a.localeCompare(b)); // Sort the array

        LocalStorgeHelper.data.set(listName,updatedArr);
    }

    static loadAll(){
        LocalStorgeHelper.loadList(PREDICTION_DIRECTORY);
        LocalStorgeHelper.loadList(GROUND_TRUTH_DIRECTORY);
        LocalStorgeHelper.loadList(OUTPUT_DIRECTORY);
    }


    static loadList(listName:string){
        let item = localStorage.getItem(listName);
        if (item == null || item == undefined){
            LocalStorgeHelper.data.set(listName,[])    
            return;
        }

        let arrItems = item.split(";");
        arrItems.sort((a,b) =>  (a > b ? 1 : -1));
        LocalStorgeHelper.data.set(listName,arrItems);
    }

    static saveInLocaStorage(){
        LocalStorgeHelper.data.forEach((value,key) => {
            let str = value.join(";")
            localStorage.setItem(key,str);
        })
    }

    static getList(listName:string){
        return LocalStorgeHelper.data.get(listName);
    }
}