/**
 * Citation component for displaying textbook references.
 */

import React from 'react';
import type { Citation as CitationType } from '../../services/chatApi';

interface CitationProps {
  citation: CitationType;
  index: number;
}

export function Citation({ citation, index }: CitationProps) {
  return (
    <a
      href={citation.url}
      className="citation"
      title={citation.snippet || `Go to ${citation.title}`}
      target="_self"
      style={{
        display: 'inline-block',
        marginLeft: '4px',
        padding: '2px 6px',
        fontSize: '0.75rem',
        fontWeight: 'bold',
        color: '#0066cc',
        textDecoration: 'none',
        backgroundColor: '#e6f2ff',
        borderRadius: '4px',
        border: '1px solid #99ccff',
      }}
    >
      [{index + 1}]
    </a>
  );
}

interface CitationListProps {
  citations: CitationType[];
}

export function CitationList({ citations }: CitationListProps) {
  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <div
      className="citation-list"
      style={{
        marginTop: '12px',
        padding: '12px',
        backgroundColor: '#f5f5f5',
        borderRadius: '6px',
        fontSize: '0.875rem',
      }}
    >
      <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
        Sources:
      </div>
      <ul style={{ margin: 0, paddingLeft: '20px' }}>
        {citations.map((citation, index) => (
          <li key={index} style={{ marginBottom: '4px' }}>
            <a
              href={citation.url}
              target="_self"
              style={{ color: '#0066cc', textDecoration: 'none' }}
            >
              [{index + 1}] {citation.title}
            </a>
            {citation.snippet && (
              <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '2px' }}>
                "{citation.snippet}"
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
