import { useMemo } from 'react';
import { Eye, FileText, Users } from 'lucide-react';
import { Card, CardHeader } from '@/components/ui/Card';
import { useLatestInvestigation } from '@/hooks/useLatestInvestigation';
import { getObservations } from '@/api/attribution';
import { getEntities, getEntityId } from '@/api/entities';
import { getEvidence, getEvidenceId } from '@/api/evidence';
import { pick, show, formatDateTime, EMPTY } from '@/utils/format';

const KIND_META = {
  observation: { icon: Eye, color: 'var(--color-info)' },
  evidence: { icon: FileText, color: 'var(--color-normal)' },
  entity: { icon: Users, color: 'var(--color-accent)' },
};

/** Builds a chronological list purely from real timestamps already present on the data — no synthetic events. */
function buildTimeline(investigation) {
  const events = [];

  getObservations(investigation).forEach((o, i) => {
    if (o.observed_at) {
      events.push({
        id: `obs-${i}`,
        date: o.observed_at,
        kind: 'observation',
        label: show(pick(o, ['content', 'description', 'observation_type', 'type'])),
        detail: show(pick(o, ['source'])),
      });
    }
  });

  getEntities(investigation).forEach((e) => {
    const id = getEntityId(e);
    if (e.first_seen) {
      events.push({ id: `${id}-first`, date: e.first_seen, kind: 'entity', label: `Entity first seen: ${show(pick(e, ['value', 'name', 'label']))}`, detail: show(pick(e, ['entity_type', 'type'])) });
    }
    if (e.last_seen) {
      events.push({ id: `${id}-last`, date: e.last_seen, kind: 'entity', label: `Entity last seen: ${show(pick(e, ['value', 'name', 'label']))}`, detail: show(pick(e, ['entity_type', 'type'])) });
    }
  });

  getEvidence(investigation).forEach((e) => {
    if (e.observed_at) {
      events.push({
        id: getEvidenceId(e),
        date: e.observed_at,
        kind: 'evidence',
        label: show(pick(e, ['description', 'evidence_type', 'type'])),
        detail: show(pick(e, ['source'])),
      });
    }
  });

  return events
    .filter((e) => !Number.isNaN(new Date(e.date).getTime()))
    .sort((a, b) => new Date(a.date) - new Date(b.date));
}

export default function Timeline() {
  const { investigation, loading, error, empty } = useLatestInvestigation();
  const events = useMemo(() => buildTimeline(investigation), [investigation]);

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading timeline…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (empty) return <p className="text-[13px] text-[var(--color-ink-muted)]">No investigations yet — run one to populate a timeline.</p>;

  return (
    <Card>
      <CardHeader
        eyebrow={`Investigation ${investigation.investigation_id}`}
        title="Investigation Timeline"
        subtitle="Chronological record built from observation, entity, and evidence timestamps."
      />
      <div className="px-6 py-8">
        {events.length === 0 ? (
          <p className="text-[13px] text-[var(--color-ink-muted)]">{EMPTY}</p>
        ) : (
          <div className="relative ml-3 space-y-8 border-l-2 border-[var(--color-border)] pl-8">
            {events.map((e) => {
              const meta = KIND_META[e.kind] || KIND_META.observation;
              const Icon = meta.icon;
              return (
                <div key={e.id} className="relative">
                  <span
                    className="absolute -left-[41px] flex h-6 w-6 items-center justify-center rounded-full border-2"
                    style={{ borderColor: meta.color, backgroundColor: 'var(--color-panel)', color: meta.color }}
                  >
                    <Icon size={12} />
                  </span>
                  <div className="flex flex-wrap items-baseline gap-2">
                    <span className="font-mono text-[11px] font-semibold uppercase tracking-wider" style={{ color: meta.color }}>{e.kind}</span>
                    <span className="font-mono text-[11px] text-[var(--color-ink-faint)]">{formatDateTime(e.date)}</span>
                  </div>
                  <p className="mt-1 font-display text-[14px] font-semibold text-[var(--color-ink)]">{e.label}</p>
                  {e.detail && e.detail !== EMPTY && <p className="mt-0.5 text-[12.5px] text-[var(--color-ink-muted)]">{e.detail}</p>}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </Card>
  );
}
