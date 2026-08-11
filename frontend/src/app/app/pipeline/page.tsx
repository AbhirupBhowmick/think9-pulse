'use client';

import { useState, useEffect } from 'react';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import EmptyState from '@/components/ui/EmptyState';
import Link from 'next/link';
import { api } from '@/lib/api';
import { PipelineRun } from '@/lib/types';

export default function PipelinePage() {
  const [runs, setRuns] = useState<PipelineRun[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadRuns() {
      try {
        setLoading(true);
        const data = await api.getPipelineRuns('user');
        setRuns(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load pipeline runs');
      } finally {
        setLoading(false);
      }
    }
    loadRuns();
  }, []);

  return (
    <div className="space-y-8 max-w-5xl">
      <PageHeader
        title="AI Pipeline Audit Trail"
        description="Technical execution history and audit logs across the 6-stage Gemini pipeline."
      />

      {error && (
        <div className="p-4 rounded bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300 font-mono">
          Pipeline Alert: {error}
        </div>
      )}

      {/* Historical Audit Log Table */}
      <div className="space-y-4">
        <h2 className="text-xs font-mono font-bold text-[#8B95A5] uppercase tracking-wider">
          USER PIPELINE EXECUTION LOGS
        </h2>

        {loading && <p className="text-xs font-mono text-[#8B95A5]">Loading audit logs...</p>}

        {!loading && runs.length === 0 && (
          <EmptyState
            title="No analyses have been run yet."
            description="Submit a research question from the home page to execute a 6-stage Gemini analysis."
            action={
              <Link
                href="/app"
                className="px-5 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-950 text-xs font-bold font-mono rounded transition-colors"
              >
                Start an Analysis &rarr;
              </Link>
            }
          />
        )}

        {!loading && runs.length > 0 && (
          <div className="bg-[#0F141B] border border-white/[0.08] rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-sans">
                <thead className="bg-[#151B23] text-[#8B95A5] font-mono uppercase border-b border-white/[0.08]">
                  <tr>
                    <th className="p-4">Investigated Question</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Current Stage</th>
                    <th className="p-4">Run ID</th>
                    <th className="p-4">Timestamp</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/[0.08]">
                  {runs.map((r) => (
                    <tr key={r.id} className="hover:bg-[#151B23]/50 transition-colors">
                      <td className="p-4 font-bold text-[#F5F7FA]">
                        {r.user_query || r.scenario_name}
                      </td>
                      <td className="p-4 font-mono">
                        <StatusBadge
                          variant={
                            r.status === 'COMPLETED' || r.status === 'completed'
                              ? 'emerald'
                              : r.status === 'FAILED'
                              ? 'rose'
                              : 'amber'
                          }
                        >
                          {r.status.toUpperCase()}
                        </StatusBadge>
                      </td>
                      <td className="p-4 font-mono text-[#8B95A5]">
                        {r.current_stage || 'ALL 6 STAGES COMPLETED'}
                      </td>
                      <td className="p-4 font-mono text-[#8B95A5]">{r.id.substring(0, 8)}...</td>
                      <td className="p-4 font-mono text-[#8B95A5]">
                        {new Date(r.started_at).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
