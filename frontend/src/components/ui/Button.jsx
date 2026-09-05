import { cn } from '@/utils/format';

const VARIANTS = {
  primary: 'bg-[var(--color-accent)] text-[#181206] hover:brightness-110 border border-[var(--color-accent)]',
  secondary: 'bg-transparent text-[var(--color-ink)] border border-[var(--color-border)] hover:bg-white/5',
  ghost: 'bg-transparent text-[var(--color-ink-muted)] border border-transparent hover:text-[var(--color-ink)] hover:bg-white/5',
  danger: 'bg-transparent text-[var(--color-risk)] border border-[color-mix(in_srgb,var(--color-risk)_45%,transparent)] hover:bg-[color-mix(in_srgb,var(--color-risk)_10%,transparent)]',
};

export function Button({ variant = 'primary', className, children, icon: Icon, ...props }) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-md px-3.5 py-2 font-mono text-[12px] font-semibold uppercase tracking-wide transition-colors disabled:cursor-not-allowed disabled:opacity-40',
        VARIANTS[variant],
        className
      )}
      {...props}
    >
      {Icon && <Icon size={14} strokeWidth={2.25} />}
      {children}
    </button>
  );
}
