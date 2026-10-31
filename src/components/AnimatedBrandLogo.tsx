'use client';

import React, { useState } from 'react';
import Image from 'next/image';

export type LogoMode = 'top-pill' | 'companion' | 'hero' | 'minimal' | 'badge';
export type LogoTheme = 'cyan' | 'autumn-gold' | 'terracotta';

interface AnimatedBrandLogoProps {
  mode?: LogoMode;
  theme?: LogoTheme;
  size?: number;
  className?: string;
  enableRadarWaves?: boolean;
  onLogoClick?: () => void;
}

export default function AnimatedBrandLogo({
  mode = 'top-pill',
  theme = 'cyan',
  size = 32,
  className = '',
  enableRadarWaves = true,
  onLogoClick,
}: AnimatedBrandLogoProps) {
  const [isSpinning, setIsSpinning] = useState(false);

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsSpinning(true);
    setTimeout(() => setIsSpinning(false), 650);
    if (onLogoClick) onLogoClick();
  };

  const isGold = theme === 'autumn-gold';
  const isTerracotta = theme === 'terracotta';

  // Mode 1: Top Brand Pill (Frosted glass capsule, blends seamlessly with header or background)
  if (mode === 'top-pill') {
    return (
      <div
        onClick={handleClick}
        className={className}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '4px 12px 4px 6px',
          borderRadius: '9999px',
          backgroundColor: isTerracotta
            ? 'rgba(158, 59, 36, 0.12)'
            : 'rgba(250, 240, 223, 0.92)',
          border: isTerracotta
            ? '1.5px solid rgba(158, 59, 36, 0.3)'
            : '1.5px solid rgba(158, 59, 36, 0.2)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 2px 8px rgba(158, 59, 36, 0.08)',
          cursor: 'pointer',
          userSelect: 'none',
          transition: 'all 0.25s ease',
        }}
        title="MotionIQ AI Engine"
      >
        <div
          style={{
            position: 'relative',
            width: size,
            height: size,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {enableRadarWaves && (
            <div
              style={{
                position: 'absolute',
                inset: 0,
                borderRadius: '50%',
                border: '1.5px solid rgba(6, 182, 212, 0.45)',
                animation: 'radarPulse 2.8s infinite ease-out',
                pointerEvents: 'none',
              }}
            />
          )}
          <div
            style={{
              width: size,
              height: size,
              transform: isSpinning ? 'rotate(360deg) scale(1.15)' : 'rotate(0deg) scale(1)',
              transition: 'transform 0.65s cubic-bezier(0.34, 1.56, 0.64, 1)',
            }}
          >
            <Image
              src="/images/custom-ui/motioniq_logo_transparent.png"
              alt="MotionIQ"
              width={size}
              height={size}
              unoptimized
              style={{ width: '100%', height: '100%', objectFit: 'contain' }}
            />
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span
            style={{
              fontWeight: 800,
              fontSize: '0.85rem',
              letterSpacing: '-0.3px',
              color: '#9E3B24',
              lineHeight: 1,
            }}
          >
            MotionIQ
          </span>
          <span
            style={{
              fontSize: '0.62rem',
              fontWeight: 800,
              padding: '2px 6px',
              borderRadius: '9999px',
              backgroundColor: '#9E3B24',
              color: '#FFFFFF',
              letterSpacing: '0.4px',
            }}
          >
            AI
          </span>
        </div>
      </div>
    );
  }

  // Mode 2: Mascot Companion Orb (Floating circular emblem)
  if (mode === 'companion') {
    return (
      <div
        onClick={handleClick}
        className={className}
        style={{
          position: 'relative',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: size + 12,
          height: size + 12,
          cursor: 'pointer',
          userSelect: 'none',
        }}
        title="Quả cầu AI đồng hành MotionIQ"
      >
        {enableRadarWaves && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              borderRadius: '50%',
              border: '1.5px solid rgba(6, 182, 212, 0.4)',
              animation: 'radarPulse 3s infinite ease-out',
              pointerEvents: 'none',
            }}
          />
        )}

        <div
          style={{
            width: size,
            height: size,
            borderRadius: '50%',
            backgroundColor: '#FAF0DF',
            border: '2px solid rgba(158, 59, 36, 0.35)',
            boxShadow: '0 4px 12px rgba(158, 59, 36, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '3px',
            transform: isSpinning ? 'rotate(360deg) scale(1.15)' : 'rotate(0deg) scale(1)',
            transition: 'transform 0.65s cubic-bezier(0.34, 1.56, 0.64, 1)',
          }}
        >
          <Image
            src="/images/custom-ui/motioniq_logo_transparent.png"
            alt="MotionIQ"
            width={size}
            height={size}
            unoptimized
            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
          />
        </div>
      </div>
    );
  }

  // Mode 3: Badge mode (Minimalist inline pill)
  if (mode === 'badge') {
    return (
      <span
        onClick={handleClick}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          padding: '3px 10px 3px 6px',
          borderRadius: '9999px',
          backgroundColor: 'rgba(255, 255, 255, 0.18)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          backdropFilter: 'blur(8px)',
          color: '#FFFFFF',
          fontSize: '0.75rem',
          fontWeight: 800,
          cursor: 'pointer',
          userSelect: 'none',
        }}
      >
        <span
          style={{
            width: size,
            height: size,
            borderRadius: '50%',
            backgroundColor: '#FAF0DF',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2px',
            transform: isSpinning ? 'rotate(360deg)' : 'none',
            transition: 'transform 0.6s ease',
          }}
        >
          <Image
            src="/images/custom-ui/motioniq_logo_transparent.png"
            alt="MotionIQ"
            width={size - 4}
            height={size - 4}
            unoptimized
            style={{ objectFit: 'contain' }}
          />
        </span>
        <span>MotionIQ AI</span>
      </span>
    );
  }

  // Default / Minimal mode: Pure icon with click animation
  return (
    <div
      onClick={handleClick}
      className={className}
      style={{
        position: 'relative',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: size,
        height: size,
        cursor: 'pointer',
        transform: isSpinning ? 'rotate(360deg) scale(1.15)' : 'rotate(0deg) scale(1)',
        transition: 'transform 0.65s cubic-bezier(0.34, 1.56, 0.64, 1)',
      }}
      title="MotionIQ Logo"
    >
      <Image
        src="/images/custom-ui/motioniq_logo_transparent.png"
        alt="MotionIQ"
        width={size}
        height={size}
        unoptimized
        style={{ width: '100%', height: '100%', objectFit: 'contain' }}
      />
    </div>
  );
}
