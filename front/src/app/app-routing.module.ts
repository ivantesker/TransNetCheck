import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';
import { HomeComponent } from './home/home.component';


const routes: Routes = [];

@NgModule({
  imports: [RouterModule.forRoot([
    { path: '', pathMatch: 'full', redirectTo: '/home' },
    { path: 'home', component: HomeComponent },
    { path: 'map', component: MapComponent }
  ],
    {
      anchorScrolling: 'enabled'
    })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
