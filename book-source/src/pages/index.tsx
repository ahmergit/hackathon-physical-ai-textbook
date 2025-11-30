import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import HomepageHero from '@site/src/components/HomepageHero';
import TagBlock from '@site/src/components/TagBlock';

export default function Home(): React.JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  const coverImage = useBaseUrl('/img/book-cover.png');

  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Learn humanoid robotics from fundamentals to advanced applications">
      <main>
        <HomepageHero
          coverImage={coverImage}
          title="Physical AI & Humanoid Robotics"
          subtitle="From Fundamentals to Advanced Applications"
          ctaText="Start Reading"
          ctaLink="/docs/preface"
        />
        <TagBlock tags={['Open Source', 'Embodied Intelligence']} />
      </main>
    </Layout>
  );
}
