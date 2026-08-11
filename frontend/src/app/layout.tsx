import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'THINK9 PULSE — Agentic Consumer Intelligence & Opportunity Engine',
  description: 'Central Consumer Intelligence Engine for Think9 Consumer Brands Portfolio.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0B0F17] text-slate-100 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
