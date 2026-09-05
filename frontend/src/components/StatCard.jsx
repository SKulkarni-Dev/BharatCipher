import { Card } from '@/components/ui/Card';

const TONE_CLASSES = {
  accent: 'bg-[color-mix(in_srgb,var(--color-accent)_16%,transparent)] text-[var(--color-accent)]',
  info: 'bg-[color-mix(in_srgb,var(--color-info)_16%,transparent)] text-[var(--color-info)]',
  warning: 'bg-[color-mix(in_srgb,var(--color-warning)_16%,transparent)] text-[var(--color-warning)]',
  risk: 'bg-[color-mix(in_srgb,var(--color-risk)_16%,transparent)] text-[var(--color-risk)]',
  success: 'bg-[color-mix(in_srgb,var(--color-success)_16%,transparent)] text-[var(--color-success)]',
  contradiction: 'bg-[color-mix(in_srgb,var(--color-contradiction)_16%,transparent)] text-[var(--color-contradiction)]',
};

export function StatCard({ label, value, icon: Icon, tone = 'accent', hint }) {
  return (
    <Card className="p-4">
      <div className="flex items-start justify-between">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">{label}</p>
          <p className="mt-1.5 font-display text-2xl font-semibold text-[var(--color-ink)]">{value}</p>
          {hint && <p className="mt-1 text-[11px] text-[var(--color-ink-muted)]">{hint}</p>}
        </div>
        {Icon && (
          <div className={`flex h-8 w-8 items-center justify-center rounded-md ${TONE_CLASSES[tone] || TONE_CLASSES.accent}`}>
            <Icon size={16} strokeWidth={2.25} />
          </div>
        )}
      </div>
    </Card>
  );
}
