# LeadTrack Web — Next.js 15 + React 19 + TypeScript frontend

A small dashboard for the LeadTrack API: add leads manually, or paste raw
notes into the AI qualifier. Built with the App Router, Server Components
for data fetching, and Client Components for the two interactive forms.

## What's real here

- **Type-checks clean** (`npx tsc --noEmit`) — verified.
- **ESLint clean** — verified.
- **Production build succeeds** (`npm run build`) — verified, using a
  temporary system-font substitute (this sandbox can't reach Google
  Fonts to test the exact shipped version — see note below).
- **Runtime-tested against the real backend and real Postgres data** —
  verified: the homepage genuinely rendered live rows from the database
  through the Server Component, not mock data.

## One honest caveat

`app/layout.tsx` uses `next/font/google` (Geist + Source Serif 4), which
downloads font files from Google Fonts *at build time* and self-hosts
them — this is standard, zero-config Next.js behavior that works for
any project with normal internet access. The sandbox this was built in
couldn't reach `fonts.googleapis.com`, so that one specific step
(fetching the fonts) couldn't be verified here. Everything else — the
actual page logic, the data fetching, the two forms, the build process
itself — was verified using a temporary local-font substitute, then
swapped back to the real Google Fonts version before packaging. On your
Mac, with normal internet access, `npm run build` should just work. If
it doesn't, the error will clearly say "Failed to fetch font," and the
fix is simply checking your internet connection.

## Running it

```bash
npm install
npm run dev
```
Open http://localhost:3000. By default it talks to the API at
`http://localhost:8000` (plain uvicorn). Once you're running the full
`docker compose` stack from the backend project, set:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8080 npm run dev
```
to route through Nginx instead.

## Structure

```
app/page.tsx                    Server Component — fetches leads, renders the page
app/layout.tsx                  Root layout, fonts, metadata
components/AddLeadForm.tsx      Client Component — manual add form
components/AiQualifierForm.tsx  Client Component — AI pipeline form
components/LeadsTable.tsx       Server-renderable table
lib/api.ts                      Typed fetch calls to the FastAPI backend
types.ts                        Shared TypeScript types
```

## Talking points

- "The leads list is a Server Component — it fetches data on the server
  and streams rendered HTML, no client-side loading spinner for the
  initial view."
- "The two forms are Client Components (`use client`) since they need
  interactivity — state, event handlers. After a successful submit they
  call `router.refresh()`, which re-runs the server fetch without a full
  page reload — that's the actual mechanism connecting a client mutation
  back to server-rendered data in the App Router."
- "Types are shared between the API client and the components via a
  single `types.ts`, matching the FastAPI Pydantic schemas by hand right
  now — a natural next step would be generating these from the OpenAPI
  schema instead of keeping them in sync manually."
