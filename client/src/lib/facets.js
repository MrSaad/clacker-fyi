// Facet definitions and brand extraction.
//
// Two kinds of facets:
//   1. inferred  -> direct enums on entry.inferred.*
//   2. brands    -> tokens parsed out of free-text entry.parts.*
//
// Brand allowlists are intentionally strict to avoid the long-tail of
// one-off names from 83 entries. Extend as needed.

export const INFERRED_FACETS = [
  { key: 'sound_profile',    label: 'Sound profile' },
  { key: 'build_tier',       label: 'Build tier' },
  { key: 'typing_feel',      label: 'Typing feel' },
  { key: 'build_complexity', label: 'Build complexity' },
  { key: 'aesthetic',        label: 'Aesthetic', multi: true },
];

export const BRAND_GROUPS = [
  {
    key: 'switch_brand',
    label: 'Switch brand',
    fields: ['switches'],
    brands: [
      'Gateron', 'Cherry', 'Kailh', 'JWK', 'Durock', 'Tecsee', 'Zealio',
      'Holy Panda', 'Tangerine', 'Boba', 'Alpaca', 'Sakurio', 'Sakurios',
      'NK Cream', 'Cream', 'Topre', 'Halo', 'Box', 'Outemu', 'TTC',
    ],
  },
  {
    key: 'keycap_brand',
    label: 'Keycap set',
    fields: ['keycaps'],
    brands: [
      'GMK', 'ePBT', 'JTK', 'KAT', 'MT3', 'SA', 'DSA', 'XDA', 'KAM',
      'Drop', 'Domikey', 'Cherry profile', 'PBT', 'Infinikey',
    ],
  },
  {
    key: 'case_brand',
    label: 'Case maker',
    fields: ['case'],
    brands: [
      'Tofu', 'KBDfans', 'Bakeneko', 'Mode', 'TGR', 'V4N4G0N', 'PAW',
      'Satisfaction', 'Think', 'Polaris', 'Discipline', 'Iron165',
      'Norbauer', 'Heavy', 'Salvun', 'Class', 'Frog', 'Lily', 'Rama',
      'Keycult', 'Lin', 'Mr. Suit', 'Singa', 'Owlab',
    ],
  },
];

// Build a lower-cased searchable blob and per-entry brand tags. Mutates and
// returns the input array (cheaper than cloning 83 entries).
export function annotateKeyboards(keyboards) {
  for (const kb of keyboards) {
    const partsText = Object.values(kb.parts || {})
      .filter(Boolean)
      .join(' ');
    const inferredText = [
      kb.inferred?.sound_profile,
      kb.inferred?.build_tier,
      kb.inferred?.typing_feel,
      kb.inferred?.build_complexity,
      ...(kb.inferred?.aesthetic || []),
    ]
      .filter(Boolean)
      .join(' ');
    kb._search = [
      kb.title,
      kb.author,
      partsText,
      inferredText,
      kb.raw?.parts_source_text || '',
    ]
      .join(' ')
      .toLowerCase();

    // Per-entry brand tags: { switch_brand: Set, keycap_brand: Set, case_brand: Set }
    kb._brands = {};
    for (const group of BRAND_GROUPS) {
      const found = new Set();
      const haystack = group.fields
        .map((f) => kb.parts?.[f] || '')
        .join(' ')
        .toLowerCase();
      for (const brand of group.brands) {
        if (haystack.includes(brand.toLowerCase())) {
          found.add(brand);
        }
      }
      kb._brands[group.key] = found;
    }
  }
  return keyboards;
}

// Build a facet index: counts of each value across all keyboards.
// Used to populate the sidebar with stable option lists.
export function buildFacetIndex(keyboards) {
  const inferred = {};
  for (const facet of INFERRED_FACETS) {
    const counts = new Map();
    for (const kb of keyboards) {
      const v = kb.inferred?.[facet.key];
      if (v == null) continue;
      const values = Array.isArray(v) ? v : [v];
      for (const val of values) {
        counts.set(val, (counts.get(val) || 0) + 1);
      }
    }
    inferred[facet.key] = [...counts.entries()]
      .map(([value, count]) => ({ value, count }))
      .sort((a, b) => b.count - a.count);
  }

  const brands = {};
  for (const group of BRAND_GROUPS) {
    const counts = new Map();
    for (const kb of keyboards) {
      for (const brand of kb._brands[group.key]) {
        counts.set(brand, (counts.get(brand) || 0) + 1);
      }
    }
    brands[group.key] = [...counts.entries()]
      .map(([value, count]) => ({ value, count }))
      .sort((a, b) => b.count - a.count);
  }

  return { inferred, brands };
}
