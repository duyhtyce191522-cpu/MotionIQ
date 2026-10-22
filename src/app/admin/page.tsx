'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import HeaderNav from '@/components/HeaderNav';
import {
  getAuthSession,
  getAllPatients,
  createPatient,
  updatePatient,
  deletePatient,
  changeAdminPassword,
  loginAsPatient,
  PatientUser,
} from '@/features/auth/authService';
import { getHistoryEntries } from '@/features/storage/storageService';
import { EXERCISES } from '@/features/exercises/exerciseRules';
import { WorkoutHistoryEntry } from '@/types';

export default function AdminPage() {
  const router = useRouter();
  const [patients, setPatients] = useState<PatientUser[]>([]);
  const [historyEntries, setHistoryEntries] = useState<WorkoutHistoryEntry[]>([]);
  const [totalSessions, setTotalSessions] = useState(0);
  const [totalGoodReps, setTotalGoodReps] = useState(0);

  // Edit / Add Modal
  const [modalMode, setModalMode] = useState<'create' | 'edit' | null>(null);
  const [editingPatient, setEditingPatient] = useState<PatientUser | null>(null);
  const [formName, setFormName] = useState('');
  const [formAge, setFormAge] = useState(68);
  const [formGender, setFormGender] = useState<'male' | 'female' | 'other'>('male');
  const [formCondition, setFormCondition] = useState('');
  const [formTherapist, setFormTherapist] = useState('');
  const [formEmergency, setFormEmergency] = useState('115');
  const [formAvatar, setFormAvatar] = useState('👴');
  const [formPin, setFormPin] = useState('');
  const [formPrescribed, setFormPrescribed] = useState<string[]>([]);
  const [formDailyGoal, setFormDailyGoal] = useState<number>(15);

  // Password Change
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordToast, setPasswordToast] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);

  // Delete confirm
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const loadData = useCallback(() => {
    const list = getAllPatients();
    setPatients(list);

    const history = getHistoryEntries();
    setHistoryEntries(history);
    setTotalSessions(history.length);
    const goodRepsCount = history.reduce((acc, h) => acc + h.goodReps, 0);
    setTotalGoodReps(goodRepsCount);
  }, []);

  useEffect(() => {
    const session = getAuthSession();
    if (!session || session.role !== 'admin') {
      router.push('/login');
      return;
    }
    loadData();
  }, [router, loadData]);

  const openCreateModal = () => {
    setModalMode('create');
    setEditingPatient(null);
    setFormName('');
    setFormAge(65);
    setFormGender('male');
    setFormCondition('Tập phục hồi chức năng sau tai biến / tăng thăng bằng');
    setFormTherapist('BS. Khoa PHCN');
    setFormEmergency('115');
    setFormAvatar('👴');
    setFormPin('');
    setFormPrescribed(['sit-to-stand', 'squat']);
    setFormDailyGoal(15);
  };

  const openEditModal = (p: PatientUser) => {
    setModalMode('edit');
    setEditingPatient(p);
    setFormName(p.name);
    setFormAge(p.age);
    setFormGender(p.gender);
    setFormCondition(p.condition || '');
    setFormTherapist(p.therapist || '');
    setFormEmergency(p.emergencyContact || '115');
    setFormAvatar(p.avatarIcon || '👴');
    setFormPin(p.pin || '');
    setFormPrescribed(p.prescribedExercises || []);
    setFormDailyGoal(p.dailyRepGoal || 15);
  };

  const handleSavePatientModal = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName.trim()) return;

    if (modalMode === 'create') {
      createPatient({
        name: formName.trim(),
        age: formAge,
        gender: formGender,
        condition: formCondition.trim(),
        therapist: formTherapist.trim(),
        emergencyContact: formEmergency.trim(),
        avatarIcon: formAvatar,
        pin: formPin.trim() || undefined,
        prescribedExercises: formPrescribed,
        dailyRepGoal: formDailyGoal,
      });
    } else if (modalMode === 'edit' && editingPatient) {
      updatePatient(editingPatient.id, {
        name: formName.trim(),
        age: formAge,
        gender: formGender,
        condition: formCondition.trim(),
        therapist: formTherapist.trim(),
        emergencyContact: formEmergency.trim(),
        avatarIcon: formAvatar,
        pin: formPin.trim() || undefined,
        prescribedExercises: formPrescribed,
        dailyRepGoal: formDailyGoal,
      });
    }

    setModalMode(null);
    loadData();
  };

  const handleDeletePatient = (id: string) => {
    deletePatient(id);
    setDeletingId(null);
    loadData();
  };

  const handleLoginAsPatient = (patient: PatientUser) => {
    loginAsPatient(patient.id, patient.pin);
    router.push('/');
  };

  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);
    setPasswordToast(null);

    if (newPassword !== confirmPassword) {
      setPasswordError('Mật khẩu xác nhận không khớp.');
      return;
    }

    const res = changeAdminPassword(oldPassword, newPassword);
    if (res.success) {
      setPasswordToast('✅ Đã đổi mật khẩu quản trị viên thành công!');
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => setPasswordToast(null), 3500);
    } else {
      setPasswordError(res.error || 'Đổi mật khẩu thất bại.');
    }
  };

  const avatarOptions = ['👴', '👵', '🧓', '🧑', '👩', '🏃‍♂️', '🏃‍♀️'];

  return (
    <div className="page">
      <HeaderNav />
      <div className="container page-content" style={{ maxWidth: '820px' }}>
        <button className="back-nav" onClick={() => router.push('/')}>
          ← Trang chủ
        </button>

        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 'var(--space-3)',
          marginBottom: 'var(--space-6)',
        }}>
          <div>
            <h1 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>🛡️</span> Bảng điều khiển Quản trị
            </h1>
            <p className="text-muted" style={{ margin: '4px 0 0 0', fontSize: 'var(--font-size-sm)' }}>
              Quản lý danh sách bệnh nhân, cấu hình hồ sơ và bảo mật hệ thống
            </p>
          </div>

          <button
            className="btn btn-primary"
            style={{ padding: '10px 20px', fontSize: 'var(--font-size-sm)' }}
            onClick={openCreateModal}
          >
            ➕ Thêm bệnh nhân mới
          </button>
        </div>

        {/* Metric Cards Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: 'var(--space-4)',
          marginBottom: 'var(--space-8)',
        }}>
          <div className="card" style={{ padding: 'var(--space-4)', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', marginBottom: '4px' }}>👥</div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--color-accent-primary)' }}>
              {patients.length}
            </div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
              Hồ sơ người tập
            </div>
          </div>

          <div className="card" style={{ padding: 'var(--space-4)', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', marginBottom: '4px' }}>🏋️</div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--color-accent-info)' }}>
              {totalSessions}
            </div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
              Tổng buổi tập ghi nhận
            </div>
          </div>

          <div className="card" style={{ padding: 'var(--space-4)', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', marginBottom: '4px' }}>🎯</div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--color-accent-success)' }}>
              {totalGoodReps}
            </div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
              Số lần tập đạt chuẩn
            </div>
          </div>

          <div className="card" style={{ padding: 'var(--space-4)', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', marginBottom: '4px' }}>🔒</div>
            <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#10b981', marginTop: '8px' }}>
              Edge AI Offline
            </div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
              Bảo mật 100% tại chỗ
            </div>
          </div>
        </div>

        {/* Patient List Section */}
        <div style={{ marginBottom: 'var(--space-8)' }}>
          <h2 style={{ fontSize: '1.4rem', marginBottom: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>📋</span> Danh sách hồ sơ bệnh nhân ({patients.length})
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
            {patients.map((p) => (
              <div
                key={p.id}
                className="card"
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: 'var(--space-5)',
                  flexWrap: 'wrap',
                  gap: 'var(--space-4)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)', flex: 1, minWidth: '240px' }}>
                  <div style={{
                    fontSize: '2.5rem',
                    width: '64px',
                    height: '64px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%)',
                    borderRadius: 'var(--radius-full)',
                    border: '1px solid rgba(6, 182, 212, 0.3)',
                    flexShrink: 0,
                  }}>
                    {p.avatarIcon || '👤'}
                  </div>

                    <div>
                      <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--color-text-primary)' }}>
                        {p.name}
                      </div>
                      <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
                        {p.age} tuổi • {p.gender === 'male' ? 'Nam' : p.gender === 'female' ? 'Nữ' : 'Khác'} • {p.condition || 'Phục hồi chức năng'}
                      </div>
                      <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)', marginTop: '2px', display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                        <span>KTV/Bác sĩ: {p.therapist || 'Khoa PHCN'}</span>
                        <span>• SĐT: {p.emergencyContact || '115'}</span>
                        {p.pin && <span style={{ color: '#f59e0b' }}>🔒 Có PIN</span>}
                      </div>
                      <div style={{ marginTop: '6px', display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center' }}>
                        <span className="patient-identity-badge">
                          🏋️ {historyEntries.filter(h => h.patientId === p.id || (!h.patientId && p.id === 'patient-1')).length} buổi tập
                        </span>
                        {p.prescribedExercises && p.prescribedExercises.length > 0 && (
                          <span className="prescribed-badge" style={{ fontSize: '0.72rem', padding: '2px 8px' }}>
                            ⭐ Chỉ định {p.prescribedExercises.length} bài ({p.dailyRepGoal || 15} lần/ngày)
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)', flexWrap: 'wrap' }}>
                    <button
                      type="button"
                      className="btn btn-secondary"
                      style={{ padding: '6px 12px', fontSize: 'var(--font-size-xs)', display: 'inline-flex', alignItems: 'center', gap: '4px' }}
                      onClick={() => handleLoginAsPatient(p)}
                      title="Chuyển sang chế độ tập luyện với hồ sơ này"
                    >
                      🏃 Vào tập
                    </button>

                    <button
                      type="button"
                      className="btn btn-secondary"
                      style={{ padding: '6px 12px', fontSize: 'var(--font-size-xs)', display: 'inline-flex', alignItems: 'center', gap: '4px', borderColor: 'rgba(56, 189, 248, 0.4)', color: '#38bdf8' }}
                      onClick={() => router.push(`/history?patientId=${p.id}`)}
                      title="Xem lịch sử và xuất báo cáo lâm sàng cho bệnh nhân này"
                    >
                      📊 Báo cáo / Lịch sử
                    </button>

                    <button
                      type="button"
                      className="btn btn-secondary"
                      style={{ padding: '6px 12px', fontSize: 'var(--font-size-xs)' }}
                      onClick={() => openEditModal(p)}
                      title="Chỉnh sửa thông tin bệnh nhân"
                    >
                      ✏️ Sửa
                    </button>

                    <button
                      type="button"
                      className="btn btn-danger"
                      style={{ padding: '6px 12px', fontSize: 'var(--font-size-xs)' }}
                      onClick={() => setDeletingId(p.id)}
                      title="Xóa hồ sơ bệnh nhân"
                    >
                      🗑️ Xóa
                    </button>
                  </div>
                </div>
              ))}
            </div>
        </div>

        {/* Change Admin Password Card */}
        <div className="card" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: 'var(--space-3)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>🔑</span> Đổi mật khẩu Quản trị viên
          </h2>
          <p className="text-muted" style={{ fontSize: 'var(--font-size-xs)', marginBottom: 'var(--space-4)' }}>
            Mật khẩu mới sẽ được lưu cục bộ trên thiết bị của bạn.
          </p>

          {passwordToast && (
            <div style={{
              padding: '10px 14px',
              background: 'rgba(16, 185, 129, 0.15)',
              border: '1px solid #10b981',
              color: '#34d399',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-size-sm)',
              marginBottom: 'var(--space-4)',
            }}>
              {passwordToast}
            </div>
          )}

          {passwordError && (
            <div style={{
              padding: '10px 14px',
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid #ef4444',
              color: '#f87171',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-size-sm)',
              marginBottom: 'var(--space-4)',
            }}>
              ⚠️ {passwordError}
            </div>
          )}

          <form onSubmit={handleChangePassword} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
            <div>
              <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: '4px' }}>
                Mật khẩu hiện tại
              </label>
              <input
                type="password"
                className="input-field"
                placeholder="Nhập mật khẩu đang dùng (mặc định admin123)"
                value={oldPassword}
                required
                onChange={(e) => setOldPassword(e.target.value)}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)' }}>
              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: '4px' }}>
                  Mật khẩu mới
                </label>
                <input
                  type="password"
                  className="input-field"
                  placeholder="Tối thiểu 4 ký tự"
                  value={newPassword}
                  required
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: '4px' }}>
                  Xác nhận mật khẩu mới
                </label>
                <input
                  type="password"
                  className="input-field"
                  placeholder="Nhập lại mật khẩu mới"
                  value={confirmPassword}
                  required
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              style={{ alignSelf: 'flex-start', marginTop: 'var(--space-2)' }}
            >
              🔒 Cập nhật mật khẩu Admin
            </button>
          </form>
        </div>
      </div>

      {/* Create / Edit Patient Modal */}
      {modalMode && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: 'var(--space-4)',
          overflowY: 'auto',
        }}>
          <form
            onSubmit={handleSavePatientModal}
            className="card"
            style={{
              maxWidth: '520px',
              width: '100%',
              padding: 'var(--space-6)',
              animation: 'popIn 0.3s ease',
            }}
          >
            <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 'var(--space-4)' }}>
              {modalMode === 'create' ? '➕ Thêm hồ sơ bệnh nhân mới' : '✏️ Chỉnh sửa hồ sơ bệnh nhân'}
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                  Họ và tên / Tên thân mật *
                </label>
                <input
                  type="text"
                  className="input-field"
                  value={formName}
                  required
                  autoFocus
                  onChange={(e) => setFormName(e.target.value)}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)' }}>
                <div>
                  <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                    Tuổi
                  </label>
                  <input
                    type="number"
                    min={10}
                    max={120}
                    className="input-field"
                    value={formAge}
                    onChange={(e) => setFormAge(parseInt(e.target.value, 10) || 60)}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                    Giới tính
                  </label>
                  <select
                    className="select-field"
                    value={formGender}
                    onChange={(e) => setFormGender(e.target.value as any)}
                  >
                    <option value="male">Nam</option>
                    <option value="female">Nữ</option>
                    <option value="other">Khác</option>
                  </select>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                  Tình trạng bệnh lý / Mục tiêu điều trị
                </label>
                <input
                  type="text"
                  className="input-field"
                  value={formCondition}
                  onChange={(e) => setFormCondition(e.target.value)}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)' }}>
                <div>
                  <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                    Bác sĩ / Kỹ thuật viên
                  </label>
                  <input
                    type="text"
                    className="input-field"
                    value={formTherapist}
                    onChange={(e) => setFormTherapist(e.target.value)}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                    Số điện thoại khẩn cấp
                  </label>
                  <input
                    type="tel"
                    className="input-field"
                    value={formEmergency}
                    onChange={(e) => setFormEmergency(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                  Biểu tượng đại diện
                </label>
                <div style={{ display: 'flex', gap: '8px' }}>
                  {avatarOptions.map((icon) => (
                    <button
                      key={icon}
                      type="button"
                      onClick={() => setFormAvatar(icon)}
                      style={{
                        fontSize: '1.5rem',
                        padding: '6px 10px',
                        borderRadius: 'var(--radius-md)',
                        border: formAvatar === icon ? '2px solid var(--color-accent-primary)' : '1px solid var(--color-border)',
                        background: formAvatar === icon ? 'rgba(6, 182, 212, 0.25)' : 'rgba(255, 255, 255, 0.05)',
                        cursor: 'pointer',
                        transform: formAvatar === icon ? 'scale(1.15)' : 'scale(1)',
                        transition: 'all 0.2s',
                      }}
                    >
                      {icon}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                  Mã PIN 4 số (Để trống nếu không cài mã bảo mật)
                </label>
                <input
                  type="password"
                  maxLength={4}
                  className="input-field"
                  placeholder="Tùy chọn mã PIN bảo mật"
                  value={formPin}
                  onChange={(e) => setFormPin(e.target.value)}
                />
              </div>

              {/* Prescribed Exercises Selection */}
              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '6px' }}>
                  ⭐ Bài tập Bác sĩ / KTV chỉ định cho bệnh nhân:
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                  {Object.values(EXERCISES).map((ex) => {
                    const isSelected = formPrescribed.includes(ex.id);
                    return (
                      <button
                        key={ex.id}
                        type="button"
                        onClick={() => {
                          if (isSelected) {
                            setFormPrescribed(formPrescribed.filter((id) => id !== ex.id));
                          } else {
                            setFormPrescribed([...formPrescribed, ex.id]);
                          }
                        }}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                          padding: '6px 10px',
                          fontSize: 'var(--font-size-xs)',
                          textAlign: 'left',
                          borderRadius: 'var(--radius-md)',
                          border: isSelected ? '1px solid #f59e0b' : '1px solid var(--color-border)',
                          background: isSelected ? 'rgba(245, 158, 11, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                          color: isSelected ? '#fbbf24' : 'var(--color-text-secondary)',
                          cursor: 'pointer',
                          transition: 'all 0.15s ease',
                        }}
                      >
                        <span>{isSelected ? '✅' : '⚪'}</span>
                        <span>{ex.icon}</span>
                        <span style={{ fontWeight: isSelected ? 600 : 400, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {ex.name}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Daily Rep Goal */}
              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                  🎯 Mục tiêu số lần tập mỗi ngày
                </label>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                  {[10, 15, 20, 30].map((goal) => (
                    <button
                      key={goal}
                      type="button"
                      className={`goal-pill ${formDailyGoal === goal ? 'active' : ''}`}
                      onClick={() => setFormDailyGoal(goal)}
                    >
                      {goal} lần
                    </button>
                  ))}
                  <input
                    type="number"
                    min={5}
                    max={100}
                    style={{ width: '80px', padding: '6px 10px' }}
                    className="input-field"
                    value={formDailyGoal}
                    onChange={(e) => setFormDailyGoal(parseInt(e.target.value, 10) || 15)}
                  />
                </div>
              </div>

              <div style={{ display: 'flex', gap: 'var(--space-2)', marginTop: 'var(--space-3)' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  style={{ flex: 1 }}
                  onClick={() => setModalMode(null)}
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  style={{ flex: 1 }}
                >
                  Lưu hồ sơ
                </button>
              </div>
            </div>
          </form>
        </div>
      )}

      {/* Delete Confirm Modal */}
      {deletingId && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: 'var(--space-4)',
        }}>
          <div className="card" style={{ maxWidth: '400px', width: '100%', padding: 'var(--space-6)', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: 'var(--space-2)' }}>🗑️</div>
            <h3 style={{ fontSize: '1.2rem', marginBottom: 'var(--space-2)' }}>Xác nhận xóa hồ sơ</h3>
            <p className="text-muted" style={{ fontSize: 'var(--font-size-sm)', marginBottom: 'var(--space-4)' }}>
              Bạn có chắc chắn muốn xóa hồ sơ bệnh nhân này không? Hành động này không thể hoàn tác.
            </p>
            <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
              <button
                type="button"
                className="btn btn-secondary"
                style={{ flex: 1 }}
                onClick={() => setDeletingId(null)}
              >
                Hủy
              </button>
              <button
                type="button"
                className="btn btn-danger"
                style={{ flex: 1 }}
                onClick={() => handleDeletePatient(deletingId)}
              >
                Xóa vĩnh viễn
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
