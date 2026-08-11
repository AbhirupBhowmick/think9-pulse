'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import EmptyState from '@/components/ui/EmptyState';
import { api } from '@/lib/api';
import { PipelineRun } from '@/lib/types';

export default function MyAnalysesPage() {
  const [runs, setRuns] = useState<PipelineRun[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadUserAnalyses() {
      try {
        setLoading(true);
        // Fetch only user-generated runs
        const data = await api.getPipelineRuns('user');
        setRuns(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load user analyses');
      } finally {
        setLoading(false);
      }
    }
    loadUserAnalyses();
  }, []);

  return (
    <div className="space-y-6 max-w-5xl">
      <PageHeader
        title="My Analyses"
        description="Analyses you have submitted through THINK9 PULSE."
        badge={<StatusBadge variant="emerald">{runs.length} USER ANALYSES</StatusBadge>}
      />

      {loading && <p className="text-xs font-mono text-[#8B95A5]">Loading your analyses...</p>}
      
      {error && (
        <div className="p-4 rounded bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300 font-mono">
          Error: {error}
        </div>
      )}

      {!loading && runs.length === 0 && (
        <EmptyState
          title="No analyses yet."
          description="You haven't run any custom consumer research queries yet."
          action={
            <Link
              href="/app"
              className="px-4 py-2 bg-emerald-400 text-slate-950 text-xs font-bold rounded font-mono"
            >
              Start your first analysis &rarr;
            </Link>
          }
        />
      )}

      {!loading && runs.length > 0 && (
        <div className="space-y-4">
          {runs.map((r) => (
            <div key={r.id} className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <StatusBadge variant={r.status === 'COMPLETED' || r.status === 'completed' ? 'emerald' : 'rose'}>
                  {r.status.toUpperCase()}
                </StatusBadge>
                <span className="text-xs font-mono text-[#8B95A5]">
                  {new Date(r.started_at).toLocaleString()}
                </span>
              </div>

              <div>
                <h3 className="text-xs font-mono font-bold text-[#8B95A5] uppercase">Investigated Question:</h3>
                <p className="text-sm font-bold text-[#F5F7FA] mt-1">
                  {r.user_query || r.scenario_name}
                </p>
              </div>

              <div className="pt-2 flex items-center justify-between text-xs border-t border-white/[0.08]">
                <span className="font-mono text-[#8B95A5]">Stage: {r.current_stage}</span>
                <Link
                  href="/app/opportunities"
                  className="text-emerald-400 hover:underline font-mono font-semibold"
                >
                  View Generated Opportunities &rarr;
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
