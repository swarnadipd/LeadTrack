import type { Lead, QualifiedLead } from "@/types";

// Points at the FastAPI backend. In local dev this is uvicorn on :8000;
// once you're running the full docker-compose stack, point it at
// localhost:8080 (Nginx) instead via NEXT_PUBLIC_API_URL.
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function fetchLeads(): Promise<Lead[]> {
  const res = await fetch(`${API_BASE}/leads`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch leads (${res.status})`);
  return res.json();
}

export async function createLead(input: {
  name: string;
  email: string;
  company?: string;
}): Promise<Lead> {
  const res = await fetch(`${API_BASE}/leads`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) throw new Error(`Failed to create lead (${res.status})`);
  return res.json();
}

export async function qualifyLead(rawText: string): Promise<QualifiedLead> {
  const res = await fetch(`${API_BASE}/leads/qualify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ raw_text: rawText }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}) as { detail?: string });
    throw new Error(body.detail ?? `AI qualification failed (${res.status})`);
  }
  return res.json();
}
