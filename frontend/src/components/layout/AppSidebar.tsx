'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';

export default function AppSidebar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navigation = [
    {
      group: 'MAIN',
      items: [
        { name: 'Start an Analysis', href: '/app' },
      ],
    },
    {
      group: 'RESULTS',
      items: [
        { name: 'My Analyses', href: '/app/analyses' },
        { name: 'Opportunities', href: '/app/opportunities' },
      ],
    },
    {
      group: 'LEARN',
      items: [
        { name: 'How It Works', href: '/app/how-it-works' },
      ],
    },
    {
      group: 'TECHNICAL',
      items: [
        { name: 'Analysis History', href: '/app/pipeline' },
      ],
    },
  ];

  const isActive = (href: string) => {
    if (href === '/app') return pathname === '/app';
    return pathname.startsWith(href);
  };

  return (
    <>
      {/* Mobile Top Bar */}
      <div className="lg:hidden bg-[#0F141B] border-b border-white/[0.08] px-4 py-3 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <Link href="/app" className="font-bold text-base tracking-tight text-[#F5F7FA]">
            THINK9 PULSE
          </Link>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/50">
            ONLINE
          </span>
        </div>
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="text-[#8B95A5] hover:text-[#F5F7FA] p-1.5 focus:outline-none"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={mobileMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'} />
          </svg>
        </button>
      </div>

      {/* Desktop & Mobile Sidebar Container */}
      <aside
        className={`fixed lg:sticky top-0 inset-y-0 left-0 z-40 w-56 bg-[#0F141B] border-r border-white/[0.08] flex flex-col justify-between transition-transform duration-200 ease-in-out ${
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        } min-h-screen`}
      >
        <div className="p-6 space-y-6">
          {/* Brand Header */}
          <div className="space-y-2 border-b border-white/[0.08] pb-5">
            <Link href="/app" className="block font-extrabold text-lg tracking-tight text-[#F5F7FA] hover:text-emerald-400 transition-colors">
              THINK9 PULSE
            </Link>
          </div>

          {/* Navigation Groups */}
          <nav className="space-y-6">
            {navigation.map((section) => (
              <div key={section.group} className="space-y-2">
                <h3 className="text-[10px] font-mono font-bold tracking-widest text-[#8B95A5] uppercase">
                  {section.group}
                </h3>
                <div className="space-y-1">
                  {section.items.map((item) => {
                    const active = isActive(item.href);
                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        onClick={() => setMobileMenuOpen(false)}
                        className={`block px-3 py-2 rounded text-xs transition-colors duration-150 ${
                          active
                            ? 'bg-[#151B23] text-[#F5F7FA] font-semibold border-l-2 border-emerald-400'
                            : 'text-[#8B95A5] hover:text-[#F5F7FA] hover:bg-[#151B23]/40'
                        }`}
                      >
                        {item.name}
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </nav>
        </div>

        {/* Footer info */}
        <div className="p-6 border-t border-white/[0.08] text-[11px] font-mono text-[#8B95A5]">
          <p className="font-semibold text-slate-300">Model: gemini-3.6-flash</p>
          <p className="mt-0.5 text-[10px] text-slate-500">FastAPI + SQLite Backend</p>
        </div>
      </aside>

      {/* Mobile Backdrop */}
      {mobileMenuOpen && (
        <div
          onClick={() => setMobileMenuOpen(false)}
          className="fixed inset-0 bg-black/60 z-30 lg:hidden"
        />
      )}
    </>
  );
}
