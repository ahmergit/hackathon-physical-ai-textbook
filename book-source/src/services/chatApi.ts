/**
 * Chat API client with SSE (Server-Sent Events) streaming support.
 */

// Helper to get access token from localStorage
function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface Citation {
  chapter: string;
  section: string;
  title: string;
  url: string;
  relevance_score: number;
  snippet?: string;
}

export interface ChatRequest {
  message: string;
  conversation_history?: ConversationMessage[];
  selected_text?: string;
  quick_action?: 'explain' | 'summarize' | 'simplify';
}

export type ChatStreamEvent =
  | { type: 'delta'; content: string }
  | { type: 'citation'; citation: Citation }
  | { type: 'done'; citations: Citation[] }
  | { type: 'error'; message: string; code: string };

export type StreamEventHandler = (event: ChatStreamEvent) => void;

/**
 * Chat API client for communicating with the backend chatbot service.
 */
export class ChatApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000/api') {
    this.baseUrl = baseUrl;
  }

  /**
   * Send a chat message and receive streaming response via SSE.
   *
   * @param request Chat request parameters
   * @param onEvent Callback for each SSE event
   * @param signal AbortSignal for cancelling the stream
   */
  async streamChat(
    request: ChatRequest,
    onEvent: StreamEventHandler,
    signal?: AbortSignal
  ): Promise<void> {
    const accessToken = getAccessToken();
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify(request),
      signal,
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Please log in to use the chat');
      }
      throw new Error(`Chat API error: ${response.statusText}`);
    }

    if (!response.body) {
      throw new Error('No response body');
    }

    // Read SSE stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        // Decode chunk and add to buffer
        buffer += decoder.decode(value, { stream: true });

        // Process complete SSE messages (separated by \n\n)
        const messages = buffer.split('\n\n');
        buffer = messages.pop() || ''; // Keep incomplete message in buffer

        for (const message of messages) {
          if (message.startsWith('data: ')) {
            const data = message.slice(6); // Remove 'data: ' prefix
            try {
              const event: ChatStreamEvent = JSON.parse(data);
              onEvent(event);
            } catch (e) {
              console.error('Failed to parse SSE event:', data, e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  /**
   * Health check for the chat service.
   */
  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await fetch(`${this.baseUrl}/chat/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }
}

// Singleton instance
export const chatApi = new ChatApiClient(
  typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api'
    : '/api' // Use relative path in production
);
