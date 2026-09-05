// Evidence arrives bundled inside an investigation document
// (`investigation.evidence`) from GET /investigations/<investigation_id>.
// These helpers are pure selectors over that already-fetched data, not
// network calls — there is no standalone /evidence endpoint in the
// current backend.

import { pick } from '@/utils/format';

export function getEvidence(investigation) {
  return Array.isArray(investigation?.evidence) ? investigation.evidence : [];
}

export function getEvidenceId(item) {
  return pick(item, ['evidence_id', 'id', '_id']);
}

export function getEvidenceById(investigation, evidenceId) {
  return getEvidence(investigation).find((e) => getEvidenceId(e) === evidenceId) || null;
}
