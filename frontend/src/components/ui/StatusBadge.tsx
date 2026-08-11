import React from 'react';

interface StatusBadgeProps {
  variant?: 'emerald' | 'amber' | 'cyan' | 'rose' | 'neutral';
  children: React.ReactNode;
  className?: string;
}

export default function StatusBadge({
  variant = 'neutral',
  children,
  className = '',
}: StatusBadgeProps) {
  const variantStyles = {
    emerald: 'bg-emerald-950/60 text-emerald-400 border-emerald-800/50',
    amber: 'bg-amber-950/60 text-amber-400 border-amber-800/50',
    cyan: 'bg-cyan-950/60 text-cyan-400 border-cyan-800/50',
    rose: 'bg-rose-950/60 text-rose-400 border-rose-800/50',
    neutral: 'bg-slate-900 text-slate-300 border-slate-800',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[11px] font-mono uppercase tracking-wider border font-medium ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
