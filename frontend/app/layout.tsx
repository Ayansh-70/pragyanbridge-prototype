import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PragyanBridge - AI Candidate Matching & Verification",
  description: "Next-generation AI recruitment and accreditation platform (SIH 2026 PS 26044)",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 antialiased selection:bg-emerald-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
