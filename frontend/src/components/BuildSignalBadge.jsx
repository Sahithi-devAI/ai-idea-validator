import { CheckIcon, SeedlingIcon, RefreshIcon } from "./icons.jsx";

export const SIGNAL_META = {
  strong_yes: {
    label: "Strong Yes",
    description: "Strong opportunity — build it",
    tier: "#2E7D4F",
    Icon: CheckIcon,
  },
  cautious_yes: {
    label: "Cautious Yes",
    description: "Worth building, with execution or competition risk",
    tier: "#D1A62C",
    tierText: "#B5841C",
    Icon: CheckIcon,
  },
  explore_more: {
    label: "Explore More",
    description: "Needs validation — unclear wedge",
    tier: "#8A94A0",
    Icon: SeedlingIcon,
  },
  not_recommended: {
    label: "Not There Yet",
    description: "Needs a sharper wedge before building",
    tier: "#B5542B",
    Icon: RefreshIcon,
  },
};

export default function BuildSignalBadge({ signal, verdict, weakestDimension }) {
  const meta = SIGNAL_META[signal];
  if (!meta) return null;
  const { label, description, tier, Icon } = meta;
  const tierText = meta.tierText || tier;

  return (
    <div className="relative">
      <div
        className="pointer-events-none absolute -inset-14 -z-10 blur-md"
        style={{ background: `radial-gradient(circle at 50% 38%, ${tier}66, transparent 65%)` }}
        aria-hidden="true"
      />
      <div
        className="animate-card-reveal relative rounded-3xl border-2 bg-card p-6 text-ink sm:p-8"
        style={{ "--tilt": "-1deg", borderColor: tier, boxShadow: `0 28px 56px -28px ${tier}66` }}
      >
        <div className="flex items-start gap-4">
          <div
            className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full"
            style={{ background: tier, boxShadow: `0 6px 14px -4px ${tier}99` }}
          >
            <Icon className="h-5 w-5 text-white" />
          </div>
          <div className="min-w-0">
            <h2 className="font-display text-2xl font-bold sm:text-[26px]" style={{ color: tierText }}>
              {label}
            </h2>
            <p className="mt-0.5 text-sm text-card-muted2">{description}</p>
          </div>
        </div>

        {verdict && (
          <p className="mt-5 border-t border-divider pt-5 text-lg font-medium leading-snug text-ink">
            {verdict}
          </p>
        )}

        {weakestDimension && (
          <div className="mt-4 inline-block rounded-lg bg-black/[0.03] px-3.5 py-2.5">
            <span className="font-mono text-[11px] font-semibold uppercase tracking-[0.1em] text-card-muted2">
              Weakest dimension —
            </span>
            <span className="ml-1.5 text-sm font-semibold text-ink">{weakestDimension}</span>
          </div>
        )}
      </div>
    </div>
  );
}
