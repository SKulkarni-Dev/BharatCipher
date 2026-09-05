import { useLocation } from 'react-router-dom';
import { Circle, UserCircle2 } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

const TITLES = {
  '/': 'Dashboard',
  '/investigations': 'Investigations',
  '/investigations/new': 'New Investigation',
  '/sources': 'Intelligence Sources',
  '/entities': 'Entity Explorer',
  '/evidence': 'Evidence Explorer',
  '/graph': 'Investigation Graph',
  '/timeline': 'Timeline',
  '/attribution': 'Attribution Assessment',
  '/attribution/challenge': 'Challenge Attribution',
  '/alerts': 'Alerts',
  '/settings': 'Settings / System Status',
};

export function Topbar() {
  const location = useLocation();
  const { investigator } = useAuth();
  const title = TITLES[location.pathname] || 'SIH26151';

  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-panel)] px-5">
      <h1 className="font-display text-[15px] font-semibold text-[var(--color-ink)]">{title}</h1>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5 rounded-full border border-[var(--color-border)] px-2.5 py-1 font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-muted)]">
          <Circle size={7} className="fill-[var(--color-success)] text-[var(--color-success)]" />
          Live API
        </div>
        <div className="flex items-center gap-2 text-[13px] text-[var(--color-ink-muted)]">
          <UserCircle2 size={20} />
          {investigator?.name || 'Investigator'}
        </div>
      </div>
    </header>
  );
}
