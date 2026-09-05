import { cn } from '@/utils/format';

export function Card({ className, children, ...props }) {
  return (
    <div
      className={cn(
        'rounded-lg border border-[var(--color-border)] bg-[var(--color-panel)]',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, action, eyebrow, className }) {
  return (
    <div className={cn('flex items-start justify-between gap-4 border-b border-[var(--color-border-soft)] px-5 py-4', className)}>
      <div>
        {eyebrow && (
          <div className="mb-1 font-mono text-[11px] uppercase tracking-wider text-[var(--color-ink-faint)]">
            {eyebrow}
          </div>
        )}
        <h3 className="font-display text-[15px] font-semibold text-[var(--color-ink)]">{title}</h3>
        {subtitle && <p className="mt-0.5 text-[13px] text-[var(--color-ink-muted)]">{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

export function CardBody({ className, children }) {
  return <div className={cn('px-5 py-4', className)}>{children}</div>;
}
