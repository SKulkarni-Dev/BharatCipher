import { useMemo } from 'react';
import { Card } from '@/components/ui/Card';
import { useLatestInvestigation } from '@/hooks/useLatestInvestigation';
import { getSourcesFromInvestigation } from '@/api/sources';
import { EMPTY } from '@/utils/format';

export default function Sources() {
  const { investigation, loading, error, empty } = useLatestInvestigation();
  const sources = useMemo(() => getSourcesFromInvestigation(investigation), [investigation]);

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading sources…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (empty) return <p className="text-[13px] text-[var(--color-ink-muted)]">No investigations yet — run one to populate sources.</p>;

  return (
    <div className="space-y-4">
      <p className="text-[12.5px] text-[var(--color-ink-muted)]">
        There is no dedicated sources endpoint in the current backend. These are the distinct <code className="font-mono">source</code> values
        found on observations and evidence in investigation <span className="font-mono">{investigation.investigation_id}</span>.
      </p>

      {sources.length === 0 ? (
        <Card className="p-8 text-center text-[13px] text-[var(--color-ink-muted)]">{EMPTY}</Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {sources.map((s) => (
            <Card key={s.name} className="p-4">
              <p className="font-display text-[14px] font-semibold text-[var(--color-ink)]">{s.name}</p>
              <div className="mt-3 grid grid-cols-2 gap-2 text-center">
                <MiniMetric label="Observations" value={s.observations} />
                <MiniMetric label="Evidence" value={s.evidence} />
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

function MiniMetric({ label, value }) {
  return (
    <div className="rounded bg-white/[0.03] py-2">
      <p className="font-display text-[13px] font-semibold text-[var(--color-ink)]">{value}</p>
      <p className="font-mono text-[9px] uppercase tracking-wider text-[var(--color-ink-faint)]">{label}</p>
    </div>
  );
}
