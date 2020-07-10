import { Component, OnInit } from '@angular/core';

import { faChevronUp } from '@fortawesome/free-solid-svg-icons';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-cali-dashboard',
  templateUrl: './cali-dashboard.component.html',
  styleUrls: ['./cali-dashboard.component.css']
})
export class CaliDashboardComponent implements OnInit {
  fa_SortUp = faChevronUp;
  fa_SortDown = faChevronDown;

  constructor() { }

  ngOnInit(): void {
  }

}
