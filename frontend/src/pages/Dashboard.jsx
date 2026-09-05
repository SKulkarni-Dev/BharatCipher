import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FolderKanban, Bell, Users, Archive, Target, ArrowRight, BellOff } from 'lucide-react';
import { StatCard } from '@/components/StatCard';
import { Card, CardHeader } from '@/components/ui/Card';
import { getCases } from '@/api/cases';
import { getInvestigations } from '@/api/investigations';
import { getAlerts } from '@/api/alerts';
import { pick, show, timeAgo, EMPTY } from '@/utils/format';

function countIfArray(obj, key) {
  return Array.isArray(obj?.[key]) ? obj[key].length : undefined;
}

export default function Dashboard() {
  const [cases, setCases] = useState([]);
  const [investigations, setInvestigations] = useState([]);
  const [alertsState, setAlertsState] = useState({ available: false, alerts: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([getCases(), getInvestigations(), getAlerts()])
      .then(([c, inv, a]) => {
        setCases(c);
        setInvestigations(inv);
        setAlertsState(a);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <PageSkeleton />;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;

  // Totals below are only summed when the list endpoints already include the
  // nested arrays; otherwise the stat shows the unavailable state rather
  // than a fabricated number.
  const entityTotals = investigations.map((i) => countIfArray(i, 'entities'));
  const evidenceTotals = investigations.map((i) => countIfArray(i, 'evidence'));
  const hasNestedCounts = entityTotals.some((v) => v !== undefined);

  const trackedEntities = hasNestedCounts ? entityTotals.reduce((a, b) => a + (b || 0), 0) : undefined;
  const evidenceItems = hasNestedCounts ? evidenceTotals.reduce((a, b) => a + (b || 0), 0) : undefined;

  const recentInvestigations = [...investigations]
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .slice(0, 4);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
        <StatCard label="Cases" value={show(cases.length)} icon={FolderKanban} tone="accent" />
        <StatCard label="Investigations" value={show(investigations.length)} icon={Target} tone="contradiction" />
        <StatCard label="New Alerts" value={alertsState.available ? show(alertsState.alerts.filter((a) => !a.read).length) : EMPTY} icon={Bell} tone="warning" />
        <StatCard label="Tracked Entities" value={show(trackedEntities)} icon={Users} tone="info" />
        <StatCard label="Evidence Items" value={show(evidenceItems)} icon={Archive} tone="success" />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader
            eyebrow="Pipeline Runs"
            title="Recent Investigations"
            action={
              <Link to="/investigations" className="flex items-center gap-1 font-mono text-[11px] uppercase tracking-wide text-[var(--color-ink-muted)] hover:text-[var(--color-accent)]">
                View all <ArrowRight size={12} />
              </Link>
            }
          />
          <div className="divide-y divide-[var(--color-border-soft)]">
            {recentInvestigations.length === 0 && (
              <p className="px-5 py-6 text-[13px] text-[var(--color-ink-muted)]">No investigations yet.</p>
            )}
            {recentInvestigations.map((inv) => {
              const id = pick(inv, ['investigation_id', 'id', '_id']);
              return (
                <Link key={id} to={`/investigations/${id}`} className="flex items-center justify-between gap-4 px-5 py-3.5 transition-colors hover:bg-white/[0.03]">
                  <div className="min-w-0">
                    <span className="font-mono text-[12px] text-[var(--color-ink-faint)]">{id}</span>
                    <p className="mt-0.5 text-[11px] text-[var(--color-ink-muted)]">Created {timeAgo(inv.created_at)}</p>
                  </div>
                  <div className="shrink-0 font-mono text-[11px] text-[var(--color-ink-muted)]">
                    {show(countIfArray(inv, 'entities'))} entities
                  </div>
                </Link>
              );
            })}
          </div>
        </Card>

        <Card>
          <CardHeader
            eyebrow="Live Feed"
            title="Recent Alerts"
            action={
              <Link to="/alerts" className="flex items-center gap-1 font-mono text-[11px] uppercase tracking-wide text-[var(--color-ink-muted)] hover:text-[var(--color-accent)]">
                View all <ArrowRight size={12} />
              </Link>
            }
          />
          {!alertsState.available ? (
            <div className="flex flex-col items-center gap-2 px-5 py-8 text-center">
              <BellOff size={20} className="text-[var(--color-ink-faint)]" />
              <p className="text-[12px] text-[var(--color-ink-muted)]">Alerts API not connected.</p>
            </div>
          ) : alertsState.alerts.length === 0 ? (
            <p className="px-5 py-6 text-[13px] text-[var(--color-ink-muted)]">No alerts.</p>
          ) : null}
        </Card>
      </div>
    </div>
  );
}

function PageSkeleton() {
  return <div className="animate-pulse-soft text-[13px] text-[var(--color-ink-muted)]">Loading dashboard…</div>;
}
