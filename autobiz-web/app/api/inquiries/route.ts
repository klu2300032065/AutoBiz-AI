import { NextRequest, NextResponse } from "next/server";
import { createInquiry, getInquiries } from "@/lib/db";
import { sendInquiryNotificationEmail } from "@/lib/email";
import { checkRateLimit } from "@/lib/rateLimit";

const VALID_PROJECT_TYPES = [
  "Web Development",
  "AI Development",
  "Business Automation",
  "Scaling & Analytics",
  "Marketing",
  "Digital Product",
  "Other",
];

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(req: NextRequest) {
  try {
    // 1. IP & Rate limiting
    const forwardedFor = req.headers.get("x-forwarded-for");
    const ip = forwardedFor ? forwardedFor.split(",")[0].trim() : "127.0.0.1";

    const { allowed } = checkRateLimit(ip);
    if (!allowed) {
      return NextResponse.json(
        {
          success: false,
          error: "Too many inquiries submitted from this connection. Please wait a few minutes or contact us directly.",
        },
        { status: 429 }
      );
    }

    // 2. Parse body
    const body = await req.json();
    const { name, email, phone, company, projectType, message, _hp_website } = body;

    // 3. Honeypot check (anti-bot)
    if (_hp_website) {
      console.warn(`[Anti-Spam] Bot detected via honeypot field. IP: ${ip}`);
      // Return synthetic success to confuse spam bot
      return NextResponse.json(
        { success: true, message: "Inquiry received" },
        { status: 200 }
      );
    }

    // 4. Validate fields
    if (!name || typeof name !== "string" || name.trim().length < 2 || name.trim().length > 100) {
      return NextResponse.json(
        { success: false, error: "Please provide a valid name (2-100 characters)." },
        { status: 400 }
      );
    }

    if (!email || typeof email !== "string" || !EMAIL_REGEX.test(email.trim())) {
      return NextResponse.json(
        { success: false, error: "Please provide a valid email address." },
        { status: 400 }
      );
    }

    if (!projectType || typeof projectType !== "string" || !VALID_PROJECT_TYPES.includes(projectType)) {
      return NextResponse.json(
        { success: false, error: "Please select a valid project type from the list." },
        { status: 400 }
      );
    }

    if (!message || typeof message !== "string" || message.trim().length < 10 || message.trim().length > 4000) {
      return NextResponse.json(
        { success: false, error: "Message must be between 10 and 4,000 characters." },
        { status: 400 }
      );
    }

    if (phone && (typeof phone !== "string" || phone.trim().length > 40)) {
      return NextResponse.json(
        { success: false, error: "Phone number is invalid or too long." },
        { status: 400 }
      );
    }

    if (company && (typeof company !== "string" || company.trim().length > 120)) {
      return NextResponse.json(
        { success: false, error: "Company name is invalid or too long." },
        { status: 400 }
      );
    }

    // 5. Store lead in database
    const lead = await createInquiry({
      name: name.trim(),
      email: email.trim(),
      phone: phone ? String(phone).trim() : null,
      company: company ? String(company).trim() : null,
      project_type: projectType.trim(),
      message: message.trim(),
    });

    console.log(`[Inquiry API] Lead created in database: ${lead.id} (${lead.name}, ${lead.project_type})`);

    // 6. Send notification email to autobizai01@gmail.com
    const emailResult = await sendInquiryNotificationEmail(lead);

    // 7. Return production-ready structured response
    return NextResponse.json(
      {
        success: true,
        message: "Inquiry received. We'll review the details and get back to you.",
        leadId: lead.id,
        status: lead.status,
        emailSent: emailResult.sent,
        emailNote: emailResult.sent
          ? "Notification dispatched"
          : "Lead saved in database; email notification queued/logged",
      },
      { status: 201 }
    );
  } catch (error: any) {
    console.error("[Inquiry API Error]:", error);
    return NextResponse.json(
      {
        success: false,
        error: "An error occurred while processing your inquiry. Please try again or contact autobizai01@gmail.com directly.",
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    const leads = await getInquiries(10);
    return NextResponse.json({
      service: "Auto BIZ Inquiry Lead Management",
      status: "Operational",
      recentCount: leads.length,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error?.message || "Error" }, { status: 500 });
  }
}
