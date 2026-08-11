'use client';

import { useState, useEffect } from 'react';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import EmptyState from '@/components/ui/EmptyState';
import { api } from '@/lib/api';
import { Signal } from '@/lib/types';

export default function SignalsPage() {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadSignals() {
      try {
        setLoading(true);
        const data = await api.getSignals();
        setSignals(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load consumer signals.');
      } finally {
        setLoading(false);
      }
    }
    loadSignals();
  }, []);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Consumer Signals"
        description="Ingested multi-channel stream capturing raw consumer discussions, reviews, and search trends."
        badge={<StatusBadge variant="cyan">{signals.length} INGESTED SIGNALS</StatusBadge>}
      />

      {loading && <p className="text-xs font-mono text-[#8B95A5]">Loading consumer signals stream...</p>}
      {error && (
        <div className="p-4 rounded bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300 font-mono">
          Error loading signals: {error}
        </div>
      )}

      {!loading && signals.length === 0 && (
        <EmptyState
          title="No Signals Ingested"
          description="There are currently no raw consumer signals stored in the database."
        />
      )}

      {!loading && signals.length > 0 && (
        <div className="bg-[#0F141B] border border-white/[0.08] rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#151B23] text-[#8B95A5] font-mono uppercase border-b border-white/[0.08]">
                <tr>
                  <th className="p-4">Signal Source</th>
                  <th className="p-4">Content &amp; Raw Feedback</th>
                  <th className="p-4">Sector</th>
                  <th className="p-4">Sentiment</th>
                  <th className="p-4">Signal Strength</th>
                  <th className="p-4">Geography</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.08]">
                {signals.map((sig) => (
                  <tr key={sig.id} className="hover:bg-[#151B23]/50 transition-colors">
                    <td className="p-4 font-semibold font-mono">
                      <StatusBadge variant="cyan">{sig.source}</StatusBadge>
                    </td>
                    <td className="p-4 max-w-md">
                      <p className="font-bold text-[#F5F7FA] mb-1">{sig.title || sig.source}</p>
                      <p className="text-[#8B95A5] leading-relaxed line-clamp-2 font-sans text-xs">
                        "{sig.content}"
                      </p>
                    </td>
                    <td className="p-4 font-mono text-[#8B95A5]">{sig.sector}</td>
                    <td className="p-4 font-mono">
                      <StatusBadge variant={sig.sentiment >= 0.5 ? 'emerald' : sig.sentiment < 0 ? 'rose' : 'neutral'}>
                        {sig.sentiment >= 0.5 ? `+${sig.sentiment}` : sig.sentiment}
                      </StatusBadge>
                    </td>
                    <td className="p-4 font-mono text-emerald-400 font-bold">
                      {Math.round(sig.signal_strength * 100)}%
                    </td>
                    <td className="p-4 font-mono text-[#8B95A5]">{sig.geography || 'US/Global'}</td>
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
