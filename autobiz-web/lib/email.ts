import nodemailer from "nodemailer";
import { Resend } from "resend";
import { InquiryLead } from "./db";

export interface EmailDispatchResult {
  sent: boolean;
  service?: "resend" | "smtp";
  messageId?: string;
  error?: string;
}

/**
 * Constructs and sends a notification email for a new project inquiry.
 * Supports both Resend API (recommended for Next.js) and standard SMTP (e.g. Gmail App Password).
 */
export async function sendInquiryNotificationEmail(lead: InquiryLead): Promise<EmailDispatchResult> {
  const recipient = process.env.NOTIFICATION_EMAIL || "autobizai01@gmail.com";
  const resendApiKey = process.env.RESEND_API_KEY;
  const smtpHost = process.env.SMTP_HOST || "smtp.gmail.com";
  const smtpUser = process.env.SMTP_USER;
  const smtpPass = process.env.SMTP_PASS;
  const smtpPort = parseInt(process.env.SMTP_PORT || "465", 10);
  const smtpSecure = process.env.SMTP_SECURE ? process.env.SMTP_SECURE === "true" : smtpPort === 465;
  const smtpFrom = process.env.SMTP_FROM || `"Auto BIZ Inquiries" <${smtpUser || "onboarding@resend.dev"}>`;

  // Format date nicely
  const formattedDate = new Date(lead.created_at).toLocaleString("en-US", {
    dateStyle: "full",
    timeStyle: "medium",
    timeZone: "Asia/Kolkata",
  });

  const subject = `New Auto BIZ Project Inquiry — ${lead.project_type}`;

  const textBody = `
NEW PROJECT INQUIRY RECEIVED — AUTO BIZ
========================================

Lead ID:       ${lead.id}
Submitted At:  ${formattedDate}

CUSTOMER DETAILS:
-----------------
Name:          ${lead.name}
Email:         ${lead.email}
Phone:         ${lead.phone || "Not provided"}
Company:       ${lead.company || "Not provided"}
Project Type:  ${lead.project_type}

PROJECT REQUIREMENTS & MESSAGE:
-------------------------------
${lead.message}

========================================
Status: ${lead.status}
Auto BIZ System Notification
`.trim();

  const htmlBody = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0c0f18; color: #e4e4e7; margin: 0; padding: 24px; }
    .container { max-width: 600px; margin: 0 auto; background-color: #121624; border: 1px solid #27272a; border-radius: 12px; overflow: hidden; }
    .header { background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%); padding: 24px; color: #ffffff; }
    .header h1 { margin: 0; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
    .header p { margin: 4px 0 0 0; font-size: 12px; opacity: 0.9; }
    .content { padding: 24px; }
    .field-group { margin-bottom: 16px; border-bottom: 1px solid #1e2438; padding-bottom: 12px; }
    .field-label { font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 4px; }
    .field-value { font-size: 14px; color: #f8fafc; font-weight: 500; }
    .message-box { background-color: #07090e; border: 1px solid #1e2438; border-radius: 8px; padding: 16px; font-size: 13px; line-height: 1.6; color: #cbd5e1; white-space: pre-wrap; }
    .badge { display: inline-block; background-color: rgba(6, 182, 212, 0.15); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); padding: 4px 10px; border-radius: 9999px; font-size: 11px; font-weight: 600; }
    .footer { padding: 16px 24px; background-color: #0a0d15; border-top: 1px solid #1e2438; font-size: 11px; color: #64748b; text-align: center; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>New Auto BIZ Project Inquiry</h1>
      <p>Submitted via Auto BIZ Web Portal</p>
    </div>
    <div class="content">
      <div style="margin-bottom: 20px;">
        <span class="badge">${escapeHtml(lead.project_type)}</span>
      </div>
      <div class="field-group">
        <div class="field-label">Customer Name</div>
        <div class="field-value">${escapeHtml(lead.name)}</div>
      </div>
      <div class="field-group">
        <div class="field-label">Email Address</div>
        <div class="field-value"><a href="mailto:${escapeHtml(lead.email)}" style="color: #38bdf8; text-decoration: none;">${escapeHtml(lead.email)}</a></div>
      </div>
      <div class="field-group">
        <div class="field-label">Phone Number</div>
        <div class="field-value">${lead.phone ? escapeHtml(lead.phone) : '<span style="color: #64748b;">Not provided</span>'}</div>
      </div>
      <div class="field-group">
        <div class="field-label">Company / Organization</div>
        <div class="field-value">${lead.company ? escapeHtml(lead.company) : '<span style="color: #64748b;">Not provided</span>'}</div>
      </div>
      <div class="field-group">
        <div class="field-label">Submitted At</div>
        <div class="field-value">${formattedDate}</div>
      </div>
      <div style="margin-top: 20px;">
        <div class="field-label">Project Requirements & Message</div>
        <div class="message-box">${escapeHtml(lead.message)}</div>
      </div>
    </div>
    <div class="footer">
      Lead ID: ${lead.id} • Auto BIZ Inquiries Automated Dispatch
    </div>
  </div>
</body>
</html>
`.trim();

  // 1. Check for Resend API Key
  if (resendApiKey) {
    try {
      const resend = new Resend(resendApiKey);
      const resendFrom = process.env.RESEND_FROM || "Auto BIZ <onboarding@resend.dev>";
      const { data, error } = await resend.emails.send({
        from: resendFrom,
        to: [recipient],
        replyTo: lead.email,
        subject,
        text: textBody,
        html: htmlBody,
      });

      if (error) {
        console.error("[Email Notification: Resend Error]:", error);
        return { sent: false, service: "resend", error: error.message };
      }

      console.log(`[Email Notification] Delivered via Resend to ${recipient}. ID: ${data?.id}`);
      return { sent: true, service: "resend", messageId: data?.id };
    } catch (err: any) {
      console.error("[Email Notification: Resend Exception]:", err);
      return { sent: false, service: "resend", error: err?.message };
    }
  }

  // 2. Check for SMTP credentials (e.g. Gmail App Password)
  if (smtpUser && smtpPass) {
    try {
      const transporter = nodemailer.createTransport({
        host: smtpHost,
        port: smtpPort,
        secure: smtpSecure,
        auth: {
          user: smtpUser,
          pass: smtpPass,
        },
        connectionTimeout: 10000,
      });

      const info = await transporter.sendMail({
        from: smtpFrom,
        to: recipient,
        replyTo: lead.email,
        subject,
        text: textBody,
        html: htmlBody,
      });

      console.log(`[Email Notification] Delivered via SMTP to ${recipient}. Message ID: ${info.messageId}`);
      return {
        sent: true,
        service: "smtp",
        messageId: info.messageId,
      };
    } catch (error: any) {
      console.error(`[Email Notification] Failed to send email via SMTP for Lead ID ${lead.id}:`, error);
      return {
        sent: false,
        service: "smtp",
        error: error?.message || "Failed to dispatch email via SMTP transporter",
      };
    }
  }

  // 3. Neither configured in .env.local
  console.warn(
    `[Email Notification Alert] No outbound email credentials (RESEND_API_KEY or SMTP_USER/SMTP_PASS) configured in .env.local. The lead was safely saved in the database (${lead.id}), but real email delivery requires valid credentials.`
  );

  return {
    sent: false,
    error: "No email credentials configured in .env.local (provide either RESEND_API_KEY or SMTP_USER/SMTP_PASS).",
  };
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
