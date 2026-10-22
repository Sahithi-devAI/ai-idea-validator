export default function DimensionCard({ name, score, justification }) {
  const pct = Math.max(0, Math.min(5, score)) / 5 * 100;

  return (
    <div className="rounded-lg border border-hairline-light dark:border-hairline-dark bg-surface-light dark:bg-surface-dark p-4">
      <div className="flex items-baseline justify-between gap-3">
        <h3 className="text-sm font-semibold text-ink-primary-light dark:text-ink-primary-dark">
          {name}
        </h3>
        <span className="text-xs text-ink-secondary-light dark:text-ink-secondary-dark tabular-nums">
          {score}/5
        </span>
      </div>

      <div className="mt-2 h-2 w-full rounded-full bg-seq-track-light dark:bg-seq-track-dark overflow-hidden">
        <div
          className="h-full rounded-full bg-seq-fill-light dark:bg-seq-fill-dark"
          style={{ width: `${pct}%` }}
        />
      </div>

      <p className="mt-3 text-sm text-ink-secondary-light dark:text-ink-secondary-dark">
        {justification}
      </p>
    </div>
  );
}
