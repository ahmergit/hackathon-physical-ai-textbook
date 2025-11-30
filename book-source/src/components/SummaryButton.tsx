import React, { useState } from 'react';
import styles from './SummaryButton.module.css';

interface SummaryButtonProps {
  lessonId: string;
  title?: string;
  className?: string;
  icon?: string;
}

const MOCK_SUMMARIES: Record<string, string> = {
  'lesson-01': 'Physical AI combines artificial intelligence with physical embodiment, enabling systems to interact directly with the real world. Unlike purely digital AI, Physical AI requires perception, planning, and action capabilities grounded in sensorimotor experience.',
  'lesson-02': 'Embodied intelligence emphasizes that true intelligence requires physical interaction with the environment. Sensorimotor grounding and real-world feedback loops enable adaptive behavior that purely digital systems cannot achieve.',
  'lesson-03': 'AI systems have evolved from language-only models (LLMs) to multimodal vision-language-action systems. Modern Physical AI integrates perception, reasoning, and action to enable robots to understand and manipulate their environment.',
  'lesson-04': 'The Embodied AI Pipeline follows a Perception → Planning → Action workflow. Robots sense their environment through sensors, plan actions using reasoning systems, and execute physical movements through actuators.',
  'lesson-05': 'Traditional robotics approaches using hand-crafted rules and brittle pipelines fail in complex, dynamic environments. Modern embodied AI leverages learning-based methods, enabling robots to adapt and generalize across diverse scenarios.',
};

export default function SummaryButton({
  lessonId,
  title = 'AI Summary',
  className = '',
  icon = '✨',
}: SummaryButtonProps): React.ReactElement {
  const [isOpen, setIsOpen] = useState(false);
  const summary = MOCK_SUMMARIES[lessonId] || 'Summary not available for this lesson.';

  const toggleSummary = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`${styles.summaryContainer} ${className}`}>
      <button
        className={styles.summaryButton}
        onClick={toggleSummary}
        aria-expanded={isOpen}
        aria-label={`${isOpen ? 'Hide' : 'Show'} ${title}`}
      >
        <span className={styles.icon}>{icon}</span>
        <span className={styles.buttonText}>{title}</span>
        <span className={styles.arrow}>{isOpen ? '▲' : '▼'}</span>
      </button>
      {isOpen && (
        <div className={styles.summaryContent} role="region" aria-label={title}>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}
