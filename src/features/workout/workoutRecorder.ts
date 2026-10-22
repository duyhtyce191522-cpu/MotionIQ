/**
 * workoutRecorder.ts
 * 
 * Theo dõi buổi tập:
 * - Thời gian tập (tổng và active)
 * - Quản lý pause/resume
 * - Thu thập kết quả từ state machine
 * - Tạo summary
 */

import { WorkoutSession, WorkoutStatus, ExerciseId, RepetitionResult } from '@/types';
import { EXERCISES } from '../exercises/exerciseRules';

export class WorkoutRecorder {
  private session: WorkoutSession;
  private pauseStartTime: number | null = null;
  private totalPauseDuration: number = 0;

  constructor(exerciseId: ExerciseId, patientId?: string, patientName?: string) {
    const exercise = EXERCISES[exerciseId];
    this.session = {
      id: this.generateId(),
      patientId,
      patientName,
      exerciseId,
      exerciseName: exercise.name,
      status: 'not_started',
      startTime: 0,
      totalDuration: 0,
      activeDuration: 0,
      repetitions: [],
      totalReps: 0,
      goodReps: 0,
      qualityRatio: null,
      warnings: [],
      createdAt: new Date().toISOString(),
    };
  }

  setPatient(patientId?: string, patientName?: string): void {
    if (patientId) this.session.patientId = patientId;
    if (patientName) this.session.patientName = patientName;
  }

  /** Bắt đầu buổi tập */
  start(): void {
    this.session.status = 'active';
    this.session.startTime = Date.now();
  }

  /** Tạm dừng */
  pause(): void {
    if (this.session.status !== 'active') return;
    this.session.status = 'paused';
    this.pauseStartTime = Date.now();
  }

  /** Tiếp tục */
  resume(): void {
    if (this.session.status !== 'paused') return;
    this.session.status = 'active';
    if (this.pauseStartTime) {
      this.totalPauseDuration += Date.now() - this.pauseStartTime;
      this.pauseStartTime = null;
    }
  }

  /** Kết thúc buổi tập */
  finish(repetitions: RepetitionResult[]): WorkoutSession {
    const now = Date.now();
    
    if (this.pauseStartTime) {
      this.totalPauseDuration += now - this.pauseStartTime;
      this.pauseStartTime = null;
    }

    this.session.status = 'completed';
    this.session.endTime = now;
    this.session.totalDuration = now - this.session.startTime;
    this.session.activeDuration = this.session.totalDuration - this.totalPauseDuration;
    this.session.repetitions = repetitions;
    this.session.totalReps = repetitions.length;
    this.session.goodReps = repetitions.filter((r) => r.meetsBasicCriteria).length;

    // Tính quality ratio
    if (this.session.totalReps > 0) {
      this.session.qualityRatio =
        (this.session.goodReps / this.session.totalReps) * 100;
    } else {
      this.session.qualityRatio = null;
    }

    // Tổng hợp warnings
    const warningCounts = new Map<string, number>();
    for (const rep of repetitions) {
      for (const fb of rep.feedback) {
        if (this.isWarning(fb)) {
          warningCounts.set(fb, (warningCounts.get(fb) || 0) + 1);
        }
      }
    }
    this.session.warnings = Array.from(warningCounts.entries())
      .filter(([, count]) => count >= 2) // Chỉ hiện warning xuất hiện >= 2 lần
      .sort((a, b) => b[1] - a[1])
      .map(([text, count]) => `${text} (${count} lần)`);

    return { ...this.session };
  }

  /** Lấy trạng thái hiện tại */
  getStatus(): WorkoutStatus {
    return this.session.status;
  }

  /** Lấy thời gian active (ms) */
  getActiveDuration(): number {
    if (this.session.status === 'not_started') return 0;
    
    const now = Date.now();
    let elapsed = now - this.session.startTime - this.totalPauseDuration;
    
    if (this.pauseStartTime) {
      elapsed -= now - this.pauseStartTime;
    }
    
    return Math.max(0, elapsed);
  }

  /** Lấy session ID */
  getSessionId(): string {
    return this.session.id;
  }

  private isWarning(text: string): boolean {
    const lower = text.toLowerCase();
    return (
      lower.includes('thẳng hơn') ||
      lower.includes('không đều') ||
      lower.includes('chưa đứng thẳng') ||
      lower.includes('hạ sâu hơn') ||
      lower.includes('nâng tay cao hơn') ||
      lower.includes('tham khảo')
    );
  }

  private generateId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
  }
}
