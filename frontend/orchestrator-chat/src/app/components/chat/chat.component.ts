import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { OrchestratorService } from '../../services/orchestrator.service';


@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  userMessage = '';
  messages: { role: string; content: string }[] = [];

  constructor(private orchestratorService: OrchestratorService) {}

  sendMessage() {
    if (!this.userMessage.trim()) return;

    // Push user message
    this.messages.push({ role: 'user', content: this.userMessage });

    const msgToSend = this.userMessage;
    this.userMessage = '';

    // Call orchestrator
    this.orchestratorService.sendMessage(msgToSend).subscribe({
      next: (res) => {
        this.messages.push({ role: 'orchestrator', content: JSON.stringify(res) || 'No response' });
      },
      error: () => {
        this.messages.push({ role: 'orchestrator', content: 'Error contacting orchestrator.' });
      }
    });
  }
}
