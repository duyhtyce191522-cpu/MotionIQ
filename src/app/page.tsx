'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import {
  getTodayStats,
  setDailyGoal,
  TodayStats,
  getHistoryEntries,
} from '@/features/storage/storageService';
import {
  getAuthSession,
  getPatientById,
  PatientUser,
} from '@/features/auth/authService';
import { EXERCISES } from '@/features/exercises/exerciseRules';
import { ExerciseId, WorkoutHistoryEntry } from '@/types';

import HeaderNav from '@/components/HeaderNav';
import AnimatedBrandLogo from '@/components/AnimatedBrandLogo';
import KinematicsLineChart from '@/components/KinematicsLineChart';
import HydrationCareSchedule from '@/components/HydrationCareSchedule';

export default function HomePage() {
  const router = useRouter();
  const [todayStats, setTodayStats] = useState<TodayStats | null>(null);
  const [currentPatient, setCurrentPatient] = useState<PatientUser | null>(null);
  const [historyEntries, setHistoryEntries] = useState<WorkoutHistoryEntry[]>([]);
  const [greetingTime, setGreetingTime] = useState<'sáng' | 'chiều' | 'tối'>('sáng');

  useEffect(() => {
    // Time of day greeting
    const hour = new Date().getHours();
    if (hour < 12) setGreetingTime('sáng');
    else if (hour < 18) setGreetingTime('chiều');
    else setGreetingTime('tối');

    const auth = getAuthSession();
    const patientId = auth?.role === 'patient' ? (auth.user.patientId || auth.user.id) : undefined;

    if (patientId) {
      const p = getPatientById(patientId);
      setCurrentPatient(p);
    }

    setTodayStats(getTodayStats(patientId));
    setHistoryEntries(getHistoryEntries(patientId));
  }, []);

  const handleSelectGoal = (goal: number) => {
    setDailyGoal(goal);
    const auth = getAuthSession();
    const patientId = auth?.role === 'patient' ? (auth.user.patientId || auth.user.id) : undefined;
    setTodayStats(getTodayStats(patientId));
  };

  const handleStartExercise = (exerciseId: ExerciseId) => {
    router.push(`/workout/${exerciseId}`);
  };

  // Determine top priority exercise to start
  const topPrescribedId: ExerciseId =
    (currentPatient?.prescribedExercises?.[0] as ExerciseId) || 'sit-to-stand';

  return (
    <div
      className="page"
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#FAF0DF',
        color: '#4A1E14',
      }}
    >
      <HeaderNav />

      <main className="container page-content" style={{ flex: 1, paddingBottom: 'var(--space-12)' }}>
        
        {/* ============================================================
            HERO GREETING BANNER WITH MASCOT & BRAND LOGO (MOBILE FIRST)
            ============================================================ */}
        <section
          style={{
            marginTop: '10px',
            marginBottom: '16px',
            padding: '20px 18px',
            background: 'linear-gradient(135deg, #9E3B24 0%, #B8472E 100%)',
            color: '#FFFFFF',
            borderRadius: '28px',
            boxShadow: '0 12px 30px rgba(158, 59, 36, 0.28)',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Subtle Ambient Watermark Logo — Tệp chìm vào nền card */}
          <div
            style={{
              position: 'absolute',
              right: '-30px',
              bottom: '-35px',
              width: '210px',
              height: '210px',
              opacity: 0.12,
              pointerEvents: 'none',
              userSelect: 'none',
              zIndex: 1,
              transform: 'rotate(-12deg)',
            }}
          >
            <Image
              src="/images/custom-ui/motioniq_logo_transparent.png"
              alt=""
              width={210}
              height={210}
              unoptimized
              style={{ width: '100%', height: '100%', objectFit: 'contain', filter: 'brightness(2)' }}
            />
          </div>

          {/* Autumn leaf & spark accents */}
          <div style={{ position: 'absolute', top: '12px', right: '25%', fontSize: '16px', opacity: 0.4 }}>🍂</div>
          <div style={{ position: 'absolute', bottom: '12px', left: '20%', fontSize: '14px', opacity: 0.35 }}>✨</div>

          <div style={{ position: 'relative', zIndex: 10, display: 'flex', flexDirection: 'column', gap: '14px' }}>
            
            {/* Top Row: Mascot + Greeting Info */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
              {/* Mascot Avatar with Idle Bobbing Animation & Micro Logo Seal */}
              <div
                style={{
                  position: 'relative',
                  width: '72px',
                  height: '72px',
                  borderRadius: '20px',
                  backgroundColor: '#FAF0DF',
                  padding: '4px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 6px 16px rgba(0, 0, 0, 0.2)',
                  flexShrink: 0,
                  animation: 'mascotBobbing 2.8s infinite ease-in-out',
                }}
              >
                <Image
                  src="/images/custom-ui/mascot_login.png"
                  alt="Bé Nấm MotionIQ"
                  width={64}
                  height={64}
                  unoptimized
                  style={{ objectFit: 'contain' }}
                />

                {/* Micro MotionIQ Verified Seal */}
                <div
                  style={{
                    position: 'absolute',
                    bottom: '-3px',
                    right: '-3px',
                    width: '22px',
                    height: '22px',
                    borderRadius: '50%',
                    backgroundColor: '#FAF0DF',
                    border: '1.5px solid #9E3B24',
                    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.25)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '1px',
                  }}
                  title="MotionIQ On-Device AI Verified"
                >
                  <Image
                    src="/images/custom-ui/motioniq_logo_transparent.png"
                    alt="MotionIQ"
                    width={15}
                    height={15}
                    unoptimized
                    style={{ width: '15px', height: '15px', objectFit: 'contain' }}
                  />
                </div>
              </div>

              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px', flexWrap: 'wrap' }}>
                  <span
                    style={{
                      background: 'rgba(255, 255, 255, 0.2)',
                      color: '#FFFFFF',
                      padding: '3px 10px 3px 6px',
                      borderRadius: '9999px',
                      fontSize: '0.68rem',
                      fontWeight: 800,
                      letterSpacing: '0.4px',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '5px',
                    }}
                  >
                    <span
                      style={{
                        width: '14px',
                        height: '14px',
                        borderRadius: '50%',
                        backgroundColor: '#FAF0DF',
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '1px',
                      }}
                    >
                      <Image
                        src="/images/custom-ui/motioniq_logo_transparent.png"
                        alt="MotionIQ"
                        width={11}
                        height={11}
                        unoptimized
                        style={{ objectFit: 'contain' }}
                      />
                    </span>
                    <span>100% ON-DEVICE AI</span>
                  </span>

                  {currentPatient?.therapist && (
                    <span
                      style={{
                        background: '#FAF0DF',
                        color: '#9E3B24',
                        padding: '3px 8px',
                        borderRadius: '9999px',
                        fontSize: '0.68rem',
                        fontWeight: 700,
                      }}
                    >
                      BS: {currentPatient.therapist.split('.').slice(-1)[0]}
                    </span>
                  )}
                </div>

                <h1
                  style={{
                    fontSize: '1.4rem',
                    fontWeight: 900,
                    margin: '2px 0',
                    lineHeight: 1.2,
                    color: '#FFFFFF',
                    textShadow: '0 2px 6px rgba(0, 0, 0, 0.35)',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                  }}
                >
                  Chào buổi {greetingTime},{' '}
                  <span style={{ color: '#FFFFFF' }}>{currentPatient?.name.split(' ').slice(-2).join(' ') || 'Bác'}</span> {currentPatient?.avatarIcon || '👴'}
                </h1>
              </div>
            </div>

            {/* Description Text */}
            <p
              style={{
                margin: 0,
                fontSize: '0.86rem',
                color: '#FFFFFF',
                opacity: 0.95,
                lineHeight: 1.45,
                textShadow: '0 1px 3px rgba(0, 0, 0, 0.2)',
              }}
            >
              {currentPatient?.condition
                ? `${currentPatient.condition} • Bé Nấm và AI đếm nhịp sẵn sàng!`
                : 'Bé Nấm và Trợ lý AI đếm nhịp sẵn sàng đồng hành trong mỗi buổi tập phục hồi hôm nay!'}
            </p>

            {/* Full-width 1-Tap Workout Button */}
            <button
              type="button"
              onClick={() => handleStartExercise(topPrescribedId)}
              style={{
                width: '100%',
                backgroundColor: '#FAF0DF',
                color: '#9E3B24',
                border: 'none',
                padding: '14px 20px',
                borderRadius: '9999px',
                fontSize: '1rem',
                fontWeight: 900,
                boxShadow: '0 6px 20px rgba(0, 0, 0, 0.22)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transition: 'transform 0.2s ease',
              }}
            >
              <span style={{ fontSize: '1.2rem' }}>🏋️</span>
              <span>Vào phòng tập AI ngay</span>
              <span style={{ fontSize: '1rem' }}>➔</span>
            </button>

          </div>
        </section>

        {/* ============================================================
            PRIMARY KPI METRICS GRID (2x2 MOBILE FIRST)
            ============================================================ */}
        <section
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: '10px',
            marginBottom: '16px',
          }}
        >
          {/* KPI 1: Tiến độ hôm nay */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              border: '1.5px solid rgba(158, 59, 36, 0.15)',
              borderRadius: '20px',
              padding: '14px 12px',
              boxShadow: '0 4px 12px rgba(158, 59, 36, 0.06)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#9E3B24', letterSpacing: '0.4px' }}>
                🎯 MỤC TIÊU
              </span>
              <span
                style={{
                  fontSize: '0.65rem',
                  fontWeight: 800,
                  color: todayStats?.isGoalReached ? '#10B981' : '#9E3B24',
                  backgroundColor: todayStats?.isGoalReached ? 'rgba(16, 185, 129, 0.12)' : '#FAF0DF',
                  padding: '2px 6px',
                  borderRadius: '9999px',
                }}
              >
                {todayStats?.isGoalReached ? 'ĐẠT' : `${todayStats?.goalPercent || 0}%`}
              </span>
            </div>

            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '6px 0 2px 0' }}>
              <span style={{ fontSize: '1.9rem', fontWeight: 900, color: '#9E3B24', lineHeight: 1 }}>
                {todayStats?.todayReps || 0}
              </span>
              <span style={{ fontSize: '0.82rem', color: '#888', fontWeight: 600 }}>
                /{todayStats?.dailyGoal || 15} lần
              </span>
            </div>

            {/* Progress Bar in Terracotta */}
            <div style={{ width: '100%', height: '7px', backgroundColor: '#F1E5D4', borderRadius: '9999px', overflow: 'hidden', margin: '4px 0 6px 0' }}>
              <div
                style={{
                  width: `${todayStats?.goalPercent || 0}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #F59E0B, #9E3B24)',
                  borderRadius: '9999px',
                  transition: 'width 0.4s ease',
                }}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.68rem', color: '#666' }}>
              <span>{todayStats?.todayGoodReps || 0} đạt chuẩn</span>
              <div style={{ display: 'flex', gap: '3px' }}>
                {[10, 15, 20].map((g) => (
                  <button
                    key={g}
                    type="button"
                    onClick={() => handleSelectGoal(g)}
                    style={{
                      border: 'none',
                      backgroundColor: todayStats?.dailyGoal === g ? '#9E3B24' : '#F1E5D4',
                      color: todayStats?.dailyGoal === g ? '#FFFFFF' : '#666',
                      borderRadius: '4px',
                      padding: '1px 5px',
                      fontSize: '0.65rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                    }}
                  >
                    {g}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* KPI 2: Chuỗi ngày tập (Streak) */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              border: '1.5px solid rgba(158, 59, 36, 0.15)',
              borderRadius: '20px',
              padding: '14px 12px',
              boxShadow: '0 4px 12px rgba(158, 59, 36, 0.06)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#9E3B24', letterSpacing: '0.4px' }}>
                🔥 CHUỖI TẬP
              </span>
              <span style={{ fontSize: '1.1rem' }}>⭐</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '6px 0 2px 0' }}>
              <span style={{ fontSize: '1.9rem', fontWeight: 900, color: '#D97706', lineHeight: 1 }}>
                {todayStats?.streak || 0}
              </span>
              <span style={{ fontSize: '0.85rem', color: '#888', fontWeight: 600 }}>
                ngày liên tục
              </span>
            </div>

            <p style={{ margin: 0, fontSize: '0.72rem', color: '#666', lineHeight: 1.35 }}>
              {todayStats && todayStats.streak > 0
                ? 'Xuất sắc! Giữ vững vận động mỗi ngày.'
                : 'Bắt đầu bài tập đầu tiên cùng Bé Nấm!'}
            </p>
          </div>

          {/* KPI 3: Biên độ góc ROM */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              border: '1.5px solid rgba(158, 59, 36, 0.15)',
              borderRadius: '20px',
              padding: '14px 12px',
              boxShadow: '0 4px 12px rgba(158, 59, 36, 0.06)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#9E3B24', letterSpacing: '0.4px' }}>
                📐 GÓC ROM TỐT
              </span>
              <span style={{ fontSize: '0.65rem', fontWeight: 800, color: '#10B981' }}>+18.5%</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '6px 0 2px 0' }}>
              <span style={{ fontSize: '1.9rem', fontWeight: 900, color: '#10B981', lineHeight: 1 }}>
                122°
              </span>
              <span style={{ fontSize: '0.78rem', color: '#888', fontWeight: 600 }}>
                Gập gối
              </span>
            </div>

            <p style={{ margin: 0, fontSize: '0.72rem', color: '#666', lineHeight: 1.35 }}>
              Đạt chuẩn an toàn UI-PRMD (90°–125°).
            </p>
          </div>

          {/* KPI 4: Bài tập chỉ định Bác sĩ */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              border: '1.5px solid rgba(158, 59, 36, 0.15)',
              borderRadius: '20px',
              padding: '14px 12px',
              boxShadow: '0 4px 12px rgba(158, 59, 36, 0.06)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#9E3B24', letterSpacing: '0.4px' }}>
                📋 CHỈ ĐỊNH BS
              </span>
              <span style={{ fontSize: '1rem' }}>👨‍⚕️</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '6px 0 2px 0' }}>
              <span style={{ fontSize: '1.9rem', fontWeight: 900, color: '#9E3B24', lineHeight: 1 }}>
                {currentPatient?.prescribedExercises?.length || 2}
              </span>
              <span style={{ fontSize: '0.82rem', color: '#888', fontWeight: 600 }}>
                bài ưu tiên ⭐
              </span>
            </div>

            <p style={{ margin: 0, fontSize: '0.72rem', color: '#666', lineHeight: 1.35 }}>
              Chỉ định bởi {currentPatient?.therapist ? currentPatient.therapist.split('.').slice(-1)[0] : 'Khoa PHCN'}.
            </p>
          </div>
        </section>

        {/* ============================================================
            SECTION: 4 BÀI TẬP CHUẨN HÓA Y SINH (3 DATASETS)
            ============================================================ */}
        <section style={{ marginBottom: 'var(--space-8)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '12px', marginBottom: 'var(--space-4)' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.5rem' }}>🍄</span>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 900, margin: 0, color: '#9E3B24' }}>
                  4 Bài Tập Chuẩn Hóa Theo 3 Dataset Y Sinh
                </h2>
              </div>
              <p style={{ margin: '4px 0 0 0', fontSize: '0.85rem', color: '#666' }}>
                Chuẩn hóa đối chiếu dữ liệu <strong>UI-PRMD</strong>, <strong>KIMORE</strong> và <strong>EHE</strong>.
              </p>
            </div>

            <button
              type="button"
              onClick={() => router.push('/exercises')}
              style={{
                backgroundColor: '#FFFFFF',
                color: '#9E3B24',
                border: '2px solid #9E3B24',
                padding: '8px 18px',
                borderRadius: '9999px',
                fontSize: '0.85rem',
                fontWeight: 700,
                cursor: 'pointer',
              }}
            >
              Xem tất cả bài tập ➔
            </button>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(270px, 1fr))',
              gap: 'var(--space-4)',
            }}
          >
            {Object.values(EXERCISES).map((ex) => {
              const isPrescribed = currentPatient?.prescribedExercises?.includes(ex.id);
              return (
                <div
                  key={ex.id}
                  onClick={() => handleStartExercise(ex.id)}
                  style={{
                    backgroundColor: '#FFFFFF',
                    borderRadius: '28px',
                    padding: '24px',
                    border: isPrescribed ? '2.5px solid #9E3B24' : '1.5px solid rgba(158, 59, 36, 0.15)',
                    boxShadow: '0 6px 20px rgba(158, 59, 36, 0.08)',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    position: 'relative',
                    cursor: 'pointer',
                    transition: 'all 0.25s ease',
                  }}
                >
                  {/* Prescribed Star Badge */}
                  {isPrescribed && (
                    <div
                      style={{
                        position: 'absolute',
                        top: '14px',
                        right: '14px',
                        backgroundColor: '#9E3B24',
                        color: '#FFFFFF',
                        padding: '4px 12px',
                        borderRadius: '9999px',
                        fontSize: '0.72rem',
                        fontWeight: 800,
                        boxShadow: '0 2px 8px rgba(158, 59, 36, 0.3)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px',
                      }}
                    >
                      <span>⭐</span> Bác sĩ chỉ định
                    </div>
                  )}

                  <div>
                    {/* Exercise Icon & Title */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '14px' }}>
                      <div
                        style={{
                          width: '60px',
                          height: '60px',
                          borderRadius: '18px',
                          backgroundColor: '#FAF0DF',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          overflow: 'hidden',
                          flexShrink: 0,
                          boxShadow: '0 4px 12px rgba(158, 59, 36, 0.1)',
                        }}
                      >
                        {ex.iconImage ? (
                          <Image
                            src={ex.iconImage}
                            alt={ex.name}
                            width={48}
                            height={48}
                            unoptimized
                            style={{ objectFit: 'contain' }}
                          />
                        ) : (
                          <span style={{ fontSize: '2rem' }}>{ex.icon}</span>
                        )}
                      </div>

                      <div style={{ minWidth: 0 }}>
                        <h3
                          style={{
                            fontSize: '1.2rem',
                            fontWeight: 900,
                            margin: 0,
                            color: '#9E3B24',
                            whiteSpace: 'nowrap',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                          }}
                        >
                          {ex.name}
                        </h3>
                        <span
                          style={{
                            display: 'inline-block',
                            fontSize: '0.72rem',
                            fontWeight: 700,
                            color: '#0891B2',
                            backgroundColor: '#E0F2FE',
                            padding: '2px 8px',
                            borderRadius: '6px',
                            marginTop: '4px',
                          }}
                        >
                          {ex.datasetSource}
                        </span>
                      </div>
                    </div>

                    <p
                      style={{
                        fontSize: '0.85rem',
                        color: '#666',
                        lineHeight: 1.5,
                        margin: '0 0 14px 0',
                        minHeight: '40px',
                      }}
                    >
                      {ex.description}
                    </p>

                    <div
                      style={{
                        padding: '8px 12px',
                        borderRadius: '12px',
                        backgroundColor: '#FAF0DF',
                        fontSize: '0.78rem',
                        color: '#78350F',
                        marginBottom: '16px',
                        fontWeight: 600,
                      }}
                    >
                      🎯 <strong>Mục tiêu:</strong> {ex.targetAngleDescription}
                    </div>
                  </div>

                  <button
                    type="button"
                    style={{
                      width: '100%',
                      padding: '12px 18px',
                      borderRadius: '9999px',
                      backgroundColor: '#9E3B24',
                      color: '#FFFFFF',
                      border: 'none',
                      fontSize: '0.95rem',
                      fontWeight: 800,
                      boxShadow: '0 4px 14px rgba(158, 59, 36, 0.3)',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '6px',
                    }}
                  >
                    Bắt đầu bài tập ➔
                  </button>
                </div>
              );
            })}
          </div>
        </section>

        {/* ============================================================
            SECTION: KINEMATICS LINE CHART & RECOVERY TREND
            ============================================================ */}
        <section style={{ marginBottom: 'var(--space-8)' }}>
          <KinematicsLineChart entries={historyEntries} />
        </section>

        {/* ============================================================
            SECTION: HYDRATION & CARE SCHEDULE (2 COLUMNS)
            ============================================================ */}
        <section
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: 'var(--space-6)',
            marginBottom: 'var(--space-8)',
          }}
        >
          {/* Left Column: Hydration & Care Schedule */}
          <div>
            <HydrationCareSchedule />
          </div>

          {/* Right Column: Project & Business Model Canvas Gateway */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              border: '2px solid rgba(158, 59, 36, 0.15)',
              borderRadius: '28px',
              padding: '24px',
              boxShadow: '0 6px 20px rgba(158, 59, 36, 0.08)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <span style={{ fontSize: '1.6rem' }}>🏛️</span>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 900, margin: 0, color: '#9E3B24' }}>
                  Mô Hình Dự Án & Năng Lực Cốt Lõi
                </h3>
              </div>

              <p style={{ fontSize: '0.9rem', color: '#666', lineHeight: 1.6, margin: '0 0 16px 0' }}>
                MotionIQ là dự án nghiên cứu y sinh và công nghệ thị giác máy tính với kiến trúc <strong>100% On-Device AI</strong>, giúp người cao tuổi tập phục hồi tại nhà mà không cần thiết bị đeo chuyên dụng đắt tiền.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: '#4A1E14' }}>
                  <span style={{ color: '#10B981', fontWeight: 900 }}>✓</span>
                  <span><strong>3 Dataset chuẩn hóa:</strong> EHE (869 reps), KIMORE (78 đối tượng), UI-PRMD</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: '#4A1E14' }}>
                  <span style={{ color: '#06B6D4', fontWeight: 900 }}>✓</span>
                  <span><strong>Zero-Hardware:</strong> Camera smartphone phổ thông, không cần thiết bị cảm biến</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: '#4A1E14' }}>
                  <span style={{ color: '#9E3B24', fontWeight: 900 }}>✓</span>
                  <span><strong>Khử rung One-Euro:</strong> Triệt tiêu nhiễu chuyển động tay chân người già</span>
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                type="button"
                onClick={() => router.push('/history')}
                style={{
                  width: '100%',
                  padding: '14px 20px',
                  borderRadius: '9999px',
                  backgroundColor: '#9E3B24',
                  color: '#FFFFFF',
                  border: 'none',
                  fontSize: '0.95rem',
                  fontWeight: 800,
                  boxShadow: '0 4px 14px rgba(158, 59, 36, 0.3)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                }}
              >
                <span>📈</span>
                <span>Xem Lịch sử Tập & Báo cáo Y sinh</span>
                <span>➔</span>
              </button>
            </div>
          </div>
        </section>

        {/* ============================================================
            PRIVACY & CLINICAL DISCLAIMER
            ============================================================ */}
        <section
          style={{
            padding: '18px 24px',
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
            border: '1.5px solid rgba(158, 59, 36, 0.2)',
            borderRadius: '24px',
            fontSize: '0.8rem',
            color: '#777',
            lineHeight: 1.6,
            textAlign: 'center',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginBottom: '4px', color: '#9E3B24', fontWeight: 800 }}>
            <span>🛡️ Bảo mật tuyệt đối (100% On-Device AI)</span>
            <span>•</span>
            <span>Bộ môn Vật lý Trị liệu & PHCN</span>
          </div>
          MotionIQ phân tích tư thế cục bộ trên trình duyệt thiết bị, không lưu trữ hay truyền video lên Cloud. Điểm số và góc khớp chỉ mang tính tham khảo vận động, không thay thế chẩn đoán y khoa của Bác sĩ chuyên khoa.
        </section>

      </main>
    </div>
  );
}
