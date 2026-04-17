// Pure filter pipeline: search terms (AND across comma-separated tokens) +
// attribute and component selections.
//
// Selection semantics:
//   - within a single group: OR
//   - across groups: AND
//
// selections shape: { attributes: { <at.key>: Set }, components: { <ct.key>: Set } }

export function parseSearchInput(input) {
  return (input || '')
    .split(',')
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

export function emptySelections(taxonomy) {
  const attributes = {};
  for (const at of taxonomy?.attribute_types || []) attributes[at.key] = new Set();
  const components = {};
  for (const ct of taxonomy?.component_types || []) components[ct.key] = new Set();
  return { attributes, components };
}

function matchesAttributes(kb, selected, taxonomy) {
  for (const at of taxonomy.attribute_types) {
    const sel = selected[at.key];
    if (!sel || sel.size === 0) continue;
    const values = kb.attributes?.[at.key] || [];
    let any = false;
    for (const v of values) {
      if (sel.has(v)) { any = true; break; }
    }
    if (!any) return false;
  }
  return true;
}

function matchesComponents(kb, selected, taxonomy) {
  for (const ct of taxonomy.component_types) {
    const sel = selected[ct.key];
    if (!sel || sel.size === 0) continue;
    const set = kb._components?.[ct.key];
    if (!set) return false;
    let any = false;
    for (const brand of sel) {
      if (set.has(brand)) { any = true; break; }
    }
    if (!any) return false;
  }
  return true;
}

function matchesSearch(kb, terms) {
  for (const t of terms) if (!kb._search.includes(t)) return false;
  return true;
}

export function applyFilters(keyboards, terms, selections, taxonomy) {
  return keyboards.filter(
    (kb) =>
      matchesSearch(kb, terms) &&
      matchesAttributes(kb, selections.attributes, taxonomy) &&
      matchesComponents(kb, selections.components, taxonomy)
  );
}
