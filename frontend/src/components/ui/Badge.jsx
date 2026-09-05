import { cn } from '@/utils/format';

// Semantic status tones used consistently across the whole platform.
const TONES = {
  normal: 'bg-[color-mix(in_srgb,var(--color-normal)_16%,transparent)] text-[var(--color-normal)] border-[color-mix(in_srgb,var(--color-normal)_35%,transparent)]',
  info: 'bg-[color-mix(in_srgb,var(--color-info)_16%,transparent)] text-[var(--color-info)] border-[color-mix(in_srgb,var(--color-info)_35%,transparent)]',
  warning: 'bg-[color-mix(in_srgb,var(--color-warning)_16%,transparent)] text-[var(--color-warning)] border-[color-mix(in_srgb,var(--color-warning)_35%,transparent)]',
  risk: 'bg-[color-mix(in_srgb,var(--color-risk)_16%,transparent)] text-[var(--color-risk)] border-[color-mix(in_srgb,var(--color-risk)_35%,transparent)]',
  contradiction: 'bg-[color-mix(in_srgb,var(--color-contradiction)_16%,transparent)] text-[var(--color-contradiction)] border-[color-mix(in_srgb,var(--color-contradiction)_35%,transparent)]',
  success: 'bg-[color-mix(in_srgb,var(--color-success)_16%,transparent)] text-[var(--color-success)] border-[color-mix(in_srgb,var(--color-success)_35%,transparent)]',
  accent: 'bg-[color-mix(in_srgb,var(--color-accent)_16%,transparent)] text-[var(--color-accent)] border-[color-mix(in_srgb,var(--color-accent)_35%,transparent)]',
  muted: 'bg-white/5 text-[var(--color-ink-muted)] border-[var(--color-border)]',
};

export function Badge({ tone = 'muted', dot = false, className, children }) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded border px-2 py-0.5 font-mono text-[11px] font-medium uppercase tracking-wide',
        TONES[tone] || TONES.muted,
        className
      )}
    >
      {dot && <span className={cn('h-1.5 w-1.5 rounded-full', dotColor(tone))} />}
      {children}
    </span>
  );
}

function dotColor(tone) {
  return {
    normal: 'bg-[var(--color-normal)]',
    info: 'bg-[var(--color-info)]',
    warning: 'bg-[var(--color-warning)]',
    risk: 'bg-[var(--color-risk)]',
    contradiction: 'bg-[var(--color-contradiction)]',
    success: 'bg-[var(--color-success)]',
    accent: 'bg-[var(--color-accent)]',
    muted: 'bg-[var(--color-ink-faint)]',
  }[tone] || 'bg-[var(--color-ink-faint)]';
}

export function statusTone(status) {
  const map = {
    active: 'success',
    monitoring: 'info',
    closed: 'muted',
    degraded: 'warning',
    inactive: 'muted',
    connected: 'success',
    online: 'success',
  };
  return map[status] || 'muted';
}
