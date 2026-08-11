'use client';

import Link from 'next/link';
import AcidSquares from '@/components/ui/AcidSquares';
import ScrollExpand from '@/components/ui/ScrollExpand';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[#080B10] text-[#F5F7FA] font-sans flex flex-col justify-between selection:bg-emerald-500 selection:text-slate-950 overflow-x-hidden">
      {/* 1. Navigation Header */}
      <header className="border-b border-white/[0.08] bg-[#080B10]/90 backdrop-blur-md sticky top-0 z-50 px-6 lg:px-12 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-lg font-extrabold tracking-tight text-[#F5F7FA]">THINK9 PULSE</span>
            <span className="hidden sm:inline-block text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/50 uppercase">
              CONSUMER INTELLIGENCE ENGINE
            </span>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              href="/app/pipeline"
              className="px-4 py-2 text-xs font-semibold text-slate-950 bg-emerald-400 hover:bg-emerald-300 rounded transition-colors"
            >
              Start an Analysis
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* 2. Hero Section with AcidSquares Background ONLY */}
        <section className="relative min-h-[85vh] flex flex-col justify-center items-center overflow-hidden border-b border-white/[0.08] bg-[#080B10]">
          {/* Layer 1: AcidSquares Animation Canvas */}
          <div className="absolute inset-0 z-0 pointer-events-auto opacity-35">
            <AcidSquares
              color1="#5227FF"
              color2="#A855F7"
              color3="#FFFFFF"
              detail="medium"
              speed={0.7}
              waveDepth={1}
              zoom={1.3}
              density={10}
              glow={1}
              exposure={2700}
              spread={0.3}
              stepSize={0.002}
              colorShift={0}
              contrast={1}
              brightness={1}
              opacity={1}
              mouseInteraction
              mouseStrength={0.1}
              mouseRadius={0.35}
              blur={0}
              grain
              grainIntensity={0.05}
            />
          </div>

          {/* Layer 2: Subtle Dark Gradient Vignette Overlay */}
          <div className="absolute inset-0 z-1 pointer-events-none bg-gradient-to-b from-[#080B10]/70 via-[#080B10]/40 to-[#080B10]" />

          {/* Layer 3: Crisp Hero Content */}
          <div className="relative z-10 text-center max-w-5xl mx-auto px-6 py-20 space-y-8 pointer-events-none">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#0F141B]/95 backdrop-blur-md border border-white/[0.12] text-xs font-mono text-[#8B95A5] pointer-events-auto">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span>INTELLIGENCE ENGINE</span>
            </div>

            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-[#F5F7FA] leading-tight max-w-4xl mx-auto drop-shadow-md">
              From signals to validated product decisions.
            </h1>

            <p className="text-base sm:text-xl text-[#8B95A5] font-normal leading-relaxed max-w-3xl mx-auto">
              Turn consumer behavior, retail feedback, and market shifts into actionable commercial opportunities for your brand portfolio.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4 pointer-events-auto">
              <Link
                href="/app/pipeline"
                className="w-full sm:w-auto px-6 py-3.5 text-sm font-semibold text-slate-950 bg-emerald-400 hover:bg-emerald-300 rounded-md transition-colors text-center shadow-lg"
              >
                Start an Analysis
              </Link>
            </div>
          </div>
        </section>

        {/* 3. Unified ScrollExpand Demonstration Section (100vh) */}
        <ScrollExpand
          src="/think9-consumer.jpg"
          alt="Consumer product discovery"
          title="From signal to decision."
          startWidth={42}
          startHeight={52}
          startRadius={24}
          endRadius={0}
          mediaZoom={1.35}
          smoothing={0.1}
          overlayScrim={0.45}
          enabled
        >
          <h2 className="text-2xl sm:text-4xl font-extrabold text-[#F5F7FA] tracking-tight">
            Evidence becomes opportunity.
          </h2>
          <p className="text-sm sm:text-base text-slate-300 font-medium max-w-2xl mt-2 leading-relaxed">
            THINK9 PULSE connects consumer signals, market trends, AI reasoning, brand fit, and risk validation into one traceable decision workflow.
          </p>
        </ScrollExpand>

      </main>

      {/* 7. Footer */}
      <footer className="border-t border-white/[0.08] py-8 px-6 lg:px-12 text-xs text-[#8B95A5] font-mono">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            THINK9 PULSE &copy; 2026 | Agentic Consumer Intelligence &amp; Opportunity Engine
          </div>
          <div className="flex items-center space-x-4 text-[11px]">
            <span>Model: gemini-3.6-flash</span>
            <span>•</span>
            <span>FastAPI Backend</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
