'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  getAllPatients,
  loginAsPatient,
  loginAsAdmin,
  createPatient,
  PatientUser,
  getAuthSession,
} from '@/features/auth/authService';

export default function LoginPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'patient' | 'admin'>('patient');
  const [patients, setPatients] = useState<PatientUser[]>([]);
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  // Admin form
  const [adminUsername, setAdminUsername] = useState('admin');
  const [adminPassword, setAdminPassword] = useState('');
  const [adminError, setAdminError] = useState<string | null>(null);
  const [isShaking, setIsShaking] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // New patient registration form
  const [showAddPatient, setShowAddPatient] = useState(false);
  const [newName, setNewName] = useState('');
  const [newAge, setNewAge] = useState(65);
  const [newGender, setNewGender] = useState<'male' | 'female' | 'other'>('male');
  const [newCondition, setNewCondition] = useState('');
  const [newAvatar, setNewAvatar] = useState('👴');
  const [newPin, setNewPin] = useState('');

  // PIN modal prompt for protected patient profile
  const [pinModalPatient, setPinModalPatient] = useState<PatientUser | null>(null);
  const [enteredPin, setEnteredPin] = useState('');
  const [pinError, setPinError] = useState<string | null>(null);

  useEffect(() => {
    // If already logged in, redirect to respective home
    const session = getAuthSession();
    if (session) {
      if (session.role === 'admin') {
        router.push('/admin');
      } else {
        router.push('/');
      }
      return;
    }

    setPatients(getAllPatients());

    const savedTheme = (localStorage.getItem('motioniq_theme') as 'dark' | 'light') || 'dark';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, [router]);

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    localStorage.setItem('motioniq_theme', nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  const handlePatientSelect = (p: PatientUser) => {
    if (p.pin && p.pin.trim() !== '') {
      setPinModalPatient(p);
      setEnteredPin('');
      setPinError(null);
    } else {
      const res = loginAsPatient(p.id);
      if (res.success) {
        router.push('/');
      }
    }
  };

  const handlePinSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!pinModalPatient) return;
    const res = loginAsPatient(pinModalPatient.id, enteredPin);
    if (res.success) {
      setPinModalPatient(null);
      router.push('/');
    } else {
      setPinError(res.error || 'Mã PIN không đúng');
    }
  };

  const handleCreatePatient = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;

    const created = createPatient({
      name: newName.trim(),
      age: newAge || 65,
      gender: newGender,
      condition: newCondition.trim() || 'Tập phục hồi chức năng cơ bản',
      avatarIcon: newAvatar,
      pin: newPin.trim() || undefined,
    });

    setPatients(getAllPatients());
    setShowAddPatient(false);

    // Auto login as the newly created patient
    loginAsPatient(created.id, created.pin);
    router.push('/');
  };

  const handleAdminSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setAdminError(null);
    const res = loginAsAdmin(adminUsername, adminPassword);
    if (res.success) {
      router.push('/admin');
    } else {
      setAdminError(res.error || 'Đăng nhập thất bại.');
      setIsShaking(true);
      setTimeout(() => setIsShaking(false), 600);
    }
  };

  const avatarOptions = ['👴', '👵', '🧓', '🧑', '👩', '🏃‍♂️', '🏃‍♀️'];

  return (
    <div className="page" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Bar with Brand & Theme Switcher */}
      <div style={{
        padding: 'var(--space-3) var(--space-4)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        maxWidth: '560px',
        width: '100%',
        margin: '0 auto',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '2rem', animation: 'bounceSlow 3s ease-in-out infinite' }}>🏃‍♂️</span>
          <span style={{
            fontSize: '1.4rem',
            fontWeight: 800,
            background: 'var(--gradient-primary)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '-0.5px',
          }}>
            MotionIQ
          </span>
        </div>

        <button
          id="theme-toggle-btn"
          type="button"
          className="theme-toggle-btn"
          onClick={toggleTheme}
          title={theme === 'dark' ? 'Chuyển sang Chế độ Sáng' : 'Chuyển sang Chế độ Tối'}
        >
          {theme === 'dark' ? (
            <>
              <span className="theme-toggle-icon">☀️</span>
              <span className="theme-toggle-text">Sáng</span>
            </>
          ) : (
            <>
              <span className="theme-toggle-icon">🌙</span>
              <span className="theme-toggle-text">Tối</span>
            </>
          )}
        </button>
      </div>

      <div className="container page-content" style={{ maxWidth: '520px', margin: '0 auto', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        {/* Welcome Header */}
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-6)' }}>
          <h1 style={{
            fontSize: '2rem',
            fontWeight: 800,
            marginBottom: 'var(--space-2)',
            color: 'var(--color-text-primary)',
          }}>
            Chào mừng bạn đến với MotionIQ
          </h1>
          <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)', margin: 0 }}>
            Hệ thống AI hỗ trợ người cao tuổi tập vận động và phục hồi chức năng
          </p>
        </div>

        {/* Tab Switcher (Người tập vs Quản trị viên) */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          background: 'rgba(255, 255, 255, 0.05)',
          padding: '4px',
          borderRadius: 'var(--radius-xl)',
          border: '1px solid var(--color-border)',
          marginBottom: 'var(--space-6)',
          backdropFilter: 'blur(8px)',
        }}>
          <button
            type="button"
            onClick={() => setActiveTab('patient')}
            style={{
              padding: '12px 16px',
              borderRadius: 'var(--radius-lg)',
              border: 'none',
              background: activeTab === 'patient' ? 'var(--gradient-primary)' : 'transparent',
              color: activeTab === 'patient' ? '#ffffff' : 'var(--color-text-secondary)',
              fontWeight: 700,
              fontSize: 'var(--font-size-base)',
              cursor: 'pointer',
              transition: 'all 0.25s cubic-bezier(0.16, 1, 0.3, 1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: activeTab === 'patient' ? '0 4px 16px rgba(6, 182, 212, 0.4)' : 'none',
            }}
          >
            <span>👤</span> Người tập / Bệnh nhân
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('admin')}
            style={{
              padding: '12px 16px',
              borderRadius: 'var(--radius-lg)',
              border: 'none',
              background: activeTab === 'admin' ? 'var(--gradient-primary)' : 'transparent',
              color: activeTab === 'admin' ? '#ffffff' : 'var(--color-text-secondary)',
              fontWeight: 700,
              fontSize: 'var(--font-size-base)',
              cursor: 'pointer',
              transition: 'all 0.25s cubic-bezier(0.16, 1, 0.3, 1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: activeTab === 'admin' ? '0 4px 16px rgba(6, 182, 212, 0.4)' : 'none',
            }}
          >
            <span>🛡️</span> Quản trị viên
          </button>
        </div>

        {/* TAB 1: NGƯỜI TẬP / BỆNH NHÂN */}
        {activeTab === 'patient' && (
          <div style={{ animation: 'popIn 0.35s cubic-bezier(0.16, 1, 0.3, 1)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
              <span style={{ fontWeight: 700, fontSize: 'var(--font-size-base)', color: 'var(--color-text-primary)' }}>
                Chọn hồ sơ để bắt đầu:
              </span>
              <button
                type="button"
                className="btn btn-secondary"
                style={{
                  padding: '6px 14px',
                  fontSize: 'var(--font-size-xs)',
                  color: 'var(--color-accent-primary)',
                  borderColor: 'rgba(6, 182, 212, 0.4)',
                }}
                onClick={() => setShowAddPatient(!showAddPatient)}
              >
                {showAddPatient ? '✕ Đóng form' : '➕ Thêm người tập'}
              </button>
            </div>

            {/* Expandable New Patient Form */}
            {showAddPatient && (
              <form
                onSubmit={handleCreatePatient}
                className="card"
                style={{
                  marginBottom: 'var(--space-5)',
                  padding: 'var(--space-5)',
                  border: '1px solid var(--color-accent-primary)',
                  animation: 'popIn 0.3s ease',
                }}
              >
                <h3 style={{ fontSize: 'var(--font-size-base)', marginBottom: 'var(--space-3)', color: 'var(--color-accent-primary)' }}>
                  ✨ Tạo hồ sơ người tập mới
                </h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                      Họ và tên / Tên thân mật *
                    </label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="Ví dụ: Bác Minh, Bà Lan..."
                      value={newName}
                      required
                      autoFocus
                      onChange={(e) => setNewName(e.target.value)}
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
                        value={newAge}
                        onChange={(e) => setNewAge(parseInt(e.target.value, 10) || 60)}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: 'var(--font-size-xs)', fontWeight: 600, marginBottom: '4px' }}>
                        Giới tính
                      </label>
                      <select
                        className="select-field"
                        value={newGender}
                        onChange={(e) => setNewGender(e.target.value as any)}
                      >
                        <option value="male">Nam</option>
                        <option value="female">Nữ</option>
                        <option value="other">Khác</option>
                      </select>
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
                          onClick={() => setNewAvatar(icon)}
                          style={{
                            fontSize: '1.5rem',
                            padding: '6px 10px',
                            borderRadius: 'var(--radius-md)',
                            border: newAvatar === icon ? '2px solid var(--color-accent-primary)' : '1px solid var(--color-border)',
                            background: newAvatar === icon ? 'rgba(6, 182, 212, 0.25)' : 'rgba(255, 255, 255, 0.05)',
                            cursor: 'pointer',
                            transform: newAvatar === icon ? 'scale(1.15)' : 'scale(1)',
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
                      Mã PIN bảo mật 4 số (Tùy chọn)
                    </label>
                    <input
                      type="password"
                      maxLength={4}
                      className="input-field"
                      placeholder="Để trống nếu không muốn cài mật mã"
                      value={newPin}
                      onChange={(e) => setNewPin(e.target.value)}
                    />
                  </div>

                  <button type="submit" className="btn btn-primary btn-full" style={{ marginTop: 'var(--space-2)' }}>
                    ✅ Lưu hồ sơ & Bắt đầu tập ngay
                  </button>
                </div>
              </form>
            )}

            {/* Patient Cards List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
              {patients.map((p) => (
                <div
                  key={p.id}
                  className="card card-interactive"
                  onClick={() => handlePatientSelect(p)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: 'var(--space-4) var(--space-5)',
                    cursor: 'pointer',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
                    <div style={{
                      fontSize: '2.4rem',
                      width: '60px',
                      height: '60px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%)',
                      borderRadius: 'var(--radius-full)',
                      border: '1px solid rgba(6, 182, 212, 0.3)',
                    }}>
                      {p.avatarIcon || '👤'}
                    </div>
                    <div>
                      <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--color-text-primary)' }}>
                        {p.name}
                      </div>
                      <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
                        {p.age} tuổi • {p.condition || 'Phục hồi chức năng'}
                      </div>
                      {p.pin && (
                        <span style={{ fontSize: '11px', color: '#f59e0b', display: 'inline-flex', alignItems: 'center', gap: '2px', marginTop: '3px' }}>
                          🔒 Có mã PIN
                        </span>
                      )}
                    </div>
                  </div>

                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    color: 'var(--color-accent-primary)',
                    fontWeight: 700,
                    fontSize: 'var(--font-size-sm)',
                  }}>
                    <span>Vào tập</span>
                    <span style={{ fontSize: '1.4rem' }}>→</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: QUẢN TRỊ VIÊN */}
        {activeTab === 'admin' && (
          <form
            onSubmit={handleAdminSubmit}
            className="card"
            style={{
              padding: 'var(--space-6)',
              animation: isShaking ? 'shakeError 0.5s ease-in-out' : 'popIn 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
            }}
          >
            <div style={{ textAlign: 'center', marginBottom: 'var(--space-5)' }}>
              <div style={{
                fontSize: '2.5rem',
                width: '70px',
                height: '70px',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'rgba(6, 182, 212, 0.15)',
                border: '1px solid rgba(6, 182, 212, 0.4)',
                borderRadius: 'var(--radius-full)',
                marginBottom: 'var(--space-2)',
              }}>
                🛡️
              </div>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--color-text-primary)', margin: 0 }}>
                Đăng nhập Quản trị viên
              </h2>
              <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginTop: '4px' }}>
                Dành cho Bác sĩ, Kỹ thuật viên & Người quản lý
              </p>
            </div>

            {/* Quick Demo Hint */}
            <div style={{
              background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
              border: '1px dashed rgba(6, 182, 212, 0.4)',
              borderRadius: 'var(--radius-md)',
              padding: '10px 14px',
              fontSize: 'var(--font-size-xs)',
              color: 'var(--color-text-secondary)',
              marginBottom: 'var(--space-4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}>
              <span>💡 Tài khoản mặc định:</span>
              <span style={{ fontWeight: 700, color: 'var(--color-accent-primary)' }}>
                admin / admin123
              </span>
            </div>

            {adminError && (
              <div style={{
                padding: '10px 14px',
                background: 'rgba(239, 68, 68, 0.15)',
                border: '1px solid #ef4444',
                color: '#f87171',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--font-size-sm)',
                marginBottom: 'var(--space-4)',
                textAlign: 'center',
              }}>
                ⚠️ {adminError}
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: '6px' }}>
                  Tên đăng nhập (Username)
                </label>
                <input
                  type="text"
                  className="input-field"
                  placeholder="Nhập tên đăng nhập"
                  value={adminUsername}
                  required
                  onChange={(e) => setAdminUsername(e.target.value)}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: '6px' }}>
                  Mật khẩu (Password)
                </label>
                <div style={{ position: 'relative' }}>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    className="input-field"
                    placeholder="Nhập mật khẩu"
                    value={adminPassword}
                    required
                    onChange={(e) => setAdminPassword(e.target.value)}
                    style={{ paddingRight: '48px' }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '12px',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      background: 'none',
                      border: 'none',
                      fontSize: '1.2rem',
                      cursor: 'pointer',
                      color: 'var(--color-text-muted)',
                    }}
                    title={showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'}
                  >
                    {showPassword ? '👁️' : '🔒'}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="btn btn-primary btn-full"
                style={{ marginTop: 'var(--space-2)' }}
              >
                🔐 Đăng nhập vào Bảng điều khiển
              </button>
            </div>
          </form>
        )}
      </div>

      {/* PIN Verification Modal */}
      {pinModalPatient && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: 'var(--space-4)',
        }}>
          <form
            onSubmit={handlePinSubmit}
            className="card"
            style={{
              maxWidth: '380px',
              width: '100%',
              padding: 'var(--space-6)',
              textAlign: 'center',
              animation: 'popIn 0.3s ease',
            }}
          >
            <div style={{ fontSize: '3rem', marginBottom: 'var(--space-2)' }}>
              {pinModalPatient.avatarIcon || '👤'}
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '4px' }}>
              Xác thực: {pinModalPatient.name}
            </h3>
            <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-4)' }}>
              Hồ sơ này yêu cầu mã PIN 4 số để vào bài tập
            </p>

            {pinError && (
              <div style={{
                color: '#f87171',
                fontSize: 'var(--font-size-xs)',
                marginBottom: 'var(--space-3)',
                fontWeight: 600,
              }}>
                ⚠️ {pinError}
              </div>
            )}

            <input
              type="password"
              maxLength={4}
              autoFocus
              className="input-field"
              placeholder="••••"
              value={enteredPin}
              onChange={(e) => setEnteredPin(e.target.value)}
              style={{
                textAlign: 'center',
                letterSpacing: '12px',
                fontSize: '1.8rem',
                fontWeight: 800,
                marginBottom: 'var(--space-4)',
              }}
            />

            <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
              <button
                type="button"
                className="btn btn-secondary"
                style={{ flex: 1 }}
                onClick={() => setPinModalPatient(null)}
              >
                Hủy
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                style={{ flex: 1 }}
              >
                Xác nhận
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
