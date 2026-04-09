// Pure filter pipeline: search terms (AND across comma-separated tokens) +
// facet selections. Facet semantics:
//   - within a single facet group: OR
//   - across facet groups: AND
//
// selectedFacets shape:
//   {
//     inferred: { sound_profile: Set, build_tier: Set, ... },
//     brands:   { switch_brand: Set, keycap_brand: Set, case_brand: Set },
//   }

import { INFERRED_FACETS, BRAND_GROUPS } from './facets.js';

export function parseSearchInput(input) {
  return (input || '')
    .split(',')
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

export function emptySelections() {
  const inferred = {};
  for (const f of INFERRED_FACETS) inferred[f.key] = new Set();
  const brands = {};
  for (const g of BRAND_GROUPS) brands[g.key] = new Set();
  return { inferred, brands };
}

function matchesInferred(kb, selectedInferred) {
  for (const facet of INFERRED_FACETS) {
    const sel = selectedInferred[facet.key];
    if (!sel || sel.size === 0) continue;
    const v = kb.inferred?.[facet.key];
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

function matchesBrands(kb, selectedBrands) {
  for (const group of BRAND_GROUPS) {
    const sel = selectedBrands[group.key];
    if (!sel || sel.size === 0) continue;
    let any = false;
    for (const brand of sel) {
      if (kb._brands[group.key].has(brand)) {
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
      matchesInferred(kb, selections.inferred) &&
      matchesBrands(kb, selections.brands)
  );
}
