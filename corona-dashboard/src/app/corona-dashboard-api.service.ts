import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

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

  testAPIService(payload){
    console.log(payload);
    return this._httpClient.post( 'fsdfafa', payload).pipe( catchError(this.handleError));;
  }

  handleError(error: HttpErrorResponse){
    var temp = ['SERVE ERROR: Server not responding. Try again later.'];
    return temp;
  }
}
