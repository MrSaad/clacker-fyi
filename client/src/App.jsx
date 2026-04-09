import { useEffect, useMemo, useState, useCallback } from 'react';
import { fetchKeyboards } from './lib/api.js';
import { annotateKeyboards, buildFacetIndex } from './lib/facets.js';
import { applyFilters, parseSearchInput, emptySelections } from './lib/filter.js';
import Header from './components/Header.jsx';
import FacetSidebar from './components/FacetSidebar.jsx';
import KeyboardGrid from './components/KeyboardGrid.jsx';
import DetailModal from './components/DetailModal.jsx';

export default function App() {
  const [keyboards, setKeyboards] = useState(null);
  const [error, setError] = useState(null);
  const [searchInput, setSearchInput] = useState('');
  const [selections, setSelections] = useState(() => emptySelections());
  const [selected, setSelected] = useState(null);
  const [filtersOpen, setFiltersOpen] = useState(false);

  useEffect(() => {
    if (!filtersOpen) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = prev;
    };
  }, [filtersOpen]);

  useEffect(() => {
    if (!filtersOpen) return;
    const onKey = (e) => {
      if (e.key === 'Escape') setFiltersOpen(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [filtersOpen]);

  useEffect(() => {
    fetchKeyboards()
      .then((data) => {
        annotateKeyboards(data);
        data.sort((a, b) => (b.score || 0) - (a.score || 0));
        setKeyboards(data);
      })
      .catch((e) => setError(e.message));
  }, []);

  const facetIndex = useMemo(
    () => (keyboards ? buildFacetIndex(keyboards) : null),
    [keyboards]
  );

  const terms = useMemo(() => parseSearchInput(searchInput), [searchInput]);

  const filtered = useMemo(() => {
    if (!keyboards) return [];
    return applyFilters(keyboards, terms, selections);
  }, [keyboards, terms, selections]);

  const toggleFacet = useCallback((kind, group, value) => {
    setSelections((prev) => {
      const next = {
        inferred: { ...prev.inferred },
        brands: { ...prev.brands },
      };
      const set = new Set(next[kind][group]);
      if (set.has(value)) set.delete(value);
      else set.add(value);
      next[kind][group] = set;
      return next;
    });
  }, []);

  const clearAll = useCallback(() => {
    setSelections(emptySelections());
    setSearchInput('');
  }, []);

  if (error) {
    return (
      <div className="flex h-full items-center justify-center font-mono text-xs uppercase tracking-widest text-red-400">
        failed to load — {error}
      </div>
    );
  }

  return (
    <div className="flex min-h-full flex-col">
      <Header
        value={searchInput}
        onChange={setSearchInput}
        onOpenFilters={() => setFiltersOpen(true)}
      />
      <main className="mx-auto flex w-full max-w-[1600px] flex-1 gap-6 px-4 py-4 md:px-6">
        <FacetSidebar
          facetIndex={facetIndex}
          selections={selections}
          onToggle={toggleFacet}
          onClear={clearAll}
          mobileOpen={filtersOpen}
          onMobileClose={() => setFiltersOpen(false)}
        />
        <div className="min-w-0 flex-1">
          {keyboards == null ? (
            <div className="font-mono text-[10px] uppercase tracking-[0.22em] text-ink-500">
              loading specimens…
            </div>
          ) : (
            <KeyboardGrid keyboards={filtered} onSelect={setSelected} />
          )}
        </div>
      </main>
      {selected && (
        <DetailModal keyboard={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
