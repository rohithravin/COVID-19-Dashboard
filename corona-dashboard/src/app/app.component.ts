import { Component, Inject} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'corona-dashboard';

  zipcode:number;
  userInputErrMsg: string;
  userInputErrFlag: boolean;
  accessTabsFlag: boolean;
  caliDashboardFlag: boolean;
  worldDashboardFlag: boolean;
  landingPageFlag: boolean;
  
  constructor() {
    this.userInputErrMsg = '';
    this.userInputErrFlag = false;
    this.accessTabsFlag = false;

    this.caliDashboardFlag = false;
    this.worldDashboardFlag = false;
    this.landingPageFlag = true;
  }
  
  onZipcodeClick(){
    if (this.zipcode != undefined && this.zipcode.toString().length == 5 ){
      this.userInputErrFlag = false;
      this.accessTabsFlag = true;
      this.landingPageFlag = false;
      this.caliDashboardFlag = true;
    }
    else{
      this.userInputErrMsg = 'Please enter your 5-digit zipcode.';
      this.userInputErrFlag = true;
      this.accessTabsFlag = false;
    }
  }
}