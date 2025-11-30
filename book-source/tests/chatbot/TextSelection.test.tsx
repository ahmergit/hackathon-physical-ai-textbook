/**
 * Tests for text selection functionality.
 */

import { renderHook, act } from '@testing-library/react';
import { useTextSelection } from '../../src/hooks/useTextSelection';

describe('useTextSelection', () => {
  it('should detect text selection', () => {
    const { result } = renderHook(() => useTextSelection());

    expect(result.current.selectedText).toBeNull();

    // Simulate text selection
    const mockSelection = {
      toString: () => 'Physical AI',
      rangeCount: 1,
      getRangeAt: () => ({
        cloneRange: () => ({} as Range),
      }),
      removeAllRanges: jest.fn(),
    };

    Object.defineProperty(window, 'getSelection', {
      writable: true,
      value: () => mockSelection,
    });

    // Trigger selectionchange event
    act(() => {
      document.dispatchEvent(new Event('selectionchange'));
    });

    expect(result.current.selectedText).toBe('Physical AI');
  });

  it('should clear selection', () => {
    const { result } = renderHook(() => useTextSelection());

    const mockSelection = {
      toString: () => '',
      rangeCount: 0,
      removeAllRanges: jest.fn(),
    };

    Object.defineProperty(window, 'getSelection', {
      writable: true,
      value: () => mockSelection,
    });

    act(() => {
      result.current.clearSelection();
    });

    expect(result.current.selectedText).toBeNull();
    expect(mockSelection.removeAllRanges).toHaveBeenCalled();
  });
});
