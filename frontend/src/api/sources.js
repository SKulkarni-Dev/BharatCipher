// There is no /sources (or /datasets, /feeds) endpoint in the current
// backend. Per the data-source contract, "sources" are derived from the
// actual `source` fields already present on observations and evidence
// inside an investigation document — never fabricated, and never a
// separate network call.

export function getSourcesFromInvestigation(investigation) {
  const counts = new Map();

  const bump = (name, key) => {
    if (!name) return;
    const entry = counts.get(name) || { name, observations: 0, evidence: 0 };
    entry[key] += 1;
    counts.set(name, entry);
  };

  (investigation?.observations || []).forEach((o) => bump(o?.source, 'observations'));
  (investigation?.evidence || []).forEach((e) => bump(e?.source, 'evidence'));

  return Array.from(counts.values());
}
