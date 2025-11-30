import React from 'react';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import Link from '@docusaurus/Link';
import styles from './Breadcrumbs.module.css';

interface BreadcrumbItem {
  label: string;
  path?: string;
}

export default function Breadcrumbs(): React.JSX.Element | null {
  const { metadata } = useDoc();

  // Build breadcrumb trail from the sidebar position and path
  const breadcrumbs: BreadcrumbItem[] = [];

  // Extract breadcrumb hierarchy from the document path
  const pathParts = metadata.id.split('/');

  // Add Home
  breadcrumbs.push({ label: 'Home', path: '/docs/preface' });

  // Parse the path to extract Part, Chapter, and Lesson
  if (pathParts.length > 0) {
    // Check if this is a structured path (part-X-*/chapter-X-*/lesson-X-*)
    let currentPath = '';

    pathParts.forEach((part, index) => {
      if (part.startsWith('part-')) {
        // Extract part name
        const partLabel = part.replace(/^part-\d+-/, '').replace(/-/g, ' ');
        currentPath += part;
        breadcrumbs.push({
          label: `Part: ${partLabel.charAt(0).toUpperCase() + partLabel.slice(1)}`,
          path: `/docs/${currentPath}`
        });
        currentPath += '/';
      } else if (part.startsWith('chapter-')) {
        // Extract chapter name
        const chapterLabel = part.replace(/^chapter-\d+-/, '').replace(/-/g, ' ');
        currentPath += part;
        breadcrumbs.push({
          label: `Chapter: ${chapterLabel.charAt(0).toUpperCase() + chapterLabel.slice(1)}`,
          path: `/docs/${currentPath}`
        });
        currentPath += '/';
      } else if (part.startsWith('lesson-') || index === pathParts.length - 1) {
        // This is the current page (lesson)
        if (metadata.title) {
          breadcrumbs.push({
            label: metadata.title
          });
        }
      }
    });
  }

  // Only show breadcrumbs if we have more than just "Docs"
  if (breadcrumbs.length <= 1) {
    return null;
  }

  return (
    <nav className={styles.breadcrumbs} aria-label="Breadcrumb navigation">
      <ol className={styles.breadcrumbList}>
        {breadcrumbs.map((crumb, index) => (
          <li key={index} className={styles.breadcrumbItem}>
            {crumb.path ? (
              <Link to={crumb.path} className={styles.breadcrumbLink}>
                {crumb.label}
              </Link>
            ) : (
              <span className={styles.breadcrumbCurrent}>{crumb.label}</span>
            )}
            {index < breadcrumbs.length - 1 && (
              <span className={styles.breadcrumbSeparator} aria-hidden="true">
                →
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
