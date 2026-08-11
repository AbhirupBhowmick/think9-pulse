import {
  Brand, Signal, Trend, Opportunity,
  OpportunityDetail, Evidence, PipelineRun, PipelineRunResult
} from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

async function fetchJSON<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
    ...options,
  });

  if (!res.ok) {
    const errorText = await res.text().catch(() => 'Unknown Error');
    throw new Error(`API Request Error (${res.status}): ${errorText}`);
  }

  return res.json();
}

export const api = {
  // Health Check
  getHealth: () => fetchJSON<{ status: string; service: string; database: string }>('/api/v1/health'),

  // Brands
  getBrands: (sector?: string) => {
    const query = sector ? `?sector=${encodeURIComponent(sector)}` : '';
    return fetchJSON<Brand[]>(`/api/v1/brands${query}`);
  },
  getBrand: (id: string) => fetchJSON<Brand>(`/api/v1/brands/${id}`),

  // Signals
  getSignals: (sector?: string, source?: string) => {
    const params = new URLSearchParams();
    if (sector) params.append('sector', sector);
    if (source) params.append('source', source);
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchJSON<Signal[]>(`/api/v1/signals${query}`);
  },
  getSignal: (id: string) => fetchJSON<Signal>(`/api/v1/signals/${id}`),

  // Trends
  getTrends: (sector?: string, status?: string) => {
    const params = new URLSearchParams();
    if (sector) params.append('sector', sector);
    if (status) params.append('status', status);
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchJSON<Trend[]>(`/api/v1/trends${query}`);
  },
  getTrend: (id: string) => fetchJSON<Trend>(`/api/v1/trends/${id}`),

  // Opportunities
  getOpportunities: (status?: string, brandId?: string, sourceType?: string) => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (brandId) params.append('brand_id', brandId);
    if (sourceType) params.append('source_type', sourceType);
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchJSON<Opportunity[]>(`/api/v1/opportunities${query}`);
  },
  getOpportunityDetail: (id: string) => fetchJSON<OpportunityDetail>(`/api/v1/opportunities/${id}`),
  getOpportunityEvidence: (id: string) => fetchJSON<Evidence[]>(`/api/v1/opportunities/${id}/evidence`),

  // Pipeline Runs
  getPipelineRuns: (sourceType?: string) => {
    const query = sourceType ? `?source_type=${encodeURIComponent(sourceType)}` : '';
    return fetchJSON<PipelineRun[]>(`/api/v1/pipeline/runs${query}`);
  },
  getPipelineRun: (id: string) => fetchJSON<PipelineRun>(`/api/v1/pipeline/runs/${id}`),
  triggerPipelineRun: (userQuery?: string, scenario: string = 'Consumer Query Analysis') => {
    const params = new URLSearchParams();
    params.append('scenario_name', scenario);
    if (userQuery) params.append('user_query', userQuery);
    return fetchJSON<PipelineRunResult>(`/api/v1/pipeline/run?${params.toString()}`, {
      method: 'POST',
    });
  },
};
