import { CheckCircleIcon, AlertTriangleIcon, SearchIcon, XCircleIcon } from "./icons.jsx";

const SIGNAL_META = {
  strong_yes: {
    label: "Strong Yes",
    description: "Strong opportunity",
    status: "good",
    Icon: CheckCircleIcon,
  },
  cautious_yes: {
    label: "Cautious Yes",
    description: "Worth building, with execution or competition risk",
    status: "warning",
    Icon: AlertTriangleIcon,
  },
  explore_more: {
    label: "Explore More",
    description: "Needs validation — unclear wedge",
    status: "serious",
    Icon: SearchIcon,
  },
  not_recommended: {
    label: "Not Recommended",
    description: "Fundamentally weak",
    status: "critical",
    Icon: XCircleIcon,
  },
};

const STATUS_CLASSES = {
  good: "bg-status-good/10 text-status-good border-status-good/30",
  warning: "bg-status-warning/10 text-status-warning border-status-warning/40",
  serious: "bg-status-serious/10 text-status-serious border-status-serious/40",
  critical: "bg-status-critical/10 text-status-critical border-status-critical/30",
};

export default function BuildSignalBadge({ signal }) {
  const meta = SIGNAL_META[signal];
  if (!meta) return null;
  const { label, description, status, Icon } = meta;

  return (
    <div
      className={`inline-flex items-center gap-2.5 rounded-full border px-4 py-2 ${STATUS_CLASSES[status]}`}
    >
      <Icon className="h-5 w-5 shrink-0" />
      <div className="flex flex-col leading-tight">
        <span className="text-sm font-semibold">{label}</span>
        <span className="text-xs text-ink-secondary-light dark:text-ink-secondary-dark">
          {description}
        </span>
      </div>
    </div>
  );
}
