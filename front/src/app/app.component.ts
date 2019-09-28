import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare const GetMap: any;
declare const getCustomSuggestions: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
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

