/**
 * React hook for managing chat session state.
 * Persists chat history to localStorage.
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { chatApi, type ChatRequest, type Citation, type ConversationMessage } from '../services/chatApi';

const STORAGE_KEY = 'physical-ai-chat-history';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  timestamp: Date;
  status: 'streaming' | 'complete' | 'error';
}

export interface ChatSession {
  sessionId: string;
  messages: ChatMessage[];
  isStreaming: boolean;
  selectedText: string | null;
  lastQuickAction: 'explain' | 'summarize' | 'simplify' | null;
}

/**
 * Load session from localStorage
 */
function loadFromStorage(): ChatSession {
  if (typeof window === 'undefined') {
    return createEmptySession();
  }
  
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      // Convert timestamp strings back to Date objects
      const messages = parsed.messages.map((msg: any) => ({
        ...msg,
        timestamp: new Date(msg.timestamp),
        // Reset any streaming status to complete on reload
        status: msg.status === 'streaming' ? 'complete' : msg.status,
      }));
      return {
        ...parsed,
        messages,
        isStreaming: false, // Reset streaming state on reload
      };
    }
  } catch (e) {
    console.error('Failed to load chat history from localStorage:', e);
  }
  
  return createEmptySession();
}

/**
 * Save session to localStorage
 */
function saveToStorage(session: ChatSession): void {
  if (typeof window === 'undefined') return;
  
  try {
    // Only save completed messages (not streaming ones)
    const toSave = {
      ...session,
      messages: session.messages.filter(m => m.status !== 'streaming'),
      isStreaming: false,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
  } catch (e) {
    console.error('Failed to save chat history to localStorage:', e);
  }
}

/**
 * Create empty session
 */
function createEmptySession(): ChatSession {
  return {
    sessionId: `session_${Date.now()}`,
    messages: [],
    isStreaming: false,
    selectedText: null,
    lastQuickAction: null,
  };
}

export function useChatSession() {
  const [session, setSession] = useState<ChatSession>(loadFromStorage);

  const abortControllerRef = useRef<AbortController | null>(null);

  // Save to localStorage whenever messages change (but not during streaming)
  useEffect(() => {
    if (!session.isStreaming && session.messages.length > 0) {
      saveToStorage(session);
    }
  }, [session.messages, session.isStreaming]);

  /**
   * Send a message to the chatbot.
   */
  const sendMessage = useCallback(async (
    message: string,
    options?: {
      selected_text?: string;
      quick_action?: 'explain' | 'summarize' | 'simplify';
    }
  ) => {
    if (session.isStreaming) {
      console.warn('Already streaming a message');
      return;
    }

    // Create user message
    const userMessage: ChatMessage = {
      id: `msg_${Date.now()}_user`,
      role: 'user',
      content: message,
      timestamp: new Date(),
      status: 'complete',
    };

    // Create placeholder for assistant message
    const assistantMessageId = `msg_${Date.now()}_assistant`;
    const assistantMessage: ChatMessage = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      citations: [],
      timestamp: new Date(),
      status: 'streaming',
    };

    // Update state with user message and placeholder
    setSession(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage, assistantMessage],
      isStreaming: true,
      selectedText: options?.selected_text || null,
      lastQuickAction: options?.quick_action || null,
    }));

    // Prepare conversation history (exclude the new messages)
    const conversationHistory: ConversationMessage[] = session.messages.map(msg => ({
      role: msg.role,
      content: msg.content,
    }));

    // Prepare chat request
    const request: ChatRequest = {
      message,
      conversation_history: conversationHistory,
      selected_text: options?.selected_text,
      quick_action: options?.quick_action,
    };

    // Create abort controller for cancellation
    abortControllerRef.current = new AbortController();

    try {
      await chatApi.streamChat(
        request,
        (event) => {
          setSession(prev => {
            const messages = [...prev.messages];
            const assistantMsgIndex = messages.findIndex(m => m.id === assistantMessageId);

            if (assistantMsgIndex === -1) return prev;

            const updatedMessage = { ...messages[assistantMsgIndex] };

            if (event.type === 'delta') {
              // Append content delta
              updatedMessage.content += event.content;
            } else if (event.type === 'citation') {
              // Add citation
              updatedMessage.citations = [...(updatedMessage.citations || []), event.citation];
            } else if (event.type === 'done') {
              // Mark as complete
              updatedMessage.status = 'complete';
              updatedMessage.citations = event.citations;
            } else if (event.type === 'error') {
              // Mark as error
              updatedMessage.status = 'error';
              updatedMessage.content = `Error: ${event.message}`;
            }

            messages[assistantMsgIndex] = updatedMessage;

            return {
              ...prev,
              messages,
              isStreaming: event.type !== 'done' && event.type !== 'error',
            };
          });
        },
        abortControllerRef.current.signal
      );
    } catch (error) {
      // Handle errors
      setSession(prev => {
        const messages = [...prev.messages];
        const assistantMsgIndex = messages.findIndex(m => m.id === assistantMessageId);

        if (assistantMsgIndex !== -1) {
          messages[assistantMsgIndex] = {
            ...messages[assistantMsgIndex],
            status: 'error',
            content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          };
        }

        return {
          ...prev,
          messages,
          isStreaming: false,
        };
      });
    }
  }, [session.messages, session.isStreaming]);

  /**
   * Cancel the current streaming response.
   */
  const cancelStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;

      setSession(prev => ({
        ...prev,
        isStreaming: false,
      }));
    }
  }, []);

  /**
   * Clear the chat session.
   */
  const clearSession = useCallback(() => {
    cancelStream();

    // Clear localStorage
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY);
    }

    setSession(createEmptySession());
  }, [cancelStream]);

  return {
    session,
    sendMessage,
    cancelStream,
    clearSession,
  };
}
