import { EMPTY } from '@/utils/format';

function humanizeKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatValue(value) {
  if (value === undefined || value === null || value === '') return EMPTY;
  if (Array.isArray(value)) return value.length ? value.join(', ') : EMPTY;
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

/**
 * Renders every field of a backend record generically (label: value),
 * so entities/evidence/observations/hypotheses of unknown shape are shown
 * in full without the frontend guessing at or fabricating a fixed schema.
 */
export function RawFields({ data, exclude = [] }) {
  if (!data) return <p className="text-[12px] text-[var(--color-ink-muted)]">{EMPTY}</p>;
  const keys = Object.keys(data).filter((k) => !exclude.includes(k));
  if (!keys.length) return <p className="text-[12px] text-[var(--color-ink-muted)]">{EMPTY}</p>;
  return (
    <div className="space-y-2">
      {keys.map((k) => (
        <div key={k} className="flex items-start justify-between gap-4 text-[12.5px]">
          <span className="shrink-0 text-[var(--color-ink-muted)]">{humanizeKey(k)}</span>
          <span className="break-all text-right text-[var(--color-ink)]">{formatValue(data[k])}</span>
        </div>
      ))}
    </div>
  );
}
