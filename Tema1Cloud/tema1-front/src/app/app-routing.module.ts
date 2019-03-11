import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from '../app/home/home.component'
import { RandomComponent } from 'src/app/random/random.component';
import { WeatherComponent } from 'src/app/weather/weather.component';
import { ReportComponent } from 'src/app/report/report.component';
import { MetricsComponent } from 'src/app/metrics/metrics.component';
const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'random', component: RandomComponent },
  { path: 'weather', component: WeatherComponent},
  { path: 'report', component: ReportComponent},
  { path: 'metrics', component: MetricsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
