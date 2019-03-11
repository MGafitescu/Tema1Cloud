import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { RandomComponent } from './random/random.component';
import { WeatherComponent } from './weather/weather.component';
import { ReportComponent } from './report/report.component';
import { MetricsComponent } from './metrics/metrics.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    RandomComponent,
    WeatherComponent,
    ReportComponent,
    MetricsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
