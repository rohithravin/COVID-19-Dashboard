import { TestBed } from '@angular/core/testing';

import { CoronaDashboardApiService } from './corona-dashboard-api.service';

describe('CoronaDashboardApiService', () => {
  let service: CoronaDashboardApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CoronaDashboardApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
