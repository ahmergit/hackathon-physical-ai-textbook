/**
 * Tests for QuickActions component.
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { QuickActions } from '../../src/components/ChatBot/QuickActions';

describe('QuickActions', () => {
  it('should render all quick action buttons', () => {
    const mockOnAction = jest.fn();
    render(<QuickActions onAction={mockOnAction} />);

    expect(screen.getByText(/Explain more/i)).toBeInTheDocument();
    expect(screen.getByText(/Summarize/i)).toBeInTheDocument();
    expect(screen.getByText(/Simplify/i)).toBeInTheDocument();
  });

  it('should call onAction with correct action when clicked', () => {
    const mockOnAction = jest.fn();
    render(<QuickActions onAction={mockOnAction} />);

    fireEvent.click(screen.getByText(/Explain more/i));
    expect(mockOnAction).toHaveBeenCalledWith('explain');

    fireEvent.click(screen.getByText(/Summarize/i));
    expect(mockOnAction).toHaveBeenCalledWith('summarize');

    fireEvent.click(screen.getByText(/Simplify/i));
    expect(mockOnAction).toHaveBeenCalledWith('simplify');
  });

  it('should disable buttons when disabled prop is true', () => {
    const mockOnAction = jest.fn();
    render(<QuickActions onAction={mockOnAction} disabled={true} />);

    const explainButton = screen.getByText(/Explain more/i);
    expect(explainButton).toBeDisabled();

    fireEvent.click(explainButton);
    expect(mockOnAction).not.toHaveBeenCalled();
  });
});
