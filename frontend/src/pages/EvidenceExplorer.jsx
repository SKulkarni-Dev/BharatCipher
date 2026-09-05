import { useMemo, useState } from 'react';
import { ExternalLink } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { RawFields } from '@/components/RawFields';
import { useLatestInvestigation } from '@/hooks/useLatestInvestigation';
import { getEvidence, getEvidenceId } from '@/api/evidence';
import { pick, show, EMPTY } from '@/utils/format';

export default function EvidenceExplorer() {
  const { investigation, loading, error, empty } = useLatestInvestigation();
  const [filter, setFilter] = useState('all');
  const [sourceModal, setSourceModal] = useState(null);

  const evidence = useMemo(() => getEvidence(investigation), [investigation]);
  const kinds = useMemo(() => [...new Set(evidence.map((e) => e.kind).filter(Boolean))], [evidence]);
  const filtered = filter === 'all' ? evidence : evidence.filter((e) => e.kind === filter);

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading evidence…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (empty) return <p className="text-[13px] text-[var(--color-ink-muted)]">No investigations yet — run one to populate evidence.</p>;

  return (
    <div className="space-y-4">
      {kinds.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          <FilterChip label="all" active={filter === 'all'} onClick={() => setFilter('all')} />
          {kinds.map((k) => (
            <FilterChip key={k} label={k} active={filter === k} onClick={() => setFilter(k)} />
          ))}
        </div>
      )}

      {filtered.length === 0 ? (
        <Card className="p-8 text-center text-[13px] text-[var(--color-ink-muted)]">{EMPTY}</Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {filtered.map((e) => (
            <Card key={getEvidenceId(e)} className="p-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-mono text-[11px] text-[var(--color-ink-faint)]">{show(getEvidenceId(e))}</p>
                  <p className="mt-0.5 font-display text-[14px] font-semibold text-[var(--color-ink)]">{show(pick(e, ['evidence_type', 'type']), (v) => String(v).replaceAll('_', ' '))}</p>
                </div>
                {e.kind && <Badge tone={e.kind === 'supporting' ? 'success' : 'contradiction'}>{e.kind}</Badge>}
              </div>
              {e.description && <p className="mt-2.5 text-[13px] text-[var(--color-ink)]">{e.description}</p>}
              <div className="mt-3">
                <RawFields data={e} exclude={['evidence_id', 'id', '_id', 'description', 'kind', 'evidence_type', 'type']} />
              </div>
              <Button variant="secondary" className="mt-3 !px-3 !py-1.5" icon={ExternalLink} onClick={() => setSourceModal(e)}>
                View Full Record
              </Button>
            </Card>
          ))}
        </div>
      )}

      {sourceModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4" onClick={() => setSourceModal(null)}>
          <Card className="w-full max-w-md p-5" onClick={(e) => e.stopPropagation()}>
            <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Evidence Record</p>
            <p className="mt-1 font-display text-[15px] font-semibold text-[var(--color-ink)]">{show(getEvidenceId(sourceModal))}</p>
            <div className="mt-3">
              <RawFields data={sourceModal} />
            </div>
            <Button variant="secondary" className="mt-4 w-full" onClick={() => setSourceModal(null)}>Close</Button>
          </Card>
        </div>
      )}
    </div>
  );
}

function FilterChip({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`rounded-md border px-2.5 py-1.5 font-mono text-[10.5px] uppercase tracking-wide transition-colors ${
        active ? 'border-[var(--color-accent)] bg-[color-mix(in_srgb,var(--color-accent)_16%,transparent)] text-[var(--color-accent)]' : 'border-[var(--color-border)] text-[var(--color-ink-muted)] hover:text-[var(--color-ink)]'
      }`}
    >
      {label}
    </button>
  );
}
