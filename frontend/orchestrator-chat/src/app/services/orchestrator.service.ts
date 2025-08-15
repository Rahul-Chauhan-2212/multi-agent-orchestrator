import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class OrchestratorService {
  private baseUrl = 'http://localhost:8000'; // Orchestrator URL

  constructor(private http: HttpClient) {}

  sendMessage(message: string) {
    const payload = { query: message }; // match Pydantic model
    return this.http.post(`${this.baseUrl}/ask`, payload);
  }
}
