'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getTodayStats, setDailyGoal, TodayStats, getPatientProfile, PatientProfile } from '@/features/storage/storageService';
import { getAuthSession } from '@/features/auth/authService';

import HeaderNav from '@/components/HeaderNav';

export default function HomePage() {
  const router = useRouter();
  const [todayStats, setTodayStats] = useState<TodayStats | null>(null);
  const [patientProfile, setPatientProfile] = useState<PatientProfile | null>(null);

  useEffect(() => {
    const auth = getAuthSession();
    const patientId = auth?.role === 'patient' ? (auth.user.patientId || auth.user.id) : undefined;
    setTodayStats(getTodayStats(patientId));
    setPatientProfile(getPatientProfile());
  }, []);

  const handleSelectGoal = (goal: number) => {
    setDailyGoal(goal);
    const auth = getAuthSession();
    const patientId = auth?.role === 'patient' ? (auth.user.patientId || auth.user.id) : undefined;
    setTodayStats(getTodayStats(patientId));
  };

  return (
    <div className="page">
      <HeaderNav />
      <div className="container page-content">
        {/* Hero */}
        <div className="landing-hero" style={{ paddingTop: 'var(--space-6)' }}>
          {patientProfile?.name && (
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)',
              border: '1px solid rgba(6, 182, 212, 0.4)',
              padding: '8px 20px',
              borderRadius: 'var(--radius-full)',
              color: 'var(--color-text-accent)',
              fontSize: 'var(--font-size-sm)',
              fontWeight: 700,
              marginBottom: 'var(--space-4)',
              boxShadow: '0 4px 16px rgba(6, 182, 212, 0.2)',
            }}>
              <span style={{ fontSize: '1.2rem' }}>👋</span> Chúc {patientProfile.name} một ngày vận động vui khỏe!
            </div>
          )}
          <div className="landing-logo">🏃‍♂️</div>
          <h1 className="landing-title">
            <span className="text-accent">MotionIQ</span>
          </h1>
          <p className="landing-description">
            Hỗ trợ tập vận động tại nhà bằng AI.
            Camera smartphone phân tích tư thế và đếm số lần tập cho bạn.
          </p>

          {/* Today Goal & Progress Card */}
          {todayStats && (
            <div className="today-goal-card" style={{ textAlign: 'left', marginTop: 'var(--space-4)' }}>
              <div className="today-goal-header">
                <div className="today-goal-title">
                  <span>🎯 Mục tiêu hôm nay</span>
                  {todayStats.streak > 0 && (
                    <span className="streak-badge">
                      🔥 {todayStats.streak} ngày liên tiếp
                    </span>
                  )}
                </div>
                <span className="today-goal-badge">
                  {todayStats.isGoalReached ? '🎉 Đạt mục tiêu' : `${todayStats.todayReps}/${todayStats.dailyGoal} lần`}
                </span>
              </div>

              <div className="goal-progress-bar-bg">
                <div
                  className="goal-progress-bar-fill"
                  style={{ width: `${todayStats.goalPercent}%` }}
                />
              </div>

              <div className="today-goal-footer">
                <span>
                  {todayStats.todaySessions > 0
                    ? `Đã tập ${todayStats.todaySessions} buổi (${todayStats.todayGoodReps} lần đạt chuẩn)`
                    : 'Chưa có buổi tập nào hôm nay'}
                </span>

                <div className="goal-picker">
                  <span style={{ marginRight: '4px' }}>Mục tiêu:</span>
                  {[10, 15, 20].map((goal) => (
                    <button
                      key={goal}
                      type="button"
                      className={`goal-pill ${todayStats.dailyGoal === goal ? 'active' : ''}`}
                      onClick={() => handleSelectGoal(goal)}
                    >
                      {goal}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          <button
            className="btn btn-primary btn-full"
            onClick={() => router.push('/exercises')}
          >
            🏋️ Bắt đầu tập luyện
          </button>
        </div>

        {/* Features with glowing cards */}
        <div className="landing-features">
          <div className="card card-interactive landing-feature">
            <div className="landing-feature-icon">📷</div>
            <div className="landing-feature-text">
              <strong>Không cần thiết bị chuyên dụng</strong> — Chỉ cần đặt điện thoại trước mặt và bắt đầu tập luyện
            </div>
          </div>
          <div className="card card-interactive landing-feature">
            <div className="landing-feature-icon">🗣️</div>
            <div className="landing-feature-text">
              <strong>AI theo dõi tư thế & Giọng nói tiếng Việt</strong> — Đếm nhịp chuẩn xác và hướng dẫn thời gian thực
            </div>
          </div>
          <div className="card card-interactive landing-feature">
            <div className="landing-feature-icon">🔒</div>
            <div className="landing-feature-text">
              <strong>Bảo mật riêng tư tuyệt đối</strong> — Mọi phân tích thực hiện trên máy, không gửi hình ảnh ra ngoài
            </div>
          </div>
          <div className="card card-interactive landing-feature">
            <div className="landing-feature-icon">📊</div>
            <div className="landing-feature-text">
              <strong>Hồ sơ & Báo cáo y tế chuyên sâu</strong> — Dễ dàng theo dõi tiến độ và chia sẻ cho bác sĩ/gia đình
            </div>
          </div>
        </div>

        {/* Privacy Notice */}
        <div className="privacy-notice">
          <span className="privacy-notice-icon">🛡️</span>
          <span>
            Video được xử lý hoàn toàn trên thiết bị của bạn (Edge AI).
            Không có dữ liệu hình ảnh nào được gửi lên máy chủ.
          </span>
        </div>

        {/* History link */}
        <div style={{ marginTop: 'var(--space-6)', textAlign: 'center' }}>
          <button
            className="btn btn-secondary"
            onClick={() => router.push('/history')}
          >
            📋 Xem lịch sử & Báo cáo y tế
          </button>
        </div>

        {/* Disclaimer */}
        <div className="landing-disclaimer">
          MotionIQ là công cụ hỗ trợ vận động và cung cấp phản hồi mang tính
          tham khảo. Ứng dụng không thay thế bác sĩ, chuyên viên vật lý trị
          liệu hoặc đánh giá y khoa chuyên nghiệp. Nếu bạn có bệnh lý nền
          hoặc hạn chế vận động, hãy tham khảo chuyên gia trước khi bắt đầu.
        </div>
      </div>
    </div>
  );
}
