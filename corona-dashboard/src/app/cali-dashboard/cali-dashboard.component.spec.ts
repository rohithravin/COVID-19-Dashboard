import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CaliDashboardComponent } from './cali-dashboard.component';

describe('CaliDashboardComponent', () => {
  let component: CaliDashboardComponent;
  let fixture: ComponentFixture<CaliDashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CaliDashboardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CaliDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
