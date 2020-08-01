import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { faWindowRestore } from '@fortawesome/free-solid-svg-icons';
import { faWindowMaximize } from '@fortawesome/free-solid-svg-icons';
import {MatSnackBar} from '@angular/material/snack-bar';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CoronaDashboardApiService } from '../corona-dashboard-api.service';

interface toggleForcasts {
  id: number;
  type: string;
}

@Component({
  selector: 'app-forecast-dashboard',
  templateUrl: './forecast-dashboard.component.html',
  styleUrls: ['./forecast-dashboard.component.css']
})
export class ForecastDashboardComponent implements OnInit {

  showCaliTab:boolean;
  showWorldTab:boolean;

  fa_Search = faSearch;
  fa_WindowRestore = faWindowRestore;
  fa_WindowMaximize = faWindowMaximize;

  forcastButtonToggle:toggleForcasts[];

  switchCountryPlot:toggleForcasts
  switchWorldPlot:toggleForcasts;
  switchWorldPlotDisplay:any;
  selectedCountry:string;

  showWorldForecast:boolean;
  countryForecastPlotLink:SafeResourceUrl;
  worldForecastFullPlotLink: SafeResourceUrl;
  worldForecastShortPlotLink: SafeResourceUrl;
  showCountryForecast:boolean;

  worldThresholdCI:string;
  worldThresholdDate:string;
  countryThresholdDate:string;

  constructor(private _apiService: CoronaDashboardApiService, private _snackBar: MatSnackBar, public _sanitizer: DomSanitizer) {

    this.forcastButtonToggle = [
      {id: 1234, type: 'Total Cases'},
      {id: 1235, type: 'Total Deaths'}
    ]

    this.worldThresholdCI = '';
    this.worldThresholdDate= '';
    this.countryThresholdDate = '';

    this.selectedCountry = 'United States';
    this.showCaliTab = false;
    this.showWorldTab = true;
    this.showWorldForecast = false;

    this.switchWorldPlot= this.forcastButtonToggle[0];
    this.showCountryForecast = false;

    this.switchCountryPlot = this.forcastButtonToggle[0];
    this.switchWorldPlotDisplay = this.fa_WindowMaximize;

    this.getWorldTabForecastPlots(this.switchWorldPlot,'World',1);
    this.getWorldTabForecastPlots(this.switchWorldPlot,this.selectedCountry,0);
   }

  ngOnInit(): void {
  }

  switchCountryForecast(user_country:string){
      var err = this._apiService.verifyCountry({'country': user_country });
      err.subscribe( data => {
        if (data['sucess'] == 501){
            this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
              panelClass: 'snack-bar',
              duration: 2500
            });
        }
        else if (data['sucess'] == 100){
            if (data['data']['python_code'] == 100) {
                this.selectedCountry = data['data']['country'];
                this.getWorldTabForecastPlots(this.switchCountryPlot , this.selectedCountry, 0)
            }
            else if (data['data']['python_code'] == 500) {
                this._snackBar.open( 'ERROR: Country doesn\t exit. Try again later.', 'Close', {
                  panelClass: 'snack-bar',
                  duration: 2500
                });
            }

        }
        else {
            this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
              panelClass: 'snack-bar',
              duration: 2500
            });
        }
      });
  }



  updateWorldPlotDisplay() {
    if (this.switchWorldPlotDisplay == this.fa_WindowMaximize) {
      this.switchWorldPlotDisplay = this.fa_WindowRestore;
    }
    else {
      this.switchWorldPlotDisplay = this.fa_WindowMaximize;
    }
  }

  updateCountryPlot() {
      let index = this.forcastButtonToggle.indexOf(this.switchCountryPlot)
      index == this.forcastButtonToggle.length -1 ? index = 0 : index++;
      this.switchCountryPlot = this.forcastButtonToggle[index];
      this.getWorldTabForecastPlots(this.switchCountryPlot,this.selectedCountry,0);
  }

  updateWorldPlot() {
    let index = this.forcastButtonToggle.indexOf(this.switchWorldPlot)
    index == this.forcastButtonToggle.length -1 ? index = 0 : index++;
    this.switchWorldPlot = this.forcastButtonToggle[index];
    this.getWorldTabForecastPlots(this.switchWorldPlot,'World',1);
  }

  getWorldTabForecastPlots(traceKind: toggleForcasts, country:string, dualDisplay:number){
     if (country == 'World'){
         this.showWorldForecast = false;
     } else{
         this.showCountryForecast = false;
     }

    var err = this._apiService.getCountryForecastPlots({'traceId': traceKind.id, 'dualDisplay': dualDisplay, 'country': country });
    err.subscribe( data => {
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
          if (country == 'world'){
              this.showWorldForecast = false;
          } else{
              this.showCountryForecast = false;
          }
      }
      else if (data['sucess'] == 100){

        if (country == 'World') {
            console.log(data['data'])
            this.worldForecastFullPlotLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Full Link']);
            this.worldForecastShortPlotLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Short Link']);

            this.worldThresholdCI = data['data']['Expected'];
            this.worldThresholdDate= data['data']['Expected Date']

            this.showWorldForecast = true;
        }
        else{
            this.countryForecastPlotLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Link']);
            this.countryThresholdDate = data['data']['Expected Date']
            this.showCountryForecast  = true
        }
      }
      else {
        this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
        if (country == 'world'){
            this.showWorldForecast = false;
        } else{
            this.showCountryForecast = false;
        }
      }
    });
  }

  changeForcastTab(tab:string) {
    if (tab == 'california') {
      this.showCaliTab = true;
      this.showWorldTab = false;
    } else if (tab == 'world') {
      this.showCaliTab = false;
      this.showWorldTab = true;
      this.getWorldTabForecastPlots(this.switchWorldPlot,'World',1);
      this.getWorldTabForecastPlots(this.switchWorldPlot,this.selectedCountry,0);
    }
  }
}
