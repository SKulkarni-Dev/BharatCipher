import { useEffect, useState } from 'react';
import { BellOff } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { getAlerts } from '@/api/alerts';

export default function Alerts() {
  const [state, setState] = useState({ available: false, alerts: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAlerts().then((s) => {
      setState(s);
      setLoading(false);
    });
  }, []);

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading alerts…</p>;

  if (!state.available) {
    return (
      <Card className="flex flex-col items-center gap-3 p-10 text-center">
        <BellOff size={28} className="text-[var(--color-ink-faint)]" />
        <p className="text-[14px] font-medium text-[var(--color-ink)]">Alerts aren't connected yet</p>
        <p className="max-w-md text-[12.5px] text-[var(--color-ink-muted)]">
          The current backend doesn't expose an alerts API. This page will populate once an <code className="font-mono">/alerts</code> endpoint is available.
        </p>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {state.alerts.length === 0 && (
        <Card className="p-8 text-center text-[13px] text-[var(--color-ink-muted)]">No alerts.</Card>
      )}
    </div>
  );
}
