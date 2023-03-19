import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatisticsToolService {

  segmentationsFetched = new Subject();

  //dictonary of segmentations, for example: size => ['large','small','medium']
  optionalSegmentations = new Map<string,string[]>();

  constructor() { }

  getSegmentations(){
    let keys:string[] = [];
    this.optionalSegmentations.forEach((v,k) => {
      keys.push(k)
    });

    return keys;
  }
}
