import { Component, OnInit } from '@angular/core';
import { CoronaDashboardApiService } from '../corona-dashboard-api.service';
import { faChevronUp } from '@fortawesome/free-solid-svg-icons';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import {MatSnackBar} from '@angular/material/snack-bar';

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

  constructor(private _apiService: CoronaDashboardApiService, private _snackBar: MatSnackBar) {
    this.userLocationData = JSON.parse(localStorage.getItem('CaliDashboardUserLocationInfo'));
    
    
   }

  loadDailyData():any {
    var err = this._apiService.getCaliDailyData(this.userLocationData['county']);
    err.subscribe( data => { 
      if (data['sucess'] == 501){
          this._snackBar.open('[ERROR]: Server error. Please try again later.', 'Close', {
            panelClass: 'snack-bar',
            duration: 2500
          });
      }
      else{
        this.dailyData =  data['data'];
        console.log(this.dailyData)
      }
    });
  }

  ngOnInit(): void {
    this.userLocationData = JSON.parse(localStorage.getItem('CaliDashboardUserLocationInfo'));
    this.loadDailyData()
    console.log(this.userLocationData)
  }

}
