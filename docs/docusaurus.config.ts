import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Uncanny',
  tagline: 'Detect AI-generated text from your terminal',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://dunkinfrunkin.github.io',
  baseUrl: '/docs/',

  organizationName: 'dunkinfrunkin',
  projectName: 'uncanny',

  onBrokenLinks: 'throw',

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
          routeBasePath: '/',
          editUrl:
            'https://github.com/dunkinfrunkin/uncanny/tree/main/docs/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'uncanny',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/benchmarks',
          label: 'Benchmarks',
          position: 'left',
        },
        {
          href: 'https://github.com/dunkinfrunkin/uncanny',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Getting Started', to: '/' },
            { label: 'CLI Reference', to: '/cli-reference' },
            { label: 'Analyzers', to: '/analyzers/overview' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'GitHub Issues', href: 'https://github.com/dunkinfrunkin/uncanny/issues' },
            { label: 'Contributing', href: 'https://github.com/dunkinfrunkin/uncanny/blob/main/CONTRIBUTING.md' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'GitHub', href: 'https://github.com/dunkinfrunkin/uncanny' },
            { label: 'PyPI', href: 'https://pypi.org/project/uncanny/' },
          ],
        },
      ],
      copyright: `MIT License · ${new Date().getFullYear()} Uncanny`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
