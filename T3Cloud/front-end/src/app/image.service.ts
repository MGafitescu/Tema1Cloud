import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  })
};

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  constructor(private http: HttpClient) { }

  private imageUploadUrl = 'https://back-end-t3.appspot.com/upload_photo';
  private historyUrl = 'https://back-end-t3.appspot.com';

  public postImage(image) {
    console.log('Uploading...');
    return this.http.post<any>(this.imageUploadUrl, image, httpOptions).toPromise();
  }

  public getHistory() {
    console.log('Getting history');
    return this.http.get<any>(this.historyUrl).toPromise();
  }
}
