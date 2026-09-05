import { pct, cn } from '@/utils/format';

// Signature element: an evidence-board style confidence gauge with tick
// marks rather than a smooth progress bar — deliberately reads as
// "measured assessment," never as a certainty meter.
function bandColor(value) {
  if (value >= 0.75) return 'var(--color-success)';
  if (value >= 0.55) return 'var(--color-accent)';
  if (value >= 0.35) return 'var(--color-warning)';
  return 'var(--color-risk)';
}

export function ConfidenceGauge({ value, size = 'md', label = 'CONFIDENCE', showLabel = true }) {
  const color = bandColor(value);
  const ticks = 20;
  const filled = Math.round(value * ticks);
  const heightCls = size === 'lg' ? 'h-3' : 'h-2';
  const textCls = size === 'lg' ? 'text-3xl' : 'text-lg';

  return (
    <div>
      {showLabel && (
        <div className="mb-1.5 flex items-center justify-between">
          <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">{label}</span>
          <span className={cn('font-mono font-semibold', textCls)} style={{ color }}>
            {pct(value)}
          </span>
        </div>
      )}
      <div className={cn('flex gap-[2px]', heightCls)}>
        {Array.from({ length: ticks }).map((_, i) => (
          <span
            key={i}
            className="flex-1 rounded-[1px]"
            style={{
              backgroundColor: i < filled ? color : 'var(--color-border)',
              opacity: i < filled ? 1 : 0.6,
            }}
          />
        ))}
      </div>
    </div>
  );
}
