'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import AnimatedBrandLogo, { LogoMode, LogoTheme } from '@/components/AnimatedBrandLogo';

export default function AuthMobileShowcasePage() {
  const [activeScreen, setActiveScreen] = useState<'welcome' | 'login' | 'register' | 'forgot'>('welcome');
  const [logoMode, setLogoMode] = useState<LogoMode>('top-pill');
  const [logoTheme, setLogoTheme] = useState<LogoTheme>('cyan');
  const [showPassword, setShowPassword] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center py-8 px-4 font-sans">
      {/* Top Banner Navigation */}
      <div className="w-full max-w-4xl flex flex-wrap items-center justify-between gap-4 mb-6 bg-slate-900/90 border border-slate-800 p-4 rounded-2xl shadow-xl">
        <div className="flex items-center gap-3">
          <Link href="/" className="text-xs font-bold text-cyan-400 hover:underline">
            ❮ Về Trang chủ MotionIQ
          </Link>
          <span className="text-slate-600">|</span>
          <h1 className="text-sm font-bold text-white">MotionIQ Mobile Auth Showcase</h1>
        </div>

        {/* Screen Switcher */}
        <div className="flex items-center gap-1 bg-slate-800 p-1 rounded-xl">
          {(['welcome', 'login', 'register', 'forgot'] as const).map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => setActiveScreen(s)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                activeScreen === s
                  ? 'bg-amber-600 text-white shadow'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/60'
              }`}
            >
              {s === 'welcome' && '🍄 Chào mừng'}
              {s === 'login' && '🔑 Đăng nhập'}
              {s === 'register' && '📝 Tạo tài khoản'}
              {s === 'forgot' && '🕶️ Quên mật khẩu'}
            </button>
          ))}
        </div>
      </div>

      {/* Main Container: Mobile Frame + Controls */}
      <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        
        {/* Left: Mobile Mockup */}
        <div className="md:col-span-6 flex flex-col items-center">
          <div className="relative w-[340px] sm:w-[360px] h-[720px] bg-slate-900 rounded-[50px] p-3 shadow-2xl shadow-cyan-950/40 border-[4px] border-slate-700">
            
            {/* Viewport */}
            <div className="relative w-full h-full bg-[#FDF5E8] rounded-[42px] overflow-hidden flex flex-col select-none border border-stone-200">
              
              {/* Status Bar */}
              <div className="absolute top-0 left-0 right-0 z-40 px-6 pt-3 pb-1 flex items-center justify-between text-[11px] font-bold text-stone-700 pointer-events-none">
                <span>9:41</span>
                <div className="w-22 h-5 bg-black rounded-full flex items-center justify-end px-2 gap-1.5 shadow-sm">
                  <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                </div>
                <span>5G 100%</span>
              </div>

              {/* DYNAMIC LOGO INTEGRATION LAYER */}
              {logoMode === 'top-pill' && (
                <div className="absolute top-10 left-0 right-0 z-30 flex justify-center">
                  <AnimatedBrandLogo
                    mode="top-pill"
                    theme={logoTheme}
                    size={26}
                    onLogoClick={() => showToast('Đang phân tích chuyển động AI ✨')}
                  />
                </div>
              )}

              {logoMode === 'companion' && (
                <div
                  className="absolute z-30 pointer-events-auto"
                  style={{
                    top: activeScreen === 'welcome' ? '145px' : activeScreen === 'forgot' ? '230px' : '110px',
                    right: activeScreen === 'forgot' ? '40px' : '35px',
                  }}
                >
                  <AnimatedBrandLogo
                    mode="companion"
                    theme={logoTheme}
                    size={38}
                    onLogoClick={() => showToast('Quả cầu AI MotionIQ đồng hành 🌟')}
                  />
                </div>
              )}

              {logoMode === 'hero' && (
                <div className="absolute top-12 left-0 right-0 z-30 flex justify-center">
                  <AnimatedBrandLogo
                    mode="hero"
                    theme={logoTheme}
                    size={46}
                    onLogoClick={() => showToast('MotionIQ Core AI System')}
                  />
                </div>
              )}

              {/* ======================================================== */}
              {/* SCREEN 1: WELCOME                                        */}
              {/* ======================================================== */}
              {activeScreen === 'welcome' && (
                <div className="flex flex-col w-full h-full bg-[#FDF5E8] animate-in fade-in duration-300">
                  {/* Top Terracotta Card */}
                  <div className="relative bg-[#9E3B24] pt-14 pb-4 px-6 flex-1 flex flex-col items-center justify-between rounded-b-[40px] shadow-lg overflow-hidden">
                    <div className="absolute top-16 left-6 text-amber-200/60 text-lg">✦</div>
                    <div className="absolute top-20 right-8 text-amber-200/70 text-sm">✨</div>

                    <div className="text-center mt-3 z-10">
                      <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-wide drop-shadow-sm font-serif">
                        Xin chào
                      </h2>
                    </div>

                    <div className="relative my-auto z-10 flex flex-col items-center">
                      <div className="relative" style={{ animation: 'mascotBobbing 2.8s ease-in-out infinite' }}>
                        <Image
                          src="/images/custom-ui/mascot_welcome.png"
                          alt="Bé Nấm Chào Mừng"
                          width={216}
                          height={160}
                          unoptimized
                          className="w-48 sm:w-52 h-auto object-contain drop-shadow-md rounded-2xl"
                        />
                      </div>
                    </div>
                    <div className="h-2"></div>
                  </div>

                  {/* Bottom Cream Section */}
                  <div className="relative px-7 py-6 flex flex-col justify-center gap-3.5 z-10">
                    <button
                      type="button"
                      onClick={() => setActiveScreen('login')}
                      className="w-full py-3.5 px-6 rounded-full bg-[#9E3B24] hover:bg-[#862F1B] active:scale-95 text-white font-bold text-base shadow-md transition-all flex items-center justify-center gap-2"
                    >
                      <span>Tôi đã có tài khoản</span>
                      <span>➔</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => setActiveScreen('register')}
                      className="w-full py-3.5 px-6 rounded-full bg-white hover:bg-stone-50 active:scale-95 text-[#9E3B24] border-2 border-[#9E3B24] font-bold text-base shadow-sm transition-all flex items-center justify-center gap-2"
                    >
                      <span>Tạo tài khoản</span>
                    </button>

                    {/* Bottom Clouds */}
                    <div className="absolute bottom-0 left-0 right-0 pointer-events-none overflow-hidden h-14">
                      <svg
                        className="w-full h-full"
                        style={{ animation: 'cloudSwaying 6s ease-in-out infinite' }}
                        viewBox="0 0 360 60"
                        fill="none"
                        preserveAspectRatio="none"
                      >
                        <path d="M-20 60 C30 15, 90 20, 130 60 C170 20, 240 10, 280 60 C320 25, 370 25, 400 60 Z" fill="#9E3B24"/>
                      </svg>
                    </div>
                  </div>
                </div>
              )}

              {/* ======================================================== */}
              {/* SCREEN 2: LOGIN                                          */}
              {/* ======================================================== */}
              {activeScreen === 'login' && (
                <div className="flex flex-col w-full h-full bg-[#FDF5E8] animate-in fade-in duration-300">
                  <div className="pt-12 px-6 pb-2 flex flex-col z-10">
                    <button
                      type="button"
                      onClick={() => setActiveScreen('welcome')}
                      className="self-start flex items-center gap-1 text-xs font-bold text-[#9E3B24] hover:underline mb-2 py-1"
                    >
                      <span>❮</span> <span>Trở về</span>
                    </button>
                    <h2 className="text-2xl font-black text-[#9E3B24] leading-tight text-center">
                      Chào mừng<br />trở lại
                    </h2>
                  </div>

                  {/* Peeking Mascot */}
                  <div className="relative z-20 flex justify-center -mb-8">
                    <div style={{ animation: 'mascotBobbing 2.8s ease-in-out infinite' }}>
                      <Image
                        src="/images/custom-ui/mascot_login.png"
                        alt="Bé Nấm Đăng Nhập"
                        width={125}
                        height={105}
                        unoptimized
                        className="w-24 h-auto object-contain drop-shadow-md"
                      />
                    </div>
                  </div>

                  {/* Terracotta Form Card */}
                  <div className="relative bg-[#9E3B24] flex-1 rounded-t-[36px] pt-10 px-7 pb-6 flex flex-col justify-between shadow-2xl z-10">
                    <div className="flex flex-col gap-3.5">
                      <div>
                        <label className="block text-xs font-semibold text-white/90 mb-1 pl-1">Nhập tên</label>
                        <input
                          type="text"
                          defaultValue="Bác Minh"
                          placeholder="Tên của bạn..."
                          className="w-full px-4 py-3 rounded-full bg-[#AF533E] text-white border border-white/20 focus:outline-none focus:ring-2 focus:ring-white/40 text-sm"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-white/90 mb-1 pl-1">Mật khẩu</label>
                        <div className="relative">
                          <input
                            type={showPassword ? 'text' : 'password'}
                            defaultValue="123456"
                            placeholder="Mật khẩu..."
                            className="w-full px-4 py-3 rounded-full bg-[#AF533E] text-white border border-white/20 focus:outline-none focus:ring-2 focus:ring-white/40 text-sm pr-10"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-white/80 hover:text-white text-xs"
                          >
                            {showPassword ? '🙈' : '👁️'}
                          </button>
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={() => showToast('Đăng nhập thành công! 🎉')}
                        className="w-full mt-2 py-3.5 px-6 rounded-full bg-[#FAF0DF] hover:bg-white active:scale-95 text-[#9E3B24] font-extrabold text-sm tracking-wider shadow-md transition-all uppercase"
                      >
                        ĐĂNG NHẬP
                      </button>

                      <div className="text-center mt-1">
                        <button
                          type="button"
                          onClick={() => setActiveScreen('forgot')}
                          className="text-xs italic text-white/90 hover:text-white hover:underline"
                        >
                          Quên mật khẩu?
                        </button>
                      </div>
                    </div>

                    {/* Bottom Clouds */}
                    <div className="absolute bottom-0 left-0 right-0 pointer-events-none overflow-hidden h-14">
                      <svg
                        className="w-full h-full"
                        style={{ animation: 'cloudSwaying 6s ease-in-out infinite' }}
                        viewBox="0 0 360 60"
                        fill="none"
                        preserveAspectRatio="none"
                      >
                        <path d="M-20 60 C40 10, 100 20, 140 60 C180 15, 250 15, 290 60 C330 20, 380 20, 410 60 Z" fill="#FDF5E8"/>
                      </svg>
                    </div>
                  </div>
                </div>
              )}

              {/* ======================================================== */}
              {/* SCREEN 3: REGISTER                                       */}
              {/* ======================================================== */}
              {activeScreen === 'register' && (
                <div className="flex flex-col w-full h-full bg-[#FDF5E8] animate-in fade-in duration-300">
                  <div className="pt-12 px-6 pb-1 flex flex-col z-10">
                    <button
                      type="button"
                      onClick={() => setActiveScreen('welcome')}
                      className="self-start flex items-center gap-1 text-xs font-bold text-[#9E3B24] hover:underline mb-2 py-1"
                    >
                      <span>❮</span> <span>Trở về</span>
                    </button>
                    <h2 className="text-2xl font-black text-[#9E3B24] leading-tight text-center">
                      Tạo tài khoản
                    </h2>
                  </div>

                  <div className="relative z-20 flex justify-center -mb-8">
                    <div style={{ animation: 'mascotBobbing 2.8s ease-in-out infinite' }}>
                      <Image
                        src="/images/custom-ui/mascot_register.png"
                        alt="Bé Nấm Tạo Tài Khoản"
                        width={138}
                        height={100}
                        unoptimized
                        className="w-24 h-auto object-contain drop-shadow-md"
                      />
                    </div>
                  </div>

                  <div className="relative bg-[#9E3B24] flex-1 rounded-t-[36px] pt-9 px-7 pb-6 flex flex-col justify-between shadow-2xl z-10">
                    <div className="flex flex-col gap-2.5">
                      <div>
                        <label className="block text-xs font-semibold text-white/90 mb-0.5 pl-1">Nhập tên</label>
                        <input
                          type="text"
                          placeholder="Họ và tên..."
                          className="w-full px-4 py-2 rounded-full bg-[#AF533E] text-white border border-white/20 focus:outline-none focus:ring-2 focus:ring-white/40 text-sm"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-white/90 mb-0.5 pl-1">Số điện thoại</label>
                        <input
                          type="tel"
                          placeholder="090 123 4567..."
                          className="w-full px-4 py-2 rounded-full bg-[#AF533E] text-white border border-white/20 focus:outline-none focus:ring-2 focus:ring-white/40 text-sm"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-white/90 mb-0.5 pl-1">Mật khẩu</label>
                        <input
                          type="password"
                          placeholder="Tạo mật khẩu..."
                          className="w-full px-4 py-2 rounded-full bg-[#AF533E] text-white border border-white/20 focus:outline-none focus:ring-2 focus:ring-white/40 text-sm"
                        />
                      </div>

                      <div className="flex items-center gap-2 mt-1">
                        <input type="checkbox" id="reg-terms" defaultChecked className="accent-amber-400 w-4 h-4 rounded" />
                        <label htmlFor="reg-terms" className="text-[11px] italic text-white/90 cursor-pointer">
                          Tôi đồng ý với các <u>điều khoản</u>.
                        </label>
                      </div>

                      <button
                        type="button"
                        onClick={() => showToast('Tạo tài khoản thành công! 🎉')}
                        className="w-full mt-1 py-3 px-6 rounded-full bg-[#FAF0DF] hover:bg-white active:scale-95 text-[#9E3B24] font-extrabold text-sm tracking-wider shadow-md transition-all uppercase"
                      >
                        ĐĂNG KÝ
                      </button>
                    </div>

                    <div className="absolute bottom-0 left-0 right-0 pointer-events-none overflow-hidden h-12">
                      <svg
                        className="w-full h-full"
                        style={{ animation: 'cloudSwaying 6s ease-in-out infinite' }}
                        viewBox="0 0 360 60"
                        fill="none"
                        preserveAspectRatio="none"
                      >
                        <path d="M-20 60 C40 10, 100 20, 140 60 C180 15, 250 15, 290 60 C330 20, 380 20, 410 60 Z" fill="#FDF5E8"/>
                      </svg>
                    </div>
                  </div>
                </div>
              )}

              {/* ======================================================== */}
              {/* SCREEN 4: FORGOT PASSWORD                                */}
              {/* ======================================================== */}
              {activeScreen === 'forgot' && (
                <div className="flex flex-col w-full h-full bg-[#FDF5E8] animate-in fade-in duration-300">
                  <div className="relative bg-[#9E3B24] pt-12 pb-2 px-6 flex-1 flex flex-col items-center justify-between rounded-b-[40px] shadow-lg">
                    <button
                      type="button"
                      onClick={() => setActiveScreen('login')}
                      className="self-start flex items-center gap-1 text-xs font-bold text-white/90 hover:text-white py-1 z-10"
                    >
                      <span>❮</span> <span>Trở về</span>
                    </button>

                    <div className="text-center z-10 -mt-2">
                      <span className="block text-lg font-bold text-white/90">Oh No!</span>
                      <h2 className="text-xl sm:text-2xl font-black text-white leading-tight">
                        Mật khẩu của tôi
                      </h2>
                    </div>

                    <div className="relative my-auto z-10 flex flex-col items-center">
                      <div className="relative" style={{ animation: 'mascotBobbing 2.8s ease-in-out infinite' }}>
                        <Image
                          src="/images/custom-ui/mascot_forgot.png"
                          alt="Bé Nấm Quên Mật Khẩu"
                          width={168}
                          height={180}
                          unoptimized
                          className="w-40 sm:w-44 h-auto object-contain drop-shadow-md"
                        />
                        <div className="absolute top-2 right-4 text-red-300 text-base font-black animate-ping">💢</div>
                      </div>
                    </div>
                    <div className="h-1"></div>
                  </div>

                  <div className="relative px-7 py-5 flex flex-col justify-between z-10 flex-shrink-0">
                    <p className="text-center text-[12px] text-[#9E3B24] font-medium leading-relaxed px-2">
                      Đừng lo, chuyện này ai cũng có thể gặp phải! Nhập số điện thoại của bạn để đặt lại mật khẩu!
                    </p>

                    <div className="my-3 flex flex-col gap-2.5">
                      <input
                        type="tel"
                        placeholder="Số điện thoại..."
                        className="w-full px-4 py-3 rounded-full bg-white text-[#4A1E14] border-2 border-[#9E3B24] text-center font-medium text-sm focus:outline-none focus:ring-2 focus:ring-[#9E3B24]/40"
                      />

                      <button
                        type="button"
                        onClick={() => showToast('Mã khôi phục đã được gửi qua SMS!')}
                        className="w-full py-3.5 px-6 rounded-full bg-[#9E3B24] hover:bg-[#862F1B] active:scale-95 text-white font-extrabold text-sm tracking-wider shadow-md transition-all uppercase"
                      >
                        GỬI
                      </button>
                    </div>

                    <div className="absolute bottom-0 left-0 right-0 pointer-events-none overflow-hidden h-14">
                      <svg
                        className="w-full h-full"
                        style={{ animation: 'cloudSwaying 6s ease-in-out infinite' }}
                        viewBox="0 0 360 60"
                        fill="none"
                        preserveAspectRatio="none"
                      >
                        <path d="M-20 60 C30 15, 90 20, 130 60 C170 20, 240 10, 280 60 C320 25, 370 25, 400 60 Z" fill="#9E3B24"/>
                      </svg>
                    </div>
                  </div>
                </div>
              )}

              {/* Toast */}
              {toastMessage && (
                <div className="absolute bottom-6 left-5 right-5 z-50 bg-slate-900/95 text-white text-xs font-semibold px-4 py-3 rounded-2xl shadow-2xl border border-cyan-500/40 flex items-center gap-2 animate-in fade-in slide-in-from-bottom-4">
                  <span className="text-cyan-400">✨</span>
                  <span>{toastMessage}</span>
                </div>
              )}

            </div>
          </div>
        </div>

        {/* Right: Studio Controls */}
        <div className="md:col-span-6 flex flex-col gap-6">
          <div className="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-xl">
            <h2 className="text-base font-bold text-white mb-2">Tuỳ chỉnh vị trí Logo</h2>
            <p className="text-xs text-slate-400 mb-4">
              Lựa chọn vị trí chèn logo MotionIQ phù hợp nhất với bố cục giao diện
            </p>

            <div className="flex flex-col gap-3">
              <button
                type="button"
                onClick={() => setLogoMode('top-pill')}
                className={`p-3.5 rounded-2xl text-left border transition-all ${
                  logoMode === 'top-pill'
                    ? 'border-cyan-400 bg-cyan-950/40 text-cyan-200 shadow'
                    : 'border-slate-700 bg-slate-800/40 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <div className="text-xs font-bold mb-1">💎 Thanh Đỉnh Kính Mờ (Top Brand Capsule) - Đề xuất</div>
                <div className="text-[11px] text-slate-400">
                  Logo thu nhỏ nằm trên Header, không che khuất Bé Nấm và giữ trải nghiệm nhất quán.
                </div>
              </button>

              <button
                type="button"
                onClick={() => setLogoMode('companion')}
                className={`p-3.5 rounded-2xl text-left border transition-all ${
                  logoMode === 'companion'
                    ? 'border-cyan-400 bg-cyan-950/40 text-cyan-200 shadow'
                    : 'border-slate-700 bg-slate-800/40 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <div className="text-xs font-bold mb-1">🔮 Quả Cầu Năng Lượng (Mascot Companion Orb)</div>
                <div className="text-[11px] text-slate-400">
                  Logo lơ lửng cạnh Bé Nấm như bảo bối AI đồng hành cùng người tập.
                </div>
              </button>

              <button
                type="button"
                onClick={() => setLogoMode('hero')}
                className={`p-3.5 rounded-2xl text-left border transition-all ${
                  logoMode === 'hero'
                    ? 'border-cyan-400 bg-cyan-950/40 text-cyan-200 shadow'
                    : 'border-slate-700 bg-slate-800/40 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <div className="text-xs font-bold mb-1">👑 Huy Hiệu Trung Tâm (Hero Center Emblem)</div>
                <div className="text-[11px] text-slate-400">
                  Tập trung nhận diện thương hiệu mạnh mẽ ngay đỉnh đầu màn hình.
                </div>
              </button>
            </div>
          </div>

          {/* Color Switcher */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-xl">
            <h2 className="text-base font-bold text-white mb-2">Hòa sắc Logo (Theme Harmony)</h2>
            <div className="grid grid-cols-2 gap-3 mt-3">
              <button
                type="button"
                onClick={() => setLogoTheme('cyan')}
                className={`p-3 rounded-2xl text-left border text-xs font-bold transition-all ${
                  logoTheme === 'cyan'
                    ? 'border-cyan-400 bg-cyan-950/50 text-cyan-300'
                    : 'border-slate-700 bg-slate-800/40 text-slate-400'
                }`}
              >
                🔵 Xanh Cyan Gốc (High-contrast)
              </button>

              <button
                type="button"
                onClick={() => setLogoTheme('autumn-gold')}
                className={`p-3 rounded-2xl text-left border text-xs font-bold transition-all ${
                  logoTheme === 'autumn-gold'
                    ? 'border-amber-400 bg-amber-950/50 text-amber-300'
                    : 'border-slate-700 bg-slate-800/40 text-slate-400'
                }`}
              >
                🟡 Vàng Hoàng Kim (Tiệp màu Nấm)
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

