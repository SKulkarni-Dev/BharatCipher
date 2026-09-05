// Attribution hypotheses arrive bundled inside an investigation document
// (`investigation.hypotheses`) from GET /investigations/<investigation_id>.
// Documented hypothesis fields: confidence, assessment,
// supporting_evidence_ids, contradicting_evidence_ids, entity_ids.
//
// There is no backend endpoint to re-run/challenge attribution — that
// capability does not exist in the current API, so it is not offered here.

import { pick } from '@/utils/format';

export function getHypotheses(investigation) {
  return Array.isArray(investigation?.hypotheses) ? investigation.hypotheses : [];
}

export function getHypothesisId(h, index) {
  return pick(h, ['hypothesis_id', 'id', '_id']) ?? `HYP-${index + 1}`;
}

/** The observations array, straight from the investigation document. */
export function getObservations(investigation) {
  return Array.isArray(investigation?.observations) ? investigation.observations : [];
}
