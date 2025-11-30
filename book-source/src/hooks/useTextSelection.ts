/**
 * Hook for detecting text selection on the page.
 */

import { useState, useEffect } from 'react';

export function useTextSelection() {
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [selectionRange, setSelectionRange] = useState<Range | null>(null);

  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();

      if (!selection || selection.rangeCount === 0) {
        setSelectedText(null);
        setSelectionRange(null);
        return;
      }

      const text = selection.toString().trim();

      if (text.length > 0) {
        setSelectedText(text);
        try {
          setSelectionRange(selection.getRangeAt(0).cloneRange());
        } catch (e) {
          console.error('Error getting selection range:', e);
          setSelectionRange(null);
        }
      } else {
        setSelectedText(null);
        setSelectionRange(null);
      }
    };

    document.addEventListener('selectionchange', handleSelectionChange);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
    };
  }, []);

  const clearSelection = () => {
    setSelectedText(null);
    setSelectionRange(null);
    window.getSelection()?.removeAllRanges();
  };

  return {
    selectedText,
    selectionRange,
    clearSelection,
  };
}
