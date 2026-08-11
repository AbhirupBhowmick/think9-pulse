'use client';

import React, { useCallback, useEffect, useRef } from 'react';
import './ScrollExpand.css';

const clamp = (v: number, a: number, b: number) => (v < a ? a : v > b ? b : v);

const smoothstep = (edge0: number, edge1: number, x: number) => {
  const t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
  return t * t * (3 - 2 * t);
};

export interface ScrollExpandProps {
  src: string;
  alt?: string;
  title?: string;
  startWidth?: number;
  startHeight?: number;
  startRadius?: number;
  endRadius?: number;
  mediaZoom?: number;
  smoothing?: number;
  overlayScrim?: number;
  enabled?: boolean;
  children?: React.ReactNode;
  className?: string;
}

type StageState = 'IDLE' | 'EXPANDING' | 'FULLY_EXPANDED' | 'CONTRACTING';

export default function ScrollExpand({
  src,
  alt = 'Consumer product discovery',
  title,
  startWidth = 42,
  startHeight = 52,
  startRadius = 24,
  endRadius = 0,
  mediaZoom = 1.05,
  smoothing = 0.12,
  overlayScrim = 0.45,
  enabled = true,
  children,
  className = '',
}: ScrollExpandProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const cardRef = useRef<HTMLDivElement | null>(null);
  const mediaRef = useRef<HTMLImageElement | null>(null);
  const scrimRef = useRef<HTMLDivElement | null>(null);
  const contentRef = useRef<HTMLDivElement | null>(null);
  const headerRef = useRef<HTMLDivElement | null>(null);

  const targetProgress = useRef(0);
  const currentProgress = useRef(0);
  const isLockedRef = useRef(false);
  const stageStateRef = useRef<StageState>('IDLE');
  const rafId = useRef<number | null>(null);
  const touchStartY = useRef<number | null>(null);

  const PROGRESS_FACTOR = 0.0025;
  const MAX_WHEEL_DELTA = 100;

  const applyTransforms = useCallback(
    (t: number) => {
      const card = cardRef.current;
      const media = mediaRef.current;
      const scrim = scrimRef.current;
      const content = contentRef.current;
      const header = headerRef.current;

      const w = startWidth + (100 - startWidth) * t;
      const h = startHeight + (100 - startHeight) * t;
      const r = startRadius + (endRadius - startRadius) * t;

      if (card) {
        card.style.width = `${w}vw`;
        card.style.height = `${h}vh`;
        card.style.borderRadius = `${r}px`;
      }

      if (media) {
        const z = mediaZoom - (mediaZoom - 1.0) * t;
        media.style.transform = `scale(${z})`;
      }

      if (scrim) {
        scrim.style.backgroundColor = `rgba(8, 11, 16, ${t * overlayScrim})`;
      }

      if (header) {
        // Section header stays fully visible through early expansion, fading as image reaches full bleed (t: 0.30 -> 0.70)
        const headerAlpha = 1 - smoothstep(0.3, 0.7, t);
        header.style.opacity = `${headerAlpha}`;
        header.style.transform = `translateY(${-t * 20}px)`;
      }

      if (content) {
        // Overlay text fades in smoothly as image reaches full bleed (t: 0.65 -> 0.95)
        const contentAlpha = smoothstep(0.65, 0.95, t);
        content.style.opacity = `${contentAlpha}`;
        content.style.transform = `translateY(${(1 - contentAlpha) * 16}px)`;
      }
    },
    [startWidth, startHeight, startRadius, endRadius, mediaZoom, overlayScrim]
  );

  const loop = useCallback(() => {
    const diff = targetProgress.current - currentProgress.current;

    if (Math.abs(diff) > 0.0005) {
      currentProgress.current += diff * smoothing;
    } else {
      currentProgress.current = targetProgress.current;
    }

    applyTransforms(currentProgress.current);
    rafId.current = requestAnimationFrame(loop);
  }, [smoothing, applyTransforms]);

  useEffect(() => {
    if (!enabled) {
      applyTransforms(0);
      return;
    }

    const container = containerRef.current;
    if (!container) return;

    const handleWheel = (e: WheelEvent) => {
      const rect = container.getBoundingClientRect();
      const deltaY = e.deltaY;
      const vh = window.innerHeight || 1;

      // Robust fast-scroll activation zone: section top entering or present in viewport
      const isEnteringViewportDown = rect.top <= vh * 0.85 && rect.bottom >= vh * 0.2;
      const isEnteringViewportUp = rect.bottom >= vh * 0.15 && rect.top <= vh * 0.8;

      // 1. Activation Check from IDLE (scrolling DOWN)
      if (!isLockedRef.current && stageStateRef.current === 'IDLE') {
        if (deltaY > 0 && isEnteringViewportDown && targetProgress.current < 1) {
          isLockedRef.current = true;
          stageStateRef.current = 'EXPANDING';
        }
      }

      // 2. Activation Check from FULLY_EXPANDED (scrolling UP)
      if (!isLockedRef.current && stageStateRef.current === 'FULLY_EXPANDED') {
        if (deltaY < 0 && isEnteringViewportUp && targetProgress.current > 0) {
          isLockedRef.current = true;
          stageStateRef.current = 'CONTRACTING';
        }
      }

      // 3. Locked Wheel Processing (Capture Phase)
      if (isLockedRef.current) {
        e.preventDefault();
        e.stopPropagation();

        const clampedDelta = Math.max(-MAX_WHEEL_DELTA, Math.min(MAX_WHEEL_DELTA, deltaY));
        const progressDelta = clampedDelta * PROGRESS_FACTOR;
        const currentT = targetProgress.current;

        // Scrolling Down
        if (deltaY > 0) {
          if (currentT < 1) {
            targetProgress.current = clamp(currentT + progressDelta, 0, 1);
          } else {
            // Full bleed reached (progress = 1). Consume this tick and unlock for downward scroll.
            targetProgress.current = 1;
            isLockedRef.current = false;
            stageStateRef.current = 'FULLY_EXPANDED';
          }
        }
        // Scrolling Up
        else if (deltaY < 0) {
          if (currentT > 0) {
            targetProgress.current = clamp(currentT + progressDelta, 0, 1);
          } else {
            // Original framed size reached (progress = 0). Consume this tick and unlock for upward scroll.
            targetProgress.current = 0;
            isLockedRef.current = false;
            stageStateRef.current = 'IDLE';
          }
        }
      }
    };

    const handleTouchStart = (e: TouchEvent) => {
      if (e.touches.length > 0) {
        touchStartY.current = e.touches[0].clientY;
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (touchStartY.current === null || e.touches.length === 0) return;
      const rect = container.getBoundingClientRect();
      const currentY = e.touches[0].clientY;
      const deltaY = touchStartY.current - currentY;
      touchStartY.current = currentY;
      const vh = window.innerHeight || 1;

      const isEnteringViewportDown = rect.top <= vh * 0.85 && rect.bottom >= vh * 0.2;
      const isEnteringViewportUp = rect.bottom >= vh * 0.15 && rect.top <= vh * 0.8;

      if (!isLockedRef.current && stageStateRef.current === 'IDLE') {
        if (deltaY > 0 && isEnteringViewportDown && targetProgress.current < 1) {
          isLockedRef.current = true;
          stageStateRef.current = 'EXPANDING';
        }
      }

      if (!isLockedRef.current && stageStateRef.current === 'FULLY_EXPANDED') {
        if (deltaY < 0 && isEnteringViewportUp && targetProgress.current > 0) {
          isLockedRef.current = true;
          stageStateRef.current = 'CONTRACTING';
        }
      }

      if (isLockedRef.current) {
        e.preventDefault();
        e.stopPropagation();

        const clampedDelta = Math.max(-MAX_WHEEL_DELTA, Math.min(MAX_WHEEL_DELTA, deltaY));
        const progressDelta = clampedDelta * PROGRESS_FACTOR;
        const currentT = targetProgress.current;

        if (deltaY > 0) {
          if (currentT < 1) {
            targetProgress.current = clamp(currentT + progressDelta, 0, 1);
          } else {
            targetProgress.current = 1;
            isLockedRef.current = false;
            stageStateRef.current = 'FULLY_EXPANDED';
          }
        } else if (deltaY < 0) {
          if (currentT > 0) {
            targetProgress.current = clamp(currentT + progressDelta, 0, 1);
          } else {
            targetProgress.current = 0;
            isLockedRef.current = false;
            stageStateRef.current = 'IDLE';
          }
        }
      }
    };

    window.addEventListener('wheel', handleWheel, { passive: false, capture: true });
    window.addEventListener('touchstart', handleTouchStart, { passive: true });
    window.addEventListener('touchmove', handleTouchMove, { passive: false, capture: true });

    rafId.current = requestAnimationFrame(loop);

    return () => {
      if (rafId.current !== null) {
        cancelAnimationFrame(rafId.current);
      }
      window.removeEventListener('wheel', handleWheel, { capture: true });
      window.removeEventListener('touchstart', handleTouchStart);
      window.removeEventListener('touchmove', handleTouchMove, { capture: true });
    };
  }, [enabled, loop, applyTransforms]);

  return (
    <section
      id="engine"
      ref={containerRef}
      className={`relative w-full h-[100vh] min-h-[100vh] bg-[#080B10] flex items-center justify-center overflow-hidden border-b border-white/[0.08] ${className}`}
    >
      {/* Layer 1 (z-5): Centered Card Frame */}
      <div ref={cardRef} className="scroll-expand--card bg-[#0F141B] z-5 relative">
        <div className="scroll-expand--media-wrapper">
          <img
            ref={mediaRef}
            src={src}
            alt={alt}
            className="scroll-expand--media"
          />
          {/* Layer 2 (z-10): Dark Scrim */}
          <div ref={scrimRef} className="scroll-expand--scrim z-10" />
        </div>
      </div>

      {/* Layer 3 (z-20): Single Coherent Content Overlay Layer */}
      <div className="absolute inset-0 z-20 flex flex-col items-center justify-between py-10 px-6 pointer-events-none">
        {/* Top Header Block (fades out during t: 0.30 -> 0.70) */}
        <div ref={headerRef} className="text-center max-w-4xl mx-auto space-y-2 pt-4">
          <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest block">
            SEE THE INTELLIGENCE ENGINE
          </span>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-[#F5F7FA] tracking-tight">
            From signal to decision.
          </h2>
          <p className="text-[#8B95A5] max-w-2xl mx-auto text-xs sm:text-sm leading-relaxed">
            Follow how THINK9 PULSE turns fragmented consumer behavior into evidence-backed commercial opportunities.
          </p>
        </div>

        {/* Center Overlay Text (fades in near full bleed t: 0.65 -> 0.95) */}
        <div ref={contentRef} className="text-center max-w-3xl mx-auto space-y-3 pb-12">
          {title && (
            <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest block">
              {title}
            </span>
          )}
          {children}
        </div>
      </div>
    </section>
  );
}
