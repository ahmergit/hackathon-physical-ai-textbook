import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'From Fundamentals to Advanced Applications',
  favicon: 'img/logo.svg',

  // Set the production url of your site here
  url: 'https://yourusername.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/physical-ai-humaniod-robotics/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'yourusername', // Usually your GitHub org/user name.
  projectName: 'physical-ai-humaniod-robotics', // Usually your repo name.
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  // Markdown configuration (replaces deprecated onBrokenMarkdownLinks)
  markdown: {
    mermaid: true,
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: ['@docusaurus/theme-mermaid'],

  themeConfig: {
    // Social card for link previews (Open Graph, Twitter)
    image: 'img/social-card.jpg',
    metadata: [
      {name: 'keywords', content: 'physical ai, humanoid robotics, embodied intelligence, robotics, artificial intelligence, machine learning'},
      {name: 'description', content: 'Comprehensive guide to Physical AI and Humanoid Robotics - from fundamentals to advanced applications. Learn about embodied intelligence, robot design, control systems, and real-world implementations.'},
      {name: 'author', content: 'Physical AI & Humanoid Robotics Team'},
      {property: 'og:title', content: 'Physical AI & Humanoid Robotics'},
      {property: 'og:description', content: 'Comprehensive guide to Physical AI and Humanoid Robotics - from fundamentals to advanced applications.'},
      {property: 'og:type', content: 'website'},
      {property: 'og:image', content: 'img/social-card.jpg'},
      {name: 'twitter:card', content: 'summary_large_image'},
      {name: 'twitter:title', content: 'Physical AI & Humanoid Robotics'},
      {name: 'twitter:description', content: 'Comprehensive guide to Physical AI and Humanoid Robotics - from fundamentals to advanced applications.'},
      {name: 'twitter:image', content: 'img/social-card.jpg'},
    ],
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          href: 'https://github.com/yourusername/physical-ai-humaniod-robotics',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
