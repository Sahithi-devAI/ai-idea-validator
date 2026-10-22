// Minimal inline icons (20x20, outline) — paired with text labels, never carrying meaning by color alone.

export function CheckCircleIcon(props) {
  return (
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.8" {...props}>
      <circle cx="10" cy="10" r="8" />
      <path d="M6.5 10.5l2.2 2.2L13.5 8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function AlertTriangleIcon(props) {
  return (
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.8" {...props}>
      <path d="M10 3.5l7.5 13H2.5l7.5-13z" strokeLinejoin="round" />
      <path d="M10 8.2v3.3" strokeLinecap="round" />
      <circle cx="10" cy="14.2" r="0.6" fill="currentColor" stroke="none" />
    </svg>
  );
}

export function SearchIcon(props) {
  return (
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.8" {...props}>
      <circle cx="8.8" cy="8.8" r="5.3" />
      <path d="M13.2 13.2L17 17" strokeLinecap="round" />
    </svg>
  );
}

export function XCircleIcon(props) {
  return (
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.8" {...props}>
      <circle cx="10" cy="10" r="8" />
      <path d="M7.3 7.3l5.4 5.4M12.7 7.3l-5.4 5.4" strokeLinecap="round" />
    </svg>
  );
}
