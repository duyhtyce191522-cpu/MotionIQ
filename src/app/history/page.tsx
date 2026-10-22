'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import {
  WorkoutHistoryEntry,
  WorkoutSession,
} from '@/types';
import { EXERCISES } from '@/features/exercises/exerciseRules';
import {
  getHistoryEntries,
  getFullSession,
  getWeeklyStats,
  getDailyStreak,
  deleteHistoryEntry,
  clearAllHistory,
  groupByDate,
  WeeklyStats,
  getPatientProfile,
  savePatientProfile,
  PatientProfile,
} from '@/features/storage/storageService';
import HeaderNav from '@/components/HeaderNav';
import {
  getAuthSession,
  getAllPatients,
  PatientUser,
} from '@/features/auth/authService';

export default function HistoryPage() {
  const router = useRouter();
  const [entries, setEntries] = useState<WorkoutHistoryEntry[]>([]);
  const [weeklyStats, setWeeklyStats] = useState<WeeklyStats | null>(null);
  const [streak, setStreak] = useState<number>(0);
  const [selectedSession, setSelectedSession] = useState<WorkoutSession | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<string | null>(null);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  // Auth & Multi-Patient Filtering
  const [currentUserRole, setCurrentUserRole] = useState<'patient' | 'admin'>('patient');
  const [patientsList, setPatientsList] = useState<PatientUser[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('all');
  const [activePatientUser, setActivePatientUser] = useState<PatientUser | null>(null);

  // Medical Report & Patient Profile
  const [showReportModal, setShowReportModal] = useState(false);
  const [patientProfile, setPatientProfile] = useState<PatientProfile>(getPatientProfile());
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [editName, setEditName] = useState('');
  const [editAge, setEditAge] = useState(68);
  const [editCondition, setEditCondition] = useState('');
  const [editTherapist, setEditTherapist] = useState('');

  const loadData = useCallback((targetPatientId?: string) => {
    const session = getAuthSession();
    const role = session?.role || 'patient';
    setCurrentUserRole(role);

    const patients = getAllPatients();
    setPatientsList(patients);

    let pId = targetPatientId !== undefined ? targetPatientId : selectedPatientId;
    if (role === 'patient') {
      pId = session?.user.patientId || session?.user.id || 'patient-1';
      setSelectedPatientId(pId);
      const found = patients.find((p) => p.id === pId) || null;
      setActivePatientUser(found);
    } else {
      // admin
      if (pId !== 'all') {
        const found = patients.find((p) => p.id === pId) || null;
        setActivePatientUser(found);
      } else {
        setActivePatientUser(null);
      }
    }

    const filterArg = pId === 'all' ? undefined : pId;
    setEntries(getHistoryEntries(filterArg));
    setWeeklyStats(getWeeklyStats(filterArg));
    setStreak(getDailyStreak(filterArg));
    setPatientProfile(getPatientProfile());
  }, [selectedPatientId]);

  const handleSelectPatientFilter = (id: string) => {
    setSelectedPatientId(id);
    loadData(id);
  };

  const handleOpenReport = () => {
    if (activePatientUser) {
      setEditName(activePatientUser.name);
      setEditAge(activePatientUser.age);
      setEditCondition(activePatientUser.condition || 'Tập phục hồi chức năng');
      setEditTherapist(activePatientUser.therapist || 'Khoa PHCN');
      setPatientProfile({
        name: activePatientUser.name,
        age: activePatientUser.age,
        gender: activePatientUser.gender,
        condition: activePatientUser.condition || 'Tập phục hồi chức năng',
        therapist: activePatientUser.therapist || 'Khoa PHCN',
        emergencyContact: activePatientUser.emergencyContact || '115',
        speechSpeed: 'slow',
      });
    } else {
      const prof = getPatientProfile();
      setPatientProfile(prof);
      setEditName(prof.name);
      setEditAge(prof.age);
      setEditCondition(prof.condition);
      setEditTherapist(prof.therapist);
    }
    setShowReportModal(true);
  };

  const handleSaveProfile = () => {
    const updated: PatientProfile = {
      ...patientProfile,
      name: editName.trim() || 'Người tập',
      age: editAge || 68,
      condition: editCondition.trim() || 'Tập phục hồi chức năng',
      therapist: editTherapist.trim() || 'Khoa PHCN',
    };
    savePatientProfile(updated);
    setPatientProfile(updated);
    setIsEditingProfile(false);
  };

  const handlePrint = () => {
    window.print();
  };

  const getExerciseClinicalData = () => {
    const stats: Record<string, { totalReps: number; goodReps: number; sessions: number; warnings: string[] }> = {};
    
    for (const entry of entries) {
      if (!stats[entry.exerciseId]) {
        stats[entry.exerciseId] = { totalReps: 0, goodReps: 0, sessions: 0, warnings: [] };
      }
      stats[entry.exerciseId].totalReps += entry.totalReps;
      stats[entry.exerciseId].goodReps += entry.goodReps;
      stats[entry.exerciseId].sessions += 1;

      const full = getFullSession(entry.id);
      if (full && full.warnings) {
        for (const w of full.warnings) {
          if (!stats[entry.exerciseId].warnings.includes(w)) {
            stats[entry.exerciseId].warnings.push(w);
          }
        }
      }
    }

    return stats;
  };

  useEffect(() => {
    let initialPatientId: string = 'all';
    const session = getAuthSession();
    if (session?.role === 'patient') {
      initialPatientId = session.user.patientId || session.user.id || 'patient-1';
    } else {
      if (typeof window !== 'undefined') {
        const params = new URLSearchParams(window.location.search);
        const qId = params.get('patientId');
        if (qId) {
          initialPatientId = qId;
        }
      }
    }
    setSelectedPatientId(initialPatientId);
    loadData(initialPatientId);
    setIsLoaded(true);
  }, []);

  // ============================================================
  // Helpers
  // ============================================================

  const formatDate = (isoDate: string): string => {
    try {
      const d = new Date(isoDate);
      return d.toLocaleDateString('vi-VN', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return isoDate.substring(0, 10);
    }
  };

  const formatDateShort = (isoDate: string): string => {
    try {
      const d = new Date(isoDate);
      return d.toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
      });
    } catch {
      return isoDate.substring(5, 10);
    }
  };

  const formatTime = (seconds: number): string => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return m > 0 ? `${m}p ${s}s` : `${s}s`;
  };

  const formatTimeFull = (ms: number): string => {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const getQualityClass = (ratio: number | null): string => {
    if (ratio === null) return '';
    if (ratio >= 70) return 'quality-good';
    if (ratio >= 40) return 'quality-medium';
    return 'quality-low';
  };

  const getQualityLabel = (ratio: number | null): string => {
    if (ratio === null) return '—';
    if (ratio >= 80) return 'Rất tốt';
    if (ratio >= 60) return 'Tốt';
    if (ratio >= 40) return 'Khá';
    return 'Cần cải thiện';
  };

  const getExerciseIcon = (exerciseId: string): string => {
    return EXERCISES[exerciseId as keyof typeof EXERCISES]?.icon ?? '🏋️';
  };

  const isToday = (dateStr: string): boolean => {
    return dateStr === new Date().toISOString().substring(0, 10);
  };

  const isYesterday = (dateStr: string): boolean => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    return dateStr === yesterday.toISOString().substring(0, 10);
  };

  const getDateGroupLabel = (dateKey: string): string => {
    if (isToday(dateKey)) return 'Hôm nay';
    if (isYesterday(dateKey)) return 'Hôm qua';
    return formatDate(dateKey + 'T00:00:00');
  };

  // ============================================================
  // Handlers
  // ============================================================

  const handleViewDetail = (id: string) => {
    const session = getFullSession(id);
    if (session) {
      setSelectedSession(session);
    }
  };

  const handleDelete = (id: string) => {
    deleteHistoryEntry(id);
    loadData();
    setShowDeleteConfirm(null);
    if (selectedSession?.id === id) {
      setSelectedSession(null);
    }
  };

  const handleClearAll = () => {
    clearAllHistory();
    loadData();
    setShowClearConfirm(false);
    setSelectedSession(null);
  };

  // ============================================================
  // Render — Session Detail Modal
  // ============================================================

  if (selectedSession) {
    const s = selectedSession;
    const qualityClass = s.qualityRatio !== null
      ? s.qualityRatio >= 70 ? 'quality-good' : s.qualityRatio >= 40 ? 'quality-medium' : 'quality-low'
      : '';

    return (
      <div className="page">
        <div className="container page-content">
          <button className="back-nav" onClick={() => setSelectedSession(null)}>
            ← Quay lại lịch sử
          </button>

          <div className="summary-header">
            <div className="summary-icon">{getExerciseIcon(s.exerciseId)}</div>
            <h1>{s.exerciseName}</h1>
            <p className="text-muted">{formatDate(s.createdAt)}</p>
          </div>

          {/* Quality ratio */}
          <div className="card summary-quality">
            <div className={`summary-quality-value ${qualityClass}`}>
              {s.qualityRatio !== null
                ? `${Math.round(s.qualityRatio)}%`
                : 'Chưa đủ dữ liệu'}
            </div>
            <div className="text-muted" style={{ fontSize: 'var(--font-size-sm)' }}>
              {s.qualityRatio !== null
                ? `${getQualityLabel(s.qualityRatio)} — Tỷ lệ đạt tiêu chí cơ bản`
                : 'Không có repetition được đánh giá'}
            </div>
          </div>

          {/* Stats */}
          <div className="summary-grid">
            <div className="card summary-stat">
              <div className="summary-stat-value">{s.totalReps}</div>
              <div className="summary-stat-label">Tổng lần tập</div>
            </div>
            <div className="card summary-stat">
              <div className="summary-stat-value">{s.goodReps}</div>
              <div className="summary-stat-label">Lần đạt tiêu chí</div>
            </div>
            <div className="card summary-stat">
              <div className="summary-stat-value">{formatTimeFull(s.activeDuration)}</div>
              <div className="summary-stat-label">Thời gian tập</div>
            </div>
            <div className="card summary-stat">
              <div className="summary-stat-value">{formatTimeFull(s.totalDuration)}</div>
              <div className="summary-stat-label">Tổng thời gian</div>
            </div>
          </div>

          {/* Repetitions detail */}
          {s.repetitions && s.repetitions.length > 0 && (
            <div className="card" style={{ marginTop: 'var(--space-4)' }}>
              <h3>📊 Chi tiết từng lần tập</h3>
              <div className="history-reps-list">
                {s.repetitions.map((rep, idx) => (
                  <div key={idx} className="history-rep-item">
                    <div className="history-rep-number">
                      <span className={`history-rep-badge ${rep.meetsBasicCriteria ? 'rep-good' : 'rep-bad'}`}>
                        {rep.repNumber}
                      </span>
                    </div>
                    <div className="history-rep-info">
                      <div className="history-rep-status">
                        {rep.meetsBasicCriteria ? '✅ Đạt tiêu chí' : '⚠️ Chưa đạt'}
                      </div>
                      <div className="history-rep-duration">
                        {(rep.duration / 1000).toFixed(1)}s
                      </div>
                    </div>
                    {rep.feedback.length > 0 && (
                      <div className="history-rep-feedback">
                        {rep.feedback.map((fb, fi) => (
                          <span key={fi} className="history-rep-feedback-tag">{fb}</span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Warnings */}
          {s.warnings.length > 0 && (
            <div className="card summary-warnings" style={{ marginTop: 'var(--space-4)' }}>
              <h3>⚠️ Lưu ý thường gặp</h3>
              {s.warnings.map((warning, idx) => (
                <div key={idx} className="summary-warning-item">
                  <span>⚠️</span>
                  <span>{warning}</span>
                </div>
              ))}
            </div>
          )}

          <div className="summary-disclaimer">
            📋 Kết quả trên chỉ mang tính tham khảo, được ước tính từ camera RGB.
            Không phải đánh giá y khoa hoặc kết luận về chất lượng vận động.
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)', marginTop: 'var(--space-6)' }}>
            <button
              className="btn btn-primary btn-full"
              onClick={() => router.push(`/workout/${s.exerciseId}`)}
            >
              🔄 Tập lại bài này
            </button>
            <button
              className="btn btn-secondary btn-full"
              onClick={() => setSelectedSession(null)}
            >
              📋 Quay lại lịch sử
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ============================================================
  // Render — Loading
  // ============================================================

  if (!isLoaded) {
    return (
      <div className="page">
        <div className="container page-content">
          <div className="loading-screen">
            <div className="spinner"></div>
            <div className="loading-text">Đang tải lịch sử...</div>
          </div>
        </div>
      </div>
    );
  }

  // ============================================================
  // Render — Empty State
  // ============================================================

  if (entries.length === 0) {
    return (
      <div className="page">
        <HeaderNav />
        <div className="container page-content">
          <button className="back-nav" onClick={() => router.push('/')}>
            ← Trang chủ
          </button>

          <h1>📊 Lịch sử tập luyện</h1>

          <div className="history-empty">
            <div className="history-empty-icon">🏃</div>
            <h2>Chưa có buổi tập nào</h2>
            <p className="text-muted">
              Bắt đầu tập luyện để xem lịch sử và theo dõi tiến trình của bạn.
            </p>
            <button
              className="btn btn-primary btn-full"
              onClick={() => router.push('/exercises')}
              style={{ marginTop: 'var(--space-6)' }}
            >
              🏋️ Bắt đầu tập luyện
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ============================================================
  // Render — History List
  // ============================================================

  const grouped = groupByDate(entries);
  const dateKeys = Array.from(grouped.keys());

  return (
    <div className="page">
      <HeaderNav />
      <div className="container page-content">
        <button className="back-nav" onClick={() => router.push('/')}>
          ← Trang chủ
        </button>

        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 'var(--space-3)',
          marginBottom: 'var(--space-3)',
        }}>
          <h1 style={{ margin: 0 }}>📊 Lịch sử tập luyện</h1>
          <button
            className="btn btn-secondary"
            style={{
              padding: 'var(--space-2) var(--space-4)',
              fontSize: 'var(--font-size-sm)',
              background: 'rgba(2, 132, 199, 0.15)',
              borderColor: 'rgba(2, 132, 199, 0.4)',
              color: '#38bdf8',
              fontWeight: 600,
              cursor: 'pointer',
            }}
            onClick={handleOpenReport}
          >
            🖨️ Xuất báo cáo y tế (In / PDF)
          </button>
        </div>

        {/* Admin Patient Filter Pills */}
        {currentUserRole === 'admin' && (
          <div className="patient-filter-bar">
            <button
              type="button"
              className={`patient-pill ${selectedPatientId === 'all' ? 'active' : ''}`}
              onClick={() => handleSelectPatientFilter('all')}
            >
              👥 Tất cả bệnh nhân
            </button>
            {patientsList.map((p) => (
              <button
                key={p.id}
                type="button"
                className={`patient-pill ${selectedPatientId === p.id ? 'active' : ''}`}
                onClick={() => handleSelectPatientFilter(p.id)}
              >
                <span>{p.avatarIcon || '👤'}</span>
                <span>{p.name}</span>
              </button>
            ))}
          </div>
        )}

        {/* Selected Patient Banner */}
        {activePatientUser && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '12px',
            padding: 'var(--space-3) var(--space-4)',
            background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.12), rgba(59, 130, 246, 0.15))',
            border: '1px solid rgba(6, 182, 212, 0.35)',
            borderRadius: 'var(--radius-lg)',
            marginBottom: 'var(--space-4)',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ fontSize: '2rem' }}>{activePatientUser.avatarIcon || '👤'}</div>
              <div>
                <div style={{ fontWeight: 700, fontSize: 'var(--font-size-base)', color: 'var(--color-text-primary)' }}>
                  Hồ sơ: {activePatientUser.name} ({activePatientUser.age} tuổi)
                </div>
                <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
                  {activePatientUser.condition || 'Phục hồi chức năng'} • KTV/Bác sĩ: {activePatientUser.therapist || 'Khoa PHCN'}
                </div>
              </div>
            </div>
            {activePatientUser.prescribedExercises && activePatientUser.prescribedExercises.length > 0 && (
              <span className="prescribed-badge">
                ⭐ Chỉ định {activePatientUser.prescribedExercises.length} bài ({activePatientUser.dailyRepGoal || 15} lần/ngày)
              </span>
            )}
          </div>
        )}

        {/* Streak Banner */}
        {streak > 0 && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-3)',
            padding: 'var(--space-3) var(--space-4)',
            background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(239, 68, 68, 0.15))',
            border: '1px solid rgba(245, 158, 11, 0.4)',
            borderRadius: 'var(--radius-lg)',
            marginBottom: 'var(--space-4)',
          }}>
            <span style={{ fontSize: '1.5rem' }}>🔥</span>
            <div>
              <div style={{ fontWeight: 'bold', color: '#fbbf24', fontSize: 'var(--font-size-base)' }}>
                Chuỗi tập luyện: {streak} ngày liên tiếp!
              </div>
              <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
                Tuyệt vời! Hãy tiếp tục duy trì thói quen vận động mỗi ngày.
              </div>
            </div>
          </div>
        )}

        {/* Weekly Stats Card */}
        {weeklyStats && weeklyStats.totalSessions > 0 && (
          <div className="card history-weekly-card">
            <div className="history-weekly-header">
              <span className="history-weekly-title">📅 Tuần này</span>
              <span className="history-weekly-sessions">
                {weeklyStats.totalSessions} buổi
              </span>
            </div>
            <div className="history-weekly-stats">
              <div className="history-weekly-stat">
                <div className="history-weekly-stat-value">{weeklyStats.totalReps}</div>
                <div className="history-weekly-stat-label">Tổng lần</div>
              </div>
              <div className="history-weekly-stat">
                <div className="history-weekly-stat-value">{weeklyStats.totalGoodReps}</div>
                <div className="history-weekly-stat-label">Đạt tiêu chí</div>
              </div>
              <div className="history-weekly-stat">
                <div className="history-weekly-stat-value">
                  {weeklyStats.averageQuality !== null
                    ? `${Math.round(weeklyStats.averageQuality)}%`
                    : '—'}
                </div>
                <div className="history-weekly-stat-label">Chất lượng</div>
              </div>
              <div className="history-weekly-stat">
                <div className="history-weekly-stat-value">{weeklyStats.totalDurationMinutes}p</div>
                <div className="history-weekly-stat-label">Thời gian</div>
              </div>
            </div>
          </div>
        )}

        {/* Grouped History */}
        <div className="history-list">
          {dateKeys.map((dateKey) => {
            const dayEntries = grouped.get(dateKey)!;
            return (
              <div key={dateKey} className="history-date-group">
                <div className="history-date-label">{getDateGroupLabel(dateKey)}</div>
                {dayEntries.map((entry) => (
                  <div key={entry.id} className="card card-interactive history-item" onClick={() => handleViewDetail(entry.id)}>
                    <div className="history-item-left">
                      <div className="history-item-icon">{getExerciseIcon(entry.exerciseId)}</div>
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
                          <span className="history-item-name">{entry.exerciseName}</span>
                          {(selectedPatientId === 'all' || currentUserRole === 'admin') && (
                            <span className="patient-identity-badge">
                              👤 {entry.patientName || 'Bác Nguyễn Văn An'}
                            </span>
                          )}
                        </div>
                        <div className="history-item-date">
                          {new Date(entry.date).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}
                          {' · '}
                          {formatTime(entry.durationSeconds)}
                        </div>
                      </div>
                    </div>
                    <div className="history-item-stats">
                      <div className="history-item-reps">{entry.totalReps} lần</div>
                      <div className={`history-item-quality ${getQualityClass(entry.qualityRatio)}`}>
                        {entry.qualityRatio !== null ? `${Math.round(entry.qualityRatio)}%` : '—'}
                      </div>
                    </div>
                    {/* Swipe-to-delete is not practical on desktop; use long-press/click-hold indicator */}
                    {showDeleteConfirm === entry.id && (
                      <div className="history-delete-confirm" onClick={(e) => e.stopPropagation()}>
                        <span>Xóa buổi tập này?</span>
                        <button className="btn btn-danger" style={{ padding: 'var(--space-2) var(--space-4)', fontSize: 'var(--font-size-sm)', minHeight: 'auto' }} onClick={() => handleDelete(entry.id)}>
                          Xóa
                        </button>
                        <button className="btn btn-secondary" style={{ padding: 'var(--space-2) var(--space-4)', fontSize: 'var(--font-size-sm)', minHeight: 'auto' }} onClick={() => setShowDeleteConfirm(null)}>
                          Hủy
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            );
          })}
        </div>

        {/* Clear all */}
        {entries.length > 0 && (
          <div style={{ marginTop: 'var(--space-8)', textAlign: 'center' }}>
            {!showClearConfirm ? (
              <button
                className="btn btn-secondary"
                style={{ fontSize: 'var(--font-size-sm)', opacity: 0.7, padding: 'var(--space-3) var(--space-6)' }}
                onClick={() => setShowClearConfirm(true)}
              >
                🗑️ Xóa toàn bộ lịch sử
              </button>
            ) : (
              <div className="history-clear-confirm">
                <p style={{ marginBottom: 'var(--space-3)', color: 'var(--color-accent-danger)' }}>
                  ⚠️ Xóa toàn bộ {entries.length} buổi tập? Không thể hoàn tác.
                </p>
                <div style={{ display: 'flex', gap: 'var(--space-3)', justifyContent: 'center' }}>
                  <button className="btn btn-danger" onClick={handleClearAll}>
                    Xóa tất cả
                  </button>
                  <button className="btn btn-secondary" onClick={() => setShowClearConfirm(false)}>
                    Hủy
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Bottom nav */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)', marginTop: 'var(--space-6)' }}>
          <button
            className="btn btn-primary btn-full"
            onClick={() => router.push('/exercises')}
          >
            🏋️ Tập luyện thêm
          </button>
        </div>

        {/* Medical / Clinical Report Modal */}
        {showReportModal && (
          <div className="report-modal-overlay" onClick={() => setShowReportModal(false)}>
            <div className="report-modal-content" onClick={(e) => e.stopPropagation()}>
              {/* Header */}
              <div className="report-header">
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <span style={{ fontSize: '1.4rem' }}>🏥</span>
                    <span style={{ fontWeight: 800, color: '#0284c7', letterSpacing: '1px', fontSize: '0.85rem' }}>
                      MOTIONIQ REHABILITATION KINEMATICS
                    </span>
                  </div>
                  <h2 className="report-title-main">Báo cáo phục hồi chức năng vận động</h2>
                  <p className="report-subtitle">
                    Theo dõi & Đánh giá Động học Khớp bằng AI Thị giác Máy tính tại nhà
                  </p>
                </div>
                <div style={{ textAlign: 'right', fontSize: '0.8rem', color: '#64748b' }}>
                  <div><strong>Mã hồ sơ:</strong> MIQ-{new Date().toISOString().substring(2, 10).replace(/-/g, '')}</div>
                  <div><strong>Ngày xuất:</strong> {new Date().toLocaleDateString('vi-VN')}</div>
                  <div style={{ color: '#16a34a', fontWeight: 600 }}>● Dữ liệu On-Device AI</div>
                </div>
              </div>

              {/* Patient Info */}
              <div className="report-meta-box">
                {isEditingProfile ? (
                  <div style={{ gridColumn: '1 / -1', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <input
                        type="text"
                        placeholder="Họ tên người bệnh"
                        value={editName}
                        onChange={(e) => setEditName(e.target.value)}
                        style={{ flex: 2, padding: '6px 10px', borderRadius: '4px', border: '1px solid #cbd5e1', color: '#0f172a' }}
                      />
                      <input
                        type="number"
                        placeholder="Tuổi"
                        value={editAge}
                        onChange={(e) => setEditAge(parseInt(e.target.value, 10) || 68)}
                        style={{ width: '80px', padding: '6px 10px', borderRadius: '4px', border: '1px solid #cbd5e1', color: '#0f172a' }}
                      />
                    </div>
                    <input
                      type="text"
                      placeholder="Chẩn đoán / Mục tiêu tập"
                      value={editCondition}
                      onChange={(e) => setEditCondition(e.target.value)}
                      style={{ padding: '6px 10px', borderRadius: '4px', border: '1px solid #cbd5e1', color: '#0f172a' }}
                    />
                    <input
                      type="text"
                      placeholder="Bác sĩ / KTV phụ trách"
                      value={editTherapist}
                      onChange={(e) => setEditTherapist(e.target.value)}
                      style={{ padding: '6px 10px', borderRadius: '4px', border: '1px solid #cbd5e1', color: '#0f172a' }}
                    />
                    <div style={{ display: 'flex', gap: '8px', marginTop: '4px' }}>
                      <button
                        onClick={handleSaveProfile}
                        style={{ padding: '4px 12px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem' }}
                      >
                        Lưu thông tin
                      </button>
                      <button
                        onClick={() => setIsEditingProfile(false)}
                        style={{ padding: '4px 12px', background: '#e2e8f0', color: '#334155', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem' }}
                      >
                        Hủy
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="report-meta-item">
                      <strong>Người bệnh:</strong> {patientProfile.name} ({patientProfile.age} tuổi)
                    </div>
                    <div className="report-meta-item">
                      <strong>Chuyên viên phụ trách:</strong> {patientProfile.therapist}
                    </div>
                    <div className="report-meta-item" style={{ gridColumn: '1 / -1' }}>
                      <strong>Chỉ định / Mục tiêu:</strong> {patientProfile.condition}
                      <button
                        className="report-no-print"
                        onClick={() => setIsEditingProfile(true)}
                        style={{ marginLeft: '12px', background: 'none', border: 'none', color: '#0284c7', cursor: 'pointer', fontSize: '0.8rem', textDecoration: 'underline' }}
                      >
                        ✏️ Sửa thông tin
                      </button>
                    </div>
                  </>
                )}
              </div>

              {/* Aggregate Statistics */}
              <div className="report-section-title">1. Tổng hợp mức độ tuân thủ & vận động (7 ngày gần nhất)</div>
              <table className="report-table">
                <thead>
                  <tr>
                    <th>Số buổi tập</th>
                    <th>Tổng lượt tập (Reps)</th>
                    <th>Lượt đạt chuẩn</th>
                    <th>Tỷ lệ chất lượng</th>
                    <th>Thời lượng vận động</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>{weeklyStats?.totalSessions ?? 0} buổi</strong></td>
                    <td>{weeklyStats?.totalReps ?? 0} lần</td>
                    <td>{weeklyStats?.totalGoodReps ?? 0} lần</td>
                    <td>
                      <span className={
                        (weeklyStats?.averageQuality ?? 0) >= 70 ? 'report-badge-good' :
                        (weeklyStats?.averageQuality ?? 0) >= 40 ? 'report-badge-medium' :
                        'report-badge-low'
                      }>
                        {weeklyStats?.averageQuality !== null ? `${Math.round(weeklyStats?.averageQuality ?? 0)}%` : '—'}
                      </span>
                    </td>
                    <td>{weeklyStats?.totalDurationMinutes ?? 0} phút</td>
                  </tr>
                </tbody>
              </table>

              {/* Exercise Specific Breakdown */}
              <div className="report-section-title">2. Chi tiết động học & Tầm vận động khớp (Kinematics)</div>
              <table className="report-table">
                <thead>
                  <tr>
                    <th>Bài tập</th>
                    <th>Số lần</th>
                    <th>Đạt chuẩn</th>
                    <th>Tiêu chuẩn góc khớp (ROM)</th>
                    <th>Đánh giá vận động</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(getExerciseClinicalData()).map(([id, data]) => {
                    const exInfo = EXERCISES[id as keyof typeof EXERCISES];
                    const qRate = data.totalReps > 0 ? Math.round((data.goodReps / data.totalReps) * 100) : 0;
                    return (
                      <tr key={id}>
                        <td>
                          <strong>{exInfo?.name ?? id}</strong>
                          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{exInfo?.description}</div>
                        </td>
                        <td>{data.totalReps}</td>
                        <td>{data.goodReps} ({qRate}%)</td>
                        <td style={{ fontSize: '0.8rem' }}>
                          {id === 'sit-to-stand' && 'Gối gập ≥ 90° khi ngồi, duỗi ≥ 165° khi đứng [UI-PRMD m05 & KIMORE Es4]'}
                          {id === 'squat' && 'Gối gập 90° - 110°, thân người nghiêng < 35° [UI-PRMD m01 & KIMORE Es5]'}
                          {id === 'shoulder-raise' && 'Nâng vai 85° - 110°, đối xứng hai bên [EHE LA & KIMORE Es1]'}
                          {id === 'side-leg-raise' && 'Giạng hông 25° - 65°, giữ lưng thẳng [UI-PRMD m06]'}
                        </td>
                        <td>
                          <span className={qRate >= 70 ? 'report-badge-good' : qRate >= 40 ? 'report-badge-medium' : 'report-badge-low'}>
                            {qRate >= 80 ? 'Rất tốt' : qRate >= 60 ? 'Tốt' : qRate >= 40 ? 'Khá' : 'Cần hỗ trợ'}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              {/* Detected Posture Faults & Warnings */}
              <div className="report-section-title">3. Lưu ý sai lệch tư thế ghi nhận (Compensation Patterns)</div>
              <div style={{ background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '4px', padding: '10px 14px', marginBottom: '14px', fontSize: '0.85rem' }}>
                {(() => {
                  const allWarnings: string[] = [];
                  const data = getExerciseClinicalData();
                  for (const key of Object.keys(data)) {
                    data[key].warnings.forEach(w => {
                      if (!allWarnings.includes(w)) allWarnings.push(w);
                    });
                  }
                  if (allWarnings.length === 0) {
                    return <div style={{ color: '#16a34a' }}>✅ Không ghi nhận sai lệch tư thế nghiêm trọng trong các buổi tập gần đây.</div>;
                  }
                  return (
                    <ul style={{ margin: '0', paddingLeft: '18px', color: '#b45309' }}>
                      {allWarnings.map((w, idx) => (
                        <li key={idx} style={{ marginBottom: '4px' }}>{w}</li>
                      ))}
                    </ul>
                  );
                })()}
              </div>

              {/* Clinical Assessment & Doctor Notes */}
              <div className="report-section-title">4. Đánh giá chuyên môn & Kế hoạch phục hồi</div>
              <div style={{ background: '#f1f5f9', borderLeft: '4px solid #0284c7', padding: '10px 14px', fontSize: '0.85rem', lineHeight: 1.6, marginBottom: '16px' }}>
                {(() => {
                  const avg = weeklyStats?.averageQuality ?? 0;
                  if (avg >= 80) {
                    return 'Bệnh nhân có khả năng kiểm soát thăng bằng và sức mạnh cơ chi dưới rất tốt. Biên độ vận động đạt mục tiêu đề ra. Khuyến nghị duy trì tần suất 3-5 buổi/tuần và có thể nâng mục tiêu số lần tập.';
                  } else if (avg >= 50) {
                    return 'Bệnh nhân đạt mức độ phục hồi khá. Một số lần tập còn thiếu biên độ hoặc mất thăng bằng nhẹ. Khuyến nghị chú ý nhịp thở, giữ vững gót chân khi đứng dậy và tập ở tốc độ chậm rãi.';
                  } else {
                    return 'Bệnh nhân cần thêm thời gian thích nghi và hỗ trợ. Khuyến nghị tập luyện dưới sự giám sát của người nhà hoặc chuyên viên, sử dụng ghế có tay vịn để đảm bảo an toàn tuyệt đối.';
                  }
                })()}
              </div>

              {/* Disclaimer */}
              <div className="report-disclaimer-box">
                ⚠️ <strong>LƯU Ý Y KHOA:</strong> Dữ liệu trên được phân tích tự động bằng trí tuệ nhân tạo (MediaPipe AI Landmarker) xử lý trực tiếp trên thiết bị (Edge AI). Báo cáo nhằm mục đích hỗ trợ theo dõi tiến trình phục hồi và tham khảo cho bác sĩ/chuyên viên VLTL, không thay thế hoàn toàn chẩn đoán lâm sàng.
              </div>

              {/* Signature section */}
              <div className="report-signature-grid">
                <div className="report-signature-col">
                  <div><strong>Người bệnh / Người giám hộ</strong></div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b' }}>(Ký và ghi rõ họ tên)</div>
                  <div className="report-signature-line"></div>
                  <div><strong>{patientProfile.name}</strong></div>
                </div>
                <div className="report-signature-col">
                  <div><strong>Bác sĩ / Kỹ thuật viên Phục hồi chức năng</strong></div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b' }}>(Ký, ghi rõ họ tên & đóng dấu)</div>
                  <div className="report-signature-line"></div>
                  <div><strong>{patientProfile.therapist}</strong></div>
                </div>
              </div>

              {/* Action Buttons (Hidden on Print) */}
              <div className="report-no-print" style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '24px', paddingTop: '16px', borderTop: '1px solid #e2e8f0' }}>
                <button
                  className="btn btn-secondary"
                  onClick={() => setShowReportModal(false)}
                  style={{ color: '#334155', background: '#f1f5f9', border: '1px solid #cbd5e1' }}
                >
                  ✕ Đóng
                </button>
                <button
                  className="btn btn-primary"
                  onClick={handlePrint}
                  style={{ background: '#0284c7', borderColor: '#0284c7', display: 'flex', alignItems: 'center', gap: '6px' }}
                >
                  🖨️ In báo cáo / Lưu file PDF
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
