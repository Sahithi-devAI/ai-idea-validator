import { useState } from "react";
import { evaluateIdea } from "./api.js";
import BuildSignalBadge from "./components/BuildSignalBadge.jsx";
import DimensionCard from "./components/DimensionCard.jsx";
import ListSection from "./components/ListSection.jsx";

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
    <div className="min-h-screen bg-plane-light dark:bg-plane-dark text-ink-primary-light dark:text-ink-primary-dark">
      <div className="mx-auto max-w-3xl px-4 py-10 sm:py-14">
        <header className="mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold">AI Idea Validator</h1>
          <p className="mt-1 text-ink-secondary-light dark:text-ink-secondary-dark">
            Is this idea worth building?
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-3">
          <textarea
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            placeholder="Describe your startup idea — what it does, who it's for, and how it makes money..."
            rows={6}
            maxLength={MAX_LENGTH}
            className="w-full rounded-lg border border-hairline-light dark:border-hairline-dark bg-surface-light dark:bg-surface-dark p-3 text-sm focus:outline-none focus:ring-2 focus:ring-seq-fill-light dark:focus:ring-seq-fill-dark"
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-ink-muted tabular-nums">
              {trimmedLength}/{MAX_LENGTH} (min {MIN_LENGTH})
            </span>
            <button
              type="submit"
              disabled={!isValid || loading}
              className="rounded-lg bg-seq-fill-light dark:bg-seq-fill-dark px-5 py-2 text-sm font-semibold text-white disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {loading ? "Evaluating…" : "Evaluate"}
            </button>
          </div>
        </form>

        {error && (
          <div className="mt-6 rounded-lg border border-status-critical/30 bg-status-critical/10 p-4 text-sm text-status-critical">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-10 space-y-6">
            <div className="flex flex-col gap-3">
              <BuildSignalBadge signal={result.build_signal} />
              <p className="text-lg leading-snug">{result.verdict}</p>
              <p className="text-sm text-ink-secondary-light dark:text-ink-secondary-dark">
                Weakest dimension: <span className="font-medium">{result.weakest_dimension}</span>
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              {result.dimensions.map((d) => (
                <DimensionCard key={d.name} {...d} />
              ))}
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <ListSection title="Strengths" items={result.strengths} />
              <ListSection title="Weaknesses" items={result.weaknesses} />
              <ListSection title="Risks" items={result.risks} />
              <ListSection title="Next Steps" items={result.next_steps} />
            </div>

            <details className="rounded-lg border border-hairline-light dark:border-hairline-dark bg-surface-light dark:bg-surface-dark p-4">
              <summary className="cursor-pointer text-sm font-semibold">
                Raw model output
              </summary>
              <pre className="mt-3 whitespace-pre-wrap text-xs text-ink-secondary-light dark:text-ink-secondary-dark">
                {result.raw_output}
              </pre>
            </details>
          </div>
        )}

        <footer className="mt-14 text-xs text-ink-muted">
          <a href={REPO_URL} target="_blank" rel="noreferrer" className="underline">
            View source on GitHub
          </a>
        </footer>
      </div>
    </div>
  );
}
