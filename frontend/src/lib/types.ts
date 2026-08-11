export interface Brand {
  id: string;
  name: string;
  sector: string;
  description?: string;
  target_consumer?: string;
  positioning?: string;
  product_categories: string[];
  created_at: string;
}

export interface Signal {
  id: string;
  source: string;
  source_url?: string;
  title?: string;
  content: string;
  signal_type: string;
  sector: string;
  sentiment: number;
  signal_strength: number;
  geography: string;
  detected_at: string;
  metadata: Record<string, any>;
}

export interface Trend {
  id: string;
  name: string;
  description: string;
  sector: string;
  momentum_score: number;
  confidence_score: number;
  growth_rate: number;
  signal_count: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Evidence {
  id: string;
  trend_id: string;
  signal_id: string;
  evidence_type: string;
  relevance_score: number;
  explanation: string;
  created_at: string;
  signal?: Signal;
}

export interface Opportunity {
  id: string;
  trend_id?: string;
  brand_id?: string;
  title: string;
  description: string;
  consumer_need: string;
  target_consumer: string;
  product_concept: string;
  positioning: string;
  confidence_score: number;
  risk_score: number;
  status: string; // IN_REVIEW | APPROVED | REJECTED
  source_type?: string;
  recommended_action?: string;
  created_at: string;
  updated_at: string;
  brand?: Brand;
}

export interface OpportunityDetail extends Opportunity {
  trend?: Trend;
  evidence: Evidence[];
}

export interface PipelineRun {
  id: string;
  scenario_name: string;
  user_query?: string;
  status: string;
  source_type?: string;
  current_stage: string;
  started_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface AgentExecutionStage {
  stage_name: string;
  agent_name: string;
  status: string;
  started_at: string;
  completed_at: string;
  execution_time_ms: number;
  input_summary: string;
  output_summary: string;
  confidence_score?: number;
  error?: string;
}

export interface PipelineRunResult {
  pipeline_run_id: string;
  scenario: string;
  status: string;
  opportunity_id?: string;
  opportunity_title?: string;
  matched_brand_name?: string;
  validation_status: string;
  confidence_score: number;
  summary: string;
  execution_stages: AgentExecutionStage[];
}
