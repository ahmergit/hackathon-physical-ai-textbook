import React, { useState } from 'react';
import styles from './PersonalizeButton.module.css';

export type SkillLevel = 'Beginner' | 'Intermediate' | 'Advanced';

interface PersonalizeButtonProps {
  lessonId: string;
  levels?: SkillLevel[];
  defaultLevel?: SkillLevel;
  className?: string;
  onLevelChange?: (level: SkillLevel) => void;
}

const LEVEL_DESCRIPTIONS: Record<SkillLevel, string> = {
  Beginner: 'Clear explanations with foundational concepts and simple examples',
  Intermediate: 'Technical depth with practical applications and implementation details',
  Advanced: 'Expert-level analysis with research insights and cutting-edge techniques',
};

export default function PersonalizeButton({
  lessonId,
  levels = ['Beginner', 'Intermediate', 'Advanced'],
  defaultLevel = 'Beginner',
  className = '',
  onLevelChange,
}: PersonalizeButtonProps): React.ReactElement {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedLevel, setSelectedLevel] = useState<SkillLevel>(defaultLevel);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const selectLevel = (level: SkillLevel) => {
    setSelectedLevel(level);
    setIsOpen(false);
    if (onLevelChange) {
      onLevelChange(level);
    }
  };

  return (
    <div className={`${styles.personalizeContainer} ${className}`}>
      <button
        className={styles.personalizeButton}
        onClick={toggleMenu}
        aria-expanded={isOpen}
        aria-label="Personalize content difficulty"
      >
        <span className={styles.icon}>🎯</span>
        <span className={styles.buttonText}>
          Personalize: <strong>{selectedLevel}</strong>
        </span>
        <span className={styles.arrow}>{isOpen ? '▲' : '▼'}</span>
      </button>
      {isOpen && (
        <div className={styles.menu} role="menu">
          {levels.map((level) => (
            <button
              key={level}
              className={`${styles.menuItem} ${
                level === selectedLevel ? styles.active : ''
              }`}
              onClick={() => selectLevel(level)}
              role="menuitem"
              aria-label={`Set difficulty to ${level}`}
            >
              <span className={styles.levelName}>{level}</span>
              <span className={styles.levelDescription}>
                {LEVEL_DESCRIPTIONS[level]}
              </span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
