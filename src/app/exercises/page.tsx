'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { EXERCISES } from '@/features/exercises/exerciseRules';
import { ExerciseId } from '@/types';
import { getTodayStats, TodayStats } from '@/features/storage/storageService';
import { PoseService } from '@/features/pose/poseService';
import HeaderNav from '@/components/HeaderNav';
import ExerciseIcon from '@/components/ExerciseIcon';
import { getAuthSession, getPatientById, PatientUser } from '@/features/auth/authService';

export default function ExercisesPage() {
  const router = useRouter();
  const [todayStats, setTodayStats] = useState<TodayStats | null>(null);
  const [currentPatient, setCurrentPatient] = useState<PatientUser | null>(null);

  useEffect(() => {
    const auth = getAuthSession();
    const patientId = auth?.role === 'patient' ? (auth.user.patientId || auth.user.id) : undefined;
    if (patientId) {
      const p = getPatientById(patientId);
      setCurrentPatient(p);
    }
    setTodayStats(getTodayStats(patientId));
    // Khởi động nạp trước mô hình AI trong nền khi người dùng đang xem danh sách bài tập
    PoseService.prewarm();
  }, []);

  const handleSelectExercise = (id: ExerciseId) => {
    router.push(`/workout/${id}`);
  };

  // Sort exercises: Prescribed exercises first
  const rawList = Object.values(EXERCISES);
  const exerciseList = [...rawList].sort((a, b) => {
    const aPrescribed = currentPatient?.prescribedExercises?.includes(a.id) ? 1 : 0;
    const bPrescribed = currentPatient?.prescribedExercises?.includes(b.id) ? 1 : 0;
    return bPrescribed - aPrescribed;
  });

  return (
    <div className="page">
      <HeaderNav />
      <div className="container page-content">
        <button
          className="back-nav"
          onClick={() => router.push('/')}
        >
          ← Trang chủ
        </button>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px', marginBottom: 'var(--space-2)' }}>
          <h1 style={{ margin: 0 }}>Chọn bài tập</h1>
          {currentPatient && (
            <span className="patient-identity-badge" style={{ fontSize: '0.85rem', padding: '4px 12px' }}>
              {currentPatient.avatarIcon || '👤'} {currentPatient.name}
            </span>
          )}
        </div>

        <p className="text-muted" style={{ marginBottom: 'var(--space-4)' }}>
          {currentPatient?.prescribedExercises && currentPatient.prescribedExercises.length > 0
            ? `Bác sĩ / KTV đã thiết lập kế hoạch phục hồi chức năng dành riêng cho bạn.`
            : `Chọn bài tập bạn muốn thực hiện hôm nay.`}
        </p>

        {/* Doctor Prescribed Banner */}
        {currentPatient?.prescribedExercises && currentPatient.prescribedExercises.length > 0 && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-3)',
            padding: 'var(--space-3) var(--space-4)',
            background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(217, 119, 6, 0.18))',
            border: '1px solid rgba(245, 158, 11, 0.4)',
            borderRadius: 'var(--radius-lg)',
            marginBottom: 'var(--space-5)',
            boxShadow: '0 4px 16px rgba(245, 158, 11, 0.15)',
          }}>
            <span style={{ fontSize: '1.6rem' }}>⭐</span>
            <div>
              <div style={{ fontWeight: 700, color: '#fbbf24', fontSize: 'var(--font-size-base)' }}>
                Bác sĩ / KTV chỉ định {currentPatient.prescribedExercises.length} bài tập ưu tiên
              </div>
              <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
                {currentPatient.therapist ? `Bởi ${currentPatient.therapist} • ` : ''}
                Mục tiêu: {currentPatient.dailyRepGoal || todayStats?.dailyGoal || 15} lần/ngày
              </div>
            </div>
          </div>
        )}

        {/* Today Goal Progress Bar */}
        {todayStats && (
          <div className="today-goal-card" style={{ marginBottom: 'var(--space-6)' }}>
            <div className="today-goal-header">
              <span className="today-goal-title">
                🎯 Tiến độ hôm nay
              </span>
              <span className="today-goal-badge">
                {todayStats.isGoalReached ? '🎉 Hoàn thành!' : `${todayStats.todayReps}/${todayStats.dailyGoal} lần`}
              </span>
            </div>
            <div className="goal-progress-bar-bg">
              <div
                className="goal-progress-bar-fill"
                style={{ width: `${todayStats.goalPercent}%` }}
              />
            </div>
            <div className="today-goal-footer">
              <span>{todayStats.isGoalReached ? 'Bạn đã đạt mục tiêu hàng ngày!' : `Còn ${Math.max(0, todayStats.dailyGoal - todayStats.todayReps)} lần để hoàn thành mục tiêu`}</span>
              {todayStats.streak > 0 && <span className="streak-badge">🔥 {todayStats.streak} ngày</span>}
            </div>
          </div>
        )}

        {/* Dataset Provenance Notice */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-3)',
          padding: 'var(--space-3) var(--space-4)',
          background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.08), rgba(59, 130, 246, 0.12))',
          border: '1px solid rgba(14, 165, 233, 0.3)',
          borderRadius: 'var(--radius-lg)',
          marginBottom: 'var(--space-5)',
        }}>
          <span style={{ fontSize: '1.4rem' }}>🔬</span>
          <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
            <strong style={{ color: '#38bdf8' }}>Bộ dữ liệu chuyển động mẫu: </strong>
            Mô hình nhận diện động tác được xây dựng dựa trên bộ dữ liệu <strong>UI-PRMD</strong> cho 4 bài tập vận động chức năng chuẩn hóa.
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          {exerciseList.map((exercise) => {
            const isPrescribed = Boolean(currentPatient?.prescribedExercises?.includes(exercise.id));
            return (
              <div
                key={exercise.id}
                className={`card card-interactive exercise-card ${isPrescribed ? 'is-prescribed' : ''}`}
                onClick={() => handleSelectExercise(exercise.id)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    handleSelectExercise(exercise.id);
                  }
                }}
              >
                <div className="exercise-card-icon"><ExerciseIcon exercise={exercise} size={60} /></div>
                <div className="exercise-card-content">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                    <h3 style={{ margin: 0 }}>{exercise.name}</h3>
                    {isPrescribed && (
                      <span className="prescribed-badge">⭐ Bác sĩ chỉ định</span>
                    )}
                    {exercise.datasetSource && (
                      <span className="dataset-badge">📊 {exercise.datasetSource}</span>
                    )}
                  </div>
                  <p style={{ marginTop: '4px' }}>{exercise.description}</p>
                  {exercise.targetAngleDescription && (
                    <div style={{ marginTop: 'var(--space-2)', fontSize: 'var(--font-size-xs)', color: isPrescribed ? '#fbbf24' : 'var(--color-accent-primary)' }}>
                      🎯 {exercise.targetAngleDescription}
                    </div>
                  )}
                </div>
                <div className="exercise-card-arrow">→</div>
              </div>
            );
          })}
        </div>

        {/* Safety notice */}
        <div className="summary-disclaimer" style={{ marginTop: 'var(--space-8)' }}>
          ⚠️ Nếu bạn cảm thấy đau, chóng mặt hoặc khó thở, hãy dừng tập ngay.
          Người có bệnh lý nền nên tham khảo bác sĩ trước khi bắt đầu.
        </div>
      </div>
    </div>
  );
}
