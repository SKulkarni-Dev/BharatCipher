import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FolderKanban,
  FilePlus2,
  Radio,
  Users,
  Share2,
  History,
  Target,
  ShieldAlert,
  Bell,
  Archive,
  Settings,
  ShieldHalf,
} from 'lucide-react';
import { cn } from '@/utils/format';

const NAV = [
  { section: 'Overview', items: [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
    { to: '/investigations', label: 'Investigations', icon: FolderKanban },
    { to: '/investigations/new', label: 'New Investigation', icon: FilePlus2 },
  ]},
  { section: 'Intelligence', items: [
    { to: '/sources', label: 'Intelligence Sources', icon: Radio },
    { to: '/entities', label: 'Entity Explorer', icon: Users },
    { to: '/evidence', label: 'Evidence Explorer', icon: Archive },
  ]},
  { section: 'Analysis', items: [
    { to: '/graph', label: 'Investigation Graph', icon: Share2 },
    { to: '/timeline', label: 'Timeline', icon: History },
    { to: '/attribution', label: 'Attribution Assessment', icon: Target },
    { to: '/attribution/challenge', label: 'Challenge Attribution', icon: ShieldAlert },
  ]},
  { section: 'System', items: [
    { to: '/alerts', label: 'Alerts', icon: Bell },
    { to: '/settings', label: 'Settings / Status', icon: Settings },
  ]},
];

export function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-[var(--color-border)] bg-[var(--color-panel)] md:flex">
      <div className="flex items-center gap-2.5 border-b border-[var(--color-border)] px-5 py-4">
        <div className="flex h-8 w-8 items-center justify-center rounded bg-[color-mix(in_srgb,var(--color-accent)_18%,transparent)] text-[var(--color-accent)]">
          <ShieldHalf size={18} strokeWidth={2.25} />
        </div>
        <div className="leading-tight">
          <div className="font-display text-[13px] font-semibold tracking-wide text-[var(--color-ink)]">SIH26151</div>
          <div className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Attribution Platform</div>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        {NAV.map((group) => (
          <div key={group.section} className="mb-5">
            <div className="mb-1.5 px-2 font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">
              {group.section}
            </div>
            <div className="space-y-0.5">
              {group.items.map(({ to, label, icon: Icon, end }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={end}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-2.5 rounded-md px-2.5 py-2 text-[13px] font-medium transition-colors',
                      isActive
                        ? 'bg-[color-mix(in_srgb,var(--color-accent)_14%,transparent)] text-[var(--color-accent)]'
                        : 'text-[var(--color-ink-muted)] hover:bg-white/5 hover:text-[var(--color-ink)]'
                    )
                  }
                >
                  <Icon size={16} strokeWidth={2} />
                  {label}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div className="border-t border-[var(--color-border)] px-4 py-3">
        <div className="rounded-md border border-[var(--color-border)] bg-[var(--color-panel-raised)] px-3 py-2">
          <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Disclaimer</p>
          <p className="mt-1 text-[11px] leading-snug text-[var(--color-ink-muted)]">
            All attribution is a probabilistic assessment, not proof of identity. Human review required.
          </p>
        </div>
      </div>
    </aside>
  );
}
