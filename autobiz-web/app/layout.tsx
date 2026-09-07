import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const viewport: Viewport = {
  themeColor: "#07080b",
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: "Auto BIZ | Build. Scale. Market.",
  description:
    "Auto BIZ helps businesses build digital products, scale smarter with technology and analytics, and market with purpose.",
  keywords: [
    "Auto BIZ",
    "Web Development",
    "Digital Products",
    "Business Automation",
    "Analytics",
    "Marketing Strategy",
    "AI Solutions",
  ],
  authors: [{ name: "Auto BIZ" }],
  openGraph: {
    title: "Auto BIZ | Build. Scale. Market.",
    description:
      "Turn ideas into digital products. Turn products into growing businesses.",
    url: "https://autobiz.ai",
    siteName: "Auto BIZ",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Auto BIZ | Build. Scale. Market.",
    description:
      "Turn ideas into digital products. Turn products into growing businesses.",
  },
  icons: {
    icon: "/icon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} dark scroll-smooth`}>
      <body className="bg-[#07080b] text-zinc-100 font-sans antialiased selection:bg-cyan-500 selection:text-black">
        {children}
      </body>
    </html>
  );
}
