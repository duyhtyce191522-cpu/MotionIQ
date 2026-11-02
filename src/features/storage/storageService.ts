/**
 * storageService.ts
 *
 * Client-side storage for workout history.
 * Uses localStorage with JSON serialization.
 * Max 200 sessions retained (oldest pruned on overflow).
 */

import { WorkoutSession, WorkoutHistoryEntry, ExerciseId } from '@/types';

const HISTORY_KEY = 'motioniq_history';
const SESSIONS_KEY = 'motioniq_sessions';
const MAX_ENTRIES = 200;

// ============================================================
// History Entries (lightweight list for the history page)
// ============================================================

export function getHistoryEntries(patientId?: string): WorkoutHistoryEntry[] {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    if (!raw) return [];
    const entries = JSON.parse(raw) as WorkoutHistoryEntry[];
    if (patientId) {
      return entries.filter(
        (e) => e.patientId === patientId || (!e.patientId && patientId === 'patient-1')
      );
    }
    return entries;
  } catch {
    return [];
  }
}

export function saveHistoryEntry(entry: WorkoutHistoryEntry): void {
  try {
    const entries = getHistoryEntries();
    // Prevent duplicates
    const idx = entries.findIndex((e) => e.id === entry.id);
    if (idx >= 0) {
      entries[idx] = entry;
    } else {
      entries.unshift(entry);
    }
    // Prune oldest
    localStorage.setItem(HISTORY_KEY, JSON.stringify(entries.slice(0, MAX_ENTRIES)));
  } catch (e) {
    console.warn('[StorageService] Could not save history entry', e);
  }
}

export function deleteHistoryEntry(id: string): void {
  try {
    const entries = getHistoryEntries().filter((e) => e.id !== id);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(entries));
    // Also delete full session data
    deleteFullSession(id);
  } catch (e) {
    console.warn('[StorageService] Could not delete history entry', e);
  }
}

export function clearAllHistory(): void {
  try {
    localStorage.removeItem(HISTORY_KEY);
    localStorage.removeItem(SESSIONS_KEY);
  } catch (e) {
    console.warn('[StorageService] Could not clear history', e);
  }
}

// ============================================================
// Full Session Data (for detail/review views)
// ============================================================

function getSessionMap(): Record<string, WorkoutSession> {
  try {
    const raw = localStorage.getItem(SESSIONS_KEY);
    if (!raw) return {};
    return JSON.parse(raw) as Record<string, WorkoutSession>;
  } catch {
    return {};
  }
}

export function saveFullSession(session: WorkoutSession): void {
  try {
    const map = getSessionMap();
    map[session.id] = session;

    // Prune: keep only sessions that exist in history
    const historyIds = new Set(getHistoryEntries().map((e) => e.id));
    const pruned: Record<string, WorkoutSession> = {};
    for (const key of Object.keys(map)) {
      if (historyIds.has(key)) {
        pruned[key] = map[key];
      }
    }

    localStorage.setItem(SESSIONS_KEY, JSON.stringify(pruned));
  } catch (e) {
    console.warn('[StorageService] Could not save full session', e);
  }
}

export function getFullSession(id: string): WorkoutSession | null {
  const map = getSessionMap();
  return map[id] ?? null;
}

function deleteFullSession(id: string): void {
  try {
    const map = getSessionMap();
    delete map[id];
    localStorage.setItem(SESSIONS_KEY, JSON.stringify(map));
  } catch {
    // ignore
  }
}

// ============================================================
// Statistics Helpers
// ============================================================

export interface WeeklyStats {
  totalSessions: number;
  totalReps: number;
  totalGoodReps: number;
  averageQuality: number | null;
  totalDurationMinutes: number;
  exerciseBreakdown: Record<ExerciseId, number>;
}

export function getWeeklyStats(patientId?: string): WeeklyStats {
  const entries = getHistoryEntries(patientId);
  const now = new Date();
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

  const weekEntries = entries.filter((e) => new Date(e.date) >= weekAgo);

  const totalReps = weekEntries.reduce((sum, e) => sum + e.totalReps, 0);
  const totalGoodReps = weekEntries.reduce((sum, e) => sum + e.goodReps, 0);
  const totalDurationSeconds = weekEntries.reduce((sum, e) => sum + e.durationSeconds, 0);

  const exerciseBreakdown: Record<string, number> = {};
  for (const e of weekEntries) {
    exerciseBreakdown[e.exerciseId] = (exerciseBreakdown[e.exerciseId] || 0) + 1;
  }

  return {
    totalSessions: weekEntries.length,
    totalReps,
    totalGoodReps,
    averageQuality: totalReps > 0 ? (totalGoodReps / totalReps) * 100 : null,
    totalDurationMinutes: Math.round(totalDurationSeconds / 60),
    exerciseBreakdown: exerciseBreakdown as Record<ExerciseId, number>,
  };
}

/**
 * Tính chuỗi ngày tập liên tiếp (Streak)
 */
