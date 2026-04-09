import KeyboardCard from './KeyboardCard.jsx';

export default function KeyboardGrid({ keyboards, onSelect }) {
  if (keyboards.length === 0) {
    return (
      <div className="rounded border border-dashed border-sol-base2 px-6 py-16 text-center text-sm text-sol-base1">
        No keyboards match your filters.
      </div>
    );
  }
  return (
    <div className="columns-2 gap-0.5 md:columns-3 lg:columns-4">
      {keyboards.map((kb) => (
        <KeyboardCard key={kb.id} keyboard={kb} onClick={() => onSelect(kb)} />
      ))}
    </div>
  );
}
