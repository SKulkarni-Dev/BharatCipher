import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Share2, Archive, History, ArrowLeft } from 'lucide-react';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { getInvestigation } from '@/api/investigations';
import { getEntities, getEntityId } from '@/api/entities';
import { getEvidence, getEvidenceId } from '@/api/evidence';
import { getRelationships } from '@/api/relationships';
import { getHypotheses } from '@/api/attribution';
import { pick, show, formatDateTime, EMPTY } from '@/utils/format';

export default function InvestigationDetails() {
  const { caseId: investigationId } = useParams();
  const navigate = useNavigate();
  const [investigation, setInvestigation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getInvestigation(investigationId)
      .then((inv) => {
        setInvestigation(inv);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, [investigationId]);

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading investigation…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (!investigation) return <p className="text-[13px] text-[var(--color-risk)]">Investigation not found.</p>;

  const entities = getEntities(investigation);
  const evidence = getEvidence(investigation);
  const relationships = getRelationships(investigation);
  const hypotheses = getHypotheses(investigation);

  return (
    <div className="space-y-6">
      <button onClick={() => navigate('/investigations')} className="flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wide text-[var(--color-ink-muted)] hover:text-[var(--color-ink)]">
        <ArrowLeft size={13} /> All Investigations
      </button>

      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <span className="font-mono text-[12px] text-[var(--color-ink-faint)]">{investigation.investigation_id}</span>
          <h2 className="mt-1 font-display text-xl font-semibold text-[var(--color-ink)]">Investigation {investigation.investigation_id}</h2>
          <p className="mt-1 text-[12.5px] text-[var(--color-ink-muted)]">Created {formatDateTime(investigation.created_at)}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" icon={Share2} onClick={() => navigate('/graph')}>View Graph</Button>
          <Button variant="secondary" icon={Archive} onClick={() => navigate('/evidence')}>View Evidence</Button>
          <Button variant="secondary" icon={History} onClick={() => navigate('/timeline')}>View Timeline</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader eyebrow="Attribution" title="Attribution Hypotheses" subtitle="Evidence-based assessment. Not proof of identity." />
          <CardBody>
            {hypotheses.length === 0 ? (
              <p className="text-[12.5px] text-[var(--color-ink-muted)]">{EMPTY}</p>
            ) : (
              <div className="space-y-3">
                {hypotheses.slice(0, 3).map((h, i) => (
                  <div key={i} className="flex items-center justify-between rounded-md border border-[var(--color-border)] px-3 py-2.5">
                    <span className="text-[13px] text-[var(--color-ink)]">{show(pick(h, ['assessment', 'title', 'label']))}</span>
                    <span className="font-mono text-[13px] font-semibold text-[var(--color-accent)]">{show(h.confidence, (v) => `${Math.round(v * 100)}%`)}</span>
                  </div>
                ))}
              </div>
            )}
            <Link to="/attribution" className="mt-4 inline-block font-mono text-[11px] uppercase tracking-wide text-[var(--color-accent)] hover:underline">
              View full attribution assessment →
            </Link>
          </CardBody>
        </Card>

        <Card>
          <CardHeader eyebrow="Summary" title="Investigation Summary" />
          <CardBody className="space-y-2 text-[13px]">
            <Row label="Investigation ID" value={investigation.investigation_id} mono />
            <Row label="Created" value={formatDateTime(investigation.created_at)} />
            <Row label="Entities" value={entities.length} />
            <Row label="Evidence Items" value={evidence.length} />
            <Row label="Relationships" value={relationships.length} />
            <Row label="Hypotheses" value={hypotheses.length} />
          </CardBody>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader eyebrow="Summary" title="Evidence Summary" />
          <CardBody className="space-y-2">
            {evidence.length === 0 && <p className="text-[12.5px] text-[var(--color-ink-muted)]">{EMPTY}</p>}
            {evidence.slice(0, 4).map((e) => (
              <div key={getEvidenceId(e)} className="flex items-center justify-between text-[12.5px]">
                <span className="text-[var(--color-ink)]">{show(pick(e, ['evidence_type', 'type']), (v) => String(v).replaceAll('_', ' '))}</span>
                <span className="font-mono text-[11px] text-[var(--color-ink-faint)]">{show(getEvidenceId(e))}</span>
              </div>
            ))}
          </CardBody>
        </Card>
        <Card>
          <CardHeader eyebrow="Summary" title="Entity Summary" />
          <CardBody className="space-y-2">
            {entities.length === 0 && <p className="text-[12.5px] text-[var(--color-ink-muted)]">{EMPTY}</p>}
            {entities.slice(0, 4).map((e) => (
              <div key={getEntityId(e)} className="flex items-center justify-between text-[12.5px]">
                <span className="font-mono text-[var(--color-ink)]">{show(pick(e, ['value', 'name', 'label']))}</span>
                <span className="font-mono text-[10px] uppercase text-[var(--color-ink-faint)]">{show(pick(e, ['entity_type', 'type']))}</span>
              </div>
            ))}
          </CardBody>
        </Card>
      </div>
    </div>
  );
}

function Row({ label, value, mono }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-[var(--color-ink-muted)]">{label}</span>
      <span className={mono ? 'font-mono text-[var(--color-ink)]' : 'text-[var(--color-ink)]'}>{show(value)}</span>
    </div>
  );
}
