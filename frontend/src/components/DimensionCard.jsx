const DIMENSION_META = {
  "Market Potential": {
    definition: "How big is the addressable market for this idea, and is it growing?",
  },
  "Product Usefulness": {
    definition: "Does it solve a real, painful problem well — better than what people already do today?",
  },
  "Feasibility & Defensibility": {
    definition: "Can it actually be built — and does it stay defensible once a competitor notices?",
  },
  "Monetization Viability": {
    definition: "Will people actually pay — and pay enough — for this to be a real business?",
  },
};

const RADIUS = 22;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

export default function DimensionCard({ name, score, justification, tierColor = "#1B2540", isLast = false }) {
  const meta = DIMENSION_META[name] || {};
  const clamped = Math.max(0, Math.min(5, score));
  const dash = (clamped / 5) * CIRCUMFERENCE;

  return (
    <div className={`flex gap-4 ${isLast ? "" : "mb-5 border-b border-divider pb-5"}`}>
      <div className="relative h-14 w-14 shrink-0">
        <svg width="56" height="56" viewBox="0 0 56 56">
          <circle cx="28" cy="28" r={RADIUS} fill="none" stroke="#E3E7EA" strokeWidth="5" />
          <circle
            cx="28"
            cy="28"
            r={RADIUS}
            fill="none"
            stroke={tierColor}
            strokeWidth="5"
            strokeLinecap="round"
            strokeDasharray={`${dash} ${CIRCUMFERENCE}`}
            transform="rotate(-90 28 28)"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center font-mono text-[15px] font-bold" style={{ color: tierColor }}>
          {score}
        </div>
      </div>

      <div className="min-w-0 flex-1">
        <div className="flex items-baseline justify-between gap-2">
          <div className="flex items-center">
            <h3 className="text-[15px] font-semibold text-ink">{name}</h3>
            {meta.definition && (
              <div className="group relative ml-1.5 inline-flex">
                <button
                  type="button"
                  className="flex h-[15px] w-[15px] shrink-0 items-center justify-center rounded-full border border-[#C3CBD0] font-mono text-[9px] font-bold text-[#828A91] focus-visible:outline focus-visible:outline-2 focus-visible:outline-ink"
                  aria-label={`What ${name} measures: ${meta.definition}`}
                >
                  ?
                </button>
                <span
                  role="tooltip"
                  className="pointer-events-none absolute bottom-[calc(100%+10px)] left-1/2 z-10 w-56 -translate-x-1/2 translate-y-1 rounded-xl bg-ink px-3.5 py-3 text-left text-[11.5px] font-normal leading-relaxed text-cream opacity-0 shadow-lg transition group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:translate-y-0 group-focus-within:opacity-100"
                  aria-hidden="true"
                >
                  {meta.definition}
                  <span className="absolute left-1/2 top-full h-0 w-0 -translate-x-1/2 border-[6px] border-transparent border-t-ink" />
                </span>
              </div>
            )}
          </div>
          <span className="shrink-0 font-mono text-xs text-card-muted">{score} / 5</span>
        </div>
        <p className="mt-2 text-[13.5px] leading-relaxed text-card-text2">{justification}</p>
      </div>
    </div>
  );
}
