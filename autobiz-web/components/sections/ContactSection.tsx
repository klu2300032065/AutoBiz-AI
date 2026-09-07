"use client";

import React, { useState } from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { FadeIn } from "@/components/animations/FadeIn";
import { contactInfo } from "@/data/contact";
import {
  Mail,
  Phone,
  MapPin,
  ExternalLink,
  Send,
  AlertCircle,
  CheckCircle2,
  RefreshCw,
} from "lucide-react";

interface FormData {
  name: string;
  email: string;
  phone: string;
  company: string;
  projectType: string;
  message: string;
  _hp_website?: string;
}

const initialFormData: FormData = {
  name: "",
  email: "",
  phone: "",
  company: "",
  projectType: "",
  message: "",
  _hp_website: "",
};

const projectTypeOptions = [
  "Web Development",
  "AI Development",
  "Business Automation",
  "Scaling & Analytics",
  "Marketing",
  "Digital Product",
  "Other",
];

export const ContactSection: React.FC = () => {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({});
  const [formStatus, setFormStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [submittedLead, setSubmittedLead] = useState<{ id?: string; email?: string } | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof FormData, string>> = {};

    if (!formData.name.trim()) {
      newErrors.name = "Your name is required";
    } else if (formData.name.trim().length < 2) {
      newErrors.name = "Name must be at least 2 characters";
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
      newErrors.email = "Email address is required";
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = "Please enter a valid email address";
    }

    if (!formData.projectType) {
      newErrors.projectType = "Please select a project type";
    }

    if (!formData.message.trim()) {
      newErrors.message = "Message is required";
    } else if (formData.message.trim().length < 10) {
      newErrors.message = "Please provide at least 10 characters explaining your requirements";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setFormStatus("submitting");
    setErrorMessage("");

    try {
      const response = await fetch("/api/inquiries", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setSubmittedLead({ id: data.leadId, email: formData.email });
        setFormStatus("success");
      } else {
        setErrorMessage(
          data.error || "Unable to submit your inquiry at this moment. Please try again."
        );
        setFormStatus("error");
      }
    } catch (err: any) {
      console.error("Submission network error:", err);
      setErrorMessage("Network error occurred. Please check your connection and try again.");
      setFormStatus("error");
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormData]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
    if (formStatus === "error") {
      setFormStatus("idle");
      setErrorMessage("");
    }
  };

  const handleReset = () => {
    setFormData(initialFormData);
    setErrors({});
    setFormStatus("idle");
    setSubmittedLead(null);
    setErrorMessage("");
  };

  return (
    <section id="contact" className="relative py-24 sm:py-32 overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="GET IN TOUCH"
            title="Let's build something meaningful."
            description="Have an idea, a business challenge, or a project in mind? Let's start the conversation."
          />
        </FadeIn>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* Left Column: Real Contact Information Cards */}
          <div className="lg:col-span-5 flex flex-col gap-5">
            <FadeIn delay={0.1}>
              <h3 className="text-xl font-bold text-white tracking-tight mb-1">
                Direct Contact Channels
              </h3>
              <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed mb-4">
                Reach out directly via email, phone, or connect on LinkedIn. We respond to all qualified inquiries within 24 hours.
              </p>
            </FadeIn>

            {/* Email Card */}
            <FadeIn delay={0.2}>
              <a
                href={`mailto:${contactInfo.email}`}
                className="group block p-5 rounded-xl bg-white/[0.02] border border-white/[0.08] hover:border-cyan-500/40 hover:bg-white/[0.04] transition-all duration-300"
              >
                <div className="flex items-start gap-3.5">
                  <div className="p-2.5 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 group-hover:scale-105 transition-transform">
                    <Mail className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block">
                      Email
                    </span>
                    <span className="text-sm font-bold text-white group-hover:text-cyan-400 transition-colors break-all">
                      {contactInfo.email}
                    </span>
                    <span className="text-[11px] text-zinc-400 block mt-0.5">
                      Direct executive mailbox
                    </span>
                  </div>
                </div>
              </a>
            </FadeIn>

            {/* Phone Card */}
            <FadeIn delay={0.3}>
              <a
                href={`tel:+91${contactInfo.phone}`}
                className="group block p-5 rounded-xl bg-white/[0.02] border border-white/[0.08] hover:border-emerald-500/40 hover:bg-white/[0.04] transition-all duration-300"
              >
                <div className="flex items-start gap-3.5">
                  <div className="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 group-hover:scale-105 transition-transform">
                    <Phone className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block">
                      Phone / WhatsApp
                    </span>
                    <span className="text-sm font-bold text-white group-hover:text-emerald-400 transition-colors">
                      {contactInfo.formattedPhone}
                    </span>
                    <span className="text-[11px] text-zinc-400 block mt-0.5">
                      Direct voice & messaging line
                    </span>
                  </div>
                </div>
              </a>
            </FadeIn>

            {/* Location Card */}
            <FadeIn delay={0.4}>
              <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.08]">
                <div className="flex items-start gap-3.5">
                  <div className="p-2.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    <MapPin className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block">
                      Location
                    </span>
                    <span className="text-sm font-bold text-white">
                      {contactInfo.location}
                    </span>
                    <span className="text-[11px] text-zinc-400 block mt-0.5">
                      Operational Headquarters
                    </span>
                  </div>
                </div>
              </div>
            </FadeIn>

            {/* LinkedIn Card */}
            {contactInfo.linkedin && (
              <FadeIn delay={0.5}>
                <a
                  href={contactInfo.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group block p-5 rounded-xl bg-white/[0.02] border border-white/[0.08] hover:border-purple-500/40 hover:bg-white/[0.04] transition-all duration-300"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3.5">
                      <div className="p-2.5 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20 group-hover:scale-105 transition-transform">
                        <ExternalLink className="w-5 h-5" />
                      </div>
                      <div>
                        <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block">
                          LinkedIn
                        </span>
                        <span className="text-sm font-bold text-white group-hover:text-purple-400 transition-colors">
                          Auto BIZ on LinkedIn
                        </span>
                        <span className="text-[11px] text-zinc-400 block mt-0.5">
                          Connect with our team
                        </span>
                      </div>
                    </div>
                  </div>
                </a>
              </FadeIn>
            )}
          </div>

          {/* Right Column: Contact Form / Success State */}
          <div className="lg:col-span-7">
            <FadeIn delay={0.2}>
              <Card className="p-6 sm:p-8 bg-[#0c0f18] border-white/[0.12] shadow-2xl">
                <div className="flex items-center justify-between pb-4 mb-6 border-b border-white/[0.08]">
                  <div>
                    <h3 className="text-lg font-bold text-white tracking-tight">
                      Project Inquiry Form
                    </h3>
                    <span className="text-xs text-zinc-400">
                      Submit your project requirements directly to our engineering & strategy team.
                    </span>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    Direct Server API
                  </span>
                </div>

                {/* SUCCESS STATE */}
                {formStatus === "success" ? (
                  <div className="space-y-6 py-6 animate-in fade-in zoom-in-95 duration-300">
                    <div className="p-6 rounded-2xl bg-gradient-to-b from-emerald-500/10 to-transparent border border-emerald-500/30 text-center flex flex-col items-center">
                      <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mb-4 border border-emerald-500/40 shadow-[0_0_20px_rgba(16,185,129,0.2)]">
                        <CheckCircle2 className="w-6 h-6" />
                      </div>

                      <h4 className="text-xl font-bold text-white mb-2 tracking-tight">
                        Inquiry Received
                      </h4>

                      <p className="text-sm text-zinc-300 max-w-md mx-auto leading-relaxed mb-6">
                        Thanks for reaching out to Auto BIZ. Your project inquiry has been received. We&apos;ll review the details and get back to you.
                      </p>

                      {submittedLead?.id && (
                        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-black/40 border border-white/10 text-xs font-mono text-zinc-400 mb-6">
                          <span>Reference ID:</span>
                          <span className="text-cyan-400 font-semibold">{submittedLead.id}</span>
                        </div>
                      )}

                      <Button
                        onClick={handleReset}
                        variant="outline"
                        size="md"
                        icon={<RefreshCw className="w-4 h-4" />}
                      >
                        Submit Another Inquiry
                      </Button>
                    </div>
                  </div>
                ) : (
                  <form onSubmit={handleSubmit} noValidate className="space-y-5">
                    {/* Error Banner if API error occurs */}
                    {formStatus === "error" && errorMessage && (
                      <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start gap-3 text-xs text-red-300 animate-in fade-in">
                        <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                        <div>
                          <span className="font-semibold text-white block mb-0.5">Submission Error</span>
                          <span>{errorMessage}</span>
                        </div>
                      </div>
                    )}

                    {/* Anti-spam Honeypot (hidden from human users) */}
                    <div className="hidden" aria-hidden="true">
                      <label htmlFor="_hp_website">Website</label>
                      <input
                        id="_hp_website"
                        name="_hp_website"
                        type="text"
                        tabIndex={-1}
                        autoComplete="off"
                        value={formData._hp_website}
                        onChange={handleChange}
                      />
                    </div>

                    {/* Row 1: Name & Email */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="name" className="block text-xs font-semibold text-zinc-300 mb-1.5">
                          Your Name <span className="text-cyan-400">*</span>
                        </label>
                        <input
                          id="name"
                          name="name"
                          type="text"
                          value={formData.name}
                          onChange={handleChange}
                          placeholder="e.g. Alex Morgan"
                          className={`w-full px-3.5 py-2.5 rounded-lg bg-zinc-950/80 border text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 transition-all ${
                            errors.name ? "border-red-500/80" : "border-white/[0.08]"
                          }`}
                        />
                        {errors.name && (
                          <span className="text-[11px] text-red-400 mt-1 block">{errors.name}</span>
                        )}
                      </div>

                      <div>
                        <label htmlFor="email" className="block text-xs font-semibold text-zinc-300 mb-1.5">
                          Email Address <span className="text-cyan-400">*</span>
                        </label>
                        <input
                          id="email"
                          name="email"
                          type="email"
                          value={formData.email}
                          onChange={handleChange}
                          placeholder="e.g. alex@company.com"
                          className={`w-full px-3.5 py-2.5 rounded-lg bg-zinc-950/80 border text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 transition-all ${
                            errors.email ? "border-red-500/80" : "border-white/[0.08]"
                          }`}
                        />
                        {errors.email && (
                          <span className="text-[11px] text-red-400 mt-1 block">{errors.email}</span>
                        )}
                      </div>
                    </div>

                    {/* Row 2: Phone & Company */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="phone" className="block text-xs font-semibold text-zinc-300 mb-1.5">
                          Phone Number <span className="text-zinc-500 text-[10px] font-normal">(Optional)</span>
                        </label>
                        <input
                          id="phone"
                          name="phone"
                          type="tel"
                          value={formData.phone}
                          onChange={handleChange}
                          placeholder="e.g. +91 98765 43210"
                          className="w-full px-3.5 py-2.5 rounded-lg bg-zinc-950/80 border border-white/[0.08] text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 transition-all"
                        />
                      </div>

                      <div>
                        <label htmlFor="company" className="block text-xs font-semibold text-zinc-300 mb-1.5">
                          Company / Organization <span className="text-zinc-500 text-[10px] font-normal">(Optional)</span>
                        </label>
                        <input
                          id="company"
                          name="company"
                          type="text"
                          value={formData.company}
                          onChange={handleChange}
                          placeholder="e.g. Apex Global"
                          className="w-full px-3.5 py-2.5 rounded-lg bg-zinc-950/80 border border-white/[0.08] text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 transition-all"
                        />
                      </div>
                    </div>

                    {/* Row 3: Project Type */}
                    <div>
                      <label htmlFor="projectType" className="block text-xs font-semibold text-zinc-300 mb-1.5">
                        Project Type <span className="text-cyan-400">*</span>
                      </label>
                      <select
                        id="projectType"
                        name="projectType"
                        value={formData.projectType}
                        onChange={handleChange}
                        className={`w-full px-3.5 py-2.5 rounded-lg bg-zinc-950/80 border text-sm text-white focus:outline-none focus:ring-1 focus:ring-cyan-500 transition-all cursor-pointer ${
                          errors.projectType ? "border-red-500/80" : "border-white/[0.08]"
                        }`}
                      >
                        <option value="" disabled className="bg-zinc-900 text-zinc-400">
                          Select a project category...
                        </option>
                        {projectTypeOptions.map((opt) => (
                          <option key={opt} value={opt} className="bg-zinc-900 text-white">
                            {opt}
                          </option>
                        ))}
                      </select>
                      {errors.projectType && (
                        <span className="text-[11px] text-red-400 mt-1 block">{errors.projectType}</span>
                      )}
                    </div>

                    {/* Row 4: Message */}
                    <div>
                      <label htmlFor="message" className="block text-xs font-semibold text-zinc-300 mb-1.5">
                        Project Details & Requirements <span className="text-cyan-400">*</span>
                      </label>
                      <textarea
                        id="message"
                        name="message"
                        rows={4}
                        value={formData.message}
                        onChange={handleChange}
                        placeholder="Describe your project, current business challenge, or milestones you want to achieve..."
                        className={`w-full px-3.5 py-2.5 rounded-lg bg-zinc-950/80 border text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 transition-all ${
                          errors.message ? "border-red-500/80" : "border-white/[0.08]"
                        }`}
                      />
                      {errors.message && (
                        <span className="text-[11px] text-red-400 mt-1 block">{errors.message}</span>
                      )}
                    </div>

                    {/* Submit Button */}
                    <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-4">
                      <Button
                        type="submit"
                        variant="glow"
                        size="md"
                        isLoading={formStatus === "submitting"}
                        className="w-full sm:w-auto"
                        icon={<Send className="w-4 h-4" />}
                      >
                        Submit Inquiry
                      </Button>

                      <span className="text-[11px] font-mono text-zinc-400 text-center sm:text-right">
                        Direct notification to:{" "}
                        <span className="text-zinc-300">{contactInfo.email}</span>
                      </span>
                    </div>
                  </form>
                )}
              </Card>
            </FadeIn>
          </div>
        </div>
      </Container>
    </section>
  );
};
