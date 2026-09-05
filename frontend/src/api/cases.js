// Cases API — wired to the real backend.
//
// Backend contract (as provided):
//   POST /cases   { title, description }
//   GET  /cases   -> { success, count, cases: [...] }
//
// The backend does not document the exact shape of each case object beyond
// the fields it accepts on creation, so callers should read fields
// defensively (see src/utils/format.js `pick`).

import { request } from './client';

export async function getCases() {
  const payload = await request('/cases');
  return Array.isArray(payload?.cases) ? payload.cases : [];
}

export async function createCase({ title, description }) {
  return request('/cases', { method: 'POST', body: { title, description } });
}
