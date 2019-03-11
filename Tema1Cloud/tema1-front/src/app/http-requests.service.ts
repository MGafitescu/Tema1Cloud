import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {GeoInformation } from './geoInformation';
import { Observable } from 'rxjs/internal/Observable';
import { stringify } from 'querystring';
import { WeatherInformation } from 'src/app/weatherInformation';
import { Report } from 'src/app/report';
import { Metrics } from 'src/app/metrics';

@Injectable({
  providedIn: 'root'
})
export class HttpRequestsService {

  constructor(private http: HttpClient) { }

  geoUrl = "http://localhost:8081/geolocation"
  weatherUrl = "http://localhost:8081/weather"
  reportUrl = "http://localhost:8081/pastebin"
  metricsUrl = "http://localhost:8081/metrics"

  getGeoRandom(): Observable<GeoInformation>{
    return this.http.get<GeoInformation>(this.geoUrl);
  }
  getGeo(latitude, longitude): Observable<GeoInformation>{
    let url = this.geoUrl+"?lat="+latitude+"&lon="+longitude;
    return this.http.get<GeoInformation>(url);
  }

  getWeatherRandom(): Observable<WeatherInformation>{
    return this.http.get<WeatherInformation>(this.weatherUrl);
  }
  getWeather(latitude, longitude): Observable<WeatherInformation>{
    let url = this.weatherUrl+"?lat="+latitude+"&lon="+longitude;
    return this.http.get<WeatherInformation>(url);
  }

  getReportRandom(): Observable<Report>{
    return this.http.get<Report>(this.reportUrl);
  }
  getReport(latitude, longitude): Observable<Report>{
    let url = this.reportUrl+"?lat="+latitude+"&lon="+longitude;
    return this.http.get<Report>(url);
  }

  getMetrics(): Observable<Metrics[]>{
    return this.http.get<Metrics[]>(this.metricsUrl);
  }
  
}
