import SearchBar from './SearchBar.jsx';

export default function Header({ value, onChange }) {
  return (
    <header className="border-b border-sol-base2 bg-sol-base3">
      <div className="mx-auto flex w-full max-w-[1600px] flex-col gap-3 px-5 py-5 md:flex-row md:items-center md:gap-6 md:px-8">
        <h1 className="text-2xl font-semibold tracking-tight text-sol-base01 md:text-3xl">
          Keyboard Part Picker
        </h1>
        <div className="md:ml-auto md:w-[420px]">
          <SearchBar value={value} onChange={onChange} />
        </div>
      </div>
    </header>
  );
}
