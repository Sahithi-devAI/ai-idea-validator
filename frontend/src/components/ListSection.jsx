import { CheckCircleIcon, AlertTriangleIcon, XCircleIcon, ArrowRightIcon } from "./icons.jsx";

const VARIANTS = {
  strengths: { Icon: CheckCircleIcon, color: "#2E7D4F" },
  weaknesses: { Icon: AlertTriangleIcon, color: "#B5841C" },
  risks: { Icon: XCircleIcon, color: "#B5542B" },
  next_steps: { Icon: ArrowRightIcon, color: "#1B2540", emphasize: true },
};

export default function ListSection({ title, variant, items }) {
  if (!items || items.length === 0) return null;
  const { Icon, color, emphasize } = VARIANTS[variant] || VARIANTS.strengths;

  return (
    <div
      className={`rounded-2xl bg-card p-5 ${emphasize ? "border-2" : "border border-divider"}`}
      style={emphasize ? { borderColor: color } : undefined}
    >
      <h3 className="mb-3 flex items-center gap-1.5 font-mono text-[11px] font-semibold uppercase tracking-[0.1em] text-card-muted2">
        <Icon className="h-3.5 w-3.5" style={{ color }} />
        {title}
        <span className="text-card-muted">({items.length})</span>
      </h3>
      <ul className="space-y-2.5">
        {items.map((item, i) => (
          <li key={i} className="flex gap-2.5 text-sm leading-relaxed text-ink">
            <Icon className="mt-0.5 h-4 w-4 shrink-0" style={{ color }} />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
