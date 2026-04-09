export default function SearchBar({ value, onChange }) {
  return (
    <input
      type="search"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Search — comma separated, e.g. gmk, tangerine"
      className="w-full rounded border border-sol-base2 bg-white/60 px-3 py-1.5 text-sm text-sol-base01 placeholder:text-sol-base1 outline-none transition focus:border-sol-blue focus:bg-white"
    />
  );
}
