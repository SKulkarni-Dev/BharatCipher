// There is no /system/status endpoint in the current backend. Rather than
// fabricate service health data, callers get an explicit `available: false`.

export async function getSystemStatus() {
  return { available: false, services: [] };
}
