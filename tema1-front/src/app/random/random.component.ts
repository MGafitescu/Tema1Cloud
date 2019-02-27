import { Component, OnInit } from '@angular/core';
import { HttpRequestsService } from '../http-requests.service';
import { GeoInformation } from '../geoInformation';
@Component({
  selector: 'app-random',
  templateUrl: './random.component.html',
  styleUrls: ['./random.component.css']
})
export class RandomComponent implements OnInit {


  constructor(private httpService: HttpRequestsService) { }

  geoInformation: GeoInformation;
  ngOnInit() {
   this.geoInformation = new GeoInformation;  
  }

  populateProperties(): void {
    this.httpService.getGeoRandom()
      .subscribe((geoInformation: GeoInformation) => this.geoInformation = geoInformation);
  }

  clickButton(): void{
    this.populateProperties();
  }

  generateCoordinates(latitude, longitude){
    this.httpService.getGeo(latitude,longitude)
      .subscribe((geoInformation: GeoInformation) => this.geoInformation = geoInformation);
  }

}
