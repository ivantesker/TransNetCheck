import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare const getCitiesSuggestions: any;
declare const getSuggestionsOfStArrival: any;
declare const getSuggestionsOfTrainFlight: any;
declare const getSuggestionsOfStDeparture: any;
declare const flightRouteData: any;
declare const apiURL: any;
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
  operators = {
    beeline: false,
    megafon: false,
    mts_rus: false,
    tele2: false
  };
  trainFlightFrom = null;
  trainFlightTo = null;

  ngOnInit() {
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
    this.trainFlightFrom = null;
    this.trainFlightTo = null;
    for (const key in flightRouteData.arrayStDeparture) {
      if (flightRouteData.arrayStDeparture.hasOwnProperty(key)) {
        if (document.getElementById('stDeparture')['value'] === key) {
          this.trainFlightFrom = flightRouteData.arrayStDeparture[key];
          break;
        }
      }
    }
    for (const key in flightRouteData.arrayStArrival) {
      if (flightRouteData.arrayStArrival.hasOwnProperty(key)) {
        if (document.getElementById('stArrival')['value'] === key) {
          this.trainFlightTo = flightRouteData.arrayStArrival[key];
          break;
        }
      }
    }
    if (this.trainFlightFrom == null || this.trainFlightTo == null) {
      return;
    }
    getSuggestionsOfTrainFlight(this.trainFlightFrom.trim(), this.trainFlightTo.trim());
  }

  public addObjectsToMap() {
    let number = document.getElementById('trainFlight')['value'].split(' ')[0];
    let url = `${apiURL}/routes?start_point=${this.trainFlightFrom}&end_point=${this.trainFlightTo}&number=${number}`;
    this.http.put(url, this.operators)
      .subscribe((data) => {
        console.log(data);
        GetMap(data);
      });
  }
}
