import { useEffect, useState } from 'react';
import { LogOut, ServerOff } from 'lucide-react';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { getSystemStatus } from '@/api/system';
import { API_BASE_URL } from '@/api/client';
import { useAuth } from '@/hooks/useAuth';
import { show } from '@/utils/format';

export default function Settings() {
  const [status, setStatus] = useState({ available: false, services: [] });
  const { investigator, logout } = useAuth();

  useEffect(() => {
    getSystemStatus().then(setStatus);
  }, []);

  return (
    <div className="space-y-6">
      {!status.available ? (
        <Card className="flex items-center gap-3 p-4">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-white/5 text-[var(--color-ink-muted)]">
            <ServerOff size={16} />
          </div>
          <div>
            <p className="font-display text-[13.5px] font-semibold text-[var(--color-ink)]">System status not available</p>
            <p className="mt-0.5 text-[11.5px] text-[var(--color-ink-muted)]">The backend doesn't currently expose a system/health status endpoint.</p>
          </div>
        </Card>
      ) : null}

      <Card>
        <CardHeader eyebrow="Environment" title="Runtime Configuration" />
        <CardBody className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <Row label="API Base URL" value={<span className="font-mono">{API_BASE_URL}</span>} />
        </CardBody>
      </Card>

      <Card>
        <CardHeader eyebrow="Session" title="Investigator Session" />
        <CardBody className="flex items-center justify-between">
          <div>
            <p className="text-[13px] font-medium text-[var(--color-ink)]">{show(investigator?.name)}</p>
            <p className="text-[12px] text-[var(--color-ink-muted)]">{show(investigator?.role)}</p>
          </div>
          <Button variant="danger" icon={LogOut} onClick={logout}>Log Out</Button>
        </CardBody>
      </Card>
    </div>
  );
}

function Row({ label, value }) {
  return (
    <div className="flex items-center justify-between border-b border-[var(--color-border-soft)] pb-2 text-[13px]">
      <span className="text-[var(--color-ink-muted)]">{label}</span>
      <span className="text-[var(--color-ink)]">{value}</span>
    </div>
  );
}
