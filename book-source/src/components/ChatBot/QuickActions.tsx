/**
 * Quick action buttons for assistant messages.
 */

import React from 'react';

interface QuickActionsProps {
  onAction: (action: 'explain' | 'summarize' | 'simplify') => void;
  disabled?: boolean;
}

export function QuickActions({ onAction, disabled = false }: QuickActionsProps) {
  const actions = [
    { id: 'explain' as const, label: '🔍 Explain more', title: 'Get a more detailed explanation' },
    { id: 'summarize' as const, label: '📝 Summarize', title: 'Get a concise summary' },
    { id: 'simplify' as const, label: '💡 Simplify', title: 'Get a simpler explanation' },
  ];

  return (
    <div
      style={{
        display: 'flex',
        gap: '8px',
        marginTop: '8px',
        flexWrap: 'wrap',
      }}
    >
      {actions.map((action) => (
        <button
          key={action.id}
          onClick={() => onAction(action.id)}
          disabled={disabled}
          title={action.title}
          style={{
            padding: '6px 12px',
            fontSize: '0.75rem',
            backgroundColor: disabled ? '#e0e0e0' : '#f0f0f0',
            color: disabled ? '#999' : '#333',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: disabled ? 'not-allowed' : 'pointer',
            transition: 'background-color 0.2s',
          }}
          onMouseEnter={(e) => {
            if (!disabled) {
              e.currentTarget.style.backgroundColor = '#e0e0e0';
            }
          }}
          onMouseLeave={(e) => {
            if (!disabled) {
              e.currentTarget.style.backgroundColor = '#f0f0f0';
            }
          }}
        >
          {action.label}
        </button>
      ))}
    </div>
  );
}
