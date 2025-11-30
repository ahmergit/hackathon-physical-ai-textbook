import React from 'react';
import styles from './TagBlock.module.css';

interface TagBlockProps {
  tags: string[];
}

export default function TagBlock({ tags }: TagBlockProps): React.JSX.Element {
  return (
    <div className={styles.tagBlock}>
      <div className={styles.container}>
        {tags.map((tag, idx) => (
          <span key={idx} className={styles.tag}>
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}
