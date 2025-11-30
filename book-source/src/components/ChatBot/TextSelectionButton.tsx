/**
 * Floating button that appears when text is selected.
 */

import React from 'react';

interface TextSelectionButtonProps {
  selectedText: string;
  onAskAboutSelection: () => void;
  position?: { x: number; y: number };
}

export function TextSelectionButton({
  selectedText,
  onAskAboutSelection,
  position,
}: TextSelectionButtonProps) {
  if (!selectedText) {
    return null;
  }

  const style: React.CSSProperties = {
    position: 'fixed',
    zIndex: 9999,
    backgroundColor: '#0066cc',
    color: '#ffffff',
    padding: '8px 16px',
    borderRadius: '6px',
    border: 'none',
    cursor: 'pointer',
    fontSize: '0.875rem',
    fontWeight: 'bold',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
    whiteSpace: 'nowrap',
  };

  // Position near selection if provided
  if (position) {
    style.top = `${position.y}px`;
    style.left = `${position.x}px`;
  } else {
    // Default position
    style.bottom = '80px';
    style.right = '20px';
  }

  return (
    <button
      onClick={onAskAboutSelection}
      style={style}
      onMouseDown={(e) => e.preventDefault()} // Prevent losing selection
    >
      💬 Ask about this
    </button>
  );
}
