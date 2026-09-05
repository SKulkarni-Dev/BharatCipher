import { useEffect, useState, useCallback } from 'react';
import { getInvestigations, getInvestigation } from '@/api/investigations';

/**
 * Several pages (Entity Explorer, Investigation Graph, Evidence Explorer,
 * Attribution Assessment, Timeline, Sources) show data for "the"
 * investigation without an investigation id in their route. There is no
 * backend concept of a single "current" investigation, so this hook picks
 * the most recently created one from GET /investigations and loads its
 * full detail via GET /investigations/<id> — it never fabricates data.
 */
export function useLatestInvestigation() {
  const [investigation, setInvestigation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [empty, setEmpty] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    setEmpty(false);
    getInvestigations()
      .then((list) => {
        if (!list.length) {
          setInvestigation(null);
          setEmpty(true);
          setLoading(false);
          return;
        }
        const sorted = [...list].sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
        const latest = sorted[0];
        const id = latest.investigation_id || latest.id || latest._id;
        return getInvestigation(id).then((inv) => {
          setInvestigation(inv);
          setLoading(false);
        });
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return { investigation, loading, error, empty, reload: load };
}
