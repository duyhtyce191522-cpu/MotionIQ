'use client';

import { useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { getAuthSession, logout, AuthSession } from '@/features/auth/authService';

export default function HeaderNav() {
  const router = useRouter();
  const pathname = usePathname();
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<AuthSession | null>(null);

  useEffect(() => {
    setMounted(true);
    // Kiểm tra cài đặt theme đã lưu trong localStorage hoặc hệ thống
    const savedTheme = localStorage.getItem('motioniq_theme') as 'dark' | 'light' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
    }

    // Gatekeeper: Check Auth Session
    const currentSession = getAuthSession();
    setSession(currentSession);
    if (!currentSession && pathname !== '/login') {
      router.push('/login');
    }
  }, [router, pathname]);

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    localStorage.setItem('motioniq_theme', nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  const navItems = [
    { label: '🏋️ Bài tập', path: '/exercises' },
    { label: '📊 Lịch sử', path: '/history' },
    { label: '⚙️ Cài đặt', path: '/settings' },
  ];

  if (session?.role === 'admin') {
    navItems.push({ label: '🛡️ Quản trị', path: '/admin' });
  }

  return (
    <header className="header-nav-container">
      <div className="header-nav-inner">
        {/* Logo / Brand */}
        <div
          className="header-brand"
          onClick={() => router.push(session?.role === 'admin' ? '/admin' : '/')}
          role="button"
          tabIndex={0}
          title="Trang chủ MotionIQ"
        >
          <span className="header-brand-icon">🏃‍♂️</span>
          <span className="header-brand-text">MotionIQ</span>
        </div>

        {/* Navigation Links + User + Theme Switcher */}
        <div className="header-nav-actions">
          <nav className="header-nav-links">
            {navItems.map((item) => {
              const isActive = pathname === item.path;
              return (
                <button
                  key={item.path}
                  type="button"
                  className={`nav-pill-btn ${isActive ? 'active' : ''}`}
                  onClick={() => router.push(item.path)}
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* User Profile Pill & Logout */}
          {session && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <div
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  background: session.role === 'admin' ? 'rgba(139, 92, 246, 0.15)' : 'rgba(6, 182, 212, 0.15)',
                  border: `1px solid ${session.role === 'admin' ? 'rgba(139, 92, 246, 0.4)' : 'rgba(6, 182, 212, 0.4)'}`,
                  padding: '4px 10px',
                  borderRadius: 'var(--radius-full)',
                  fontSize: 'var(--font-size-xs)',
                  fontWeight: 600,
                  color: 'var(--color-text-primary)',
                }}
                title={session.role === 'admin' ? 'Đang đăng nhập với vai trò Quản trị viên' : `Người tập: ${session.user.name}`}
              >
                <span>{session.user.avatarIcon || '👤'}</span>
                <span style={{ maxWidth: '110px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {session.role === 'admin' ? 'Admin' : session.user.name.split(' ').slice(-2).join(' ')}
                </span>
              </div>

              <button
                type="button"
                className="nav-pill-btn"
                style={{
                  padding: '4px 8px',
                  fontSize: '11px',
                  color: '#f87171',
                  borderColor: 'rgba(239, 68, 68, 0.3)',
                }}
                onClick={handleLogout}
                title="Đăng xuất / Đổi người tập"
              >
                🚪 Thoát
              </button>
            </div>
          )}

          {/* Theme Toggle Button */}
          {mounted && (
            <button
              id="theme-toggle-btn"
              type="button"
              className="theme-toggle-btn"
              onClick={toggleTheme}
              title={theme === 'dark' ? 'Chuyển sang Chế độ Sáng Rõ Nét' : 'Chuyển sang Chế độ Tối Sang Trọng'}
              aria-label="Đổi giao diện sáng tối"
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
          )}
        </div>
      </div>
    </header>
  );
}
