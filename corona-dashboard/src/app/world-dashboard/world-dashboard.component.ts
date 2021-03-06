import { Component, OnInit } from '@angular/core';
import { CoronaDashboardApiService } from '../corona-dashboard-api.service';
import { faChevronUp } from '@fortawesome/free-solid-svg-icons';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import {MatSnackBar} from '@angular/material/snack-bar';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

interface plotDropDowns {
  id: number;
  name: string;
}

interface plotTimelineButton{
  id: number;
  name: string;
  selected: boolean;
}

interface topCountryData {
  country: string;
  description: string;
  percentage: number;
  total: number;
}


@Component({
  selector: 'app-world-dashboard',
  templateUrl: './world-dashboard.component.html',
  styleUrls: ['./world-dashboard.component.css']
})
export class WorldDashboardComponent implements OnInit {

  fa_SortUp = faChevronUp;
  fa_SortDown = faChevronDown;
  fa_Search = faSearch;

  worldPlotTraceDropdown: plotDropDowns[];
  worldPlotTraceDropdownSelected: plotDropDowns;
  showWorldPlot: boolean;
  worldPlotLink:SafeResourceUrl;
  worldPlotTimeline: plotTimelineButton[];

  topCountriesTraceDropdown: plotDropDowns[];
  topCountriesTraceDropdownSelected: plotDropDowns;
  topCountriesData: topCountryData[];
  showTopCountriesData:boolean;

  topCountriesTracePlotDropdown: plotDropDowns[];
  topCountriesTracePlotDropdownSelected: plotDropDowns;
  showTopCountriesPlot:boolean;
  topCountriesPlotTimeline: plotTimelineButton[];
  topCountriesPlotLink: SafeResourceUrl;

  countryTracePlotDropdown:plotDropDowns[];
  countryTracePlotDropdownSelected: plotDropDowns;
  showCountryPlot:boolean;
  countryPlotTimeline:plotTimelineButton[];
  countryPlotLink: SafeResourceUrl;

  countryData:any;
  countryName:string;
  userInputCountry:string;

  constructor(private _apiService: CoronaDashboardApiService, private _snackBar: MatSnackBar, public _sanitizer: DomSanitizer) {

    this.countryName = '';


    this.countryTracePlotDropdown = [
      {id: 9100, name: 'New Cases'},
      {id: 9200, name: 'New Death'},
      {id: 9300, name: 'Total Cases'},
      {id: 9400, name: 'Total Deaths'},
    ]
    this.countryTracePlotDropdownSelected = this.countryTracePlotDropdown[0];
    this.showCountryPlot = false;
    this.countryPlotTimeline = [
      {id: 501, name: '2 Weeks', selected: true},
      {id: 502, name: 'Month', selected: false},
      {id: 503, name: '3 Months', selected: false},
      {id: 504, name: 'All', selected: false},
    ]

    this.topCountriesTracePlotDropdown = [
      {id: 7100, name: 'New Cases'},
      {id: 7200, name: 'New Death'},
      {id: 7300, name: 'Total Cases'},
      {id: 7400, name: 'Total Deaths'},
    ]
    this.topCountriesTracePlotDropdownSelected = this.topCountriesTracePlotDropdown[0];
    this.showTopCountriesPlot = false;
    this.topCountriesPlotTimeline = [
      {id: 501, name: '2 Weeks', selected: true},
      {id: 502, name: 'Month', selected: false},
      {id: 503, name: '3 Months', selected: false},
      {id: 504, name: 'All', selected: false},
    ]

    this.topCountriesData = [];
    this.topCountriesTraceDropdown = [
      {id: 2100, name: 'New Cases (Today)'},
      {id: 2200, name: 'New Cases'},
      {id: 2500, name: 'New Deaths (Today)'},
      {id: 2600, name: 'New Deaths'},
      {id: 2300, name: 'Total Cases'},
      {id: 2400, name: 'Total Deaths'}
    ]
    this.topCountriesTraceDropdownSelected = this.topCountriesTraceDropdown[0];
    this.showTopCountriesData = false;


    this.worldPlotTraceDropdown = [
      {id: 1100, name: 'New Cases'},
      {id: 1200, name: 'New Deaths'},
      {id: 1300, name: 'Total Cases'},
      {id: 1400, name: 'Total Deaths'}
    ]
    this.worldPlotTraceDropdownSelected = this.worldPlotTraceDropdown[0];
    this.showWorldPlot = false;
    this.worldPlotTimeline = [
      {id: 501, name: '2 Weeks', selected: true},
      {id: 502, name: 'Month', selected: false},
      {id: 503, name: '3 Months', selected: false},
      {id: 504, name: 'All', selected: false},
    ]

    this.updateWorldPlot(this.worldPlotTraceDropdownSelected,this.worldPlotTimeline)
    this.updateTopCountriesPlot(this.topCountriesTracePlotDropdownSelected, this.topCountriesPlotTimeline)
    this.updateTopCountriesData(this.topCountriesTraceDropdownSelected);
    this.getCountryData('United States')
   }

  ngOnInit(): void {
  }


  updateCountryPlotTimeline(country:string, buttonId:number, buttonList:plotTimelineButton[], plotKindTrace: plotDropDowns){
    var updatePlotFlag = false;
    for (let x in buttonList){
      if (buttonList[x]['id'] == buttonId && buttonList[x]['selected'] == false ){
          buttonList[x]['selected'] = true;
          updatePlotFlag = true;
      }
      else if (buttonList[x]['selected'] == true && buttonList[x]['id'] != buttonId){
        buttonList[x]['selected'] = false;
      }
    }
    if (updatePlotFlag){
        this.updateCountryPlot(country, plotKindTrace, buttonList)
    }
  }