export function getDailyStreak(patientId?: string): number {
  const entries = getHistoryEntries(patientId);
  if (entries.length === 0) return 0;

  const dateSet = new Set<string>();
  for (const e of entries) {
    dateSet.add(e.date.substring(0, 10)); // YYYY-MM-DD
  }

  const today = new Date();
  const formatDay = (d: Date) => d.toISOString().substring(0, 10);

  let current = today;
  let streak = 0;

  const todayStr = formatDay(current);
  if (dateSet.has(todayStr)) {
    streak++;
    current = new Date(current.getTime() - 86400000);
  } else {
    const yesterday = new Date(current.getTime() - 86400000);
    if (dateSet.has(formatDay(yesterday))) {
      current = yesterday;
    } else {
      return 0;
    }
  }

  while (dateSet.has(formatDay(current))) {
    streak++;
    current = new Date(current.getTime() - 86400000);
  }

  return streak;
}

const DAILY_GOAL_KEY = 'motioniq_daily_goal';
const DEFAULT_DAILY_GOAL = 15;

export interface TodayStats {
  todayReps: number;
  todayGoodReps: number;
  todaySessions: number;
  dailyGoal: number;
  goalPercent: number;
  streak: number;
  isGoalReached: boolean;
}

export function getDailyGoal(): number {
  if (typeof window === 'undefined') return DEFAULT_DAILY_GOAL;
  try {
    const raw = localStorage.getItem(DAILY_GOAL_KEY);
    if (!raw) return DEFAULT_DAILY_GOAL;
    const parsed = parseInt(raw, 10);
    return isNaN(parsed) || parsed <= 0 ? DEFAULT_DAILY_GOAL : parsed;
  } catch {
    return DEFAULT_DAILY_GOAL;
  }
}

export function setDailyGoal(goal: number): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(DAILY_GOAL_KEY, Math.max(5, Math.min(100, goal)).toString());
  } catch {
    // ignore
  }
}

export function getTodayStats(patientId?: string): TodayStats {
  const entries = getHistoryEntries(patientId);
  const todayStr = new Date().toISOString().substring(0, 10); // YYYY-MM-DD
  const todayEntries = entries.filter((e) => e.date.substring(0, 10) === todayStr);

  const todayReps = todayEntries.reduce((sum, e) => sum + e.totalReps, 0);
  const todayGoodReps = todayEntries.reduce((sum, e) => sum + e.goodReps, 0);
  const dailyGoal = getDailyGoal();
  const goalPercent = Math.min(100, Math.round((todayReps / dailyGoal) * 100));
  const streak = getDailyStreak(patientId);

  return {
    todayReps,
    todayGoodReps,
    todaySessions: todayEntries.length,
    dailyGoal,
    goalPercent,
    streak,
    isGoalReached: todayReps >= dailyGoal,
  };
}

/**
 * Group history entries by date (YYYY-MM-DD) for display.
 */
export function groupByDate(entries: WorkoutHistoryEntry[]): Map<string, WorkoutHistoryEntry[]> {
  const map = new Map<string, WorkoutHistoryEntry[]>();
  for (const entry of entries) {
    const dateKey = entry.date.substring(0, 10); // YYYY-MM-DD
    if (!map.has(dateKey)) {
      map.set(dateKey, []);
    }
    map.get(dateKey)!.push(entry);
  }
  return map;
}

/**
 * Save a completed workout: both the lightweight entry and full session data.
 */
export function saveCompletedWorkout(session: WorkoutSession): void {
  const entry: WorkoutHistoryEntry = {
    id: session.id,
    patientId: session.patientId,
    patientName: session.patientName,
    exerciseId: session.exerciseId,
    exerciseName: session.exerciseName,
    date: session.createdAt,
    totalReps: session.totalReps,
    goodReps: session.goodReps,
    qualityRatio: session.qualityRatio,
    durationSeconds: Math.round(session.activeDuration / 1000),
  };

  saveHistoryEntry(entry);
  saveFullSession(session);
}

// ============================================================
// Patient Profile (for clinical reports and personalized care)
// ============================================================

export interface PatientProfile {
  name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  condition: string;
  therapist: string;
  emergencyContact: string;
  speechSpeed: 'slow' | 'normal';
  volumeLevel?: 'max' | 'high' | 'medium';
}

const PATIENT_PROFILE_KEY = 'motioniq_patient_profile';

export function getPatientProfile(): PatientProfile {
  const defaultProfile: PatientProfile = {
    name: 'Bác Nguyễn Văn An',
    age: 68,
    gender: 'male',
    condition: 'Tập phục hồi chức năng cơ lực & thăng bằng',
    therapist: 'BS. Khoa Phục hồi chức năng / KTV',
    emergencyContact: '115',
    speechSpeed: 'slow',
    volumeLevel: 'max',
  };

  if (typeof window === 'undefined') return defaultProfile;
  try {
    const raw = localStorage.getItem(PATIENT_PROFILE_KEY);
    if (!raw) return defaultProfile;
    return { ...defaultProfile, ...(JSON.parse(raw) as Partial<PatientProfile>) };
  } catch {
    return defaultProfile;
  }
}

export function savePatientProfile(profile: PatientProfile): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(PATIENT_PROFILE_KEY, JSON.stringify(profile));
  } catch (e) {
    console.warn('[StorageService] Could not save patient profile', e);
  }
}

