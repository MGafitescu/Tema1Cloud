import { Component, OnInit } from '@angular/core';
import { HttpRequestsService } from '../http-requests.service';
import { WeatherInformation } from '../weatherInformation';

@Component({
  selector: 'app-weather',
  templateUrl: './weather.component.html',
  styleUrls: ['./weather.component.css']
})
export class WeatherComponent implements OnInit {

  constructor(private httpService: HttpRequestsService) { }

  weather: WeatherInformation;
  ngOnInit() {
   this.weather = new WeatherInformation;  
  }

  populateProperties(): void {
    this.httpService.getWeatherRandom()
      .subscribe((weather: WeatherInformation) => this.weather = weather);
  }

  clickButton(): void{
    this.populateProperties();
  }

  generateCoordinates(latitude, longitude){
    this.httpService.getWeather(latitude,longitude)
      .subscribe((weather: WeatherInformation) => this.weather = weather);
  }

}
