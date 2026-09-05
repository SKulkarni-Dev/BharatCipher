import { useMemo, useState } from 'react';
import { ShieldAlert, CheckCircle2, XCircle } from 'lucide-react';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { useLatestInvestigation } from '@/hooks/useLatestInvestigation';
import { getHypotheses } from '@/api/attribution';
import { show, EMPTY } from '@/utils/format';

const TONES = ['success', 'warning', 'contradiction', 'info', 'accent'];

export default function ChallengeAttribution() {
  const { investigation, loading, error, empty } = useLatestInvestigation();
  const hypotheses = useMemo(() => getHypotheses(investigation), [investigation]);
  const [expanded, setExpanded] = useState(0);

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading hypotheses…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (empty) return <p className="text-[13px] text-[var(--color-ink-muted)]">No investigations yet — run one to populate hypotheses.</p>;

  return (
    <div className="space-y-6">
      <Card className="border-[color-mix(in_srgb,var(--color-contradiction)_40%,var(--color-border))]">
        <CardBody className="flex flex-wrap items-start gap-3">
          <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-[color-mix(in_srgb,var(--color-contradiction)_16%,transparent)] text-[var(--color-contradiction)]">
            <ShieldAlert size={18} />
          </div>
          <div>
            <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-contradiction)]">Challenge Attribution</p>
            <p className="mt-1 text-[12.5px] text-[var(--color-ink-muted)]">
              Compare the assessed hypotheses side by side. Re-running attribution against new evidence isn't available yet —
              the backend doesn't currently expose an endpoint to re-evaluate a hypothesis.
            </p>
          </div>
        </CardBody>
      </Card>

      {hypotheses.length === 0 ? (
        <Card className="p-8 text-center text-[13px] text-[var(--color-ink-muted)]">{EMPTY}</Card>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {hypotheses.map((h, i) => (
              <button key={i} onClick={() => setExpanded(i)} className="text-left">
                <Card className={`h-full border-l-4 p-4 transition-shadow ${expanded === i ? 'shadow-[0_0_0_1px_var(--color-border)]' : ''}`} style={{ borderLeftColor: `var(--color-${TONES[i % TONES.length]})` }}>
                  <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">HYPOTHESIS {i + 1}</p>
                  <p className="mt-1 font-display text-[14px] font-semibold text-[var(--color-ink)]">{show(h.assessment)}</p>
                  <p className="mt-3 font-mono text-2xl font-semibold" style={{ color: `var(--color-${TONES[i % TONES.length]})` }}>{show(h.confidence, (v) => `${Math.round(v * 100)}%`)}</p>
                  <div className="mt-3 flex gap-4 text-[11.5px] text-[var(--color-ink-muted)]">
                    <span className="flex items-center gap-1"><CheckCircle2 size={12} className="text-[var(--color-success)]" /> {show(h.supporting_evidence_ids?.length)}</span>
                    <span className="flex items-center gap-1"><XCircle size={12} className="text-[var(--color-contradiction)]" /> {show(h.contradicting_evidence_ids?.length)}</span>
                  </div>
                </Card>
              </button>
            ))}
          </div>

          {hypotheses[expanded] && (
            <Card>
              <CardHeader
                eyebrow={`Hypothesis ${expanded + 1}`}
                title={show(hypotheses[expanded].assessment)}
                action={<Badge tone={TONES[expanded % TONES.length]}>{show(hypotheses[expanded].confidence, (v) => `${Math.round(v * 100)}%`)} confidence</Badge>}
              />
              <CardBody className="space-y-4">
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  <div>
                    <p className="mb-2 flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wider text-[var(--color-success)]">
                      <CheckCircle2 size={12} /> Supporting ({hypotheses[expanded].supporting_evidence_ids?.length ?? 0})
                    </p>
                    <ul className="space-y-1 font-mono text-[11.5px] text-[var(--color-ink-muted)]">
                      {(hypotheses[expanded].supporting_evidence_ids || []).map((id) => <li key={id}>{id}</li>)}
                    </ul>
                  </div>
                  <div>
                    <p className="mb-2 flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wider text-[var(--color-contradiction)]">
                      <XCircle size={12} /> Contradicting ({hypotheses[expanded].contradicting_evidence_ids?.length ?? 0})
                    </p>
                    <ul className="space-y-1 font-mono text-[11.5px] text-[var(--color-ink-muted)]">
                      {(hypotheses[expanded].contradicting_evidence_ids || []).map((id) => <li key={id}>{id}</li>)}
                    </ul>
                  </div>
                </div>
              </CardBody>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
