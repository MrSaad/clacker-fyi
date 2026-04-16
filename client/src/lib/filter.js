// Pure filter pipeline: search terms (AND across comma-separated tokens) +
// attribute and component selections.
//
// Selection semantics:
//   - within a single group: OR
//   - across groups (including across the attributes/components split): AND
//
// selections shape:
//   {
//     attributes: { sound_profile: Set, build_tier: Set, ... },
//     components: { switch_brand: Set, keycap_brand: Set, ... },
//   }

import { ATTRIBUTE_GROUPS, COMPONENT_GROUPS } from './filter-groups.js';

export function parseSearchInput(input) {
  return (input || '')
    .split(',')
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

export function emptySelections() {
  const attributes = {};
  for (const g of ATTRIBUTE_GROUPS) attributes[g.key] = new Set();
  const components = {};
  for (const g of COMPONENT_GROUPS) components[g.key] = new Set();
  return { attributes, components };
}

function matchesAttributes(kb, selected) {
  for (const group of ATTRIBUTE_GROUPS) {
    const sel = selected[group.key];
    if (!sel || sel.size === 0) continue;
    const v = kb.inferred?.[group.key];
    if (v == null) return false;
    const values = Array.isArray(v) ? v : [v];
    let any = false;
    for (const val of values) {
      if (sel.has(val)) {
        any = true;
        break;
      }
    }
    if (!any) return false;
  }
  return true;
}

function matchesComponents(kb, selected) {
  for (const group of COMPONENT_GROUPS) {
    const sel = selected[group.key];
    if (!sel || sel.size === 0) continue;
    let any = false;
    for (const brand of sel) {
      if (kb._components[group.key].has(brand)) {
        any = true;
        break;
      }
    }
    if (!any) return false;
  }
  return true;
}

function matchesSearch(kb, terms) {
  for (const t of terms) {
    if (!kb._search.includes(t)) return false;
  }
  return true;
}

export function applyFilters(keyboards, terms, selections) {
  return keyboards.filter(
    (kb) =>
      matchesSearch(kb, terms) &&
      matchesAttributes(kb, selections.attributes) &&
      matchesComponents(kb, selections.components)
  );
}
