/**
 * authService.ts
 *
 * Authentication & Role Management for MotionIQ
 * Dual-flow: Elderly Patient (Quick 1-touch profile) & Administrator (Username/Password)
 * Offline-first using localStorage.
 */

import { PatientProfile, savePatientProfile, setDailyGoal } from '../storage/storageService';

export interface PatientUser {
  id: string;
  name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  condition?: string;
  therapist?: string;
  emergencyContact?: string;
  avatarIcon: string;
  pin?: string; // Optional 4-digit PIN for privacy
  prescribedExercises?: string[]; // e.g. ['chair-squat', 'knee-raise']
  dailyRepGoal?: number; // Target repetitions per day
  createdAt: string;
}

export type UserRole = 'patient' | 'admin';

export interface AuthSession {
  role: UserRole;
  user: {
    id: string;
    name: string;
    avatarIcon?: string;
    role: UserRole;
    patientId?: string;
  };
  loginTime: string;
}

const PATIENTS_LIST_KEY = 'motioniq_patients_list';
const AUTH_SESSION_KEY = 'motioniq_auth_session';
const ADMIN_CREDENTIALS_KEY = 'motioniq_admin_credentials';

const DEFAULT_ADMIN = {
  username: 'admin',
  password: 'admin123',
};

const INITIAL_PATIENTS: PatientUser[] = [
  {
    id: 'patient-1',
    name: 'Bác Nguyễn Văn An',
    age: 68,
    gender: 'male',
    condition: 'Tập phục hồi chức năng cơ lực & thăng bằng',
    therapist: 'BS. Khoa Phục hồi chức năng',
    emergencyContact: '115',
    avatarIcon: '👴',
    prescribedExercises: ['sit-to-stand', 'squat'],
    dailyRepGoal: 15,
    createdAt: new Date().toISOString(),
  },
  {
    id: 'patient-2',
    name: 'Bà Trần Thị Mai',
    age: 72,
    gender: 'female',
    condition: 'Tập vận động khớp gối và cột sống',
    therapist: 'KTV. Lê Hoàng',
    emergencyContact: '0901234567',
    avatarIcon: '👵',
    prescribedExercises: ['shoulder-raise', 'side-leg-raise'],
    dailyRepGoal: 20,
    createdAt: new Date().toISOString(),
  },
];

// ============================================================
// Initialization & Patients List
// ============================================================

export function getAllPatients(): PatientUser[] {
  if (typeof window === 'undefined') return INITIAL_PATIENTS;
  try {
    const raw = localStorage.getItem(PATIENTS_LIST_KEY);
    if (!raw) {
      localStorage.setItem(PATIENTS_LIST_KEY, JSON.stringify(INITIAL_PATIENTS));
      return INITIAL_PATIENTS;
    }
    const parsed = JSON.parse(raw) as PatientUser[];
    if (parsed.length === 0) {
      localStorage.setItem(PATIENTS_LIST_KEY, JSON.stringify(INITIAL_PATIENTS));
      return INITIAL_PATIENTS;
    }

    // Auto-migrate: Backfill prescribedExercises and dailyRepGoal if missing, and prune non-dataset exercises
    let updated = false;
    for (const p of parsed) {
      if (!p.prescribedExercises || p.prescribedExercises.length === 0) {
        const init = INITIAL_PATIENTS.find((ip) => ip.id === p.id);
        if (init && init.prescribedExercises) {
          p.prescribedExercises = init.prescribedExercises;
          p.dailyRepGoal = init.dailyRepGoal || 15;
          updated = true;
        }
      }
      // Prune any legacy exercise not present in datasets (e.g. calf-raise)
      if (p.prescribedExercises && p.prescribedExercises.includes('calf-raise')) {
        p.prescribedExercises = p.prescribedExercises.filter((id) => id !== 'calf-raise');
        updated = true;
      }
    }
    if (updated) {
      localStorage.setItem(PATIENTS_LIST_KEY, JSON.stringify(parsed));
    }

    return parsed;
  } catch {
    return INITIAL_PATIENTS;
  }
}

export function savePatientsList(patients: PatientUser[]): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(PATIENTS_LIST_KEY, JSON.stringify(patients));
  } catch (e) {
    console.warn('[AuthService] Could not save patients list', e);
  }
}

export function createPatient(data: Omit<PatientUser, 'id' | 'createdAt'>): PatientUser {
  const patients = getAllPatients();
  const newPatient: PatientUser = {
    ...data,
    id: `patient-${Date.now()}`,
    createdAt: new Date().toISOString(),
  };
  patients.push(newPatient);
  savePatientsList(patients);
  return newPatient;
}

