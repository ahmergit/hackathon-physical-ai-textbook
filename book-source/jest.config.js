/** @type {import('jest').Config} */
const config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/tests'],
  
  // Only run unit/integration tests, not e2e (Playwright handles those)
  testMatch: [
    '**/tests/**/*.test.ts',
    '**/tests/**/*.test.tsx',
  ],
  
  // Exclude e2e tests (these use Playwright, not Jest)
  testPathIgnorePatterns: [
    '/node_modules/',
    '/tests/e2e/',
  ],
  
  // TypeScript transformation
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: 'tsconfig.json',
    }],
  },
  
  // Module resolution for Docusaurus paths
  moduleNameMapper: {
    // Handle CSS modules
    '\\.module\\.css$': 'identity-obj-proxy',
    '\\.css$': '<rootDir>/tests/__mocks__/styleMock.js',
    
    // Docusaurus aliases
    '^@docusaurus/(.*)$': '<rootDir>/tests/__mocks__/docusaurus.js',
    '^@site/(.*)$': '<rootDir>/$1',
    '^@theme/(.*)$': '<rootDir>/tests/__mocks__/theme.js',
  },
  
  // Setup file
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  
  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
  ],
};

module.exports = config;
