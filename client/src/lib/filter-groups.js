// Client-side filter helpers. The taxonomy (attribute types, values, brand
// tags) is fetched from the server — this module only handles per-keyboard
// annotation and counting.

export function annotateKeyboards(keyboards) {
  for (const kb of keyboards) {
    const componentsText = Object.values(kb.components || {})
      .filter(Boolean)
      .join(' ');
    const attrText = Object.values(kb.attributes || {})
      .flat()
      .filter(Boolean)
      .join(' ');
    kb._search = [
      kb.title,
      kb.author,
      componentsText,
      attrText,
      kb.raw?.parts_source_text || '',
    ]
      .join(' ')
      .toLowerCase();

    // Per-entry component brand tags as Sets, keyed by component_type.key.
    kb._components = {};
    for (const [ctKey, brands] of Object.entries(kb.component_brands || {})) {
      kb._components[ctKey] = new Set(brands);
    }
  }
  return keyboards;
}

export function buildFilterIndex(keyboards, taxonomy) {
  const attributes = {};
  for (const at of taxonomy.attribute_types) {
    const counts = new Map();
    for (const kb of keyboards) {
      for (const v of kb.attributes?.[at.key] || []) {
        counts.set(v, (counts.get(v) || 0) + 1);
      }
    }
    attributes[at.key] = [...counts.entries()]
      .map(([value, count]) => ({ value, count }))
      .sort((a, b) => b.count - a.count);
  }

  const components = {};
  for (const ct of taxonomy.component_types) {
    const counts = new Map();
    for (const kb of keyboards) {
      const set = kb._components?.[ct.key];
      if (!set) continue;
      for (const label of set) counts.set(label, (counts.get(label) || 0) + 1);
    }
    components[ct.key] = [...counts.entries()]
      .map(([value, count]) => ({ value, count }))
      .sort((a, b) => b.count - a.count);
  }

  return { attributes, components };
}
