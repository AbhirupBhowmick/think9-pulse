'use client';

import PageHeader from '@/components/ui/PageHeader';
import Link from 'next/link';

export default function HowItWorksPage() {
  const steps = [
    {
      num: '01',
      title: 'ASK',
      desc: 'Formulate a consumer research question or category query (e.g., "Find unmet demand for quick healthy breakfast products").'
    },
    {
      num: '02',
      title: 'ANALYZE (6 AGENTS)',
      desc: 'The 6-stage agentic engine passes your query through Gemini across Signal Collection, Trend Detection, JTBD Synthesis, Opportunity Generation, Brand Matching, and Risk Audit.'
    },
    {
      num: '03',
      title: 'DISCOVER & MATCH',
      desc: 'The system identifies macro trends, consumer pain points, Jobs-To-Be-Done, product proposal, and matches it against Think9 portfolio brands.'
    },
    {
      num: '04',
      title: 'HUMAN CHECKPOINT',
      desc: 'AI recommends. Human decides. Review the evidence, brand fit, confidence score, and perform human validation before taking formal business action.'
    }
  ];

  const agenticStages = [
    { num: '1', name: 'Signal Collector Agent', role: 'Ingests raw multi-channel consumer signals and extracts structured sentiment & topic tags.' },
    { num: '2', name: 'Trend Detection Agent', role: 'Clusters normalized signals into emerging trend candidates and computes momentum metrics.' },
    { num: '3', name: 'Consumer Insight Agent', role: 'Formulates Jobs-To-Be-Done (JTBD) framework and identifies core consumer pain points.' },
    { num: '4', name: 'Opportunity Generator Agent', role: 'Translates consumer insights into a commercial product proposal concept.' },
    { num: '5', name: 'Brand Matcher Agent', role: 'Compares product proposal against Think9 portfolio brand positioning and categories.' },
    { num: '6', name: 'Risk & Confidence Auditor', role: 'Audits evidence completeness, commercial feasibility risks, and overall confidence score.' }
  ];

  return (
    <div className="space-y-8 max-w-4xl">
      <PageHeader
        title="Central Consumer Intelligence Architecture"
        description="Formal Think9 AI & Intelligence Challenge Job Assessment — Architecture & Data Flow."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {steps.map((step) => (
          <div key={step.num} className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-3">
            <span className="text-xs font-mono font-bold text-emerald-400">{step.num} / {step.title}</span>
            <h3 className="text-sm font-bold text-[#F5F7FA]">{step.title}</h3>
            <p className="text-xs text-[#8B95A5] leading-relaxed">{step.desc}</p>
          </div>
        ))}
      </div>

      {/* 6-Stage Agentic Workflow Explanation */}
      <div className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-4">
        <h3 className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">
          THE 6-STAGE AGENTIC REASONING PIPELINE
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {agenticStages.map((agent) => (
            <div key={agent.num} className="bg-[#151B23] border border-white/[0.08] p-4 rounded space-y-1 text-xs">
              <div className="font-mono text-emerald-400 font-bold">STAGE 0{agent.num}</div>
              <h4 className="font-bold text-[#F5F7FA]">{agent.name}</h4>
              <p className="text-[#8B95A5] leading-relaxed mt-1">{agent.role}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-[#0F141B] border border-amber-500/20 p-6 rounded-lg space-y-2 text-xs">
        <h3 className="font-mono font-bold text-amber-400 uppercase tracking-wider">
          Data Integration &amp; System Capabilities
        </h3>
        <p className="text-[#8B95A5] leading-relaxed">
          THINK9 PULSE currently analyzes the consumer signals available in its internal dataset. Live external API ingestion (Reddit, TikTok, Google Trends) is not connected in this assessment build.
        </p>
      </div>

      <div className="pt-4">
        <Link
          href="/app"
          className="inline-flex items-center justify-center px-6 py-3 text-xs font-bold text-slate-950 bg-emerald-400 hover:bg-emerald-300 rounded font-mono transition-colors"
        >
          Start an Analysis &rarr;
        </Link>
      </div>
    </div>
  );
}
