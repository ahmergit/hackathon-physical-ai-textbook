import React from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './HomepageHero.module.css';

interface HomepageHeroProps {
  coverImage: string;
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
}

export default function HomepageHero({
  coverImage,
  title,
  subtitle,
  ctaText,
  ctaLink,
}: HomepageHeroProps): React.JSX.Element {
  return (
    <section className={styles.hero}>
      <div className={styles.container}>
        {coverImage && (
          <div className={styles.coverWrapper}>
            <img
              src={coverImage}
              alt={`${title} cover`}
              className={styles.cover}
            />
          </div>
        )}
        <div className={styles.content}>
          <Heading as="h1" className={styles.title}>
            {title}
          </Heading>
          <p className={styles.subtitle}>{subtitle}</p>
          <div className={styles.cta}>
            <Link className="button button--primary button--lg" to={ctaLink}>
              {ctaText}
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
