'use client';

import { useState, useEffect } from 'react';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import EmptyState from '@/components/ui/EmptyState';
import { api } from '@/lib/api';
import { Brand } from '@/lib/types';

export default function BrandsPage() {
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadBrands() {
      try {
        setLoading(true);
        const data = await api.getBrands();
        setBrands(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load brand portfolio.');
      } finally {
        setLoading(false);
      }
    }
    loadBrands();
  }, []);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Portfolio Brands"
        description="Think9 portfolio brand profiles, market positioning, and target consumer definitions."
        badge={<StatusBadge variant="cyan">{brands.length} PORTFOLIO BRANDS</StatusBadge>}
      />

      {loading && <p className="text-xs font-mono text-[#8B95A5]">Loading portfolio brands...</p>}
      {error && (
        <div className="p-4 rounded bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300 font-mono">
          Error loading brands: {error}
        </div>
      )}

      {!loading && brands.length === 0 && (
        <EmptyState
          title="No Brands Found"
          description="There are currently no portfolio brands configured in the database."
        />
      )}

      {!loading && brands.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {brands.map((b) => (
            <div
              key={b.id}
              className="bg-[#0F141B] border border-white/[0.08] p-6 rounded-lg space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-[#8B95A5] uppercase">SECTOR</span>
                  <StatusBadge variant="cyan">{b.sector}</StatusBadge>
                </div>

                <h2 className="text-xl font-bold text-[#F5F7FA]">{b.name}</h2>
                <p className="text-xs text-[#8B95A5] leading-relaxed">{b.description}</p>

                <div className="space-y-2 pt-3 border-t border-white/[0.08] text-xs">
                  <div>
                    <span className="text-[#8B95A5] font-mono text-[10px] uppercase block">Positioning Statement:</span>
                    <span className="text-[#F5F7FA] font-medium block mt-0.5">"{b.positioning}"</span>
                  </div>

                  <div>
                    <span className="text-[#8B95A5] font-mono text-[10px] uppercase block">Target Audience:</span>
                    <span className="text-[#8B95A5] block mt-0.5">{b.target_consumer}</span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-white/[0.08] flex flex-wrap gap-1.5">
                {b.product_categories.map((cat, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-0.5 rounded bg-[#151B23] text-[#8B95A5] text-[10px] font-mono border border-white/[0.08]"
                  >
                    {cat}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
