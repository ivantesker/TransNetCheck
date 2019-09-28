import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare const getCustomSuggestions: any;
declare const GetMap: any;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {

  constructor(private http: HttpClient) {

  }
  title = 'HackMap';

  ngOnInit() {
    this._getMap();
    this.getCustomSuggestions();
  }
  public getCustomSuggestions() {
    getCustomSuggestions();
  }

  public _getMap() {
    this.http.get('../data/info.json').subscribe((data) => GetMap(data));
  }

}
