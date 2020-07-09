import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { CaliDashboardComponent } from './cali-dashboard/cali-dashboard.component';
import { WorldDashboardComponent } from './world-dashboard/world-dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    CaliDashboardComponent,
    WorldDashboardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    NoopAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