export function updatePatient(id: string, updates: Partial<PatientUser>): PatientUser | null {
  const patients = getAllPatients();
  const idx = patients.findIndex((p) => p.id === id);
  if (idx === -1) return null;
  patients[idx] = { ...patients[idx], ...updates };
  savePatientsList(patients);

  // If currently active user is this patient, sync session & profile
  const session = getAuthSession();
  if (session && session.user.id === id) {
    session.user.name = patients[idx].name;
    session.user.avatarIcon = patients[idx].avatarIcon;
    saveAuthSession(session);
    syncToLegacyProfile(patients[idx]);
  }
  return patients[idx];
}

export function getPatientById(id: string): PatientUser | null {
  const patients = getAllPatients();
  return patients.find((p) => p.id === id) || null;
}

export function deletePatient(id: string): void {
  const patients = getAllPatients().filter((p) => p.id !== id);
  savePatientsList(patients);
  const session = getAuthSession();
  if (session && session.user.id === id) {
    logout();
  }
}

// ============================================================
// Session Management
// ============================================================

export function getAuthSession(): AuthSession | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(AUTH_SESSION_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as AuthSession;
  } catch {
    return null;
  }
}

export function saveAuthSession(session: AuthSession): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(session));
  } catch (e) {
    console.warn('[AuthService] Could not save session', e);
  }
}

export function logout(): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.removeItem(AUTH_SESSION_KEY);
  } catch (e) {
    console.warn('[AuthService] Could not logout', e);
  }
}

// ============================================================
// Login Flows
// ============================================================

export function loginAsPatient(patientId: string, enteredPin?: string): { success: boolean; error?: string } {
  const patients = getAllPatients();
  const patient = patients.find((p) => p.id === patientId);
  if (!patient) {
    return { success: false, error: 'Không tìm thấy hồ sơ người tập.' };
  }

  if (patient.pin && patient.pin.trim() !== '') {
    if (!enteredPin || enteredPin.trim() !== patient.pin.trim()) {
      return { success: false, error: 'Mã PIN bảo mật không chính xác.' };
    }
  }

  const session: AuthSession = {
    role: 'patient',
    user: {
      id: patient.id,
      patientId: patient.id,
      name: patient.name,
      avatarIcon: patient.avatarIcon || '👤',
      role: 'patient',
    },
    loginTime: new Date().toISOString(),
  };

  saveAuthSession(session);
  syncToLegacyProfile(patient);
  return { success: true };
}

export function loginAsAdmin(username: string, password: string): { success: boolean; error?: string } {
  const adminCreds = getAdminCredentials();
  if (username.trim() !== adminCreds.username || password !== adminCreds.password) {
    return { success: false, error: 'Tên đăng nhập hoặc mật khẩu quản trị không chính xác.' };
  }

  const session: AuthSession = {
    role: 'admin',
    user: {
      id: 'admin-master',
      name: 'Quản trị viên / Bác sĩ',
      avatarIcon: '🛡️',
      role: 'admin',
    },
    loginTime: new Date().toISOString(),
  };

  saveAuthSession(session);
  return { success: true };
}

// ============================================================
// Admin Credentials
// ============================================================

function getAdminCredentials(): typeof DEFAULT_ADMIN {
  if (typeof window === 'undefined') return DEFAULT_ADMIN;
  try {
    const raw = localStorage.getItem(ADMIN_CREDENTIALS_KEY);
    if (!raw) {
      localStorage.setItem(ADMIN_CREDENTIALS_KEY, JSON.stringify(DEFAULT_ADMIN));
      return DEFAULT_ADMIN;
    }
    return JSON.parse(raw);
  } catch {
    return DEFAULT_ADMIN;
  }
}

export function changeAdminPassword(oldPass: string, newPass: string): { success: boolean; error?: string } {
  const creds = getAdminCredentials();
  if (oldPass !== creds.password) {
    return { success: false, error: 'Mật khẩu hiện tại không đúng.' };
  }
  if (!newPass || newPass.trim().length < 4) {
    return { success: false, error: 'Mật khẩu mới phải có ít nhất 4 ký tự.' };
  }

  creds.password = newPass.trim();
  try {
    localStorage.setItem(ADMIN_CREDENTIALS_KEY, JSON.stringify(creds));
    return { success: true };
  } catch {
    return { success: false, error: 'Không thể lưu mật khẩu vào thiết bị.' };
  }
}

// ============================================================
// Helper: Sync PatientUser to legacy PatientProfile in storageService
// ============================================================

function syncToLegacyProfile(patient: PatientUser): void {
  const prof: PatientProfile = {
    name: patient.name,
    age: patient.age,
    gender: patient.gender,
    condition: patient.condition || 'Tập phục hồi chức năng',
    therapist: patient.therapist || 'Khoa PHCN',
    emergencyContact: patient.emergencyContact || '115',
    speechSpeed: 'slow',
  };
  savePatientProfile(prof);
  if (patient.dailyRepGoal) {
    setDailyGoal(patient.dailyRepGoal);
  }
}
