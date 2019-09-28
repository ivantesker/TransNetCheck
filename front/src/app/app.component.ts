import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { startWith, map } from 'rxjs/operators';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
declare const GetMap: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(private http: HttpClient) {

  }
  title = 'HackMap';
  myControl = new FormControl();
  options: string[] = ['One', 'Two', 'Three'];
  filteredOptions: Observable<string[]>;

  ngOnInit() {
    this._getMap();

    this.filteredOptions = this.myControl.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value))
    );
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();
    if (filterValue === '') {
      return;
    } else {

      return this.options.filter(option => option.toLowerCase().indexOf(filterValue) === 0);
    }
  }

  private _getMap() {
    this.http.get('../data/info.json').subscribe((data) => GetMap(data));
  }
}

