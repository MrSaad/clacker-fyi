import { useState } from 'react';
import { INFERRED_FACETS, BRAND_GROUPS } from '../lib/facets.js';

function FacetGroup({ label, options, selected, onToggle }) {
  const [open, setOpen] = useState(true);
  if (!options || options.length === 0) return null;
  return (
    <div className="border-t border-sol-base2 py-3">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center justify-between text-left text-xs font-semibold uppercase tracking-wide text-sol-base01 hover:text-sol-base02"
      >
        <span>{label}</span>
        <span className="text-sol-base1">{open ? '−' : '+'}</span>
      </button>
      {open && (
        <ul className="mt-2 space-y-0.5">
          {options.map(({ value, count }) => {
            const isSelected = selected.has(value);
            return (
              <li key={value}>
                <label className="flex cursor-pointer items-center gap-2 py-0.5 text-[13px] text-sol-base00 hover:text-sol-base01">
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => onToggle(value)}
                    className="h-3.5 w-3.5 accent-sol-blue"
                  />
                  <span className="flex-1 truncate">{value}</span>
                  <span className="text-[11px] tabular-nums text-sol-base1">
                    {count}
                  </span>
                </label>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

export default function FacetSidebar({
  facetIndex,
  selections,
  onToggle,
  onClear,
}) {
  if (!facetIndex) return <aside className="hidden w-56 lg:block" />;

  const groups = [
    ...INFERRED_FACETS.map((f) => ({
      kind: 'inferred',
      key: f.key,
      label: f.label,
      options: facetIndex.inferred[f.key],
      selected: selections.inferred[f.key],
    })),
    ...BRAND_GROUPS.map((g) => ({
      kind: 'brands',
      key: g.key,
      label: g.label,
      options: facetIndex.brands[g.key],
      selected: selections.brands[g.key],
    })),
  ];

  return (
    <aside className="hidden w-56 shrink-0 lg:block">
      <div className="fancy-scroll sticky top-4 max-h-[calc(100vh-32px)] overflow-y-auto pr-2">
        <div className="flex items-center justify-between pb-1">
          <span className="text-xs font-semibold uppercase tracking-wide text-sol-base01">
            Filters
          </span>
          <button
            type="button"
            onClick={onClear}
            className="text-[11px] text-sol-blue hover:underline"
          >
            clear
          </button>
        </div>
        {groups.map((g) => (
          <FacetGroup
            key={`${g.kind}.${g.key}`}
            label={g.label}
            options={g.options}
            selected={g.selected}
            onToggle={(v) => onToggle(g.kind, g.key, v)}
          />
        ))}
        <div className="h-6" />
      </div>
    </aside>
  );
}
