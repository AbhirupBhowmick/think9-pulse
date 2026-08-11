'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import EmptyState from '@/components/ui/EmptyState';
import { api } from '@/lib/api';
import { Opportunity } from '@/lib/types';

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadOpportunities() {
      try {
        setLoading(true);
        // Fetch user-generated opportunities only
        const data = await api.getOpportunities(undefined, undefined, 'user');
        setOpportunities(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load opportunities');
      } finally {
        setLoading(false);
      }
    }
    loadOpportunities();
  }, []);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Commercial Opportunities"
        description="Validated product proposals synthesized by multi-agent intelligence."
        badge={<StatusBadge variant="cyan">{opportunities.length} PROPOSALS</StatusBadge>}
      />

      {loading && <p className="text-xs font-mono text-[#8B95A5]">Loading opportunities...</p>}
      {error && (
        <div className="p-4 rounded bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300 font-mono">
          Error loading opportunities: {error}
        </div>
      )}

      {!loading && opportunities.length === 0 && (
        <EmptyState
          title="No opportunities generated yet."
          description="There are currently no user-generated product opportunities stored. Submit a research query to generate opportunities."
          action={
            <Link
              href="/app"
              className="px-4 py-2 bg-emerald-400 text-slate-950 text-xs font-bold rounded font-mono"
            >
              Start an Analysis &rarr;
            </Link>
          }
        />
      )}

      {!loading && opportunities.length > 0 && (
        <div className="space-y-4">
          {opportunities.map((opp) => (
            <div
              key={opp.id}
              className="bg-[#0F141B] border border-white/[0.08] hover:border-emerald-500/30 p-6 rounded-lg space-y-4 transition-colors"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <StatusBadge variant={opp.status === 'APPROVED' ? 'emerald' : opp.status === 'NEEDS_REVIEW' ? 'amber' : 'neutral'}>
                      {opp.status}
                    </StatusBadge>
                    {opp.brand && <StatusBadge variant="cyan">BRAND: {opp.brand.name}</StatusBadge>}
                  </div>
                  <h2 className="text-lg font-bold text-[#F5F7FA] mt-1">{opp.title}</h2>
                </div>

                <div className="flex items-center gap-6 font-mono text-xs">
                  <div className="text-right">
                    <span className="text-[#8B95A5] block text-[10px] uppercase">Confidence</span>
                    <span className="text-base font-bold text-emerald-400">{opp.confidence_score}%</span>
                  </div>
                  <div className="text-right border-l border-white/[0.08] pl-6">
                    <span className="text-[#8B95A5] block text-[10px] uppercase">Risk Index</span>
                    <span className="text-base font-bold text-amber-400">{opp.risk_score}%</span>
                  </div>
                </div>
              </div>

              <p className="text-xs text-[#8B95A5] leading-relaxed">{opp.description}</p>

              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 border-t border-white/[0.08] text-xs">
                <div className="text-[#8B95A5]">
                  Consumer Need: <span className="text-[#F5F7FA]">{opp.consumer_need}</span>
                </div>
                <Link
                  href={`/app/opportunities/${opp.id}`}
                  className="text-xs font-mono text-emerald-400 hover:underline font-semibold"
                >
                  Inspect Strategic File &amp; Evidence →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
