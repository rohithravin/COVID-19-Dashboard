import { Component, Inject} from '@angular/core';
import { CoronaDashboardApiService } from './corona-dashboard-api.service';
import {MatSnackBar} from '@angular/material/snack-bar';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'corona-dashboard';

  zipcode:number;
  accessTabsFlag: boolean;
  caliDashboardFlag: boolean;
  worldDashboardFlag: boolean;
  landingPageFlag: boolean;

  caliButtonSelected: string;
  worldButtonSelected: string;
  
  constructor(private _apiService: CoronaDashboardApiService, private _snackBar: MatSnackBar) {
    this.accessTabsFlag = false;

    this.caliDashboardFlag = false;
    this.worldDashboardFlag = false;
    this.landingPageFlag = true;

    this.caliButtonSelected = 'btn-primary';
    this.worldButtonSelected = 'btn-primary';

    
  }

  getUserLocation(){
    var err = this._apiService.getUserLocation(this.zipcode);
    err.subscribe( data => { 
      if (data['sucess'] == 501){
        this._snackBar.open(data['msg'], 'Close', {
          panelClass: 'snack-bar',
          duration: 2500
        });
        this.accessTabsFlag = false;
        this.landingPageFlag = true;
      }
      else{
        this.accessTabsFlag = true;
        this.landingPageFlag = false;
        this.caliDashboardFlag = true;
        this.caliButtonSelected = 'btn-outline-primary';
        this.worldButtonSelected = 'btn-primary';
        console.log(data['data']);
      }
      
    });
  }

  onCaliButtonClick(){
    if (this.caliDashboardFlag != true){
      this.caliButtonSelected = 'btn-outline-primary';
      this.worldButtonSelected = 'btn-primary';
      this.caliDashboardFlag = true;
      this.worldDashboardFlag = false;
    }
  }

  onWorldButtonClick(){
    if (this.worldDashboardFlag != true){
      this.caliDashboardFlag = false;
      this.worldDashboardFlag = true;
      this.caliButtonSelected = 'btn-primary';
      this.worldButtonSelected = 'btn-outline-primary';
    }
  }
  
  onZipcodeClick(){
    if (this.zipcode != undefined && this.zipcode.toString().length == 5 ){
      this.getUserLocation();
    }
    else{
      this._snackBar.open('ERROR: Please enter your 5-digit zipcode.', 'Close', {
        panelClass: 'snack-bar',
        duration: 2500
      });
      this.accessTabsFlag = false;
      
    }
  }

}