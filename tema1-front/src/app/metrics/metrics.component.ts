import { Component, OnInit } from '@angular/core';
import { Metrics } from 'src/app/metrics';
import { HttpRequestsService } from '../http-requests.service';

@Component({
  selector: 'app-metrics',
  templateUrl: './metrics.component.html',
  styleUrls: ['./metrics.component.css']
})
export class MetricsComponent implements OnInit {

  constructor(private httpService: HttpRequestsService) { }

  metricsList: Metrics[]
  ngOnInit() {
   this.populateProperties()
  }

  populateProperties(): void {
    this.httpService.getMetrics()
      .subscribe((list: Metrics[]) => this.metricsList = list);
  }



}
