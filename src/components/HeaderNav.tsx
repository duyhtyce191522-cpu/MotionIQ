'use client';

import { useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { getAuthSession, logout, AuthSession } from '@/features/auth/authService';
import AnimatedBrandLogo from '@/components/AnimatedBrandLogo';

export default function HeaderNav() {
  const router = useRouter();
  const pathname = usePathname();
  const [theme, setTheme] = useState<'dark' | 'light'>('light');
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<AuthSession | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  useEffect(() => {
    setMounted(true);
    const savedTheme = localStorage.getItem('motioniq_theme') as 'dark' | 'light' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
      setTheme('light');
      document.documentElement.setAttribute('data-theme', 'light');
    }

    const currentSession = getAuthSession();
    setSession(currentSession);
    if (!currentSession && pathname !== '/login') {
      router.push('/login');
    }
  }, [router, pathname]);

  // Lock body scroll when drawer is open
  useEffect(() => {
    if (isDrawerOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isDrawerOpen]);

  // Close drawer on ESC key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsDrawerOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    localStorage.setItem('motioniq_theme', nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  const handleLogout = () => {
    setIsDrawerOpen(false);
    logout();
    router.push('/login');
  };

  const handleNavigate = (path: string) => {
    setIsDrawerOpen(false);
    router.push(path);
  };

  const menuSections = [
    {
      id: 'home',
      label: 'Trang chủ / Dashboard',
      icon: '🏠',
      desc: 'Tiến độ phục hồi, mục tiêu & KPI',
      path: '/',
    },
    {
      id: 'exercises',
      label: 'Phòng tập AI (4 Bài tập)',
      icon: '🏋️',
      desc: 'Đứng-Ngồi, Squat, Dạng vai, Nâng chân',
      path: '/exercises',
      badge: 'UI-PRMD',
    },
    {
      id: 'history',
      label: 'Lịch sử & Báo cáo Y sinh',
      icon: '📈',
      desc: 'Biểu đồ góc ROM & Xuất báo cáo PDF',
      path: '/history',
    },
    {
      id: 'settings',
      label: 'Cài đặt & Giọng nói AI',
      icon: '⚙️',
      desc: 'Âm thanh, đếm nhịp & tốc độ đọc',
      path: '/settings',
    },
  ];

  if (session?.role === 'admin') {
    menuSections.push({
      id: 'admin',
      label: 'Bác sĩ / Quản trị viên',
      icon: '🛡️',
      desc: 'Bảng điều khiển & Chỉ định bài tập',
      path: '/admin',
      badge: 'Admin',
    });
  }

  return (
    <>
      <header
        style={{
          width: '100%',
          position: 'sticky',
          top: 0,
          zIndex: 80,
          backgroundColor: theme === 'dark' ? 'rgba(11, 19, 41, 0.92)' : 'rgba(250, 240, 223, 0.95)',
          backdropFilter: 'blur(16px)',
          borderBottom: theme === 'dark' ? '1px solid rgba(148, 163, 184, 0.2)' : '1px solid rgba(158, 59, 36, 0.2)',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.05)',
          transition: 'all 0.25s ease',
        }}
      >
        <div
          style={{
            width: '100%',
            maxWidth: '430px',
            margin: '0 auto',
            padding: '8px 12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '8px',
          }}
        >
          {/* ========================================================
              LEFT: HAMBURGER (3 GẠCH) + LOGO + BRAND NAME
              ======================================================== */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {/* Hamburger Button (3 Gạch ☰) */}
            <button
              type="button"
              onClick={() => setIsDrawerOpen(true)}
              style={{
                width: '38px',
                height: '38px',
                borderRadius: '12px',
                backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.08)' : 'rgba(158, 59, 36, 0.1)',
                border: theme === 'dark' ? '1px solid rgba(255, 255, 255, 0.15)' : '1px solid rgba(158, 59, 36, 0.25)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '4px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                padding: 0,
                flexShrink: 0,
              }}
              title="Mở menu chức năng (3 gạch)"
              aria-label="Mở danh mục chức năng"
            >
              <span
                style={{
                  width: '18px',
                  height: '2px',
                  backgroundColor: theme === 'dark' ? '#38bdf8' : '#9E3B24',
                  borderRadius: '2px',
                  transition: 'all 0.2s ease',
                }}
              />
              <span
                style={{
                  width: '13px',
                  height: '2px',
                  backgroundColor: theme === 'dark' ? '#38bdf8' : '#9E3B24',
                  borderRadius: '2px',
                  alignSelf: 'center',
                  transition: 'all 0.2s ease',
                }}
              />
              <span
                style={{
                  width: '18px',
                  height: '2px',
                  backgroundColor: theme === 'dark' ? '#38bdf8' : '#9E3B24',
                  borderRadius: '2px',
                  transition: 'all 0.2s ease',
                }}
              />
            </button>

            {/* Brand Logo & Name */}
            <div
              onClick={() => router.push(session?.role === 'admin' ? '/admin' : '/')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
                userSelect: 'none',
              }}
              role="button"
              tabIndex={0}
              title="Trang chủ MotionIQ"
            >
              <AnimatedBrandLogo mode="minimal" size={28} />
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span
                  style={{
                    fontSize: '1.15rem',
                    fontWeight: 900,
                    letterSpacing: '-0.3px',
                    color: theme === 'dark' ? '#38bdf8' : '#9E3B24',
                    lineHeight: 1.1,
                  }}
                >
                  MotionIQ
                </span>
                <span
                  style={{
                    fontSize: '0.58rem',
                    fontWeight: 800,
                    color: theme === 'dark' ? 'rgba(255,255,255,0.6)' : 'rgba(158, 59, 36, 0.7)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.6px',
                  }}
                >
                  AI Care
                </span>
              </div>
            </div>
          </div>

          {/* ========================================================
              RIGHT: ACTIVE USER PILL + THEME TOGGLE
              ======================================================== */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>

            {/* User Profile Pill */}
            {session && (
              <div
                onClick={() => setIsDrawerOpen(true)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.08)' : '#FFFFFF',
                  border: theme === 'dark' ? '1px solid rgba(255, 255, 255, 0.15)' : '1.5px solid rgba(158, 59, 36, 0.25)',
                  padding: '4px 8px',
                  borderRadius: '9999px',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  color: theme === 'dark' ? '#FFFFFF' : '#9E3B24',
                  boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                  cursor: 'pointer',
                }}
                title="Bấm để xem hồ sơ và menu chức năng"
              >
                <span style={{ fontSize: '1rem' }}>{session.user.avatarIcon || '👤'}</span>
                <span style={{ maxWidth: '65px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {session.role === 'admin' ? 'Admin' : session.user.name.split(' ').slice(-1)[0]}
                </span>
              </div>
            )}

            {/* Theme Toggle Button */}
            {mounted && (
              <button
                type="button"
                onClick={toggleTheme}
                style={{
                  width: '38px',
                  height: '38px',
                  borderRadius: '50%',
                  backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.08)' : 'rgba(158, 59, 36, 0.1)',
                  border: 'none',
                  fontSize: '1rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transition: 'all 0.2s ease',
                }}
                title={theme === 'dark' ? 'Chuyển sang Chế độ Ấm Áp' : 'Chuyển sang Chế độ Tối'}
              >
                {theme === 'dark' ? '☀️' : '🌙'}
              </button>
            )}
          </div>
        </div>
      </header>

      {/* ============================================================
          SIDEBAR NAVIGATION DRAWER (MENU TRƯỢT TỪ BÊN TRÁI)
          ============================================================ */}
      {isDrawerOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 999,
            backgroundColor: 'rgba(0, 0, 0, 0.65)',
            backdropFilter: 'blur(8px)',
            display: 'flex',
            animation: 'fadeIn 0.2s ease',
          }}
          onClick={() => setIsDrawerOpen(false)}
        >
          {/* Drawer Panel */}
          <div
            style={{
              width: '100%',
              maxWidth: '340px',
              height: '100%',
              backgroundColor: theme === 'dark' ? '#0B1329' : '#FAF0DF',
              color: theme === 'dark' ? '#F8FAFC' : '#4A1E14',
              boxShadow: '10px 0 40px rgba(0, 0, 0, 0.4)',
              display: 'flex',
              flexDirection: 'column',
              overflowY: 'auto',
              animation: 'slideInLeft 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
              position: 'relative',
              borderRight: theme === 'dark' ? '1px solid rgba(6, 182, 212, 0.3)' : '2px solid rgba(158, 59, 36, 0.25)',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Drawer Header */}
            <div
              style={{
                padding: '24px 20px 16px 20px',
                borderBottom: theme === 'dark' ? '1px solid rgba(255, 255, 255, 0.1)' : '1px solid rgba(158, 59, 36, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <AnimatedBrandLogo mode="minimal" size={36} />
                <div>
                  <h2 style={{ fontSize: '1.2rem', fontWeight: 900, margin: 0, color: theme === 'dark' ? '#38BDF8' : '#9E3B24' }}>
                    Menu Chức Năng
                  </h2>
                  <span style={{ fontSize: '0.72rem', color: theme === 'dark' ? '#94A3B8' : '#78350F' }}>
                    MotionIQ • AI Elderly Care
                  </span>
                </div>
              </div>

              <button
                type="button"
                onClick={() => setIsDrawerOpen(false)}
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(158, 59, 36, 0.15)',
                  border: 'none',
                  color: theme === 'dark' ? '#FFFFFF' : '#9E3B24',
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                ✕
              </button>
            </div>

            {/* Active Patient Card Inside Drawer */}
            {session && (
              <div
                style={{
                  margin: '16px 16px 8px 16px',
                  padding: '16px',
                  borderRadius: '20px',
                  backgroundColor: theme === 'dark' ? 'rgba(15, 28, 63, 0.8)' : '#FFFFFF',
                  border: theme === 'dark' ? '1px solid rgba(6, 182, 212, 0.3)' : '1.5px solid rgba(158, 59, 36, 0.2)',
                  boxShadow: '0 4px 14px rgba(0, 0, 0, 0.06)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div
                    style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '50%',
                      backgroundColor: theme === 'dark' ? 'rgba(6, 182, 212, 0.2)' : '#FAF0DF',
                      fontSize: '1.8rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    {session.user.avatarIcon || '👴'}
                  </div>

                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: 800, fontSize: '0.95rem', color: theme === 'dark' ? '#FFFFFF' : '#9E3B24', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {session.user.name}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: theme === 'dark' ? '#94A3B8' : '#78350F' }}>
                      {session.role === 'admin' ? '🛡️ Quản trị viên y tế' : '🏃‍♂️ Người tập phục hồi'}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Main Menu Items */}
            <div style={{ flex: 1, padding: '12px 16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 800, textTransform: 'uppercase', color: theme === 'dark' ? '#94A3B8' : 'rgba(158, 59, 36, 0.7)', letterSpacing: '0.5px', paddingLeft: '4px' }}>
                Danh mục chức năng
              </span>

              {menuSections.map((item) => {
                const isActive = pathname === item.path;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => handleNavigate(item.path)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '14px',
                      padding: '12px 14px',
                      borderRadius: '16px',
                      border: isActive
                        ? theme === 'dark' ? '1.5px solid #06B6D4' : '2px solid #9E3B24'
                        : '1px solid transparent',
                      backgroundColor: isActive
                        ? theme === 'dark' ? 'rgba(6, 182, 212, 0.18)' : '#FFFFFF'
                        : theme === 'dark' ? 'rgba(255, 255, 255, 0.03)' : 'rgba(255, 255, 255, 0.45)',
                      color: isActive
                        ? theme === 'dark' ? '#38BDF8' : '#9E3B24'
                        : theme === 'dark' ? '#E2E8F0' : '#4A1E14',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.2s ease',
                      boxShadow: isActive ? '0 4px 12px rgba(158, 59, 36, 0.1)' : 'none',
                    }}
                  >
                    <span style={{ fontSize: '1.5rem', flexShrink: 0 }}>{item.icon}</span>

                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontWeight: 800, fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span>{item.label}</span>
                        {item.badge && (
                          <span
                            style={{
                              fontSize: '0.65rem',
                              padding: '1px 6px',
                              borderRadius: '4px',
                              backgroundColor: theme === 'dark' ? 'rgba(6, 182, 212, 0.25)' : '#9E3B24',
                              color: '#FFFFFF',
                            }}
                          >
                            {item.badge}
                          </span>
                        )}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: theme === 'dark' ? '#94A3B8' : '#78350F', marginTop: '1px' }}>
                        {item.desc}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Drawer Footer: Hotline & Logout */}
            <div
              style={{
                padding: '16px',
                borderTop: theme === 'dark' ? '1px solid rgba(255, 255, 255, 0.1)' : '1px solid rgba(158, 59, 36, 0.15)',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
              }}
            >
              {/* Emergency Hotline for seniors */}
              <div
                style={{
                  padding: '10px 14px',
                  borderRadius: '14px',
                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                  border: '1px solid rgba(239, 68, 68, 0.3)',
                  color: '#EF4444',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
              >
                <span>📞</span>
                <span>Cấp cứu y tế & Người thân: <strong>115</strong></span>
              </div>

              {/* Logout Button */}
              <button
                type="button"
                onClick={handleLogout}
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '9999px',
                  backgroundColor: theme === 'dark' ? 'rgba(255, 255, 255, 0.08)' : '#FFFFFF',
                  color: '#EF4444',
                  border: '1.5px solid rgba(239, 68, 68, 0.3)',
                  fontWeight: 800,
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                }}
              >
                <span>🚪</span>
                <span>Đổi người tập / Đăng xuất</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
