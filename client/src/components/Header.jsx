import SearchBar from './SearchBar.jsx';

export default function Header({ value, onChange, onOpenFilters }) {
  return (
    <header className="border-b border-sol-base2 bg-sol-base3">
      <div className="mx-auto flex w-full max-w-[1600px] flex-col gap-3 px-5 py-5 md:flex-row md:items-center md:gap-6 md:px-8">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onOpenFilters}
            aria-label="Open filters"
            className="-ml-1 inline-flex h-9 w-9 items-center justify-center rounded text-sol-base01 hover:bg-sol-base2 hover:text-sol-base02 lg:hidden"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
          <h1 className="font-space flex items-center text-2xl font-semibold text-sol-base01 md:text-3xl">
            <span className="flex gap-[3px]">
              {'clacker'.split('').map((letter, i) => (
                <span
                  key={i}
                  className="inline-flex items-center justify-center w-[1.4em] h-[1.4em] bg-sol-base2 border border-sol-base1 border-b-[4px] rounded-lg text-sol-base02 pb-[2px] shadow-sm"
                >
                  {letter}
                </span>
              ))}
            </span>
            <span className="ml-2 text-sol-base01">.fyi</span>
          </h1>
        </div>
        <div className="md:ml-auto md:w-[420px]">
          <SearchBar value={value} onChange={onChange} />
        </div>
      </div>
    </header>
  );
}
