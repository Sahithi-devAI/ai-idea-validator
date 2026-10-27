import { useState } from "react";
import { evaluateIdea } from "./api.js";
import BuildSignalBadge, { SIGNAL_META } from "./components/BuildSignalBadge.jsx";
import DimensionCard from "./components/DimensionCard.jsx";
import ListSection from "./components/ListSection.jsx";
import { ClockIcon, GridIcon, ArrowRightIcon, ChevronDownIcon } from "./components/icons.jsx";

const MIN_LENGTH = 10;
const MAX_LENGTH = 2000;
const REPO_URL = "https://github.com/Sahithi-devAI/ai-idea-validator";

export default function App() {
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const trimmedLength = idea.trim().length;
  const isValid = trimmedLength >= MIN_LENGTH && trimmedLength <= MAX_LENGTH;
  const tierColor = result ? SIGNAL_META[result.build_signal]?.tier || "#1B2540" : "#1B2540";

  async function handleSubmit(e) {
    e.preventDefault();
    if (!isValid || loading) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await evaluateIdea(idea.trim());
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-ink bg-dot-grid text-cream">
      <div className="mx-auto max-w-3xl px-4 py-14 pb-24 sm:py-16">
        <header className="mb-14 flex items-center justify-center sm:mb-16">
          <h1 className="font-display text-base font-bold tracking-wide">IDEA VALIDATOR</h1>
        </header>

        <div className="mx-auto mb-11 max-w-xl text-center">
          <h2 className="font-display text-4xl font-bold leading-tight tracking-tight sm:text-[50px]">
            Find out if it's worth building.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Describe your idea and get a clear build signal — scored across four dimensions, with
            real risks and next steps. Not a confidence score. A verdict.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="mx-auto max-w-xl rounded-[20px] border-2 border-ink bg-card p-8 shadow-[0_24px_48px_-28px_rgba(0,0,0,0.45)]"
        >
          <label
            htmlFor="idea-field"
            className="mb-3.5 block font-mono text-[11px] font-semibold uppercase tracking-[0.1em] text-card-muted2"
          >
            Your idea
          </label>
          <textarea
            id="idea-field"
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            placeholder="What it does, who it's for, and how it makes money..."
            rows={5}
            maxLength={MAX_LENGTH}
            className="w-full resize-none rounded-xl border-[1.5px] border-[#D7DEE2] p-4 text-[15px] leading-relaxed text-ink placeholder:text-card-muted focus:outline-none focus:ring-2 focus:ring-ink"
          />
          <div className="mt-4 flex items-center justify-between">
            <span className="font-mono text-xs text-card-muted">
              {trimmedLength} / {MAX_LENGTH} · min {MIN_LENGTH}
            </span>
            <button
              type="submit"
              disabled={!isValid || loading}
              className="inline-flex items-center gap-2 rounded-full bg-ink px-6 py-3 font-display text-sm font-bold text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? "Evaluating…" : "Evaluate"}
              <span aria-hidden="true">→</span>
            </button>
          </div>
        </form>

        <div className="mx-auto mt-7 flex max-w-xl flex-wrap justify-center gap-2.5">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-[#D7DEE2] bg-card px-3.5 py-2">
            <ClockIcon className="h-3.5 w-3.5 text-card-muted2" />
            <span className="font-mono text-[11px] text-ink">~15 sec</span>
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-[#D7DEE2] bg-card px-3.5 py-2">
            <GridIcon className="h-3.5 w-3.5 text-card-muted2" />
            <span className="font-mono text-[11px] text-ink">4 dimensions scored</span>
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-[#D7DEE2] bg-card px-3.5 py-2">
            <ArrowRightIcon className="h-3.5 w-3.5 text-card-muted2" />
            <span className="font-mono text-[11px] text-ink">Clear next steps</span>
          </span>
        </div>

        {error && (
          <div className="mx-auto mt-8 max-w-xl rounded-xl border border-tier-reject/40 bg-tier-reject/10 p-4 text-sm text-cream">
            {error}
          </div>
        )}

        {result && (
          <div className="mx-auto mt-14 max-w-xl space-y-8">
            <BuildSignalBadge
              signal={result.build_signal}
              verdict={result.verdict}
              weakestDimension={result.weakest_dimension}
            />

            <section className="rounded-2xl border border-divider bg-card p-6">
              <h2 className="mb-5 font-mono text-[11px] font-semibold uppercase tracking-[0.1em] text-card-muted2">
                Dimensions
              </h2>
              {result.dimensions.map((d, i) => (
                <DimensionCard
                  key={d.name}
                  {...d}
                  tierColor={tierColor}
                  isLast={i === result.dimensions.length - 1}
                />
              ))}
            </section>

            <section>
              <h2 className="mb-3 px-1 font-mono text-[11px] font-semibold uppercase tracking-[0.1em] text-muted">
                Findings
              </h2>
              <div className="grid gap-4 sm:grid-cols-2">
                <ListSection title="Strengths" variant="strengths" items={result.strengths} />
                <ListSection title="Weaknesses" variant="weaknesses" items={result.weaknesses} />
                <ListSection title="Risks" variant="risks" items={result.risks} />
                <ListSection title="Next Steps" variant="next_steps" items={result.next_steps} />
              </div>
            </section>

            <details className="group rounded-2xl border border-divider bg-card p-5">
              <summary className="flex cursor-pointer list-none items-center justify-between font-mono text-[11px] font-semibold uppercase tracking-[0.1em] text-card-muted2">
                Raw model output
                <ChevronDownIcon className="h-4 w-4 transition-transform group-open:rotate-180" />
              </summary>
              <pre className="mt-3 whitespace-pre-wrap font-mono text-xs leading-relaxed text-card-text2">
                {result.raw_output}
              </pre>
            </details>
          </div>
        )}

        <footer className="mt-20 text-center text-xs text-muted">
          <a href={REPO_URL} target="_blank" rel="noreferrer" className="underline">
            View source on GitHub
          </a>
        </footer>
      </div>
    </div>
  );
}
