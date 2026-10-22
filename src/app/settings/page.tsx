'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  getPatientProfile,
  savePatientProfile,
  PatientProfile,
  getDailyGoal,
  setDailyGoal,
  getHistoryEntries,
  clearAllHistory,
} from '@/features/storage/storageService';
import { SpeechService } from '@/features/feedback/speechService';
import HeaderNav from '@/components/HeaderNav';

export default function SettingsPage() {
  const router = useRouter();
  const [profile, setProfile] = useState<PatientProfile>({
    name: '',
    age: 65,
    gender: 'male',
    condition: '',
    therapist: '',
    emergencyContact: '115',
    speechSpeed: 'slow',
  });
  const [dailyGoal, setDailyGoalVal] = useState<number>(10);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [isTestingVoice, setIsTestingVoice] = useState(false);

  useEffect(() => {
    setProfile(getPatientProfile());
    setDailyGoalVal(getDailyGoal());
  }, []);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    savePatientProfile(profile);
    setDailyGoal(dailyGoal);
    showToast('✅ Đã lưu cài đặt và hồ sơ thành công!');
  };

  const handleTestVoice = () => {
    setIsTestingVoice(true);
    const speech = new SpeechService();
    const nameToSay = profile.name ? profile.name : 'Bác';
    speech.speak(`Xin chào ${nameToSay}! MotionIQ luôn sẵn sàng đồng hành cùng bác trong mỗi buổi tập.`, true);
    setTimeout(() => setIsTestingVoice(false), 3500);
  };

  const handleExportData = () => {
    const history = getHistoryEntries();
    const fullData = {
      profile,
      dailyGoal,
      exportedAt: new Date().toISOString(),
      workoutHistory: history,
    };
    const jsonStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(fullData, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', jsonStr);
    downloadAnchor.setAttribute('download', `MotionIQ_BaoCao_${profile.name.replace(/\s+/g, '_') || 'NguoiTap'}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    showToast('📥 Đã xuất tệp dữ liệu JSON thành công!');
  };

  const handleClearData = () => {
    clearAllHistory();
    setShowClearConfirm(false);
    showToast('🗑️ Đã xóa toàn bộ dữ liệu lịch sử tập luyện.');
  };

  return (
    <div className="page">
      <HeaderNav />
      <div className="container page-content" style={{ maxWidth: '680px' }}>
        <button className="back-nav" onClick={() => router.push('/')}>
          ← Trang chủ
        </button>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
          <h1>⚙️ Cài đặt & Hồ sơ</h1>
        </div>
        <p className="text-muted" style={{ marginBottom: 'var(--space-6)' }}>
          Cá nhân hóa hồ sơ người tập, giọng nói hướng dẫn và an toàn khẩn cấp
        </p>

        <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
          {/* Card 1: Thông tin người tập */}
          <div className="card" style={{ padding: 'var(--space-5)' }}>
            <h2 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>👤</span> Thông tin người tập
            </h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
                  Họ và tên / Tên thân mật
                </label>
                <input
                  type="text"
                  className="input-field"
                  placeholder="Ví dụ: Bác Nguyễn Văn An"
                  value={profile.name}
                  onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                />
                <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '4px', display: 'block' }}>
                  Giọng nói AI sẽ chào bác bằng tên này khi bắt đầu bài tập.
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)' }}>
                <div>
                  <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
                    Tuổi
                  </label>
                  <input
                    type="number"
                    min={10}
                    max={120}
                    className="input-field"
                    value={profile.age}
                    onChange={(e) => setProfile({ ...profile, age: parseInt(e.target.value, 10) || 60 })}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
                    Giới tính
                  </label>
                  <select
                    className="select-field"
                    value={profile.gender}
                    onChange={(e) => setProfile({ ...profile, gender: e.target.value as any })}
                  >
                    <option value="male">Nam</option>
                    <option value="female">Nữ</option>
                    <option value="other">Khác</option>
                  </select>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
                  Mục đích / Tình trạng vận động
                </label>
                <input
                  type="text"
                  className="input-field"
                  placeholder="Ví dụ: Tập sau tai biến / Tăng thăng bằng chống ngã"
                  value={profile.condition}
                  onChange={(e) => setProfile({ ...profile, condition: e.target.value })}
                />
              </div>
            </div>
          </div>

          {/* Card 2: Cài đặt tập luyện & Âm thanh */}
          <div className="card" style={{ padding: 'var(--space-5)' }}>
            <h2 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>🔊</span> Giọng nói & Mục tiêu vận động
            </h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-2)' }}>
                  Mục tiêu số lần tập mỗi ngày
                </label>
                <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                  {[5, 10, 15, 20, 30].map((goal) => (
                    <button
                      key={goal}
                      type="button"
                      className={`goal-pill ${dailyGoal === goal ? 'active' : ''}`}
                      style={{ flex: 1, padding: '10px 0', fontSize: 'var(--font-size-base)' }}
                      onClick={() => setDailyGoalVal(goal)}
                    >
                      {goal} lần
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-2)' }}>
                  Tốc độ giọng đọc hướng dẫn
                </label>
                <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                  <button
                    type="button"
                    className={`btn ${profile.speechSpeed === 'slow' ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ flex: 1, fontSize: 'var(--font-size-sm)' }}
                    onClick={() => setProfile({ ...profile, speechSpeed: 'slow' })}
                  >
                    🐢 Chậm rãi (Dễ nghe cho người lớn tuổi)
                  </button>
                  <button
                    type="button"
                    className={`btn ${profile.speechSpeed === 'normal' ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ flex: 1, fontSize: 'var(--font-size-sm)' }}
                    onClick={() => setProfile({ ...profile, speechSpeed: 'normal' })}
                  >
                    🚶 Bình thường
                  </button>
                </div>
              </div>

              <div style={{ marginTop: 'var(--space-2)' }}>
                <button
                  type="button"
                  className="btn btn-secondary btn-full"
                  style={{
                    background: 'rgba(56, 189, 248, 0.15)',
                    borderColor: 'rgba(56, 189, 248, 0.4)',
                    color: '#38bdf8',
                    fontWeight: 600,
                  }}
                  disabled={isTestingVoice}
                  onClick={handleTestVoice}
                >
                  {isTestingVoice ? 'Đang phát âm thanh...' : '🔊 Thử giọng nói tiếng Việt'}
                </button>
              </div>
            </div>
          </div>

          {/* Card 3: An toàn khẩn cấp */}
          <div className="card" style={{ padding: 'var(--space-5)' }}>
            <h2 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>🚨</span> Liên hệ khẩn cấp khi phát hiện ngã
            </h2>

            <div>
              <label style={{ display: 'block', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
                Số điện thoại khẩn cấp (Cấp cứu hoặc người thân)
              </label>
              <input
                type="tel"
                className="input-field"
                placeholder="115 hoặc số điện thoại người nhà"
                value={profile.emergencyContact}
                onChange={(e) => setProfile({ ...profile, emergencyContact: e.target.value })}
              />
              <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '4px', display: 'block' }}>
                Khi hệ thống phát hiện té ngã, nút gọi nhanh sẽ kết nối tới số điện thoại này.
              </span>
            </div>
          </div>

          {/* Save Button */}
          <button type="submit" className="btn btn-primary btn-full" style={{ padding: '16px', fontSize: 'var(--font-size-lg)' }}>
            💾 Lưu tất cả cài đặt
          </button>
        </form>

        {/* Card 4: Quản lý & Xuất dữ liệu */}
        <div className="card" style={{ padding: 'var(--space-5)', marginTop: 'var(--space-6)' }}>
          <h2 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>📦</span> Quản lý dữ liệu & Báo cáo
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
            <button
              type="button"
              className="btn btn-secondary btn-full"
              onClick={handleExportData}
            >
              📥 Xuất dữ liệu lịch sử tập luyện (Tệp JSON)
            </button>

            {!showClearConfirm ? (
              <button
                type="button"
                className="btn btn-danger btn-full"
                style={{ background: 'transparent', border: '1px solid rgba(239, 68, 68, 0.4)', color: '#f87171' }}
                onClick={() => setShowClearConfirm(true)}
              >
                🗑️ Xóa toàn bộ lịch sử tập luyện
              </button>
            ) : (
              <div style={{
                background: 'rgba(239, 68, 68, 0.15)',
                border: '1px solid #ef4444',
                padding: 'var(--space-4)',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                flexDirection: 'column',
                gap: 'var(--space-2)',
              }}>
                <span style={{ color: '#fca5a5', fontSize: 'var(--font-size-sm)', fontWeight: 600 }}>
                  ⚠️ Bác có chắc chắn muốn xóa toàn bộ lịch sử tập luyện không? Hành động này không thể hoàn tác.
                </span>
                <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                  <button type="button" className="btn btn-danger" style={{ flex: 1 }} onClick={handleClearData}>
                    Đồng ý xóa
                  </button>
                  <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => setShowClearConfirm(false)}>
                    Hủy bỏ
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {toastMessage && (
          <div className="toast-notification">
            {toastMessage}
          </div>
        )}
      </div>
    </div>
  );
}
