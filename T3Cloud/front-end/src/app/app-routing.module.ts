import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ImageUploadComponent } from './image-upload/image-upload.component';
import { HistoryComponent } from './history/history.component';

const routes: Routes = [
  { path: 'upload', component: ImageUploadComponent},
  { path: 'history', component: HistoryComponent},
  { path: '', redirectTo: '/upload',pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
