import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Plus, ArrowUpDown } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { getInvestigations } from '@/api/investigations';
import { pick, show, timeAgo } from '@/utils/format';

const SORTS = [
  { key: 'created_at', label: 'Created' },
  { key: 'investigation_id', label: 'ID' },
];

function idOf(inv) {
  return pick(inv, ['investigation_id', 'id', '_id']);
}

function countOf(inv, key) {
  return Array.isArray(inv?.[key]) ? inv[key].length : undefined;
}

export default function Investigations() {
  const navigate = useNavigate();
  const [investigations, setInvestigations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [sortKey, setSortKey] = useState('created_at');

  useEffect(() => {
    getInvestigations()
      .then((list) => {
        setInvestigations(list);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  const filtered = useMemo(() => {
    let rows = investigations;
    if (query.trim()) {
      const q = query.toLowerCase();
      rows = rows.filter((inv) => (idOf(inv) || '').toLowerCase().includes(q));
    }
    rows = [...rows].sort((a, b) => {
      if (sortKey === 'investigation_id') return (idOf(a) || '').localeCompare(idOf(b) || '');
      return new Date(b.created_at || 0) - new Date(a.created_at || 0);
    });
    return rows;
  }, [investigations, query, sortKey]);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-1 items-center gap-2">
          <div className="relative max-w-sm flex-1">
            <Search size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-ink-faint)]" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search investigation ID…"
              className="w-full rounded-md border border-[var(--color-border)] bg-[var(--color-panel)] py-2 pl-9 pr-3 text-[13px] text-[var(--color-ink)] outline-none focus:border-[var(--color-accent)]"
            />
          </div>
          <button
            onClick={() => setSortKey(SORTS[(SORTS.findIndex((s) => s.key === sortKey) + 1) % SORTS.length].key)}
            className="flex items-center gap-1.5 rounded-md border border-[var(--color-border)] bg-[var(--color-panel)] px-2.5 py-2 font-mono text-[11px] uppercase tracking-wide text-[var(--color-ink-muted)] hover:text-[var(--color-ink)]"
          >
            <ArrowUpDown size={13} />
            {SORTS.find((s) => s.key === sortKey)?.label}
          </button>
        </div>
        <Button icon={Plus} onClick={() => navigate('/investigations/new')}>
          Create Investigation
        </Button>
      </div>

      <Card className="overflow-hidden">
        <table className="w-full text-left text-[13px]">
          <thead>
            <tr className="border-b border-[var(--color-border)] bg-white/[0.02] font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">
              <th className="px-5 py-3 font-medium">Investigation ID</th>
              <th className="px-5 py-3 font-medium">Created</th>
              <th className="px-5 py-3 font-medium">Entities</th>
              <th className="px-5 py-3 font-medium">Relationships</th>
              <th className="px-5 py-3 font-medium">Evidence</th>
              <th className="px-5 py-3 font-medium">Hypotheses</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--color-border-soft)]">
            {loading ? (
              <tr>
                <td colSpan={6} className="px-5 py-8 text-center text-[var(--color-ink-muted)]">Loading investigations…</td>
              </tr>
            ) : error ? (
              <tr>
                <td colSpan={6} className="px-5 py-8 text-center text-[var(--color-risk)]">{error.message}</td>
              </tr>
            ) : filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-5 py-8 text-center text-[var(--color-ink-muted)]">
                  {investigations.length === 0 ? 'No investigations yet. Create one to get started.' : 'No investigations match your search.'}
                </td>
              </tr>
            ) : (
              filtered.map((inv) => {
                const id = idOf(inv);
                return (
                  <tr key={id} className="cursor-pointer transition-colors hover:bg-white/[0.03]" onClick={() => navigate(`/investigations/${id}`)}>
                    <td className="px-5 py-3">
                      <Link to={`/investigations/${id}`} className="font-mono text-[12px] font-medium text-[var(--color-ink)] hover:text-[var(--color-accent)]" onClick={(e) => e.stopPropagation()}>
                        {show(id)}
                      </Link>
                    </td>
                    <td className="px-5 py-3 text-[12px] text-[var(--color-ink-muted)]">{timeAgo(inv.created_at)}</td>
                    <td className="px-5 py-3 text-[var(--color-ink-muted)]">{show(countOf(inv, 'entities'))}</td>
                    <td className="px-5 py-3 text-[var(--color-ink-muted)]">{show(countOf(inv, 'relationships'))}</td>
                    <td className="px-5 py-3 text-[var(--color-ink-muted)]">{show(countOf(inv, 'evidence'))}</td>
                    <td className="px-5 py-3 text-[var(--color-ink-muted)]">{show(countOf(inv, 'hypotheses'))}</td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
