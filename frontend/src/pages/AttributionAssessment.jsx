import { useMemo } from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { ConfidenceGauge } from '@/components/ui/ConfidenceGauge';
import { useLatestInvestigation } from '@/hooks/useLatestInvestigation';
import { getHypotheses } from '@/api/attribution';
import { getEntities, getEntityId } from '@/api/entities';
import { getEvidence, getEvidenceId } from '@/api/evidence';
import { pick, show, EMPTY } from '@/utils/format';

export default function AttributionAssessment() {
  const { investigation, loading, error, empty } = useLatestInvestigation();
  const hypotheses = useMemo(() => getHypotheses(investigation), [investigation]);
  const entities = useMemo(() => getEntities(investigation), [investigation]);
  const evidence = useMemo(() => getEvidence(investigation), [investigation]);

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading attribution assessment…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (empty) return <p className="text-[13px] text-[var(--color-ink-muted)]">No investigations yet — run one to populate attribution hypotheses.</p>;

  function entityLabel(id) {
    const e = entities.find((en) => getEntityId(en) === id);
    return e ? show(pick(e, ['value', 'name', 'label'])) : id;
  }

  function evidenceLabel(id) {
    const e = evidence.find((ev) => getEvidenceId(ev) === id);
    return e ? show(pick(e, ['description', 'evidence_type', 'type'])) : id;
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader
          eyebrow={`Investigation ${investigation.investigation_id}`}
          title="Attribution Assessment"
          subtitle="This is a probabilistic, evidence-based assessment — not proof of identity."
        />
        <CardBody>
          {hypotheses.length === 0 ? (
            <p className="text-[13px] text-[var(--color-ink-muted)]">{EMPTY}</p>
          ) : (
            <div className="space-y-6">
              {hypotheses.map((h, i) => (
                <div key={i} className="border-b border-[var(--color-border-soft)] pb-6 last:border-0 last:pb-0">
                  <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
                    <div className="md:col-span-2">
                      <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Assessment</p>
                      <p className="mt-1 font-display text-lg font-semibold text-[var(--color-ink)]">{show(h.assessment)}</p>
                      <div className="mt-4 grid grid-cols-2 gap-3">
                        <MiniStat label="Supporting Evidence" value={Array.isArray(h.supporting_evidence_ids) ? h.supporting_evidence_ids.length : undefined} tone="success" />
                        <MiniStat label="Contradicting Evidence" value={Array.isArray(h.contradicting_evidence_ids) ? h.contradicting_evidence_ids.length : undefined} tone="contradiction" />
                      </div>
                    </div>
                    <div>
                      <ConfidenceGauge value={h.confidence} size="lg" label="Confidence" />
                    </div>
                  </div>

                  <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
                    <div>
                      <p className="mb-2 flex items-center gap-1.5 font-mono text-[11px] font-semibold uppercase tracking-wider text-[var(--color-success)]">
                        <CheckCircle2 size={13} /> Supporting
                      </p>
                      {(!h.supporting_evidence_ids || h.supporting_evidence_ids.length === 0) && <p className="text-[12px] text-[var(--color-ink-muted)]">{EMPTY}</p>}
                      <ul className="space-y-1 text-[12.5px] text-[var(--color-ink-muted)]">
                        {(h.supporting_evidence_ids || []).map((id) => <li key={id}>{evidenceLabel(id)}</li>)}
                      </ul>
                    </div>
                    <div>
                      <p className="mb-2 flex items-center gap-1.5 font-mono text-[11px] font-semibold uppercase tracking-wider text-[var(--color-contradiction)]">
                        <XCircle size={13} /> Contradicting
                      </p>
                      {(!h.contradicting_evidence_ids || h.contradicting_evidence_ids.length === 0) && <p className="text-[12px] text-[var(--color-ink-muted)]">{EMPTY}</p>}
                      <ul className="space-y-1 text-[12.5px] text-[var(--color-ink-muted)]">
                        {(h.contradicting_evidence_ids || []).map((id) => <li key={id}>{evidenceLabel(id)}</li>)}
                      </ul>
                    </div>
                  </div>

                  {Array.isArray(h.entity_ids) && h.entity_ids.length > 0 && (
                    <div className="mt-3">
                      <p className="mb-1.5 font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Entities</p>
                      <div className="flex flex-wrap gap-1.5">
                        {h.entity_ids.map((id) => <Badge key={id} tone="info">{entityLabel(id)}</Badge>)}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}

function MiniStat({ label, value, tone }) {
  const color = { success: 'var(--color-success)', contradiction: 'var(--color-contradiction)', info: 'var(--color-info)' }[tone];
  return (
    <div className="rounded-md border border-[var(--color-border)] px-3 py-2.5 text-center">
      <p className="font-display text-lg font-semibold" style={{ color }}>{show(value)}</p>
      <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">{label}</p>
    </div>
  );
}
