import { Component, Inject} from '@angular/core';
import {MatDialog,  MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';


export interface DialogData {
  animal: string;
  name: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'corona-dashboard';
  animal: string;
  name: string;
  
  constructor(public dialog: MatDialog) {}
 
}