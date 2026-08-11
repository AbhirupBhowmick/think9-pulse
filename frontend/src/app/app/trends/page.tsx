'use client';

import { useState, useEffect } from 'react';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import EmptyState from '@/components/ui/EmptyState';
import { api } from '@/lib/api';
import { Trend } from '@/lib/types';

export default function TrendsPage() {
  const [trends, setTrends] = useState<Trend[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadTrends() {
      try {
        setLoading(true);
        const data = await api.getTrends();
        setTrends(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load market trends.');
      } finally {
        setLoading(false);
      }
    }
    loadTrends();
  }, []);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Detected Market Trends"
        description="Macro consumer trend clusters synthesized by Trend Detection Agent."
        badge={<StatusBadge variant="emerald">{trends.length} ACTIVE CLUSTERS</StatusBadge>}
      />

      {loading && <p className="text-xs font-mono text-[#8B95A5]">Loading market trend clusters...</p>}
      {error && (
        <div className="p-4 rounded bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300 font-mono">
          Error loading trends: {error}
        </div>
      )}

      {!loading && trends.length === 0 && (
        <EmptyState
          title="No Trends Found"
          description="There are currently no detected trend clusters recorded in the database."
        />
      )}

      {!loading && trends.length > 0 && (
        <div className="bg-[#0F141B] border border-white/[0.08] rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#151B23] text-[#8B95A5] font-mono uppercase border-b border-white/[0.08]">
                <tr>
                  <th className="p-4">Trend Cluster Name</th>
                  <th className="p-4">Category Sector</th>
                  <th className="p-4">Momentum Velocity</th>
                  <th className="p-4">Confidence</th>
                  <th className="p-4">Signal Density</th>
                  <th className="p-4">Cluster Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.08]">
                {trends.map((t) => (
                  <tr key={t.id} className="hover:bg-[#151B23]/50 transition-colors">
                    <td className="p-4">
                      <p className="font-bold text-[#F5F7FA] mb-1">{t.name}</p>
                      <p className="text-[#8B95A5] text-xs leading-relaxed max-w-lg">{t.description}</p>
                    </td>
                    <td className="p-4 font-mono text-[#8B95A5]">{t.sector}</td>
                    <td className="p-4 font-mono text-emerald-400 font-bold text-sm">
                      {t.momentum_score}/100
                    </td>
                    <td className="p-4 font-mono text-[#F5F7FA] font-semibold">
                      {t.confidence_score}%
                    </td>
                    <td className="p-4 font-mono text-[#8B95A5]">{t.signal_count} Signals</td>
                    <td className="p-4 font-mono">
                      <StatusBadge variant="emerald">{t.status}</StatusBadge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
