import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PlayCircle, FolderPlus, CheckCircle2 } from 'lucide-react';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { createInvestigation } from '@/api/investigations';
import { createCase } from '@/api/cases';

const DEFAULT_DATASET_PATH = 'intelligence/ingestion/test_data.json';

export default function NewInvestigation() {
  const navigate = useNavigate();

  const [datasetPath, setDatasetPath] = useState(DEFAULT_DATASET_PATH);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const [caseForm, setCaseForm] = useState({ title: '', description: '' });
  const [caseSubmitting, setCaseSubmitting] = useState(false);
  const [caseError, setCaseError] = useState(null);
  const [caseCreated, setCaseCreated] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const result = await createInvestigation({ dataset_path: datasetPath });
      navigate(`/investigations/${result.investigation_id}`);
    } catch (err) {
      setError(err);
      setSubmitting(false);
    }
  }

  async function handleCaseSubmit(e) {
    e.preventDefault();
    setCaseSubmitting(true);
    setCaseError(null);
    try {
      const result = await createCase(caseForm);
      setCaseCreated(result);
      setCaseForm({ title: '', description: '' });
    } catch (err) {
      setCaseError(err);
    } finally {
      setCaseSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <Card>
        <CardHeader
          eyebrow="Pipeline Run"
          title="New Investigation"
          subtitle="Runs the intelligence pipeline against a dataset to extract entities, relationships, evidence, and attribution hypotheses."
        />
        <form onSubmit={handleSubmit}>
          <CardBody className="space-y-5">
            <Field label="Dataset Path">
              <input
                required
                value={datasetPath}
                onChange={(e) => setDatasetPath(e.target.value)}
                placeholder={DEFAULT_DATASET_PATH}
                className="input font-mono"
              />
              <p className="mt-1.5 text-[11.5px] text-[var(--color-ink-muted)]">
                Path to the dataset file the backend should ingest, e.g. <code className="font-mono">{DEFAULT_DATASET_PATH}</code>.
              </p>
            </Field>
            {error && <p className="text-[12.5px] text-[var(--color-risk)]">{error.message}</p>}
          </CardBody>
          <div className="flex items-center justify-end gap-2 border-t border-[var(--color-border-soft)] px-5 py-4">
            <Button type="button" variant="secondary" onClick={() => navigate('/investigations')}>
              Cancel
            </Button>
            <Button type="submit" icon={PlayCircle} disabled={submitting}>
              {submitting ? 'Starting…' : 'Start Investigation'}
            </Button>
          </div>
        </form>
      </Card>

      <Card>
        <CardHeader
          eyebrow="Case Management"
          title="Create a Case"
          subtitle="Optional. The current backend does not link a case to an investigation — this creates a case record independently via POST /cases."
        />
        <form onSubmit={handleCaseSubmit}>
          <CardBody className="space-y-5">
            <Field label="Title">
              <input
                required
                value={caseForm.title}
                onChange={(e) => setCaseForm((f) => ({ ...f, title: e.target.value }))}
                placeholder="e.g. ShadowX Investigation"
                className="input"
              />
            </Field>
            <Field label="Description">
              <textarea
                value={caseForm.description}
                onChange={(e) => setCaseForm((f) => ({ ...f, description: e.target.value }))}
                placeholder="Context for this case, authorization reference, scope notes…"
                rows={3}
                className="input resize-none"
              />
            </Field>
            {caseError && <p className="text-[12.5px] text-[var(--color-risk)]">{caseError.message}</p>}
            {caseCreated && (
              <p className="flex items-center gap-1.5 text-[12.5px] text-[var(--color-success)]">
                <CheckCircle2 size={14} /> Case created.
              </p>
            )}
          </CardBody>
          <div className="flex items-center justify-end gap-2 border-t border-[var(--color-border-soft)] px-5 py-4">
            <Button type="submit" variant="secondary" icon={FolderPlus} disabled={caseSubmitting}>
              {caseSubmitting ? 'Creating…' : 'Create Case'}
            </Button>
          </div>
        </form>
      </Card>

      <style>{`
        .input {
          width: 100%;
          border-radius: 0.375rem;
          border: 1px solid var(--color-border);
          background: var(--color-panel-raised);
          padding: 0.5rem 0.75rem;
          font-size: 13px;
          color: var(--color-ink);
          outline: none;
        }
        .input:focus { border-color: var(--color-accent); }
      `}</style>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <div>
      <label className="mb-1.5 block font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">{label}</label>
      {children}
    </div>
  );
}
