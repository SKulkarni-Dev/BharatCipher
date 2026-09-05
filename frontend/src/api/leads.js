// No /leads endpoints are documented in the current backend API, and this
// module is not currently imported by any page. Kept as an integration
// point for when a leads endpoint exists; it makes a real request and
// does not fall back to demo data.

import { request } from './client';

export async function createLead(caseId, payload) {
  return request(`/cases/${caseId}/leads`, { method: 'POST', body: payload });
}

export async function getLead(leadId) {
  return request(`/leads/${leadId}`);
}
