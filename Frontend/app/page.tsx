import { fetchLeads } from "@/lib/api";
import AddLeadForm from "@/components/AddLeadForm";
import AiQualifierForm from "@/components/AiQualifierForm";
import LeadsTable from "@/components/LeadsTable";
import type { Lead } from "@/types";

// Always fetch fresh leads server-side rather than caching the page —
// this is a live dashboard, not static marketing content.
export const dynamic = "force-dynamic";

export default async function Home() {
  let leads: Lead[] = [];
  let fetchError: string | null = null;

  try {
    leads = await fetchLeads();
  } catch {
    fetchError =
      "Couldn't reach the LeadTrack API. Is it running on localhost:8000?";
  }

  return (
    <main className="mx-auto w-full max-w-4xl flex-1 px-6 py-16">
      <header className="mb-12">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--color-brass)]">
          AI-ASSISTED CRM · PROTOTYPE
        </p>
        <h1 className="mt-2 font-serif text-4xl text-[var(--color-navy)]">
          LeadTrack
        </h1>
        <p className="mt-2 max-w-lg text-sm text-[var(--color-ink)]/60">
          A small lead ledger — add prospects by hand, or paste raw notes and
          let the AI pipeline extract and qualify them.
        </p>
      </header>

      {fetchError && (
        <p className="mb-8 border-l-2 border-[var(--color-lost)] pl-3 text-sm text-[var(--color-lost)]">
          {fetchError}
        </p>
      )}

      <section className="grid grid-cols-1 gap-10 sm:grid-cols-2">
        <AddLeadForm />
        <AiQualifierForm />
      </section>

      <LeadsTable leads={leads} />
    </main>
  );
}
