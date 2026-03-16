import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'intro',
    'installation',
    'quickstart',
    'cli-reference',
    {
      type: 'category',
      label: 'Analyzers',
      items: [
        'analyzers/overview',
        'analyzers/compression',
        'analyzers/burstiness',
        'analyzers/perplexity',
        'analyzers/ensemble',
      ],
    },
    'visualizer',
    'benchmarks',
    'ci-integration',
    'limitations',
  ],
};

export default sidebars;
