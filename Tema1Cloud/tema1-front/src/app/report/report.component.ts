import { Component, OnInit } from '@angular/core';
import { HttpRequestsService } from '../http-requests.service';
import { Report } from '../report';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {

 
  constructor(private httpService: HttpRequestsService) { }

  report: Report;
  ngOnInit() {
   this.report= new Report;  
  }

  populateProperties(): void {
    this.httpService.getReportRandom()
      .subscribe((report: Report) => this.report = report);
  }

  clickButton(): void{
    this.populateProperties();
  }

  generateCoordinates(latitude, longitude){
    this.httpService.getReport(latitude,longitude)
      .subscribe((report: Report) => this.report = report);
    
  }

}
