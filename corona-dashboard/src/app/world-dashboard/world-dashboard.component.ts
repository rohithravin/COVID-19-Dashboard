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
  selector: 'app-world-dashboard',
  templateUrl: './world-dashboard.component.html',
  styleUrls: ['./world-dashboard.component.css']
})
export class WorldDashboardComponent implements OnInit {

  worldPlotTraceDropdown: plotDropDowns[];
  worldPlotTraceDropdownSelected: plotDropDowns;
  showWorldPlot: boolean;
  worldPlotLink:SafeResourceUrl;
  worldPlotTimeline: plotTimelineButton[];

  topCountriesTraceDropdown: plotDropDowns[];
  topCountriesTraceDropdownSelected: plotDropDowns;

  constructor(private _apiService: CoronaDashboardApiService, private _snackBar: MatSnackBar, public _sanitizer: DomSanitizer) {

    this.topCountriesTraceDropdown = [
      {id: 2100, name: 'New Cases (Today)'},
      {id: 2200, name: 'New Cases'},
      {id: 2500, name: 'New Deaths (Today)'},
      {id: 2600, name: 'New Deaths'},
      {id: 2300, name: 'Total Deaths'},
      {id: 2400, name: 'Total Cases'}
    ]
    this.topCountriesTraceDropdownSelected = this.topCountriesTraceDropdown[0];


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
   }

  ngOnInit(): void {
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
    }
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
