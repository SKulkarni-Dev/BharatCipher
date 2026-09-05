// Central API client for SIH26151.
//
// Every function in src/api/ talks to the real Flask backend at
// API_BASE_URL. Nothing in this app falls back to synthetic/demo data —
// if the backend doesn't have something, callers surface an empty or
// error state instead.
//
// No component ever fetches directly - they only ever import from
// src/api/*, so this is the single place that knows the backend's base URL.

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

class ApiError extends Error {
  constructor(message, status, payload) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.payload = payload;
  }
}

/** Thin fetch wrapper used by every API function in src/api/. */
export async function request(path, { method = 'GET', body, headers = {}, signal } = {}) {
  let res;
  try {
    res = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      body: body ? JSON.stringify(body) : undefined,
      signal,
    });
  } catch (err) {
    // Network-level failure (backend down, CORS, DNS, offline, etc.)
    throw new ApiError(
      `Could not reach the backend at ${API_BASE_URL}. Is it running?`,
      0,
      null
    );
  }

  let payload = null;
  try {
    payload = await res.json();
  } catch (_) {
    // no JSON body
  }

  if (!res.ok) {
    throw new ApiError(payload?.message || `Request failed (${res.status})`, res.status, payload);
  }
  if (payload && payload.success === false) {
    throw new ApiError(payload.message || 'Request was not successful', res.status, payload);
  }
  return payload;
}

export { ApiError };
