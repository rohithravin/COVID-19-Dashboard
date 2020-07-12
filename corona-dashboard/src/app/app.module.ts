import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { CaliDashboardComponent } from './cali-dashboard/cali-dashboard.component';
import { WorldDashboardComponent } from './world-dashboard/world-dashboard.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CoronaDashboardApiService } from './corona-dashboard-api.service';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@NgModule({
  declarations: [
    AppComponent,
    CaliDashboardComponent,
    WorldDashboardComponent
  ],
  imports: [
    BrowserModule,
    NgbModule,
    NoopAnimationsModule,
    FormsModule,
    HttpClientModule,
    MatSnackBarModule,
    FontAwesomeModule
  ],
  providers: [CoronaDashboardApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
