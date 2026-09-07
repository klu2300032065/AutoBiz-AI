import fs from "fs";
import path from "path";
import crypto from "crypto";

export interface InquiryLead {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  company: string | null;
  project_type: string;
  message: string;
  status: "NEW" | "IN_REVIEW" | "CONTACTED" | "ARCHIVED";
  created_at: string;
  updated_at: string;
}

export interface CreateInquiryInput {
  name: string;
  email: string;
  phone?: string | null;
  company?: string | null;
  project_type: string;
  message: string;
}

// Database directory and storage files
const DATA_DIR = path.join(process.cwd(), "data");
const LEADS_FILE = path.join(DATA_DIR, "inquiries.json");

function ensureDataDirectory() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  if (!fs.existsSync(LEADS_FILE)) {
    fs.writeFileSync(LEADS_FILE, JSON.stringify([], null, 2), "utf-8");
  }
}

/**
 * Reads all inquiry leads from persistent storage.
 */
export async function getInquiries(limit = 50): Promise<InquiryLead[]> {
  ensureDataDirectory();
  try {
    const fileContent = fs.readFileSync(LEADS_FILE, "utf-8");
    const leads: InquiryLead[] = JSON.parse(fileContent || "[]");
    // Sort descending by created_at
    leads.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    return leads.slice(0, limit);
  } catch (error) {
    console.error("[Database] Error reading leads file:", error);
    return [];
  }
}

/**
 * Inserts a new inquiry lead into persistent database storage with atomic write.
 */
export async function createInquiry(input: CreateInquiryInput): Promise<InquiryLead> {
  ensureDataDirectory();

  const id = `lead_${crypto.randomUUID()}`;
  const now = new Date().toISOString();

  const newLead: InquiryLead = {
    id,
    name: input.name.trim(),
    email: input.email.trim().toLowerCase(),
    phone: input.phone?.trim() || null,
    company: input.company?.trim() || null,
    project_type: input.project_type.trim(),
    message: input.message.trim(),
    status: "NEW",
    created_at: now,
    updated_at: now,
  };

  try {
    const fileContent = fs.readFileSync(LEADS_FILE, "utf-8");
    const leads: InquiryLead[] = JSON.parse(fileContent || "[]");
    leads.unshift(newLead);

    // Atomic write via temporary file to prevent corruption
    const tempFile = `${LEADS_FILE}.${crypto.randomBytes(4).toString("hex")}.tmp`;
    fs.writeFileSync(tempFile, JSON.stringify(leads, null, 2), "utf-8");
    fs.renameSync(tempFile, LEADS_FILE);

    console.log(`[Database] Lead saved successfully. ID: ${newLead.id} (${newLead.email})`);
    return newLead;
  } catch (error) {
    console.error("[Database] Error saving lead to storage:", error);
    throw new Error("Failed to persist inquiry lead to database storage.");
  }
}
