'use client';

import React, { useRef, useEffect } from 'react';
import { Renderer, Program, Mesh, Triangle } from 'ogl';
import './AcidSquares.css';

interface AcidSquaresProps {
  color1?: string;
  color2?: string;
  color3?: string;
  detail?: 'low' | 'medium' | 'high';
  speed?: number;
  waveDepth?: number;
  zoom?: number;
  density?: number;
  glow?: number;
  exposure?: number;
  spread?: number;
  stepSize?: number;
  colorShift?: number;
  contrast?: number;
  brightness?: number;
  opacity?: number;
  mouseInteraction?: boolean;
  mouseStrength?: number;
  mouseRadius?: number;
  blur?: number;
  grain?: boolean;
  grainIntensity?: number;
  className?: string;
}

function hexToRgb(hex: string): [number, number, number] {
  const cleanHex = hex.replace('#', '');
  const bigint = parseInt(cleanHex, 16);
  const r = ((bigint >> 16) & 255) / 255;
  const g = ((bigint >> 8) & 255) / 255;
  const b = (bigint & 255) / 255;
  return [r, g, b];
}

const vertexShader = `#version 300 es
in vec2 position;
in vec2 uv;
out vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const fragmentShader = `#version 300 es
precision highp float;

uniform float uTime;
uniform vec2 uResolution;
uniform vec3 uColor1;
uniform vec3 uColor2;
uniform vec3 uColor3;
uniform float uSpeed;
uniform float uWaveDepth;
uniform float uZoom;
uniform float uDensity;
uniform float uGlow;
uniform float uExposure;
uniform float uSpread;
uniform float uStepSize;
uniform float uColorShift;
uniform float uContrast;
uniform float uBrightness;
uniform float uOpacity;
uniform vec2 uMouse;
uniform float uMouseRadius;
uniform float uMouseStrength;
uniform float uGrain;
uniform float uGrainIntensity;

in vec2 vUv;
out vec4 fragColor;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

mat2 rotate2D(float angle) {
    return mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
}

void main() {
    vec2 st = (gl_FragCoord.xy - 0.5 * uResolution.xy) / min(uResolution.x, uResolution.y);
    st *= uZoom;

    // Mouse influence
    vec2 mouseNorm = (uMouse - 0.5 * uResolution.xy) / min(uResolution.x, uResolution.y);
    float mouseDist = length(st - mouseNorm);
    float mouseDisp = smoothstep(uMouseRadius, 0.0, mouseDist) * uMouseStrength;
    st += normalize(st - mouseNorm + 0.0001) * mouseDisp;

    float t = uTime * uSpeed;
    vec2 grid = floor(st * uDensity);
    vec2 pos = fract(st * uDensity) - 0.5;

    // Raymarching step pattern for acid squares effect
    float dist = length(pos);
    float angle = atan(pos.y, pos.x);
    
    float wave = sin(dist * 10.0 - t * 2.0 + dot(grid, vec2(0.5, 0.5))) * uWaveDepth;
    float squares = abs(sin(pos.x * 12.0 + wave)) * abs(cos(pos.y * 12.0 - wave));
    
    float glowEffect = exp(-dist * (6.0 - uGlow * 3.0));
    
    // Color interpolation
    float mix1 = clamp((sin(t + length(grid) * uSpread) + 1.0) * 0.5 + uColorShift, 0.0, 1.0);
    vec3 col = mix(uColor1, uColor2, mix1);
    col = mix(col, uColor3, squares * glowEffect);

    col *= (squares + glowEffect * 0.8 + (uExposure / 5000.0));
    col = (col - 0.5) * uContrast + 0.5 + (uBrightness - 1.0);
    col = max(vec3(0.0), col);

    // Grain
    if (uGrain > 0.5) {
        float n = (random(vUv + vec2(uTime * 0.01)) - 0.5) * uGrainIntensity;
        col += n;
    }

    // Soft vignette
    vec2 uvNorm = vUv * (1.0 - vUv.yx);
    float vig = uvNorm.x * uvNorm.y * 15.0;
    vig = clamp(pow(vig, 0.35), 0.0, 1.0);
    col *= vig;

    fragColor = vec4(col, uOpacity);
}
`;

export default function AcidSquares({
  color1 = '#5227FF',
  color2 = '#A855F7',
  color3 = '#FFFFFF',
  detail = 'medium',
  speed = 0.7,
  waveDepth = 1,
  zoom = 1.3,
  density = 10,
  glow = 1,
  exposure = 2700,
  spread = 0.3,
  stepSize = 0.002,
  colorShift = 0,
  contrast = 1,
  brightness = 1,
  opacity = 1,
  mouseInteraction = true,
  mouseStrength = 0.1,
  mouseRadius = 0.35,
  blur = 0,
  grain = true,
  grainIntensity = 0.05,
  className = '',
}: AcidSquaresProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mousePos = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const renderer = new Renderer({ antialias: true, alpha: true });
    const gl = renderer.gl;
    container.appendChild(gl.canvas);

    const geometry = new Triangle(gl);
    const program = new Program(gl, {
      vertex: vertexShader,
      fragment: fragmentShader,
      uniforms: {
        uTime: { value: 0 },
        uResolution: { value: [0, 0] },
        uColor1: { value: hexToRgb(color1) },
        uColor2: { value: hexToRgb(color2) },
        uColor3: { value: hexToRgb(color3) },
        uSpeed: { value: speed },
        uWaveDepth: { value: waveDepth },
        uZoom: { value: zoom },
        uDensity: { value: density },
        uGlow: { value: glow },
        uExposure: { value: exposure },
        uSpread: { value: spread },
        uStepSize: { value: stepSize },
        uColorShift: { value: colorShift },
        uContrast: { value: contrast },
        uBrightness: { value: brightness },
        uOpacity: { value: opacity },
        uMouse: { value: [0, 0] },
        uMouseRadius: { value: mouseRadius },
        uMouseStrength: { value: mouseInteraction ? mouseStrength : 0.0 },
        uGrain: { value: grain ? 1.0 : 0.0 },
        uGrainIntensity: { value: grainIntensity },
      },
    });

    const mesh = new Mesh(gl, { geometry, program });

    function resize() {
      if (!container) return;
      const width = container.clientWidth;
      const height = container.clientHeight;
      renderer.setSize(width, height);
      program.uniforms.uResolution.value = [width, height];
    }

    resize();
    window.addEventListener('resize', resize);

    const handleMouseMove = (e: MouseEvent) => {
      if (!mouseInteraction || !container) return;
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = rect.height - (e.clientY - rect.top);
      mousePos.current = { x, y };
      program.uniforms.uMouse.value = [x, y];
    };

    if (mouseInteraction) {
      window.addEventListener('mousemove', handleMouseMove);
    }

    let animationId: number;
    function update(t: number) {
      animationId = requestAnimationFrame(update);
      program.uniforms.uTime.value = t * 0.001;
      renderer.render({ scene: mesh });
    }
    animationId = requestAnimationFrame(update);

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
      if (mouseInteraction) {
        window.removeEventListener('mousemove', handleMouseMove);
      }
      if (container && gl.canvas.parentNode === container) {
        container.removeChild(gl.canvas);
      }
    };
  }, [
    color1, color2, color3, detail, speed, waveDepth, zoom, density, glow,
    exposure, spread, stepSize, colorShift, contrast, brightness, opacity,
    mouseInteraction, mouseStrength, mouseRadius, blur, grain, grainIntensity
  ]);

  return (
    <div ref={containerRef} className={`acid-squares-container ${className}`} />
  );
}
