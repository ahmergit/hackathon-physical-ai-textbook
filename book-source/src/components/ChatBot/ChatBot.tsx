/**
 * Main ChatBot component shell.
 * Home page themed chat interface for Physical AI textbook.
 * Requires user login to interact.
 */

import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { useHistory } from '@docusaurus/router';
import { useChatSession } from '../../hooks/useChatSession';
import { useAuth } from '../../contexts/AuthContext';

// Hook to detect mobile screen
function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false);
  
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth <= 767);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  return isMobile;
}

interface ChatBotProps {
  onClose?: () => void;
  isVisible?: boolean;
  pendingText?: string | null;
  onPendingTextUsed?: () => void;
}

export function ChatBot({ onClose, isVisible = true, pendingText, onPendingTextUsed }: ChatBotProps) {
  const { session, sendMessage, clearSession, cancelStream } = useChatSession();
  const { user } = useAuth();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const history = useHistory();
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const isMobile = useIsMobile();

  const isLoggedIn = !!user;

  // Handle pending text from text selection
  useEffect(() => {
    if (pendingText && isVisible) {
      setInput(pendingText);
      onPendingTextUsed?.();
      // Focus the input and auto-resize after setting the text
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
          // Trigger auto-resize for pasted content
          inputRef.current.style.height = 'auto';
          inputRef.current.style.height = Math.min(inputRef.current.scrollHeight, 200) + 'px';
        }
      }, 100);
    }
  }, [pendingText, isVisible, onPendingTextUsed]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [session.messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || session.isStreaming || !isLoggedIn) {
      return;
    }

    sendMessage(input.trim());
    setInput('');
    
    // Reset textarea to original size
    if (inputRef.current) {
      inputRef.current.style.height = '44px';
    }
  };

  const handleLoginClick = () => {
    // Dispatch event to open login modal
    window.dispatchEvent(new CustomEvent('openAuthModal', { detail: { mode: 'login' } }));
  };

  return (
    <div
      className="chatbot-container"
      style={{
        position: 'fixed',
        ...(isMobile ? {
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          width: '100%',
          height: '100%',
          maxHeight: '100%',
          borderRadius: 0,
        } : {
          bottom: '20px',
          right: '20px',
          width: '400px',
          maxHeight: '550px',
          borderRadius: '20px',
        }),
        background: 'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)',
        boxShadow: isMobile ? 'none' : '0 10px 40px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(99, 102, 241, 0.2)',
        display: isVisible ? 'flex' : 'none',
        flexDirection: 'column',
        overflow: 'hidden',
        zIndex: 9999,
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: '16px 20px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: '#ffffff',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '12px',
            background: 'rgba(255, 255, 255, 0.2)',
            backdropFilter: 'blur(10px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '20px',
          }}>
            🤖
          </div>
          <div>
            <div style={{ fontWeight: '700', fontSize: '1rem' }}>AI Assistant</div>
            <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>Physical AI Textbook</div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          {isLoggedIn && (
            <button
              onClick={clearSession}
              style={{
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                color: '#ffffff',
                cursor: 'pointer',
                fontSize: '1rem',
                padding: '8px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'background 0.2s',
              }}
              title="Clear chat"
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'}
            >
              🗑️
            </button>
          )}
          {onClose && (
            <button
              onClick={onClose}
              style={{
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                color: '#ffffff',
                cursor: 'pointer',
                fontSize: '1.1rem',
                padding: '8px',
                borderRadius: '8px',
                lineHeight: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'background 0.2s',
              }}
              title="Close"
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'}
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: isMobile ? '20px' : '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          background: 'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)',
          minHeight: isMobile ? 'auto' : '300px',
        }}
      >
        {!isLoggedIn ? (
          <div style={{ 
            textAlign: 'center', 
            color: '#9ca3af', 
            padding: '60px 20px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '16px',
          }}>
            <div style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '28px',
            }}>
              🔒
            </div>
            <div style={{ fontSize: '1rem', fontWeight: '600', color: '#e5e7eb' }}>
              Login Required
            </div>
            <div style={{ fontSize: '0.85rem', lineHeight: '1.5' }}>
              Sign in to chat with our AI assistant and get help with Physical AI & Robotics topics.
            </div>
          </div>
        ) : session.messages.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            color: '#9ca3af', 
            padding: '40px 16px',
            fontSize: '0.9rem',
          }}>
            Ask me anything about Physical AI and Humanoid Robotics!
          </div>
        ) : null}

        {isLoggedIn && session.messages.map((message) => (
          <div
            key={message.id}
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
            }}
          >
            {message.role === 'user' ? (
              <div style={{ alignSelf: 'flex-end', maxWidth: '85%' }}>
                <div
                  style={{
                    padding: '10px 14px',
                    borderRadius: '12px 12px 4px 12px',
                    backgroundColor: '#6366f1',
                    color: '#ffffff',
                    fontSize: '0.9rem',
                    lineHeight: '1.5',
                  }}
                >
                  {message.content}
                </div>
              </div>
            ) : (
              <div style={{ maxWidth: '95%' }}>
                {/* Assistant message */}
                <div
                  style={{
                    padding: '12px 14px',
                    borderRadius: '4px 12px 12px 12px',
                    backgroundColor: '#252536',
                    color: '#e5e7eb',
                    fontSize: '0.9rem',
                    lineHeight: '1.6',
                    border: '1px solid #2d2d3d',
                  }}
                >
                  <div className="markdown-content" style={{ 
                    wordBreak: 'break-word',
                  }}>
                    {message.content ? (
                      <ReactMarkdown
                        components={{
                          p: ({children}) => <p style={{ margin: '0 0 8px 0' }}>{children}</p>,
                          strong: ({children}) => <strong style={{ fontWeight: 700, color: '#ffffff' }}>{children}</strong>,
                          em: ({children}) => <em style={{ fontStyle: 'italic' }}>{children}</em>,
                          ul: ({children}) => <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>{children}</ul>,
                          ol: ({children}) => <ol style={{ margin: '8px 0', paddingLeft: '20px' }}>{children}</ol>,
                          li: ({children}) => <li style={{ marginBottom: '4px' }}>{children}</li>,
                          code: ({children}) => <code style={{ backgroundColor: '#1e1e2e', padding: '2px 6px', borderRadius: '4px', fontSize: '0.85em' }}>{children}</code>,
                          h1: ({children}) => <h1 style={{ fontSize: '1.2em', fontWeight: 700, margin: '12px 0 8px', color: '#ffffff' }}>{children}</h1>,
                          h2: ({children}) => <h2 style={{ fontSize: '1.1em', fontWeight: 700, margin: '10px 0 6px', color: '#ffffff' }}>{children}</h2>,
                          h3: ({children}) => <h3 style={{ fontSize: '1em', fontWeight: 600, margin: '8px 0 4px', color: '#ffffff' }}>{children}</h3>,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    ) : (message.status === 'streaming' && (
                      <span style={{ color: '#6b7280' }}>Thinking...</span>
                    ))}
                  </div>

                  {message.status === 'error' && (
                    <div style={{ color: '#ef4444', fontSize: '0.8rem', marginTop: '8px' }}>
                      ⚠️ Error occurred
                    </div>
                  )}
                </div>

                {/* Sources/Citations - Below the message */}
                {message.citations && message.citations.length > 0 && (
                  <div style={{ marginTop: '10px' }}>
                    <div style={{ 
                      color: '#f59e0b', 
                      fontSize: '0.8rem', 
                      fontWeight: '600',
                      marginBottom: '6px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                    }}>
                      📚 Sources:
                    </div>
                    {message.citations.map((citation, idx) => {
                      // Add base path for Docusaurus
                      let citationUrl = citation.url || '';
                      if (citationUrl.startsWith('/docs/')) {
                        citationUrl = `/physical-ai-humaniod-robotics${citationUrl}`;
                      }
                      return (
                        <span
                          key={idx}
                          onClick={() => history.push(citationUrl)}
                          style={{
                            color: '#60a5fa',
                            fontSize: '0.75rem',
                            padding: '4px 0',
                            lineHeight: '1.4',
                            display: 'block',
                            textDecoration: 'none',
                            cursor: 'pointer',
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.textDecoration = 'underline'}
                          onMouseLeave={(e) => e.currentTarget.style.textDecoration = 'none'}
                        >
                          • {citation.title} ({Math.round(citation.relevance_score * 100)}% match)
                        </span>
                      );
                    })}
                  </div>
                )}

                {/* Timestamp */}
                {message.timestamp && (
                  <div style={{ 
                    color: '#6b7280', 
                    fontSize: '0.7rem', 
                    marginTop: '4px',
                  }}>
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {session.isStreaming && (
          <div style={{ textAlign: 'center', padding: '8px' }}>
            <button
              onClick={cancelStream}
              style={{
                padding: '6px 14px',
                backgroundColor: '#ef4444',
                color: '#ffffff',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '0.8rem',
                fontWeight: '500',
              }}
            >
              Stop generating
            </button>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input / Login Button */}
      {isLoggedIn ? (
        <form
          onSubmit={handleSubmit}
          style={{
            padding: '14px 16px',
            borderTop: '1px solid rgba(99, 102, 241, 0.2)',
            background: 'linear-gradient(180deg, #1e1e38 0%, #1a1a2e 100%)',
            display: 'flex',
            gap: '10px',
            alignItems: 'flex-end',
          }}
        >
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              // Submit on Enter (without Shift), allow Shift+Enter for new line
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (input.trim() && !session.isStreaming) {
                  handleSubmit(e);
                }
              }
            }}
            placeholder="Ask a question... (Shift+Enter for new line)"
            disabled={session.isStreaming}
            rows={1}
            style={{
              flex: 1,
              padding: '12px 16px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(99, 102, 241, 0.3)',
              borderRadius: '12px',
              fontSize: '0.9rem',
              color: '#e5e7eb',
              outline: 'none',
              transition: 'border-color 0.2s, height 0.2s',
              resize: 'none',
              minHeight: '44px',
              maxHeight: '200px',
              overflowY: 'auto',
              lineHeight: '1.5',
              fontFamily: 'inherit',
            }}
            onFocus={(e) => e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.6)'}
            onBlur={(e) => e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.3)'}
            onInput={(e) => {
              // Auto-resize textarea based on content
              const target = e.currentTarget;
              target.style.height = 'auto';
              target.style.height = Math.min(target.scrollHeight, 200) + 'px';
            }}
          />
          <button
            type="submit"
            disabled={!input.trim() || session.isStreaming}
            style={{
              padding: '12px',
              background: !input.trim() || session.isStreaming 
                ? 'rgba(99, 102, 241, 0.3)' 
                : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: '#ffffff',
              border: 'none',
              borderRadius: '12px',
              cursor: !input.trim() || session.isStreaming ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'transform 0.2s, box-shadow 0.2s',
              boxShadow: !input.trim() || session.isStreaming ? 'none' : '0 4px 15px rgba(102, 126, 234, 0.4)',
            }}
            onMouseEnter={(e) => {
              if (input.trim() && !session.isStreaming) {
                e.currentTarget.style.transform = 'scale(1.05)';
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13M22 2L15 22L11 13L2 9L22 2Z" />
            </svg>
          </button>
        </form>
      ) : (
        <div
          style={{
            padding: '16px',
            borderTop: '1px solid rgba(99, 102, 241, 0.2)',
            background: 'linear-gradient(180deg, #1e1e38 0%, #1a1a2e 100%)',
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <button
            onClick={handleLoginClick}
            style={{
              width: '100%',
              padding: '14px 24px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: '#ffffff',
              border: 'none',
              borderRadius: '12px',
              fontSize: '0.95rem',
              fontWeight: '600',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              transition: 'transform 0.2s, box-shadow 0.2s',
              boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.5)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
              <polyline points="10 17 15 12 10 7" />
              <line x1="15" y1="12" x2="3" y2="12" />
            </svg>
            Sign In to Chat
          </button>
        </div>
      )}
    </div>
  );
}