  updateCountryPlot(country:string, plotKindTrace: plotDropDowns, plotTimeline:plotTimelineButton[]) { 
      this.showCountryPlot = false;
      var updatedPlotTimeline = -1;
      for (let x in plotTimeline){
        if (plotTimeline[x]['selected'] == true ){
            updatedPlotTimeline = plotTimeline[x]['id']
        }
      }
      console.log(updatedPlotTimeline)
      console.log(country)
      console.log(plotKindTrace)
      
      var err = this._apiService.getCountryPlot({'traceId': plotKindTrace.id, 'timelineId': updatedPlotTimeline, 'country': this.countryName });
      err.subscribe( data => { 
        console.log(data)
        if (data['sucess'] == 501){
            this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
              panelClass: 'snack-bar',
              duration: 2500
            });
            this.showCountryPlot = false;
        }
        else if (data['sucess'] == 100){
          console.log(data['data']['Plot Link'])
          this.countryPlotLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Link']);
          this.showCountryPlot = true;
        }
        else {
          this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
          this.showCountryPlot = false;
        }
      });



  }

  getCountryData(country) {
    console.log(country)

    this.showCountryPlot = false;
      var updatedPlotTimeline = -1;
      for (let x in this.topCountriesPlotTimeline){
        if (this.topCountriesPlotTimeline[x]['selected'] == true ){
            updatedPlotTimeline = this.topCountriesPlotTimeline[x]['id']
        }
      }

    var err = this._apiService.getCountryData({'country': country, 'traceId': this.countryTracePlotDropdownSelected.id, 'timelineId': 501 });
    err.subscribe( data => { 
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
      }
      else if (data['sucess'] == 100){
        if (data['data']['python_code'] == 501){
          this._snackBar.open( 'ERROR: Please enter a real country.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
        }
        else {
          this.countryData = data['data']['country_data'];
          this.countryName = data['data']['country']
          this.userInputCountry=undefined;
          this.countryPlotLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['plot_link']);
          console.log({'testing1213': this.countryPlotLink})
          console.log({'testing1234':this.countryData })
          this.countryPlotTimeline = [
            {id: 501, name: '2 Weeks', selected: true},
            {id: 502, name: 'Month', selected: false},
            {id: 503, name: '3 Months', selected: false},
            {id: 504, name: 'All', selected: false},
          ]
          this.showCountryPlot = true;

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

  updateTopCountriesData(traceKind:plotDropDowns){
    this.showTopCountriesData = false;
    this.topCountriesData = []
    var err = this._apiService.getTopCountriesData({'plotTraceId': traceKind.id, 'numLimit': 8 });
    err.subscribe( data => { 
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
          this.showTopCountriesData = false;
      }
      else if (data['sucess'] == 100){
        var temp2 = (data['data']['Top Countries Data']['topCountriesData'])
        for (let country of temp2){
          var temp: topCountryData;
          temp = {
            country: country['country'],
            description: country['description'],
            percentage: country['percentage'],
            total: country['total']
          }
          this.topCountriesData.push(temp);
          this.showTopCountriesData = true;
          
        }
      }
      else {
        this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
        this.showTopCountriesData = false;
      }
    });
  }

  updateButtonSelected(typePlot:string, buttonId:number, buttonList:plotTimelineButton[], plotKindTrace: plotDropDowns){
    var updatePlotFlag = false;
    for (let x in buttonList){
      if (buttonList[x]['id'] == buttonId && buttonList[x]['selected'] == false ){
          buttonList[x]['selected'] = true;
          updatePlotFlag = true;
      }
      else if (buttonList[x]['selected'] == true && buttonList[x]['id'] != buttonId){
        buttonList[x]['selected'] = false;
      }
    }
    if (updatePlotFlag){
      if (typePlot == 'world'){
        this.updateWorldPlot(plotKindTrace, buttonList)
      }
      if (typePlot == 'topCountries'){
        this.updateTopCountriesPlot(plotKindTrace, buttonList)
      }
    }
  }

  updateTopCountriesPlot(plotKindTrace: plotDropDowns, plotTimeline:plotTimelineButton[]){

    this.showTopCountriesPlot = false;
    var updatedPlotTimeline = -1;
    for (let x in plotTimeline){
      if (plotTimeline[x]['selected'] == true ){
          updatedPlotTimeline = plotTimeline[x]['id']
      }
    }

    var err = this._apiService.getTopCountriesPlot({'plotTraceId': plotKindTrace.id, 'plotTimeline': updatedPlotTimeline, 'numLimit': 8 });
    err.subscribe( data => { 
      console.log(data)
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
          this.showTopCountriesPlot = false;
      }
      else if (data['sucess'] == 100){
        console.log(data['data']['Plot Link'])
        this.topCountriesPlotLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Link']);
        this.showTopCountriesPlot = true;
      }
      else {
        this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
        this.showTopCountriesPlot = false;
      }
    });

  }

  updateWorldPlot(plotKindTrace: plotDropDowns, plotTimeline:plotTimelineButton[]){

    this.showWorldPlot = false;
    var updatedPlotTimeline = -1;
    for (let x in plotTimeline){
      if (plotTimeline[x]['selected'] == true ){
          updatedPlotTimeline = plotTimeline[x]['id']
      }
    }

    var err = this._apiService.getWorldPlot({'plotTraceId': plotKindTrace.id, 'plotTimeline': updatedPlotTimeline });
    err.subscribe( data => { 
      console.log(data)
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
          this.showWorldPlot = false;
      }
      else if (data['sucess'] == 100){
        console.log(data['data']['Plot Link'])
        this.worldPlotLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Link']);
        this.showWorldPlot = true;
      }
      else {
        this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
        this.showWorldPlot = false;
      }
    });
  }
}
