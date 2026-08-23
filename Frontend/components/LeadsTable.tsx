import type { Lead } from "@/types";

const STATUS_LABEL: Record<string, string> = {
  new: "New",
  contacted: "Contacted",
  won: "Won",
  lost: "Lost",
};

const STATUS_DOT: Record<string, string> = {
  new: "bg-[var(--color-navy)]",
  contacted: "bg-[var(--color-brass)]",
  won: "bg-[var(--color-won)]",
  lost: "bg-[var(--color-lost)]",
};

export default function LeadsTable({ leads }: { leads: Lead[] }) {
  if (leads.length === 0) {
    return (
      <p className="mt-10 text-sm text-[var(--color-ink)]/60">
        No leads yet — add one on the left, or qualify one from raw notes on the right.
      </p>
    );
  }

  return (
    <table className="mt-10 w-full border-collapse text-left">
      <thead>
        <tr className="border-b border-[var(--color-ledger-line)]">
          {["ID", "Name", "Company", "Email", "Status"].map((h) => (
            <th
              key={h}
              className="pb-3 text-xs font-semibold uppercase tracking-[0.12em] text-[var(--color-ink)]/50"
            >
              {h}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {leads.map((lead) => (
          <tr
            key={lead.id}
            className="border-b border-[var(--color-ledger-line)] last:border-0"
          >
            <td className="py-3 font-serif text-sm text-[var(--color-ink)]/50">
              {String(lead.id).padStart(4, "0")}
            </td>
            <td className="py-3 text-sm font-medium">{lead.name}</td>
            <td className="py-3 text-sm text-[var(--color-ink)]/70">
              {lead.company ?? "—"}
            </td>
            <td className="py-3 text-sm text-[var(--color-ink)]/70">
              {lead.email}
            </td>
            <td className="py-3">
              <span className="inline-flex items-center gap-1.5 text-xs font-medium">
                <span
                  className={`h-1.5 w-1.5 rounded-full ${STATUS_DOT[lead.status] ?? "bg-gray-400"}`}
                />
                {STATUS_LABEL[lead.status] ?? lead.status}
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
