'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import EmptyState from '@/components/ui/EmptyState';
import { api } from '@/lib/api';
import { OpportunityDetail } from '@/lib/types';

export default function OpportunityDetailPage() {
  const params = useParams();
  const router = useRouter();
  const oppId = params.id as string;

  const [opp, setOpp] = useState<OpportunityDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [userDecision, setUserDecision] = useState<string>('');
  const [decisionNotes, setDecisionNotes] = useState<string>('');
  const [decisionSubmitted, setDecisionSubmitted] = useState<boolean>(false);

  useEffect(() => {
    async function loadOpportunity() {
      try {
        setLoading(true);
        const data = await api.getOpportunityDetail(oppId);
        setOpp(data);
        setUserDecision(data.status);
      } catch (err: any) {
        setError(err.message || 'Failed to load opportunity file.');
      } finally {
        setLoading(false);
      }
    }
    if (oppId) {
      loadOpportunity();
    }
  }, [oppId]);

  const handleDecision = (status: string) => {
    setUserDecision(status);
    setDecisionSubmitted(true);
  };

  if (loading) return <p className="text-xs font-mono text-[#8B95A5]">Loading opportunity strategic file...</p>;

  if (error || !opp) {
    return (
      <div className="space-y-4">
        <EmptyState
          title="Opportunity Not Found"
          description={error || 'Could not locate the requested opportunity in the database.'}
          action={
            <Link href="/app/opportunities" className="px-4 py-2 bg-slate-800 text-[#F5F7FA] text-xs font-mono rounded">
              Back to Opportunities
            </Link>
          }
        />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <Link href="/app/opportunities" className="text-xs font-mono text-[#8B95A5] hover:text-[#F5F7FA] transition-colors">
          ← Back to Opportunities
        </Link>
        <div className="mt-3">
          <PageHeader
            title={opp.title}
            description={`Strategic Opportunity Decision File #${opp.id.substring(0, 8)}`}
            badge={
              <div className="flex items-center gap-2">
                <StatusBadge variant={decisionSubmitted ? (userDecision === 'APPROVED' ? 'emerald' : userDecision === 'REJECTED' ? 'rose' : 'amber') : (opp.status === 'APPROVED' ? 'emerald' : 'amber')}>
                  {decisionSubmitted ? userDecision : opp.status}
                </StatusBadge>
                {opp.brand && <StatusBadge variant="cyan">{opp.brand.name}</StatusBadge>}
              </div>
            }
          />
        </div>
      </div>

      {/* Decision File Structural Hierarchy */}
      <div className="space-y-8">
        {/* 1. Opportunity Overview & Metrics */}
        <div className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
            <h2 className="text-sm font-bold font-mono text-[#8B95A5] uppercase">1. Opportunity Overview</h2>
            <div className="flex items-center gap-6 font-mono text-xs">
              <div>
                <span className="text-[#8B95A5] block text-[10px] uppercase">Confidence</span>
                <span className="text-base font-bold text-emerald-400">{opp.confidence_score}%</span>
              </div>
              <div className="border-l border-white/[0.08] pl-6">
                <span className="text-[#8B95A5] block text-[10px] uppercase">Risk Score</span>
                <span className="text-base font-bold text-amber-400">{opp.risk_score}%</span>
              </div>
            </div>
          </div>

          <p className="text-sm text-[#F5F7FA] leading-relaxed">{opp.description}</p>
          
          {opp.product_concept && (
            <div className="pt-2 border-t border-white/[0.08]">
              <span className="text-xs font-mono font-semibold text-[#8B95A5] uppercase block">Product Concept:</span>
              <p className="text-xs text-[#F5F7FA] mt-1 leading-relaxed">{opp.product_concept}</p>
            </div>
          )}

          {opp.positioning && (
            <div className="pt-2 border-t border-white/[0.08]">
              <span className="text-xs font-mono font-semibold text-[#8B95A5] uppercase block">Market Positioning:</span>
              <p className="text-xs text-emerald-400 font-semibold mt-1">"{opp.positioning}"</p>
            </div>
          )}
        </div>

        {/* 2. Consumer Grounding */}
        <div className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-3">
          <h2 className="text-sm font-bold font-mono text-[#8B95A5] uppercase">2. Consumer Need &amp; Target Grounding</h2>
          
          <div className="bg-[#151B23] p-4 rounded border border-white/[0.08]">
            <span className="text-[10px] font-mono text-[#8B95A5] font-bold uppercase block">Core Consumer Need (JTBD):</span>
            <p className="text-xs text-[#F5F7FA] font-medium mt-1">"{opp.consumer_need}"</p>
          </div>

          {opp.target_consumer && (
            <div className="text-xs text-[#8B95A5] pt-1">
              Target Audience: <span className="text-[#F5F7FA]">{opp.target_consumer}</span>
            </div>
          )}
        </div>

        {/* 3. Supporting Evidence Lineage */}
        <div className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-4">
          <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
            <h2 className="text-sm font-bold font-mono text-[#8B95A5] uppercase">3. Evidence Lineage ({opp.evidence.length} Signals)</h2>
            <span className="text-xs font-mono text-[#8B95A5]">Verifiable Consumer Data Trail</span>
          </div>

          {opp.evidence.length > 0 ? (
            <div className="space-y-3">
              {opp.evidence.map((ev) => (
                <div key={ev.id} className="bg-[#151B23] border border-white/[0.08] p-4 rounded space-y-2 text-xs">
                  <div className="flex items-center justify-between font-mono">
                    <span className="text-emerald-400 font-bold">{ev.evidence_type}</span>
                    <span className="text-[#8B95A5]">Relevance Score: {Math.round(ev.relevance_score * 100)}%</span>
                  </div>
                  <p className="text-[#F5F7FA] leading-relaxed italic">"{ev.explanation}"</p>
                  {ev.signal && (
                    <p className="text-[10px] font-mono text-[#8B95A5] pt-1 border-t border-white/[0.08]">
                      Source: {ev.signal.source} | Sector: {ev.signal.sector} | Sentiment: {ev.signal.sentiment}
                    </p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-[#8B95A5]">No specific evidence signals attached to this record.</p>
          )}
        </div>

        {/* 4. Brand Portfolio Fit */}
        <div className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-3">
          <h2 className="text-sm font-bold font-mono text-[#8B95A5] uppercase">4. Brand Portfolio Fit</h2>
          {opp.brand ? (
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-base font-bold text-[#F5F7FA]">{opp.brand.name}</span>
                <StatusBadge variant="cyan">{opp.brand.sector}</StatusBadge>
              </div>
              <p className="text-xs text-[#8B95A5]">{opp.brand.description}</p>
            </div>
          ) : (
            <p className="text-xs text-[#8B95A5]">No brand portfolio match assigned.</p>
          )}
        </div>

        {/* 5. Risk & Self-Audit */}
        <div className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold font-mono text-amber-400 uppercase">5. Risk &amp; Feasibility Audit</h2>
            <StatusBadge variant="amber">Risk Score: {opp.risk_score}%</StatusBadge>
          </div>
          <p className="text-xs text-[#8B95A5] leading-relaxed">
            {opp.recommended_action
              ? opp.recommended_action
              : "Critical self-audit requires human review of distribution feasibility and formulation constraints before R&D dispatch."}
          </p>
        </div>

        {/* 6. Human Decision Governance Layer */}
        <div className="bg-[#0F141B] border-2 border-amber-500/30 rounded-lg p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
            <div>
              <span className="text-[10px] font-mono text-amber-400 font-bold uppercase">HUMAN DECISION LAYER</span>
              <h2 className="text-base font-bold text-[#F5F7FA] mt-0.5">AI RECOMMENDS. HUMAN DECIDES.</h2>
            </div>
            {decisionSubmitted && (
              <StatusBadge variant="emerald">DECISION SAVED: {userDecision}</StatusBadge>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-xs font-mono font-semibold text-[#8B95A5] block">Executive Notes &amp; Directives:</label>
            <textarea
              rows={3}
              placeholder="Enter instructions for brand R&D..."
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              className="w-full bg-[#151B23] border border-white/[0.08] rounded p-3 text-xs text-[#F5F7FA] placeholder-[#8B95A5] focus:outline-none focus:border-amber-500 font-sans"
            />
          </div>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => handleDecision('APPROVED')}
              className="px-4 py-2 bg-emerald-400 hover:bg-emerald-300 text-slate-950 text-xs font-bold font-mono rounded transition-colors"
            >
              Approve Opportunity
            </button>
            <button
              onClick={() => handleDecision('REVISION_REQUESTED')}
              className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold font-mono rounded transition-colors"
            >
              Request Revision
            </button>
            <button
              onClick={() => handleDecision('REJECTED')}
              className="px-4 py-2 bg-rose-950/80 hover:bg-rose-900 border border-rose-800 text-rose-300 text-xs font-bold font-mono rounded transition-colors"
            >
              Reject Opportunity
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
