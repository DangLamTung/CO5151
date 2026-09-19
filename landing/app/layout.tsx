import type { Metadata } from "next";
import { Newsreader, Plus_Jakarta_Sans, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const newsreader = Newsreader({
  subsets: ["latin", "vietnamese"],
  style: ["normal", "italic"],
  variable: "--font-newsreader",
  display: "swap",
  adjustFontFallback: false,
});

const sans = Plus_Jakarta_Sans({
  subsets: ["latin", "vietnamese"],
  variable: "--font-sans",
  display: "swap",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "LegalPilot-VN | Autonomous Multi-Agent Legal Compliance",
  description:
    "Autonomous Multi-Agent RAG for Vietnamese Statutory Synthesis, Temporal Consistency, and Verifiable Claim Auditing.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`dark ${newsreader.variable} ${sans.variable} ${mono.variable}`}
    >
      <body className="min-h-screen bg-[#09090b] font-sans text-zinc-100 antialiased selection:bg-emerald-950 selection:text-emerald-400">
        {children}
      </body>
    </html>
  );
}
