'use client';

import { useState } from 'react';
import Link from 'next/link';
import StatusBadge from '@/components/ui/StatusBadge';
import { api } from '@/lib/api';
import { PipelineRunResult } from '@/lib/types';

export default function StartAnalysisPage() {
  const [query, setQuery] = useState<string>(
    'Find unmet demand for quick healthy breakfast products.'
  );
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [result, setResult] = useState<PipelineRunResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showGuide, setShowGuide] = useState<boolean>(false);
  const [showTechnicalTrace, setShowTechnicalTrace] = useState<boolean>(false);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setAnalyzing(true);
      setError(null);
      setResult(null);

      const runResult = await api.triggerPipelineRun(query.trim());
      setResult(runResult);
    } catch (err: any) {
      setError(err.message || 'AI analysis could not be completed.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setShowTechnicalTrace(false);
    setQuery('Find unmet demand for quick healthy breakfast products.');
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto py-4">
      {/* Product Hero Header */}
      <div className="space-y-3 text-center sm:text-left border-b border-white/[0.08] pb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-[#F5F7FA] tracking-tight">
            THINK9 PULSE
          </h1>
          <p className="text-base text-[#F5F7FA] font-medium mt-1">
            Turn consumer signals into evidence-backed opportunities.
          </p>
          <p className="text-xs text-[#8B95A5] leading-relaxed mt-1">
            Central Consumer Intelligence &amp; Opportunity Engine for Think9 Portfolio Brands.
          </p>
        </div>

        <button
          type="button"
          onClick={() => setShowGuide(true)}
          className="self-start sm:self-center px-3.5 py-1.5 rounded border border-white/[0.12] text-xs text-[#8B95A5] hover:text-[#F5F7FA] hover:bg-[#151B23] transition-colors"
        >
          How do I use this?
        </button>
      </div>

      {/* Subtle First-Time User Guide Modal */}
      {showGuide && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4">
          <div className="bg-[#0F141B] border border-white/[0.12] p-6 rounded-lg max-w-md w-full space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-[#F5F7FA]">HOW TO USE THINK9 PULSE</h3>
            <ol className="space-y-3 text-xs text-[#8B95A5] list-decimal list-inside leading-relaxed">
              <li><strong className="text-[#F5F7FA]">Ask a market question:</strong> Enter what consumer behavior or category demand you want to investigate.</li>
              <li><strong className="text-[#F5F7FA]">Click Analyze:</strong> The 6-stage agentic engine passes your query through Gemini and available consumer signals.</li>
              <li><strong className="text-[#F5F7FA]">Review the output:</strong> Examine the generated opportunity, reasoning, brand fit, and confidence score.</li>
              <li><strong className="text-[#F5F7FA]">Human Checkpoint:</strong> Validate the AI recommendation before taking business action.</li>
            </ol>
            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setShowGuide(false)}
                className="px-4 py-2 bg-emerald-400 text-slate-950 text-xs font-bold rounded"
              >
                Got it
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Analysis Form View */}
      {!result && !analyzing && (
        <form onSubmit={handleAnalyze} className="space-y-6 bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg">
          <div className="space-y-2">
            <label className="block text-xs font-mono font-bold text-[#8B95A5] uppercase tracking-wider">
              What would you like to investigate?
            </label>
            <textarea
              rows={4}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Find unmet demand for quick healthy breakfast products."
              className="w-full bg-[#151B23] border border-white/[0.12] rounded-md p-4 text-sm text-[#F5F7FA] placeholder-[#8B95A5] focus:outline-none focus:border-emerald-400 font-sans leading-relaxed"
              required
            />
          </div>

          {error && (
            <div className="p-4 rounded bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300 space-y-2">
              <div className="font-bold text-[#F5F7FA]">AI analysis could not be completed.</div>
              <p className="text-[#8B95A5]">
                THINK9 PULSE could not complete the AI analysis. Please check the AI connection or quota and try again.
              </p>
              <details className="text-[11px] text-rose-400/80 cursor-pointer pt-1 font-mono">
                <summary className="hover:underline">Technical details</summary>
                <div className="mt-1 p-2 bg-black/40 rounded border border-rose-900/40 break-words whitespace-pre-wrap">
                  {error}
                </div>
              </details>
            </div>
          )}

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
            <div className="text-[11px] text-[#8B95A5]">
              Analysis based on consumer signals currently available to THINK9 PULSE.
            </div>
            <button
              type="submit"
              disabled={!query.trim()}
              className="w-full sm:w-auto px-8 py-3.5 text-xs font-bold text-slate-950 bg-emerald-400 hover:bg-emerald-300 disabled:opacity-50 rounded transition-colors shadow-lg"
            >
              Analyze &rarr;
            </button>
          </div>
        </form>
      )}

      {/* Real Loading / Processing State */}
      {analyzing && (
        <div className="bg-[#0F141B] border border-emerald-500/30 p-8 rounded-lg text-center space-y-6 my-12">
          <div className="inline-block p-4 rounded-full bg-emerald-950/60 border border-emerald-800/50 text-emerald-400 animate-pulse">
            <svg className="w-8 h-8 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          </div>
          <div className="space-y-3 max-w-lg mx-auto">
            <h3 className="text-lg font-bold text-[#F5F7FA]">Analyzing your question...</h3>
            <p className="text-xs text-[#8B95A5] leading-relaxed">
              Executing the 6-stage Gemini reasoning pipeline:
            </p>
            <div className="grid grid-cols-2 gap-2 text-[11px] font-mono text-[#8B95A5] text-left pt-2">
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
                <span>1. Understanding consumer signals</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>2. Finding emerging trends</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>3. Identifying consumer needs</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>4. Generating opportunity</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>5. Checking brand fit</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>6. Reviewing confidence &amp; risks</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Real Result View */}
      {result && (
        <div className="space-y-6">
          <div className="bg-[#0F141B] border border-emerald-500/30 p-6 rounded-lg space-y-6 shadow-xl">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
              <StatusBadge variant="emerald">ANALYSIS COMPLETE</StatusBadge>
              <span className="text-xs text-[#8B95A5] font-mono">
                Status: {result.validation_status === 'NEEDS_REVIEW' ? 'Needs validation' : result.validation_status}
              </span>
            </div>

            {/* YOUR QUESTION */}
            <div className="space-y-1">
              <span className="text-xs font-mono font-bold text-[#8B95A5] uppercase">YOUR QUESTION</span>
              <p className="text-base font-bold text-[#F5F7FA]">{query}</p>
            </div>

            {/* WHAT WE FOUND */}
            <div className="space-y-1 bg-[#151B23] p-4 rounded border border-white/[0.08]">
              <span className="text-xs font-mono font-bold text-emerald-400 uppercase">WHAT WE FOUND</span>
              <p className="text-xs text-[#8B95A5] leading-relaxed mt-1">{result.summary}</p>
            </div>

            {/* POTENTIAL OPPORTUNITY & BRAND FIT */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-[#151B23] p-4 rounded border border-white/[0.08] space-y-1">
                <span className="text-xs font-mono font-bold text-[#8B95A5] uppercase">POTENTIAL OPPORTUNITY</span>
                <p className="text-sm font-bold text-[#F5F7FA]">{result.opportunity_title || 'N/A'}</p>
              </div>

              <div className="bg-[#151B23] p-4 rounded border border-white/[0.08] space-y-1">
                <span className="text-xs font-mono font-bold text-[#8B95A5] uppercase">BRAND FIT &amp; CONFIDENCE</span>
                <p className="text-sm font-bold text-emerald-400">
                  {result.matched_brand_name || 'Portfolio Alignment'} ({result.confidence_score}%)
                </p>
              </div>
            </div>

            {/* HUMAN CHECKPOINT PHILOSOPHY */}
            <div className="p-4 bg-[#151B23] rounded border border-emerald-500/20 text-xs text-[#8B95A5] space-y-1">
              <div className="flex items-center justify-between font-mono">
                <strong className="text-emerald-400 uppercase">HUMAN CHECKPOINT &mdash; AI RECOMMENDS. HUMAN DECIDES.</strong>
                <span className="text-[10px] text-[#8B95A5]">Decision Stage</span>
              </div>
              <p className="text-xs text-[#F5F7FA] leading-relaxed">
                AI has identified this as a promising opportunity. A human should validate the evidence, market feasibility, and business fit before taking formal business action.
              </p>
            </div>

            {/* PROGRESSIVE EXPOSURE: 6-STAGE AGENTIC WORKFLOW */}
            {result.execution_stages && result.execution_stages.length > 0 && (
              <div className="pt-4 border-t border-white/[0.08] space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-[#8B95A5] uppercase">
                    How the AI reached this result ({result.execution_stages.length}-stage agentic workflow)
                  </span>
                  <button
                    type="button"
                    onClick={() => setShowTechnicalTrace(!showTechnicalTrace)}
                    className="text-xs font-mono text-emerald-400 hover:underline font-semibold"
                  >
                    {showTechnicalTrace ? 'Hide Agent Trace' : 'View 6-Agent Execution Trace &rarr;'}
                  </button>
                </div>

                {showTechnicalTrace && (
                  <div className="space-y-2 pt-2">
                    {result.execution_stages.map((stg, idx) => (
                      <div key={idx} className="bg-[#151B23] p-3 rounded text-xs border border-white/[0.08] space-y-1">
                        <div className="flex justify-between font-mono">
                          <span className="font-bold text-[#F5F7FA]">{stg.stage_name} ({stg.agent_name})</span>
                          <span className="text-emerald-400 font-bold">{stg.execution_time_ms} ms</span>
                        </div>
                        <p className="text-[#8B95A5]">{stg.output_summary}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* DATA SOURCE TRANSPARENCY */}
            <div className="text-[11px] text-[#8B95A5] pt-2 border-t border-white/[0.08]">
              <strong>Data Source:</strong> Analysis based on the consumer signals currently available to THINK9 PULSE.
            </div>

            <div className="pt-2 flex items-center justify-between">
              <button
                onClick={handleReset}
                className="px-6 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-950 text-xs font-bold rounded transition-colors"
              >
                Analyze another question &rarr;
              </button>
              <Link
                href="/app/analyses"
                className="text-xs text-emerald-400 hover:underline font-semibold"
              >
                View in My Analyses &rarr;
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* How it works summary card on home */}
      {!result && !analyzing && (
        <div className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-4">
          <h2 className="text-xs font-mono font-bold text-[#8B95A5] uppercase tracking-wider">
            CENTRAL CONSUMER INTELLIGENCE WORKFLOW
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs font-sans">
            <div>
              <span className="text-emerald-400 font-bold font-mono block">01 Ask</span>
              <p className="text-[#8B95A5] mt-1">Tell us what consumer question to investigate.</p>
            </div>
            <div>
              <span className="text-emerald-400 font-bold font-mono block">02 Analyze</span>
              <p className="text-[#8B95A5] mt-1">6 agents process signals via Gemini.</p>
            </div>
            <div>
              <span className="text-emerald-400 font-bold font-mono block">03 Discover</span>
              <p className="text-[#8B95A5] mt-1">Synthesize JTBD &amp; opportunity proposal.</p>
            </div>
            <div>
              <span className="text-emerald-400 font-bold font-mono block">04 Match &amp; Validate</span>
              <p className="text-[#8B95A5] mt-1">Portfolio brand match &amp; human checkpoint.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
