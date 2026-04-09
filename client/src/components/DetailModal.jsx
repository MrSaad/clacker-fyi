import { useEffect, useState } from 'react';

const PART_LABELS = {
  case: 'Case',
  pcb: 'PCB',
  plate: 'Plate',
  switches: 'Switches',
  keycaps: 'Keycaps',
  stabilizers: 'Stabilizers',
  layout: 'Layout',
  mods: 'Mods',
  cable: 'Cable',
  deskmat: 'Deskmat',
};

function Tag({ children }) {
  return (
    <span className="inline-flex items-center rounded border border-sol-base2 bg-sol-base2/60 px-2 py-0.5 text-[11px] text-sol-base01">
      {children}
    </span>
  );
}

export default function DetailModal({ keyboard, onClose }) {
  const images = keyboard.image_urls || [];
  const [activeIdx, setActiveIdx] = useState(0);

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  const inferred = keyboard.inferred || {};
  const parts = keyboard.parts || {};
  const partRows = Object.entries(PART_LABELS).filter(([k]) => parts[k]);
  const tags = [
    inferred.sound_profile,
    inferred.build_tier,
    inferred.typing_feel,
    inferred.build_complexity,
    ...(inferred.aesthetic || []),
  ].filter(Boolean);

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-sol-base03/40 px-4 py-8 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-5xl rounded-md border border-sol-base2 bg-sol-base3 shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          type="button"
          onClick={onClose}
          aria-label="Close"
          className="absolute right-3 top-3 z-10 hidden h-7 w-7 items-center justify-center rounded text-sol-base01 hover:bg-sol-base2 md:flex"
        >
          ✕
        </button>

        {/* Mobile-only close bar */}
        <div className="flex justify-end border-b border-sol-base2 px-3 py-2 md:hidden">
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="flex h-8 w-8 items-center justify-center rounded text-sol-base01 hover:bg-sol-base2"
          >
            ✕
          </button>
        </div>

        <div className="grid gap-6 p-4 md:grid-cols-[1.15fr_1fr] md:p-6">
          {/* Gallery */}
          <div className="flex flex-col gap-3">
            <div className="overflow-hidden rounded border border-sol-base2 bg-sol-base2">
              {images[activeIdx] && (
                <img
                  src={images[activeIdx]}
                  alt={keyboard.title}
                  className="block w-full object-contain"
                />
              )}
            </div>
            {images.length > 1 && (
              <div className="flex gap-1.5 overflow-x-auto">
                {images.map((src, i) => (
                  <button
                    key={src}
                    type="button"
                    onClick={() => setActiveIdx(i)}
                    className={`h-14 w-14 shrink-0 overflow-hidden rounded border ${
                      i === activeIdx
                        ? 'border-sol-blue'
                        : 'border-sol-base2 hover:border-sol-base1'
                    }`}
                  >
                    <img src={src} alt="" className="h-full w-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Details */}
          <div className="flex min-w-0 flex-col gap-4">
            <div>
              <h2 className="text-xl font-semibold text-sol-base01">
                {keyboard.title}
              </h2>
              <div className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-sol-base00">
                <span>
                  by{' '}
                  <a
                    href={`https://reddit.com/u/${keyboard.author}`}
                    target="_blank"
                    rel="noreferrer"
                    className="font-medium text-reddit hover:underline"
                  >
                    u/{keyboard.author}
                  </a>
                </span>
                <span className="text-sol-base1">· ↑ {keyboard.score}</span>
                <a
                  href={keyboard.permalink}
                  target="_blank"
                  rel="noreferrer"
                  className="ml-auto inline-flex items-center gap-1 rounded border border-reddit bg-reddit/10 px-2 py-0.5 text-[11px] text-reddit transition hover:bg-reddit/20"
                >
                  View original post on Reddit →
                </a>
              </div>
            </div>

            {tags.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {tags.map((t, i) => (
                  <Tag key={`${t}-${i}`}>{t}</Tag>
                ))}
              </div>
            )}

            {partRows.length > 0 && (
              <dl className="overflow-hidden rounded border border-sol-base2 text-sm">
                {partRows.map(([k, label], i) => (
                  <div
                    key={k}
                    className={`grid grid-cols-[100px_1fr] gap-3 px-3 py-1.5 ${
                      i % 2 === 0 ? 'bg-sol-base2/40' : ''
                    }`}
                  >
                    <dt className="text-xs uppercase tracking-wide text-sol-base1">
                      {label}
                    </dt>
                    <dd className="text-sol-base01">{parts[k]}</dd>
                  </div>
                ))}
              </dl>
            )}

            {keyboard.raw?.parts_source_text && (
              <div>
                <div className="mb-1 text-xs uppercase tracking-wide text-sol-base1">
                  From the post
                </div>
                <pre className="max-h-44 overflow-y-auto whitespace-pre-wrap rounded border border-sol-base2 bg-sol-base2/40 p-3 text-xs leading-relaxed text-sol-base00">
                  {keyboard.raw.parts_source_text}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
