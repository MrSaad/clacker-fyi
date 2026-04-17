import { useState } from 'react';

function FilterSection({ label, options, selected, onToggle }) {
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

export default function FilterSidebar({
  taxonomy,
  filterIndex,
  selections,
  onToggle,
  onClear,
  mobileOpen,
  onMobileClose,
}) {
  if (!taxonomy || !filterIndex || !selections)
    return <aside className="hidden w-56 shrink-0 lg:block" />;

  const groups = [
    ...taxonomy.attribute_types.map((at) => ({
      kind: 'attributes',
      key: at.key,
      label: at.label,
      options: filterIndex.attributes[at.key],
      selected: selections.attributes[at.key],
    })),
    ...taxonomy.component_types.map((ct) => ({
      kind: 'components',
      key: ct.key,
      label: ct.label,
      options: filterIndex.components[ct.key],
      selected: selections.components[ct.key],
    })),
  ];

  const inner = (
    <>
      <div className="flex items-center justify-between pb-1">
        <span className="text-xs font-semibold uppercase tracking-wide text-sol-base01">
          Filters
        </span>
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onClear}
            className="text-[11px] text-reddit hover:underline"
          >
            clear
          </button>
          <button
            type="button"
            onClick={onMobileClose}
            aria-label="Close filters"
            className="text-lg leading-none text-sol-base01 hover:text-sol-base02 lg:hidden"
          >
            ×
          </button>
        </div>
      </div>
      {groups.map((g) => (
        <FilterSection
          key={`${g.kind}.${g.key}`}
          label={g.label}
          options={g.options}
          selected={g.selected}
          onToggle={(v) => onToggle(g.kind, g.key, v)}
        />
      ))}
      <div className="h-6" />
    </>
  );

  return (
    <>
      <aside className="hidden w-56 shrink-0 lg:block">
        <div className="fancy-scroll sticky top-4 max-h-[calc(100vh-32px)] overflow-y-auto pr-2">
          {inner}
        </div>
      </aside>

      <div
        className={`fixed inset-0 z-40 lg:hidden ${mobileOpen ? '' : 'pointer-events-none'}`}
        aria-hidden={!mobileOpen}
      >
        <div
          onClick={onMobileClose}
          className={`absolute inset-0 bg-black/40 transition-opacity duration-200 ${
            mobileOpen ? 'opacity-100' : 'opacity-0'
          }`}
        />
        <aside
          className={`fancy-scroll absolute left-0 top-0 h-full w-72 max-w-[85vw] overflow-y-auto border-r border-sol-base2 bg-sol-base3 px-4 py-4 shadow-xl transition-transform duration-200 ease-out ${
            mobileOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          {inner}
        </aside>
      </div>
    </>
  );
}
