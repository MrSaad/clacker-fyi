export default function SearchBar({ value, onChange }) {
  return (
    <div className="group relative">
      <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-sol-base1 transition-colors group-focus-within:text-reddit">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="11" cy="11" r="7" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </span>
      <input
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search — comma separated, e.g. gmk, tangerine"
        className="w-full rounded-full border border-sol-base2 bg-white/70 py-2 pl-9 pr-9 text-sm text-sol-base01 placeholder:text-sol-base1 shadow-sm outline-none transition focus:border-reddit focus:bg-white focus:shadow-md focus:ring-2 focus:ring-reddit/20"
      />
      {value && (
        <button
          type="button"
          onClick={() => onChange('')}
          aria-label="Clear search"
          className="absolute right-2 top-1/2 flex h-6 w-6 -translate-y-1/2 items-center justify-center rounded-full text-sol-base1 hover:bg-sol-base2 hover:text-sol-base01"
        >
          ×
        </button>
      )}
    </div>
  );
}
