// Mock for @docusaurus/* imports
module.exports = {
  useDocusaurusContext: () => ({
    siteConfig: {
      title: 'Test Site',
      tagline: 'Test Tagline',
    },
  }),
  Link: ({ children, to }) => children,
  useBaseUrl: (url) => url,
  Translate: ({ children }) => children,
  translate: (msg) => msg.message || msg,
};
