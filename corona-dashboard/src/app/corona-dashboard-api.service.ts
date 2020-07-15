import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CoronaDashboardApiService {

  constructor(private _httpClient: HttpClient) {}

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json;charset=UTF-8',
      Accept: 'application/json'
    })
  };

  getUserLocation(zipcode){
    const payload  = JSON.stringify(zipcode);
    return this._httpClient.post('http://localhost:3000/getUserLocation', { zipcode: payload }, this.httpOptions).pipe( catchError(this.handleError));
  }

  getCaliDailyData(county){
    const payload  = JSON.stringify(county);
    return this._httpClient.post('http://localhost:3000/cali/getDailyData', { county: payload }, this.httpOptions).pipe( catchError(this.handleError));
  }

  getPlotMixedKind(data){
    const payload  = JSON.stringify(data);
    return this._httpClient.post('http://localhost:3000/cali/getMixedTotalKind', { data: payload }, this.httpOptions).pipe( catchError(this.handleError));
  }

  getPlotNewKind(data){
    const payload  = JSON.stringify(data);
    return this._httpClient.post('http://localhost:3000/cali/getPlotNewKind', { data: payload }, this.httpOptions).pipe( catchError(this.handleError));
  }

  getPlotTotalKind(data){
    const payload  = JSON.stringify(data);
    return this._httpClient.post('http://localhost:3000/cali/getPlotTotalKind', { data: payload }, this.httpOptions).pipe( catchError(this.handleError));
  }

  getTopCountriesData(data){
    const payload  = JSON.stringify(data);
    return this._httpClient.post('http://localhost:3000/world/getTopCountriesData', { data: payload }, this.httpOptions).pipe( catchError(this.handleError));
  }


  getWorldPlot(data){
    const payload  = JSON.stringify(data);
    return this._httpClient.post('http://localhost:3000/world/getWorldPlot', { data: payload }, this.httpOptions).pipe( catchError(this.handleError));
  }

  handleError(error: HttpErrorResponse){
    var temp = ['SERVE ERROR: Server not responding. Try again later.'];
    return temp;
  }
}
