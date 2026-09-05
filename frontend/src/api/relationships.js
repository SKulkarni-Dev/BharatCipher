// Relationships arrive bundled inside an investigation document
// (`investigation.relationships`) from GET /investigations/<investigation_id>.
// These helpers are pure selectors — there is no standalone endpoint.

import { getEntityId } from './entities';

export function getRelationships(investigation) {
  return Array.isArray(investigation?.relationships) ? investigation.relationships : [];
}

/**
 * Resolves source_entity_id / target_entity_id against the investigation's
 * real entity list. Relationships that point at an entity id not present
 * in investigation.entities are dropped rather than rendered as a
 * fabricated/placeholder node.
 */
export function getResolvedRelationships(investigation) {
  const entities = Array.isArray(investigation?.entities) ? investigation.entities : [];
  const entityIds = new Set(entities.map(getEntityId));
  return getRelationships(investigation).filter(
    (r) => entityIds.has(r.source_entity_id) && entityIds.has(r.target_entity_id)
  );
}
