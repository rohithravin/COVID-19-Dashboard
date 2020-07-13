import { Component, OnInit } from '@angular/core';
import { CoronaDashboardApiService } from '../corona-dashboard-api.service';
import { faChevronUp } from '@fortawesome/free-solid-svg-icons';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
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



@Component({
  selector: 'app-cali-dashboard',
  templateUrl: './cali-dashboard.component.html',
  styleUrls: ['./cali-dashboard.component.css']
})

export class CaliDashboardComponent implements OnInit {

  fa_SortUp = faChevronUp;
  fa_SortDown = faChevronDown;
  dailyData: any;
  userLocationData: any;

  plotNewKind: plotDropDowns[];
  plotNewKindSelected: plotDropDowns;

  plotNewTrace: plotDropDowns[];
  plotNewTraceSelected: plotDropDowns;

  plotNewTimeline: plotTimelineButton[];
  plotNewLink:SafeResourceUrl;
  showPlotNew: boolean;

  plotTotalKind: plotDropDowns[];
  plotTotalKindSelected: plotDropDowns;
  plotTotalTrace: plotDropDowns[];
  plotTotalTraceSelected: plotDropDowns;
  showPlotTotal:boolean;
  plotTotalLink:SafeResourceUrl;


  constructor(private _apiService: CoronaDashboardApiService, private _snackBar: MatSnackBar, public _sanitizer: DomSanitizer) {


    this.plotTotalKind = [
      {id: 601, name: 'Total Cases'},
      {id: 602, name: 'Total Deaths'}
    ]
    this.plotTotalKindSelected = this.plotTotalKind[0];

    this.plotTotalTrace = [
      {id: 401, name: 'County'},
      {id: 402, name: 'State'},
      {id: 403, name: 'Bay Area Counties'},
      {id: 404, name: 'SoCal Counties'},
      {id: 405, name: 'NorCal v SoCal'},
      {id: 406, name: 'Bay Area v SoCal'},
      {id: 407, name: 'High Populous Area'}
    ]
    this.plotTotalTraceSelected = this.plotTotalTrace[0];
    this.showPlotTotal = false;

    this.plotNewTimeline = [
      {id: 501, name: '2 Weeks', selected: true},
      {id: 502, name: 'Month', selected: false},
      {id: 503, name: '3 Months', selected: false},
      {id: 504, name: 'All', selected: false},
    ]
    this.showPlotNew = false;

    this.plotNewKind = [
      {id: 301, name: 'New Cases'},
      {id: 302, name: 'New Deaths'}
    ]
    this.plotNewKindSelected = this.plotNewKind[0];

    this.plotNewTrace = [
      {id: 401, name: 'County'},
      {id: 402, name: 'State'},
      {id: 403, name: 'Bay Area Counties'},
      {id: 404, name: 'SoCal Counties'},
      {id: 405, name: 'NorCal v SoCal'},
      {id: 406, name: 'Bay Area v SoCal'},
      {id: 407, name: 'High Populous Area'}
    ]
    this.plotNewTraceSelected = this.plotNewTrace[0];

    this.userLocationData = JSON.parse(localStorage.getItem('CaliDashboardUserLocationInfo'));
    this.loadDailyData()
    console.log(this.plotNewKind)
    this.updateNewKindPlot(this.plotNewKindSelected, this.plotNewTraceSelected,this.plotNewTimeline)
    this.updateTotalPlot(this.plotTotalKindSelected, this.plotTotalTraceSelected)
    
   }

  updateButtonSelected(buttonId:number, buttonList:plotTimelineButton[], plotKind: plotDropDowns, plotKindTrace: plotDropDowns){
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
      this.updateNewKindPlot(plotKind, plotKindTrace, buttonList)
    }
  }

  updateTotalPlot(plotKind: plotDropDowns, plotKindTrace: plotDropDowns){
    this.showPlotTotal = false;
    console.log(plotKind)
    console.log(plotKindTrace)
    var err = this._apiService.getPlotTotalKind({'plotKindId': plotKind.id, 'plotTraceId':plotKindTrace.id,county: this.userLocationData['county'] });
    err.subscribe( data => { 
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
          this.showPlotTotal = false;
      }
      else if (data['sucess'] == 100){
        console.log(data['data']['Plot Link'])
        this.plotTotalLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Link']);
        this.showPlotTotal = true;
      }
      else {
        this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
        this.showPlotTotal = false;
      }
    });
  }

  updateNewKindPlot(plotKind: plotDropDowns, plotKindTrace: plotDropDowns, plotTimeline:plotTimelineButton[]){
    this.showPlotNew = false;
    var updatedPlotTimeline = -1;
    for (let x in plotTimeline){
      if (plotTimeline[x]['selected'] == true ){
          updatedPlotTimeline = plotTimeline[x]['id']
      }
    }
    var err = this._apiService.getPlotNewKind({'plotKindId': plotKind.id, 'plotTraceId':plotKindTrace.id, 'plotTimeline':updatedPlotTimeline,county: this.userLocationData['county'] });
    err.subscribe( data => { 
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
          this.showPlotNew = false;
      }
      else if (data['sucess'] == 100){
        console.log(data['data']['Plot Link'])
        this.plotNewLink = this._sanitizer.bypassSecurityTrustResourceUrl(data['data']['Plot Link']);
        this.showPlotNew = true;
      }
      else {
        this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
        this.showPlotNew = false;
      }
    });
  }

  loadDailyData():any {
    console.log('hi')
    var err = this._apiService.getCaliDailyData(this.userLocationData['county']);
    err.subscribe( data => { 
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
      }
      else if (data['sucess'] == 100){
        this.dailyData =  data['data'];
        console.log(this.dailyData)
      }
      else {
        this._snackBar.open( 'ERROR: Server not responding. Try again later.', 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
      }
    });
  }

  ngOnInit(): void {
    
  }

}
