import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare const getCitiesSuggestions: any;
declare const getSuggestionsOfStArrival: any;
declare const getSuggestionsOfTrainFlight: any;
declare const getSuggestionsOfStDeparture: any;
declare const flightRouteData: any;
declare const GetMap: any;
declare const AddObjectsToMap: any;

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
    this.initMap();

    this.getCustomSuggestions();
  }
  public async getCustomSuggestions() {
    getCitiesSuggestions();
  }

  public selectFromCityInput() {
    const fromCityInput = document.getElementById('fromCity')['value'];
    if (fromCityInput === '') {
      return;
    }
    getSuggestionsOfStDeparture(fromCityInput.trim());
  }

  public selectToCityInput() {
    const toCityInput = document.getElementById('toCity')['value'];
    if (toCityInput === '') {
      return;
    }
    getSuggestionsOfStArrival(toCityInput.trim());
  }
  public async selectTrainFlight() {
    let trainFlightFrom = null;
    let trainFlightTo = null;
    for (const key in flightRouteData.arrayStDeparture) {
      if (flightRouteData.arrayStDeparture.hasOwnProperty(key)) {
        if (document.getElementById('stDeparture')['value'] === key) {
          trainFlightFrom = flightRouteData.arrayStDeparture[key];
          break;
        }
      }
    }
    for (const key in flightRouteData.arrayStArrival) {
      if (flightRouteData.arrayStArrival.hasOwnProperty(key)) {
        if (document.getElementById('stArrival')['value'] === key) {
          trainFlightTo = flightRouteData.arrayStArrival[key];
          break;
        }
      }
    }
    if (trainFlightFrom == null || trainFlightTo == null) {
      return;
    }
    getSuggestionsOfTrainFlight(trainFlightFrom.trim(), trainFlightTo.trim());
  }
  public initMap() {
    GetMap();
  }
  public addObjectsToMap() {
    this.http.get('../data/info.json').subscribe((data) => AddObjectsToMap(data));
  }

}
