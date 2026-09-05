// Entities are not fetched from a dedicated endpoint — they arrive bundled
// inside an investigation document (`investigation.entities`) from
// GET /investigations/<investigation_id>. These helpers are pure selectors
// over that already-fetched data, not network calls.

import { pick } from '@/utils/format';

export function getEntities(investigation) {
  return Array.isArray(investigation?.entities) ? investigation.entities : [];
}

export function getEntityId(entity) {
  return pick(entity, ['entity_id', 'id', '_id']);
}

export function getEntity(investigation, entityId) {
  return getEntities(investigation).find((e) => getEntityId(e) === entityId) || null;
}
