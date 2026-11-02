'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
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
  const [activeScreen, setActiveScreen] = useState<'welcome' | 'login' | 'register' | 'forgot'>('welcome');
  const [patients, setPatients] = useState<PatientUser[]>([]);

  // Login form state
  const [loginName, setLoginName] = useState('Bác Nguyễn Văn An');
  const [loginPassword, setLoginPassword] = useState('123456');
  const [loginError, setLoginError] = useState<string | null>(null);

  // Register form state
  const [regName, setRegName] = useState('');
  const [regPhone, setRegPhone] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regTerms, setRegTerms] = useState(true);

  // Forgot password form state
  const [forgotPhone, setForgotPhone] = useState('');

  // Admin login modal
  const [showAdminModal, setShowAdminModal] = useState(false);
  const [adminUsername, setAdminUsername] = useState('admin');
  const [adminPassword, setAdminPassword] = useState('');
  const [adminError, setAdminError] = useState<string | null>(null);

  // Toast notification
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  useEffect(() => {
    const session = getAuthSession();
    if (session) {
      if (session.role === 'admin') {
        router.push('/admin');
      } else {
        router.push('/');
      }
      return;
    }

    const list = getAllPatients();
    setPatients(list);
    if (list.length > 0) {
      setLoginName(list[0].name);
    }
  }, [router]);

  // Handle Login Submit
  const handleLoginSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);

    const trimmed = loginName.trim().toLowerCase();
    const matched = patients.find(
      (p) => p.name.toLowerCase() === trimmed || p.name.toLowerCase().includes(trimmed)
    );

    const targetPatient = matched || patients[0];

    if (!targetPatient) {
      const created = createPatient({
        name: loginName.trim() || 'Người tập mới',
        age: 68,
        gender: 'male',
        condition: 'Tập phục hồi chức năng cơ bản',
        avatarIcon: '👴',
      });
      loginAsPatient(created.id);
      router.push('/');
      return;
    }

    const res = loginAsPatient(targetPatient.id);
    if (res.success) {
      showToast(`Chào mừng ${targetPatient.name}! 🎉`);
      router.push('/');
    } else {
      setLoginError(res.error || 'Đăng nhập không thành công');
    }
  };

  // Handle 1-touch profile select
  const handleSelectPatientQuick = (p: PatientUser) => {
    setLoginName(p.name);
    const res = loginAsPatient(p.id);
    if (res.success) {
      showToast(`Chào mừng ${p.name}! 🎉`);
      router.push('/');
    }
  };

  // Handle Register Submit
  const handleRegisterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!regName.trim()) {
      showToast('Vui lòng nhập họ và tên của bác');
      return;
    }

    const created = createPatient({
      name: regName.trim(),
      age: 68,
      gender: 'male',
      condition: 'Tập phục hồi khớp gối & thăng bằng',
      avatarIcon: '👴',
      emergencyContact: regPhone.trim() || '115',
    });

    setPatients(getAllPatients());
    loginAsPatient(created.id);
    showToast('Tạo tài khoản thành công! Đang chuyển đến trang chủ...');
    setTimeout(() => {
      router.push('/');
    }, 500);
  };

  // Handle Forgot Submit
  const handleForgotSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!forgotPhone.trim()) {
      showToast('Vui lòng nhập số điện thoại');
      return;
    }
    showToast(`Mã xác thực đã được gửi đến số ${forgotPhone}! ✨`);
    setTimeout(() => {
      setActiveScreen('login');
    }, 1600);
  };

  // Handle Admin Submit
  const handleAdminSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setAdminError(null);
    const res = loginAsAdmin(adminUsername, adminPassword);
    if (res.success) {
      router.push('/admin');
    } else {
      setAdminError(res.error || 'Tài khoản hoặc mật khẩu không đúng (admin / admin123)');
    }
  };

  return (
    <div
      style={{
        width: '100%',
        flex: 1,
        minHeight: '100dvh',
        backgroundColor: '#FEF0E1',
        display: 'flex',
        flexDirection: 'column',
        fontFamily: 'var(--font-family)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background Autumn Drift Leaves */}
      <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', zIndex: 0 }}>
        <div style={{ position: 'absolute', top: '8%', left: '6%', fontSize: '20px', opacity: 0.35, animation: 'mascotBobbing 4s infinite ease-in-out' }}>🍂</div>
        <div style={{ position: 'absolute', top: '20%', right: '8%', fontSize: '22px', opacity: 0.3, animation: 'mascotBobbing 5s infinite ease-in-out 1s' }}>🍁</div>
        <div style={{ position: 'absolute', bottom: '12%', left: '8%', fontSize: '18px', opacity: 0.25, animation: 'mascotBobbing 4.5s infinite ease-in-out 2s' }}>✨</div>
        <div style={{ position: 'absolute', bottom: '25%', right: '6%', fontSize: '20px', opacity: 0.3, animation: 'mascotBobbing 6s infinite ease-in-out' }}>🌾</div>
      </div>

      {/* Main Mobile App Screen (Full Viewport Height) */}
      <div
        style={{
          width: '100%',
          flex: 1,
          minHeight: '100dvh',
          display: 'flex',
          flexDirection: 'column',
          position: 'relative',
          overflow: 'hidden',
          zIndex: 10,
        }}
      >
        {/* Subtle Minimal Status Bar */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            zIndex: 40,
            padding: '10px 24px 4px 24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '11px',
            fontWeight: 800,
            color: activeScreen === 'welcome' || activeScreen === 'forgot' ? 'rgba(255, 255, 255, 0.9)' : '#B2422D',
            pointerEvents: 'none',
            transition: 'color 0.25s ease',
          }}
        >
          <span>9:41</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ fontSize: '10px' }}>●●●</span>
            <span style={{ fontSize: '11px', marginLeft: '4px' }}>100%</span>
          </div>
        </div>

        {/* ========================================================
            SCREEN 1: XIN CHÀO (WELCOME) — DÀN ĐỀU TRỌN MÀN HÌNH 100VH
            ======================================================== */}
        {activeScreen === 'welcome' && (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
              flex: 1,
              minHeight: '100dvh',
              backgroundColor: '#FEF0E1',
              animation: 'fadeIn 0.25s ease',
              position: 'relative',
              justifyContent: 'space-between',
            }}
          >
            {/* Top Terracotta Card (58% height) with curved bottom */}
            <div
              style={{
                position: 'relative',
                backgroundColor: '#B2422D',
                paddingTop: '36px',
                paddingBottom: '24px',
                paddingLeft: '20px',
                paddingRight: '20px',
                flex: '1.4',
                minHeight: '56vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'space-between',
                borderBottomLeftRadius: '40px',
                borderBottomRightRadius: '40px',
                boxShadow: '0 8px 24px rgba(178, 66, 45, 0.35)',
                overflow: 'hidden',
              }}
            >
              {/* Autumn Sparks & Elements */}
              <div style={{ position: 'absolute', top: '35px', left: '16px', color: '#FDE68A', opacity: 0.6, fontSize: '16px' }}>✦</div>
              <div style={{ position: 'absolute', top: '45px', right: '20px', color: '#FDE68A', opacity: 0.7, fontSize: '14px' }}>✨</div>
              <div style={{ position: 'absolute', bottom: '40px', left: '20px', color: '#FDE68A', opacity: 0.5, fontSize: '12px' }}>🍂</div>
              <div style={{ position: 'absolute', bottom: '50px', right: '16px', color: '#FDE68A', opacity: 0.6, fontSize: '14px' }}>🍁</div>

              {/* Logo Tệp Hoàn Hảo Vào Nền */}
              <div
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  backgroundColor: 'rgba(255, 255, 255, 0.16)',
                  border: '1px solid rgba(255, 255, 255, 0.25)',
                  padding: '3px 12px 3px 6px',
                  borderRadius: '9999px',
                  backdropFilter: 'blur(8px)',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.12)',
                  userSelect: 'none',
                  zIndex: 20,
                  marginTop: '4px',
                }}
              >
                <div
                  style={{
                    width: '18px',
                    height: '18px',
                    borderRadius: '50%',
                    backgroundColor: '#FEF0E1',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '2px',
                    boxShadow: '0 1px 4px rgba(0, 0, 0, 0.2)',
                  }}
                >
                  <Image
                    src="/images/custom-ui/motioniq_logo_transparent.png"
                    alt="MotionIQ"
                    width={14}
                    height={14}
                    unoptimized
                    style={{ width: '14px', height: '14px', objectFit: 'contain' }}
                  />
                </div>
                <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#FFFFFF', letterSpacing: '0.6px' }}>
                  MOTIONIQ AI
                </span>
              </div>

              {/* Title: "Xin chào" */}
              <div style={{ textAlign: 'center', zIndex: 10, margin: '2px 0' }}>
                <h1
                  style={{
                    fontFamily: 'var(--font-family)',
                    fontSize: 'clamp(2.1rem, 5.5vw, 2.6rem)',
                    fontWeight: 700,
                    color: '#FFFFFF',
                    margin: 0,
                    textShadow: '0 2px 6px rgba(0, 0, 0, 0.2)',
                  }}
                >
                  Xin chào
                </h1>
              </div>

              {/* Mascot Sitting on Autumn Leaves */}
              <div
                style={{
                  position: 'relative',
                  zIndex: 10,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  animation: 'mascotBobbing 2.8s infinite ease-in-out',
                  cursor: 'pointer',
                  margin: 'auto 0',
                }}
                onClick={() => showToast('Bé Nấm: Chúc bạn một ngày tập luyện vui khỏe! 🍄')}
              >
                <Image
                  src="/images/custom-ui/mascot_welcome_clean.png"
                  alt="Bé Nấm Chào Mừng"
                  width={210}
                  height={155}
                  unoptimized
                  style={{ width: '205px', height: 'auto', objectFit: 'contain' }}
                  priority
                />
              </div>

              <div style={{ height: '4px' }} />
            </div>

            {/* Bottom Cream Section (42% height) with Buttons */}
            <div
              style={{
                flex: '1',
                minHeight: '44vh',
                padding: '24px 28px 48px 28px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                gap: '16px',
                position: 'relative',
                zIndex: 10,
              }}
            >
              {/* Button 1: "Tôi đã có tài khoản" */}
              <button
                type="button"
                onClick={() => setActiveScreen('login')}
                style={{
                  width: '100%',
                  maxWidth: '340px',
                  padding: '16px 24px',
                  borderRadius: '9999px',
                  backgroundColor: '#B2422D',
                  color: '#FFFFFF',
                  border: 'none',
                  fontSize: '1.05rem',
                  fontWeight: 700,
                  boxShadow: '0 6px 18px rgba(178, 66, 45, 0.35)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                }}
              >
                <span>Tôi đã có tài khoản</span>
                <span style={{ fontSize: '1rem', opacity: 0.85 }}>➔</span>
              </button>

              {/* Button 2: "Tạo tài khoản" */}
              <button
                type="button"
                onClick={() => setActiveScreen('register')}
                style={{
                  width: '100%',
                  maxWidth: '340px',
                  padding: '16px 24px',
                  borderRadius: '9999px',
                  backgroundColor: '#FFFFFF',
                  color: '#B2422D',
                  border: '2px solid #B2422D',
                  fontSize: '1.05rem',
                  fontWeight: 700,
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.04)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <span>Tạo tài khoản</span>
              </button>

              {/* Small Doctor Login Link */}
              <div style={{ textAlign: 'center', marginTop: '4px' }}>
                <button
                  type="button"
                  onClick={() => setShowAdminModal(true)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'rgba(178, 66, 45, 0.75)',
                    fontSize: '0.8rem',
                    fontWeight: 700,
                    cursor: 'pointer',
                  }}
                >
                  🛡️ Bác sĩ / Quản trị viên
                </button>
              </div>

              {/* Decorative Bottom Terracotta Clouds (Fit sát mép dưới) */}
              <div
                style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  height: '56px',
                  pointerEvents: 'none',
                  display: 'flex',
                  alignItems: 'flex-end',
                  zIndex: 0,
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    position: 'absolute',
                    left: '-20px',
                    bottom: '-12px',
                    width: '160px',
                    height: '68px',
                    backgroundColor: '#B2422D',
                    borderRadius: '50% 50% 0 0',
                    opacity: 0.95,
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    right: '-20px',
                    bottom: '-14px',
                    width: '170px',
                    height: '72px',
                    backgroundColor: '#B2422D',
                    borderRadius: '50% 50% 0 0',
                    opacity: 0.95,
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* ========================================================
            SCREEN 2: ĐĂNG NHẬP (LOGIN) — DÀN ĐỀU TRỌN MÀN HÌNH 100VH
            ======================================================== */}
        {activeScreen === 'login' && (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
              flex: 1,
              minHeight: '100dvh',
              backgroundColor: '#FEF0E1',
              animation: 'fadeIn 0.25s ease',
              position: 'relative',
              justifyContent: 'space-between',
            }}
          >
            {/* Top Cream Area: Back button + Title + Mascot Head */}
            <div
              style={{
                flex: '0.7',
                minHeight: '32vh',
                paddingTop: '32px',
                paddingLeft: '20px',
                paddingRight: '20px',
                paddingBottom: '12px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative',
              }}
            >
              {/* Back Button */}
              <button
                type="button"
                onClick={() => setActiveScreen('welcome')}
                style={{
                  position: 'absolute',
                  top: '28px',
                  left: '16px',
                  background: 'none',
                  border: 'none',
                  color: '#B2422D',
                  fontSize: '0.88rem',
                  fontWeight: 800,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  padding: '6px',
                }}
              >
                <span>❮</span>
                <span>Trở về</span>
              </button>

              <h2
                style={{
                  fontFamily: 'var(--font-family)',
                  fontSize: '1.9rem',
                  fontWeight: 800,
                  color: '#B2422D',
                  margin: '12px 0 6px 0',
                  textAlign: 'center',
                  lineHeight: 1.15,
                }}
              >
                Chào mừng<br />trở lại
              </h2>

              {/* Clean Transparent Mascot Head */}
              <div
                style={{
                  position: 'relative',
                  width: '95px',
                  height: '80px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  animation: 'mascotBobbing 3s infinite ease-in-out',
                  margin: '4px 0',
                }}
              >
                <Image
                  src="/images/custom-ui/mascot_login_clean.png"
                  alt="Bé Nấm Login"
                  width={95}
                  height={80}
                  unoptimized
                  style={{ objectFit: 'contain' }}
                />
              </div>
            </div>

            {/* Bottom Terracotta Card (Form) */}
            <div
              style={{
                flex: '1.3',
                minHeight: '68vh',
                backgroundColor: '#B2422D',
                borderTopLeftRadius: '36px',
                borderTopRightRadius: '36px',
                padding: '24px 24px 48px 24px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                position: 'relative',
                boxShadow: '0 -8px 24px rgba(178, 66, 45, 0.3)',
                overflow: 'hidden',
              }}
            >
              {/* Quick 1-Touch Pill for Seniors */}
              <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                {patients.slice(0, 2).map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => handleSelectPatientQuick(p)}
                    style={{
                      padding: '5px 12px',
                      borderRadius: '9999px',
                      backgroundColor: loginName === p.name ? '#FEF0E1' : 'rgba(255, 255, 255, 0.2)',
                      color: loginName === p.name ? '#B2422D' : '#FFFFFF',
                      border: 'none',
                      fontSize: '0.8rem',
                      fontWeight: 800,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                    }}
                  >
                    <span>{p.avatarIcon}</span>
                    <span>{p.name.split(' ').slice(-2).join(' ')}</span>
                  </button>
                ))}
              </div>

              {/* Form Inputs */}
              <form onSubmit={handleLoginSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px', margin: 'auto 0', width: '100%', maxWidth: '340px', alignSelf: 'center' }}>
                {loginError && (
                  <div style={{ backgroundColor: 'rgba(255, 255, 255, 0.25)', color: '#FFFFFF', padding: '8px 12px', borderRadius: '12px', fontSize: '0.82rem', fontWeight: 700, textAlign: 'center' }}>
                    ⚠️ {loginError}
                  </div>
                )}

                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, color: '#FEF0E1', marginBottom: '6px' }}>
                    Nhập tên
                  </label>
                  <input
                    type="text"
                    value={loginName}
                    onChange={(e) => setLoginName(e.target.value)}
                    placeholder="Bác Nguyễn Văn An"
                    required
                    style={{
                      width: '100%',
                      padding: '13px 18px',
                      borderRadius: '9999px',
                      border: 'none',
                      backgroundColor: '#C97663',
                      color: '#FFFFFF',
                      fontSize: '1rem',
                      fontWeight: 600,
                      outline: 'none',
                      boxShadow: 'inset 0 1px 3px rgba(0, 0, 0, 0.2)',
                    }}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, color: '#FEF0E1', marginBottom: '6px' }}>
                    Mật khẩu
                  </label>
                  <input
                    type="password"
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    placeholder="••••••"
                    style={{
                      width: '100%',
                      padding: '13px 18px',
                      borderRadius: '9999px',
                      border: 'none',
                      backgroundColor: '#C97663',
                      color: '#FFFFFF',
                      fontSize: '1rem',
                      fontWeight: 600,
                      outline: 'none',
                      boxShadow: 'inset 0 1px 3px rgba(0, 0, 0, 0.2)',
                    }}
                  />
                </div>

                {/* Login Button */}
                <button
                  type="submit"
                  style={{
                    marginTop: '8px',
                    width: '100%',
                    padding: '15px',
                    borderRadius: '9999px',
                    backgroundColor: '#FEF0E1',
                    color: '#B2422D',
                    border: 'none',
                    fontSize: '1.05rem',
                    fontWeight: 900,
                    letterSpacing: '0.5px',
                    cursor: 'pointer',
                    boxShadow: '0 4px 14px rgba(0, 0, 0, 0.2)',
                  }}
                >
                  ĐĂNG NHẬP
                </button>

                <div style={{ textAlign: 'center', marginTop: '4px' }}>
                  <button
                    type="button"
                    onClick={() => setActiveScreen('forgot')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: 'rgba(255, 255, 255, 0.85)',
                      fontSize: '0.85rem',
                      fontStyle: 'italic',
                      cursor: 'pointer',
                      textDecoration: 'underline',
                    }}
                  >
                    Quên mật khẩu?
                  </button>
                </div>
              </form>

              {/* Bottom Cream Clouds */}
              <div
                style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  height: '42px',
                  pointerEvents: 'none',
                  zIndex: 0,
                }}
              >
                <div style={{ position: 'absolute', left: '-15px', bottom: '-10px', width: '150px', height: '52px', backgroundColor: '#FEF0E1', borderRadius: '50% 50% 0 0' }} />
                <div style={{ position: 'absolute', right: '-15px', bottom: '-12px', width: '160px', height: '56px', backgroundColor: '#FEF0E1', borderRadius: '50% 50% 0 0' }} />
              </div>
            </div>
          </div>
        )}

        {/* ========================================================
            SCREEN 3: TẠO TÀI KHOẢN (REGISTER) — DÀN ĐỀU TRỌN MÀN HÌNH 100VH
            ======================================================== */}
        {activeScreen === 'register' && (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
              flex: 1,
              minHeight: '100dvh',
              backgroundColor: '#FEF0E1',
              animation: 'fadeIn 0.25s ease',
              position: 'relative',
              justifyContent: 'space-between',
            }}
          >
            {/* Top Cream Area: Back button + Title + Mascot Head */}
            <div
              style={{
                flex: '0.6',
                minHeight: '28vh',
                paddingTop: '32px',
                paddingLeft: '20px',
                paddingRight: '20px',
                paddingBottom: '8px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative',
              }}
            >
              <button
                type="button"
                onClick={() => setActiveScreen('welcome')}
                style={{
                  position: 'absolute',
                  top: '28px',
                  left: '16px',
                  background: 'none',
                  border: 'none',
                  color: '#B2422D',
                  fontSize: '0.88rem',
                  fontWeight: 800,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  padding: '6px',
                }}
              >
                <span>❮</span>
                <span>Trở về</span>
              </button>

              <h2
                style={{
                  fontFamily: 'var(--font-family)',
                  fontSize: '1.9rem',
                  fontWeight: 800,
                  color: '#B2422D',
                  margin: '10px 0 4px 0',
                  textAlign: 'center',
                  lineHeight: 1.15,
                }}
              >
                Tạo tài<br />khoản
              </h2>

              <div
                style={{
                  position: 'relative',
                  width: '95px',
                  height: '75px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  animation: 'mascotBobbing 3s infinite ease-in-out',
                }}
              >
                <Image
                  src="/images/custom-ui/mascot_register_clean.png"
                  alt="Bé Nấm Register"
                  width={95}
                  height={75}
                  unoptimized
                  style={{ objectFit: 'contain' }}
                />
              </div>
            </div>

            {/* Bottom Terracotta Card */}
            <div
              style={{
                flex: '1.4',
                minHeight: '72vh',
                backgroundColor: '#B2422D',
                borderTopLeftRadius: '36px',
                borderTopRightRadius: '36px',
                padding: '20px 24px 48px 24px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                position: 'relative',
                boxShadow: '0 -8px 24px rgba(178, 66, 45, 0.3)',
                overflow: 'hidden',
              }}
            >
              <form onSubmit={handleRegisterSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px', margin: 'auto 0', width: '100%', maxWidth: '340px', alignSelf: 'center' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#FEF0E1', marginBottom: '4px' }}>
                    Nhập tên
                  </label>
                  <input
                    type="text"
                    value={regName}
                    onChange={(e) => setRegName(e.target.value)}
                    placeholder="Bác Lê Văn Minh"
                    required
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      borderRadius: '9999px',
                      border: 'none',
                      backgroundColor: '#C97663',
                      color: '#FFFFFF',
                      fontSize: '0.95rem',
                      fontWeight: 600,
                      outline: 'none',
                    }}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#FEF0E1', marginBottom: '4px' }}>
                    Số điện thoại
                  </label>
                  <input
                    type="tel"
                    value={regPhone}
                    onChange={(e) => setRegPhone(e.target.value)}
                    placeholder="0912 345 678"
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      borderRadius: '9999px',
                      border: 'none',
                      backgroundColor: '#C97663',
                      color: '#FFFFFF',
                      fontSize: '0.95rem',
                      fontWeight: 600,
                      outline: 'none',
                    }}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#FEF0E1', marginBottom: '4px' }}>
                    Mật khẩu
                  </label>
                  <input
                    type="password"
                    value={regPassword}
                    onChange={(e) => setRegPassword(e.target.value)}
                    placeholder="••••••"
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      borderRadius: '9999px',
                      border: 'none',
                      backgroundColor: '#C97663',
                      color: '#FFFFFF',
                      fontSize: '0.95rem',
                      fontWeight: 600,
                      outline: 'none',
                    }}
                  />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', margin: '4px 0' }}>
                  <input
                    type="checkbox"
                    id="regTerms"
                    checked={regTerms}
                    onChange={(e) => setRegTerms(e.target.checked)}
                    style={{ accentColor: '#FEF0E1', cursor: 'pointer', width: '16px', height: '16px' }}
                  />
                  <label htmlFor="regTerms" style={{ fontSize: '0.75rem', color: 'rgba(255, 255, 255, 0.9)', fontStyle: 'italic', cursor: 'pointer' }}>
                    Tôi đồng ý với các điều khoản và điều kiện.
                  </label>
                </div>

                <button
                  type="submit"
                  style={{
                    marginTop: '6px',
                    width: '100%',
                    padding: '14px',
                    borderRadius: '9999px',
                    backgroundColor: '#FEF0E1',
                    color: '#B2422D',
                    border: 'none',
                    fontSize: '1.05rem',
                    fontWeight: 900,
                    letterSpacing: '0.5px',
                    cursor: 'pointer',
                    boxShadow: '0 4px 14px rgba(0, 0, 0, 0.2)',
                  }}
                >
                  ĐĂNG KÝ
                </button>
              </form>

              {/* Bottom Cream Clouds */}
              <div
                style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  height: '42px',
                  pointerEvents: 'none',
                  zIndex: 0,
                }}
              >
                <div style={{ position: 'absolute', left: '-15px', bottom: '-10px', width: '150px', height: '52px', backgroundColor: '#FEF0E1', borderRadius: '50% 50% 0 0' }} />
                <div style={{ position: 'absolute', right: '-15px', bottom: '-12px', width: '160px', height: '56px', backgroundColor: '#FEF0E1', borderRadius: '50% 50% 0 0' }} />
              </div>
            </div>
          </div>
        )}

        {/* ========================================================
            SCREEN 4: QUÊN MẬT KHẨU (FORGOT PASSWORD) — DÀN ĐỀU TRỌN MÀN HÌNH 100VH
            ======================================================== */}
        {activeScreen === 'forgot' && (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
              flex: 1,
              minHeight: '100dvh',
              backgroundColor: '#FEF0E1',
              animation: 'fadeIn 0.25s ease',
              position: 'relative',
              justifyContent: 'space-between',
            }}
          >
            {/* Top Terracotta Section (52% height) */}
            <div
              style={{
                backgroundColor: '#B2422D',
                flex: '1.2',
                minHeight: '52vh',
                paddingTop: '32px',
                paddingLeft: '20px',
                paddingRight: '20px',
                paddingBottom: '20px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'space-between',
                borderBottomLeftRadius: '40px',
                borderBottomRightRadius: '40px',
                position: 'relative',
                boxShadow: '0 8px 24px rgba(178, 66, 45, 0.35)',
              }}
            >
              <button
                type="button"
                onClick={() => setActiveScreen('login')}
                style={{
                  position: 'absolute',
                  top: '28px',
                  left: '16px',
                  background: 'none',
                  border: 'none',
                  color: '#FFFFFF',
                  fontSize: '0.88rem',
                  fontWeight: 800,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  padding: '6px',
                }}
              >
                <span>❮</span>
                <span>Trở về</span>
              </button>

              <div style={{ textAlign: 'center', marginTop: '16px' }}>
                <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#FFFFFF', lineHeight: 1.2 }}>
                  Oh No!
                </div>
                <div style={{ fontSize: '1.7rem', fontWeight: 800, color: '#FFFFFF', lineHeight: 1.2 }}>
                  Mật khẩu của tôi
                </div>
              </div>

              {/* Cool Mushroom Mascot with Sunglasses */}
              <div
                style={{
                  position: 'relative',
                  width: '135px',
                  height: '145px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  animation: 'mascotBobbing 2.8s infinite ease-in-out',
                }}
              >
                <Image
                  src="/images/custom-ui/mascot_forgot_clean.png"
                  alt="Bé Nấm Forgot"
                  width={135}
                  height={145}
                  unoptimized
                  style={{ objectFit: 'contain' }}
                />
              </div>

              <div style={{ height: '4px' }} />
            </div>

            {/* Bottom Cream Section */}
            <div
              style={{
                flex: '1',
                minHeight: '48vh',
                padding: '24px 28px 48px 28px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                gap: '16px',
                position: 'relative',
              }}
            >
              <p
                style={{
                  fontSize: '0.88rem',
                  color: '#78350F',
                  textAlign: 'center',
                  lineHeight: 1.5,
                  margin: 0,
                  maxWidth: '320px',
                }}
              >
                Đừng lo, chuyện này ai cũng có thể gặp phải! Nhập số điện thoại của bạn để đặt lại mật khẩu!
              </p>

              <form onSubmit={handleForgotSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px', position: 'relative', zIndex: 10, width: '100%', maxWidth: '340px' }}>
                <input
                  type="tel"
                  value={forgotPhone}
                  onChange={(e) => setForgotPhone(e.target.value)}
                  placeholder="Số điện thoại"
                  required
                  style={{
                    width: '100%',
                    padding: '14px 18px',
                    borderRadius: '9999px',
                    border: '1.5px solid #B2422D',
                    backgroundColor: '#FEF0E1',
                    color: '#B2422D',
                    fontSize: '1rem',
                    fontWeight: 700,
                    textAlign: 'center',
                    outline: 'none',
                  }}
                />

                <button
                  type="submit"
                  style={{
                    width: '100%',
                    padding: '15px',
                    borderRadius: '9999px',
                    backgroundColor: '#B2422D',
                    color: '#FFFFFF',
                    border: 'none',
                    fontSize: '1.05rem',
                    fontWeight: 900,
                    letterSpacing: '0.5px',
                    cursor: 'pointer',
                    boxShadow: '0 6px 18px rgba(178, 66, 45, 0.35)',
                  }}
                >
                  GỬI
                </button>
              </form>

              {/* Decorative Bottom Terracotta Clouds */}
              <div
                style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  height: '56px',
                  pointerEvents: 'none',
                  display: 'flex',
                  alignItems: 'flex-end',
                  zIndex: 0,
                  overflow: 'hidden',
                }}
              >
                <div style={{ position: 'absolute', left: '-20px', bottom: '-12px', width: '160px', height: '68px', backgroundColor: '#B2422D', borderRadius: '50% 50% 0 0' }} />
                <div style={{ position: 'absolute', right: '-20px', bottom: '-14px', width: '170px', height: '72px', backgroundColor: '#B2422D', borderRadius: '50% 50% 0 0' }} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ============================================================
          MODAL: ADMIN / DOCTOR AUTH
          ============================================================ */}
      {showAdminModal && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 100,
            backgroundColor: 'rgba(0, 0, 0, 0.65)',
            backdropFilter: 'blur(8px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px',
          }}
          onClick={() => setShowAdminModal(false)}
        >
          <div
            style={{
              width: '100%',
              maxWidth: '380px',
              backgroundColor: '#FEF0E1',
              color: '#4A1E14',
              borderRadius: '28px',
              padding: '28px',
              boxShadow: '0 20px 50px rgba(0, 0, 0, 0.35)',
              border: '2px solid rgba(178, 66, 45, 0.3)',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.6rem' }}>🛡️</span>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 900, color: '#B2422D', margin: 0 }}>
                  Bác sĩ / Quản trị viên
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setShowAdminModal(false)}
                style={{
                  width: '30px',
                  height: '30px',
                  borderRadius: '50%',
                  border: 'none',
                  backgroundColor: 'rgba(178, 66, 45, 0.15)',
                  color: '#B2422D',
                  fontWeight: 900,
                  cursor: 'pointer',
                }}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAdminSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {adminError && (
                <div style={{ padding: '8px 12px', borderRadius: '10px', backgroundColor: '#FEF2F2', border: '1px solid #FCA5A5', color: '#B91C1C', fontSize: '0.8rem', fontWeight: 600 }}>
                  ⚠️ {adminError}
                </div>
              )}

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, color: '#4A1E14', marginBottom: '4px' }}>
                  Tên tài khoản
                </label>
                <input
                  type="text"
                  value={adminUsername}
                  onChange={(e) => setAdminUsername(e.target.value)}
                  placeholder="admin"
                  required
                  style={{
                    width: '100%',
                    padding: '11px 14px',
                    borderRadius: '12px',
                    border: '1.5px solid rgba(178, 66, 45, 0.3)',
                    backgroundColor: '#FFFFFF',
                    fontSize: '0.95rem',
                    fontWeight: 600,
                    outline: 'none',
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, color: '#4A1E14', marginBottom: '4px' }}>
                  Mật khẩu
                </label>
                <input
                  type="password"
                  value={adminPassword}
                  onChange={(e) => setAdminPassword(e.target.value)}
                  placeholder="admin123"
                  required
                  style={{
                    width: '100%',
                    padding: '11px 14px',
                    borderRadius: '12px',
                    border: '1.5px solid rgba(178, 66, 45, 0.3)',
                    backgroundColor: '#FFFFFF',
                    fontSize: '0.95rem',
                    fontWeight: 600,
                    outline: 'none',
                  }}
                />
                <span style={{ fontSize: '0.72rem', color: '#78350F', marginTop: '4px', display: 'block' }}>
                  * Tài khoản thử nghiệm: <strong>admin</strong> / mật khẩu: <strong>admin123</strong>
                </span>
              </div>

              <button
                type="submit"
                style={{
                  marginTop: '6px',
                  width: '100%',
                  padding: '13px',
                  borderRadius: '9999px',
                  backgroundColor: '#B2422D',
                  color: '#FFFFFF',
                  border: 'none',
                  fontWeight: 800,
                  fontSize: '0.95rem',
                  cursor: 'pointer',
                  boxShadow: '0 6px 18px rgba(178, 66, 45, 0.35)',
                }}
              >
                Đăng Nhập Quản Trị
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {toastMessage && (
        <div
          style={{
            position: 'fixed',
            bottom: '24px',
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: '#4A1E14',
            color: '#FEF0E1',
            padding: '10px 22px',
            borderRadius: '9999px',
            fontSize: '0.88rem',
            fontWeight: 700,
            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.3)',
            zIndex: 150,
            animation: 'fadeIn 0.25s ease',
            whiteSpace: 'nowrap',
          }}
        >
          {toastMessage}
        </div>
      )}
    </div>
  );
}
