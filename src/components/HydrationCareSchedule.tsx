'use client';

import React, { useState, useEffect } from 'react';

interface ScheduleItem {
  id: string;
  time: string;
  title: string;
  subtitle: string;
  completed: boolean;
  type: 'workout' | 'water' | 'rest';
}

export default function HydrationCareSchedule() {
  const [waterCups, setWaterCups] = useState<number>(4);
  const targetCups = 6;

  const [schedule, setSchedule] = useState<ScheduleItem[]>([
    {
      id: 'item-1',
      time: '07:30',
      title: 'Uống 1 ly nước ấm đầu ngày',
      subtitle: 'Khởi động tuần hoàn và bôi trơn khớp xương',
      completed: true,
      type: 'water',
    },
    {
      id: 'item-2',
      time: '08:30',
      title: 'Buổi tập sáng: Đứng lên – Ngồi xuống & Squat',
      subtitle: '10–15 lần theo chỉ định Bác sĩ PHCN',
      completed: true,
      type: 'workout',
    },
    {
      id: 'item-3',
      time: '14:00',
      title: 'Uống ly nước chiều & Xoa bóp nhẹ khớp gối',
      subtitle: 'Giữ ấm khớp và thả lỏng cơ tứ đầu đùi',
      completed: false,
      type: 'water',
    },
    {
      id: 'item-4',
      time: '16:30',
      title: 'Buổi tập chiều: Dạng vai & Nâng chân',
      subtitle: 'Mở rộng lồng ngực và ổn định thăng bằng hông',
      completed: false,
      type: 'workout',
    },
  ]);

  useEffect(() => {
    try {
      const saved = localStorage.getItem('motioniq_hydration_today');
      if (saved) {
        setWaterCups(parseInt(saved, 10));
      }
    } catch {
      // ignore
    }
  }, []);

  const handleToggleCup = (index: number) => {
    const newCups = index + 1 === waterCups ? index : index + 1;
    setWaterCups(newCups);
    try {
      localStorage.setItem('motioniq_hydration_today', newCups.toString());
    } catch {
      // ignore
    }
  };

  const handleToggleSchedule = (id: string) => {
    setSchedule((prev) =>
      prev.map((item) => (item.id === id ? { ...item, completed: !item.completed } : item))
    );
  };

  return (
    <div className="card" style={{ padding: 'var(--space-5)', position: 'relative' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)', flexWrap: 'wrap', gap: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '1.4rem' }}>💧</span>
          <div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800, margin: 0, color: 'var(--color-text-primary)' }}>
              Nhắc nhở Nước & Lịch Trình Chăm Sóc
            </h3>
            <p style={{ margin: '2px 0 0 0', fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
              Khuyến nghị lâm sàng từ Khoa Phục hồi chức năng
            </p>
          </div>
        </div>

        <span
          style={{
            fontSize: 'var(--font-size-xs)',
            fontWeight: 700,
            padding: '4px 12px',
            borderRadius: 'var(--radius-full)',
            background: waterCups >= targetCups ? 'rgba(16, 185, 129, 0.2)' : 'rgba(6, 182, 212, 0.15)',
            color: waterCups >= targetCups ? '#10b981' : '#38bdf8',
            border: `1px solid ${waterCups >= targetCups ? 'rgba(16, 185, 129, 0.4)' : 'rgba(6, 182, 212, 0.3)'}`,
          }}
        >
          {waterCups >= targetCups ? '🎉 Đạt mục tiêu nước' : `Đã uống: ${waterCups}/${targetCups} ly`}
        </span>
      </div>

      {/* Water Cups Interactive Selector */}
      <div style={{ marginBottom: 'var(--space-5)', padding: 'var(--space-3)', background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--color-border)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
          <span style={{ fontSize: 'var(--font-size-xs)', fontWeight: 600, color: 'var(--color-text-secondary)' }}>
            Chạm vào ly để ghi nhận:
          </span>
          <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-accent-info)' }}>
            {(waterCups * 250)} ml / {(targetCups * 250)} ml
          </span>
        </div>

        <div style={{ display: 'flex', gap: '10px', justifyContent: 'space-between' }}>
          {Array.from({ length: targetCups }).map((_, i) => {
            const isFull = i < waterCups;
            return (
              <button
                key={i}
                type="button"
                onClick={() => handleToggleCup(i)}
                style={{
                  flex: 1,
                  height: '52px',
                  borderRadius: 'var(--radius-md)',
                  border: isFull ? '1.5px solid #06b6d4' : '1px dashed var(--color-border)',
                  background: isFull
                    ? 'linear-gradient(180deg, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0.5) 100%)'
                    : 'rgba(255, 255, 255, 0.02)',
                  cursor: 'pointer',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transition: 'all 0.25s ease',
                  transform: isFull ? 'scale(1.03)' : 'scale(1)',
                }}
                title={`Ly ${i + 1} (250ml)`}
              >
                <span style={{ fontSize: '1.2rem', filter: isFull ? 'none' : 'grayscale(1) opacity(0.4)' }}>
                  🥛
                </span>
                <span style={{ fontSize: '0.65rem', fontWeight: 700, marginTop: '2px', color: isFull ? '#38bdf8' : 'var(--color-text-muted)' }}>
                  {i + 1}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Schedule Items List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {schedule.map((item) => (
          <div
            key={item.id}
            onClick={() => handleToggleSchedule(item.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '10px 14px',
              borderRadius: 'var(--radius-lg)',
              background: item.completed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
              border: item.completed ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid var(--color-border)',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            {/* Custom Checkbox */}
            <div
              style={{
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                border: item.completed ? '2px solid #10b981' : '2px solid var(--color-border)',
                background: item.completed ? '#10b981' : 'transparent',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
                fontSize: '12px',
                fontWeight: 'bold',
                flexShrink: 0,
              }}
            >
              {item.completed ? '✓' : ''}
            </div>

            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span
                  style={{
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    padding: '2px 6px',
                    borderRadius: '4px',
                    background: 'rgba(255, 255, 255, 0.08)',
                    color: 'var(--color-accent-info)',
                  }}
                >
                  {item.time}
                </span>
                <span
                  style={{
                    fontSize: 'var(--font-size-sm)',
                    fontWeight: 600,
                    color: item.completed ? 'var(--color-text-muted)' : 'var(--color-text-primary)',
                    textDecoration: item.completed ? 'line-through' : 'none',
                  }}
                >
                  {item.title}
                </span>
              </div>
              <p
                style={{
                  margin: '2px 0 0 0',
                  fontSize: 'var(--font-size-xs)',
                  color: 'var(--color-text-secondary)',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}
              >
                {item.subtitle}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

