// Filter group definitions for the sidebar.
//
// Two kinds of filters:
//   1. attributes — enum-like values on entry.inferred.* (sound profile,
//      build tier, etc). The data layer already picks the value per entry.
//   2. components — brands/materials parsed out of free-text entry.parts.*
//      (switches, keycaps, case, plate, stabilizers). Allowlists are
//      intentionally strict to avoid long-tail one-offs from 83 entries.
//
// Component brand entries are either a string (label doubles as the match
// token) or { label, aliases: [...] } for when several raw spellings collapse
// to one displayed value (e.g. "polycarbonate" / "polycarb" / "PC").

export const ATTRIBUTE_GROUPS = [
  { key: 'sound_profile',    label: 'Sound profile' },
  { key: 'build_tier',       label: 'Build tier' },
  { key: 'typing_feel',      label: 'Typing feel' },
  { key: 'build_complexity', label: 'Build complexity' },
  { key: 'color',            label: 'Color', multi: true },
  { key: 'theme',            label: 'Theme', multi: true },
];

// Aesthetic tags that should appear under "Color". Everything else in the
// aesthetic array falls through to "Theme". Match is case-insensitive.
const COLOR_TAGS = new Set([
  'bow', 'wob', 'pink', 'white', 'blue', 'purple', 'black', 'brass',
  'beige', 'grey', 'red', 'green', 'gold', 'copper', 'rose gold',
  'peach', 'cream', 'lilac', 'coral', 'cyan', 'brown', 'smoke',
  'eggplant', 'neon', 'rainbow', 'monochrome', 'pastel', 'dark',
  'warm', 'colorful', 'translucent', 'frosted', 'polished', 'patina',
]);

export const COMPONENT_GROUPS = [
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
  {
    key: 'plate_material',
    label: 'Plate material',
    fields: ['plate'],
    brands: [
      { label: 'Polycarbonate', aliases: ['polycarbonate', 'polycarb', 'pc'] },
      'Brass',
      'Aluminum',
      'FR4',
      'Copper',
      'POM',
      'Carbon fiber',
      'Stainless steel',
    ],
  },
  {
    key: 'stabilizer_brand',
    label: 'Stabilizers',
    fields: ['stabilizers'],
    brands: [
      'Durock', 'Cherry', 'Zeal', 'C3', 'TX', 'Gateron', 'Everglide',
      'GMK', 'Ultramarine',
    ],
  },
];

// Build a lower-cased searchable blob and per-entry component tags. Mutates
// and returns the input array (cheaper than cloning 83 entries).
export function annotateKeyboards(keyboards) {
  for (const kb of keyboards) {
    // Split the aesthetic grab-bag into color tags (from allowlist) and
    // everything else (theme). Preserves original casing.
    const aesthetic = kb.inferred?.aesthetic || [];
    const color = [];
    const theme = [];
    for (const tag of aesthetic) {
      if (COLOR_TAGS.has(tag.toLowerCase())) color.push(tag);
      else theme.push(tag);
    }
    kb.inferred = { ...(kb.inferred || {}), color, theme };

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

    // Per-entry component tags, one Set per group keyed by display label.
    kb._components = {};
    for (const group of COMPONENT_GROUPS) {
      const found = new Set();
      const haystack = group.fields
        .map((f) => kb.parts?.[f] || '')
        .join(' ')
        .toLowerCase();
      for (const brand of group.brands) {
        const label = typeof brand === 'string' ? brand : brand.label;
        const aliases =
          typeof brand === 'string' ? [brand] : brand.aliases;
        if (aliases.some((a) => haystack.includes(a.toLowerCase()))) {
          found.add(label);
        }
      }
      kb._components[group.key] = found;
    }
  }
  return keyboards;
}

// Build counts for every option across all keyboards — drives the sidebar.
export function buildFilterIndex(keyboards) {
  const attributes = {};
  for (const group of ATTRIBUTE_GROUPS) {
    const counts = new Map();
    for (const kb of keyboards) {
      const v = kb.inferred?.[group.key];
      if (v == null) continue;
      const values = Array.isArray(v) ? v : [v];
      for (const val of values) {
        counts.set(val, (counts.get(val) || 0) + 1);
      }
    }
    attributes[group.key] = [...counts.entries()]
      .map(([value, count]) => ({ value, count }))
      .sort((a, b) => b.count - a.count);
  }

  const components = {};
  for (const group of COMPONENT_GROUPS) {
    const counts = new Map();
    for (const kb of keyboards) {
      for (const brand of kb._components[group.key]) {
        counts.set(brand, (counts.get(brand) || 0) + 1);
      }
    }
    components[group.key] = [...counts.entries()]
      .map(([value, count]) => ({ value, count }))
      .sort((a, b) => b.count - a.count);
  }

  return { attributes, components };
}
