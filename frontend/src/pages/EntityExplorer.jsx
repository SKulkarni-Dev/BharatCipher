import { useMemo, useState } from 'react';
import { Search, X } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { RawFields } from '@/components/RawFields';
import { useLatestInvestigation } from '@/hooks/useLatestInvestigation';
import { getEntities, getEntityId } from '@/api/entities';
import { getEvidence } from '@/api/evidence';
import { pick, show, EMPTY } from '@/utils/format';

export default function EntityExplorer() {
  const { investigation, loading, error, empty } = useLatestInvestigation();
  const [query, setQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [selected, setSelected] = useState(null);

  const entities = useMemo(() => getEntities(investigation), [investigation]);
  const evidence = useMemo(() => getEvidence(investigation), [investigation]);
  const entityTypes = useMemo(
    () => [...new Set(entities.map((e) => pick(e, ['entity_type', 'type'])).filter(Boolean))],
    [entities]
  );

  const filtered = useMemo(() => {
    let rows = entities;
    if (typeFilter !== 'all') rows = rows.filter((e) => pick(e, ['entity_type', 'type']) === typeFilter);
    if (query.trim()) {
      const q = query.toLowerCase();
      rows = rows.filter((e) => {
        const value = String(pick(e, ['value', 'name', 'label']) || '').toLowerCase();
        const id = String(getEntityId(e) || '').toLowerCase();
        return value.includes(q) || id.includes(q);
      });
    }
    return rows;
  }, [entities, query, typeFilter]);

  const selectedEvidence = selected
    ? evidence.filter((ev) => Array.isArray(ev.entity_ids) && ev.entity_ids.includes(getEntityId(selected)))
    : [];

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading entities…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (empty) return <p className="text-[13px] text-[var(--color-ink-muted)]">No investigations yet — run one to populate entities.</p>;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <div className="lg:col-span-2 space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          <div className="relative max-w-xs flex-1">
            <Search size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-ink-faint)]" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search entity value or ID…"
              className="w-full rounded-md border border-[var(--color-border)] bg-[var(--color-panel)] py-2 pl-9 pr-3 text-[13px] text-[var(--color-ink)] outline-none focus:border-[var(--color-accent)]"
            />
          </div>
          <div className="flex flex-wrap gap-1.5">
            <FilterChip label="all" active={typeFilter === 'all'} onClick={() => setTypeFilter('all')} />
            {entityTypes.map((t) => (
              <FilterChip key={t} label={t} active={typeFilter === t} onClick={() => setTypeFilter(t)} />
            ))}
          </div>
        </div>

        <Card className="overflow-hidden">
          <table className="w-full text-left text-[13px]">
            <thead>
              <tr className="border-b border-[var(--color-border)] bg-white/[0.02] font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">
                <th className="px-4 py-3 font-medium">Entity ID</th>
                <th className="px-4 py-3 font-medium">Type</th>
                <th className="px-4 py-3 font-medium">Value</th>
                <th className="px-4 py-3 font-medium">First Seen</th>
                <th className="px-4 py-3 font-medium">Last Seen</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--color-border-soft)]">
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-[var(--color-ink-muted)]">{entities.length === 0 ? EMPTY : 'No entities match your filters.'}</td>
                </tr>
              )}
              {filtered.map((e) => (
                <tr
                  key={getEntityId(e)}
                  onClick={() => setSelected(e)}
                  className={`cursor-pointer transition-colors hover:bg-white/[0.03] ${selected && getEntityId(selected) === getEntityId(e) ? 'bg-white/[0.04]' : ''}`}
                >
                  <td className="px-4 py-2.5 font-mono text-[11.5px] text-[var(--color-ink-faint)]">{show(getEntityId(e))}</td>
                  <td className="px-4 py-2.5"><Badge tone="info">{show(pick(e, ['entity_type', 'type']))}</Badge></td>
                  <td className="px-4 py-2.5 font-mono text-[var(--color-ink)]">{show(pick(e, ['value', 'name', 'label']))}</td>
                  <td className="px-4 py-2.5 text-[var(--color-ink-muted)]">{show(e.first_seen)}</td>
                  <td className="px-4 py-2.5 text-[var(--color-ink-muted)]">{show(e.last_seen)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>

      <Card className="h-fit lg:sticky lg:top-6">
        {!selected ? (
          <div className="p-6 text-center text-[13px] text-[var(--color-ink-muted)]">Select an entity to view details</div>
        ) : (
          <div>
            <div className="flex items-start justify-between border-b border-[var(--color-border-soft)] px-5 py-4">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">{show(getEntityId(selected))}</p>
                <p className="mt-1 font-display text-[15px] font-semibold text-[var(--color-ink)]">{show(pick(selected, ['value', 'name', 'label']))}</p>
              </div>
              <button onClick={() => setSelected(null)} className="text-[var(--color-ink-muted)] hover:text-[var(--color-ink)]"><X size={16} /></button>
            </div>
            <div className="space-y-3 px-5 py-4 text-[13px]">
              <RawFields data={selected} exclude={['entity_id', 'id', '_id']} />
              <div>
                <p className="mb-1.5 font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Related Evidence</p>
                {selectedEvidence.length === 0 && <p className="text-[12px] text-[var(--color-ink-muted)]">No linked evidence found.</p>}
                <div className="space-y-2">
                  {selectedEvidence.map((ev, i) => (
                    <div key={i} className="rounded-md border border-[var(--color-border)] px-3 py-2">
                      <RawFields data={ev} />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </Card>
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
