export interface Lead {
  id: number;
  name: string;
  email: string;
  company: string | null;
  status: string; // "new" | "contacted" | "won" | "lost"
}

export interface QualifiedLead extends Lead {
  ai_priority: string;
  ai_reason: string;
  ai_notes_summary: string;
}
