export default function KeyboardCard({ keyboard, onClick }) {
  const img = keyboard.image_urls?.[0];
  return (
    <button
      type="button"
      onClick={onClick}
      className="relative mb-0.5 block w-full overflow-hidden rounded bg-sol-base2 transition hover:opacity-90 focus:outline-none focus-visible:ring-2 focus-visible:ring-sol-blue"
      style={{ breakInside: 'avoid' }}
    >
      {img ? (
        <img
          src={img}
          alt={keyboard.title}
          loading="lazy"
          className="block w-full rounded"
        />
      ) : (
        <div className="flex aspect-square items-center justify-center text-xs text-sol-base1">
          no image
        </div>
      )}
      <span className="pointer-events-none absolute bottom-1.5 right-1.5 rounded bg-black/55 px-1.5 py-0.5 text-[11px] font-medium text-white/95">
        u/{keyboard.author}
      </span>
    </button>
  );
}
