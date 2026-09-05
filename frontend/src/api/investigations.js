// Investigations API — wired to the real backend.
//
// Backend contract (as provided):
//   POST /investigations                 { dataset_path }
//     -> { success, message, investigation_id }
//   GET  /investigations                 -> { success, count, investigations: [...] }
//   GET  /investigations/<investigation_id>
//     -> { success, investigation: { investigation_id, created_at,
//            observations, entities, relationships, evidence, hypotheses } }

import { request } from './client';

export async function getInvestigations() {
  const payload = await request('/investigations');
  return Array.isArray(payload?.investigations) ? payload.investigations : [];
}

export async function getInvestigation(investigationId) {
  const payload = await request(`/investigations/${investigationId}`);
  return payload?.investigation || null;
}

/**
 * dataset_path defaults to the development dataset called out by the
 * backend team while a dataset picker doesn't exist yet.
 */
export async function createInvestigation({ dataset_path = 'intelligence/ingestion/test_data.json' } = {}) {
  return request('/investigations', { method: 'POST', body: { dataset_path } });
}
