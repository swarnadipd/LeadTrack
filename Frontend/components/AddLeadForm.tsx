"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { createLead } from "@/lib/api";

export default function AddLeadForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [company, setCompany] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await createLead({ name, email, company: company || undefined });
      setName("");
      setEmail("");
      setCompany("");
      router.refresh(); // re-runs the server component's data fetch
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <h2 className="font-serif text-lg text-[var(--color-navy)]">
        Add a lead manually
      </h2>
      <input
        required
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="border-b border-[var(--color-ledger-line)] bg-transparent py-1.5 text-sm outline-none focus:border-[var(--color-brass)]"
      />
      <input
        required
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="border-b border-[var(--color-ledger-line)] bg-transparent py-1.5 text-sm outline-none focus:border-[var(--color-brass)]"
      />
      <input
        placeholder="Company (optional)"
        value={company}
        onChange={(e) => setCompany(e.target.value)}
        className="border-b border-[var(--color-ledger-line)] bg-transparent py-1.5 text-sm outline-none focus:border-[var(--color-brass)]"
      />
      <button
        type="submit"
        disabled={submitting}
        className="mt-2 self-start rounded-sm bg-[var(--color-navy)] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-[var(--color-navy)]/90 disabled:opacity-50"
      >
        {submitting ? "Adding…" : "Add lead"}
      </button>
      {error && <p className="text-sm text-[var(--color-lost)]">{error}</p>}
    </form>
  );
}
