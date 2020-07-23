import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-forecast-dashboard',
  templateUrl: './forecast-dashboard.component.html',
  styleUrls: ['./forecast-dashboard.component.css']
})
export class ForecastDashboardComponent implements OnInit {

  showCaliTab:boolean;
  showUSTab:boolean;
  showWorldTab:boolean;

  constructor() {
    this.showCaliTab = true;
    this.showUSTab = false;
    this.showWorldTab = false;
   }

  ngOnInit(): void {
  }

  changeForcastTab(tab:string){
    if (tab == 'california'){
      this.showCaliTab = true;
      this.showUSTab = false;
      this.showWorldTab = false;

    } else if (tab == 'world') {
      this.showCaliTab = false;
      this.showUSTab = false;
      this.showWorldTab = true;

    } else if (tab == 'us'){
      this.showCaliTab = false;
      this.showUSTab = true;
      this.showWorldTab = false;
    }
    console.log(tab)
  }
}
