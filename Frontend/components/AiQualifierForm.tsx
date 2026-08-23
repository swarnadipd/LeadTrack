"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { qualifyLead } from "@/lib/api";
import type { QualifiedLead } from "@/types";

export default function AiQualifierForm() {
  const router = useRouter();
  const [rawText, setRawText] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<QualifiedLead | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setResult(null);
    try {
      const lead = await qualifyLead(rawText);
      setResult(lead);
      setRawText("");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <h2 className="font-serif text-lg text-[var(--color-navy)]">
        Qualify a lead from raw notes
      </h2>
      <p className="text-xs text-[var(--color-ink)]/60">
        Paste an email or call notes — the pipeline extracts the lead, then
        decides a follow-up priority.
      </p>
      <textarea
        required
        rows={4}
        placeholder="Spoke with Riya Sharma at Acme Hospitality Group. Wants to refinance a 120-room hotel, budget ~$15M..."
        value={rawText}
        onChange={(e) => setRawText(e.target.value)}
        className="resize-none border border-[var(--color-ledger-line)] bg-white/60 p-2 text-sm outline-none focus:border-[var(--color-brass)]"
      />
      <button
        type="submit"
        disabled={submitting}
        className="self-start rounded-sm bg-[var(--color-brass)] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-[var(--color-brass-light)] disabled:opacity-50"
      >
        {submitting ? "Qualifying…" : "Qualify & add"}
      </button>
      {error && <p className="text-sm text-[var(--color-lost)]">{error}</p>}
      {result && (
        <div className="border-l-2 border-[var(--color-brass)] pl-3 text-sm">
          <p className="font-medium">
            {result.name} · {result.company ?? "—"}
          </p>
          <p className="text-[var(--color-ink)]/70">
            {result.ai_notes_summary}
          </p>
          <p className="mt-1 text-xs uppercase tracking-wide text-[var(--color-brass)]">
            Priority: {result.ai_priority}
          </p>
          <p className="text-xs text-[var(--color-ink)]/60">
            {result.ai_reason}
          </p>
        </div>
      )}
    </form>
  );
}
