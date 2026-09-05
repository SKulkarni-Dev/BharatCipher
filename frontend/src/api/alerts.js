// There is no alerts endpoint in the current backend (no /alerts route is
// documented). Rather than fabricate alerts or silently show an empty
// list that could be mistaken for "zero alerts exist", callers get an
// explicit `available: false` so the UI can render a clear "not
// connected" state instead of empty-but-working state.

export async function getAlerts() {
  return { available: false, alerts: [] };
}
