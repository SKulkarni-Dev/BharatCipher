# SIH26151 — Frontend

Dark Web Threat Actor De-Anonymization Platform — investigator-facing frontend.

This frontend is wired to the real Flask backend. There is no mock mode:
every page either calls a real backend endpoint or clearly says a feature
isn't connected yet, rather than showing synthetic data.

---

## 1. Folder structure

```
frontend/
├── src/
│   ├── api/            # API service layer — the only place that talks to the backend
│   ├── components/     # Shared UI (Card, Badge, Button, ConfidenceGauge, StatCard, RawFields…)
│   ├── layouts/         # Sidebar, Topbar, AppLayout shell
│   ├── pages/           # One file per route (14 pages)
│   ├── hooks/           # useAuth (session context), useLatestInvestigation
│   ├── utils/           # formatting + defensive-field-read helpers
│   └── types/           # (reserved for future TS types)
├── public/
├── .env.example
├── .env.development
├── package.json
└── README.md
```

## 2. Installation

```bash
cd frontend
npm install
```

## 3. Run (development)

```bash
npm run dev
```

Opens on `http://localhost:5173`. Set `VITE_API_BASE_URL` in `.env.development`
(defaults to `http://127.0.0.1:5000`) to point at your running Flask backend.

Log in with the **Development fallback login** (type any name — this sets a
local session only and does not call any backend; there is currently no
Face-ID backend endpoint to call).

## 4. Build for production

```bash
npm run build
```

## 5. Environment

Copy `.env.example` to `.env.local` and edit as needed.

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Base URL of the Flask backend. Defaults to `http://127.0.0.1:5000`. |

## 6. Backend endpoints actually used

| Function (`src/api/...`) | Method & Path |
|---|---|
| `getCases()` | `GET /cases` |
| `createCase()` | `POST /cases` |
| `getInvestigations()` | `GET /investigations` |
| `createInvestigation()` | `POST /investigations` (`{ dataset_path }`) |
| `getInvestigation(id)` | `GET /investigations/:investigation_id` |

Everything else that used to be a mock endpoint (`entities`, `evidence`,
`relationships`, `attribution`/`hypotheses`, `observations`) is **not** a
separate network call — those all arrive nested inside the single
`GET /investigations/:id` response, and `src/api/entities.js`,
`evidence.js`, `relationships.js`, and `attribution.js` are pure selectors
over that response.

## 7. Features not connected to a backend (by design, not oversight)

These are UI states, not bugs — the backend doesn't currently expose the
data or action they'd need:

- **Alerts** — no `/alerts` endpoint exists. The page and dashboard widget
  show an explicit "not connected" state instead of an empty list (so it
  isn't mistaken for "zero alerts").
- **System status** (Settings page) — no `/system/status` endpoint exists.
- **Challenge Attribution → Re-evaluate** — no endpoint exists to re-run
  attribution against new evidence. The page is now a read-only comparison
  of the hypotheses already returned by `GET /investigations/:id`.
- **Face-ID login** — `POST /api/auth/face-id` is not part of the current
  backend. The Scan Face button surfaces a clear message instead of faking
  a successful scan; the Development fallback login (local session only)
  still works for getting into the app.
- **Sources page** — no `/sources`/`/datasets`/`/feeds` endpoints exist.
  Sources are derived client-side from the `source` field already present
  on an investigation's `observations` and `evidence`, so "Add Dataset" /
  "Add Feed" actions were removed (they had no real backend to call).
- **Cases ↔ Investigations linkage** — `POST /investigations` only accepts
  `dataset_path`; there is no `case_id` field to associate a run with a
  case. The "New Investigation" page therefore has two independent forms:
  one that calls `POST /cases`, one that calls `POST /investigations`.

## 8. Data contract notes

The backend documents only a partial schema (e.g. hypothesis fields
`confidence`, `assessment`, `supporting_evidence_ids`,
`contradicting_evidence_ids`, `entity_ids`; entity fields `first_seen`/
`last_seen`; relationship fields `source_entity_id`/`target_entity_id`).
Where a field's exact name isn't documented, the frontend reads it
defensively (checking a few likely key names) via `src/utils/format.js`
`pick()`, and falls back to a visible "No data available" rather than
guessing or fabricating a value. Entity/evidence detail panels
(`src/components/RawFields.jsx`) render every field actually present on a
record generically, so nothing the backend returns is hidden and nothing
it doesn't return is invented.

## 9. Assumptions

- The `backend/` and `intelligence/` folders were not modified, per the brief.
- Attribution is always presented as a probabilistic, evidence-based
  assessment and never as proof of identity.
- No credentials, tokens, or secrets are stored in source or `localStorage`;
  session state (investigator identity) uses `sessionStorage` only and holds
  no secrets.

## 10. Dependencies

- `react-router-dom` — routing
- `lucide-react` — icons
- `recharts` — available for future charting
- `reactflow` — Investigation Graph (nodes/edges, click-to-inspect)
- `tailwindcss` + `@tailwindcss/vite` — styling
