export default function ListSection({ title, items }) {
  if (!items || items.length === 0) return null;

  return (
    <div className="rounded-lg border border-hairline-light dark:border-hairline-dark bg-surface-light dark:bg-surface-dark p-4">
      <h3 className="text-sm font-semibold text-ink-primary-light dark:text-ink-primary-dark mb-2">
        {title}
      </h3>
      <ul className="space-y-1.5">
        {items.map((item, i) => (
          <li
            key={i}
            className="text-sm text-ink-secondary-light dark:text-ink-secondary-dark pl-3 border-l-2 border-hairline-light dark:border-hairline-dark"
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
