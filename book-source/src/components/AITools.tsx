import React, { useState, useEffect } from 'react';
import styles from './AITools.module.css';
import { ChatBot } from './ChatBot/ChatBot';
import { TextSelectionButton } from './ChatBot/TextSelectionButton';
import { useTextSelection } from '../hooks/useTextSelection';

interface AIToolsProps {
  variant?: 'button' | 'floating';
}

export default function AITools({ variant = 'button' }: AIToolsProps): React.JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const [pendingText, setPendingText] = useState<string | null>(null);
  const [buttonPosition, setButtonPosition] = useState<{ x: number; y: number } | undefined>();
  const { selectedText, selectionRange, clearSelection } = useTextSelection();

  // Calculate button position - center above the selection
  useEffect(() => {
    if (selectionRange) {
      const rect = selectionRange.getBoundingClientRect();
      const buttonWidth = 140; // Approximate button width
      const buttonHeight = 36; // Approximate button height
      
      // Center horizontally over the selection
      let x = rect.left + (rect.width / 2) - (buttonWidth / 2);
      // Position above the selection
      let y = rect.top - buttonHeight - 8;
      
      // Keep button within viewport bounds
      x = Math.max(10, Math.min(x, window.innerWidth - buttonWidth - 10));
      y = Math.max(10, y);
      
      // If not enough space above, show below the selection
      if (y < 10) {
        y = rect.bottom + 8;
      }
      
      setButtonPosition({ x, y });
    }
  }, [selectionRange]);

  const handleClick = () => {
    setIsOpen(!isOpen);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleAskAboutSelection = () => {
    if (selectedText) {
      setPendingText(selectedText);
      clearSelection();
      setIsOpen(true); // Open chat if not already open
    }
  };

  const handlePendingTextUsed = () => {
    setPendingText(null);
  };

  return (
    <div className={variant === 'floating' ? styles.floatingContainer : styles.buttonContainer}>
      <button
        className={`${styles.aiToolsButton} ${variant === 'floating' ? styles.floating : ''} ${isOpen ? styles.active : ''}`}
        onClick={handleClick}
        title="AI Assistant"
        aria-label="AI Assistant"
        aria-expanded={isOpen}
      >
        <svg
          className={styles.icon}
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
            fill="currentColor"
          />
          <circle cx="12" cy="12" r="3" fill="currentColor" />
          <path
            d="M12 6v2M12 16v2M6 12h2M16 12h2"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
        <span className={styles.text}>{isOpen ? 'Close' : 'AI Assistant'}</span>
      </button>
      
      {/* Text selection button - appears when text is selected */}
      <TextSelectionButton
        selectedText={selectedText || ''}
        onAskAboutSelection={handleAskAboutSelection}
        position={buttonPosition}
      />
      
      {/* Keep ChatBot mounted to preserve state, just hide when closed */}
      <ChatBot 
        onClose={handleClose} 
        isVisible={isOpen} 
        pendingText={pendingText}
        onPendingTextUsed={handlePendingTextUsed}
      />
    </div>
  );
}
