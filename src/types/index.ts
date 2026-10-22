/**
 * MotionIQ — Core Type Definitions
 * Shared types across all modules
 */

// ============================================================
// MediaPipe Landmark Types
// ============================================================

/** Single landmark point from MediaPipe */
export interface Landmark {
  x: number;
  y: number;
  z: number;
  visibility?: number;
  presence?: number;
}

/** Normalized landmark (0-1 range) */
export type NormalizedLandmark = Landmark;

/** World landmark (meters from hip center) */
export type WorldLandmark = Landmark;

/** Pose detection result from MediaPipe */
export interface PoseResult {
  landmarks: NormalizedLandmark[][];
  worldLandmarks: WorldLandmark[][];
  timestamp: number;
}

// ============================================================
// Landmark Indices (MediaPipe Pose — 33 landmarks)
// ============================================================

export const LANDMARK_NAMES = {
  NOSE: 0,
  LEFT_EYE_INNER: 1,
  LEFT_EYE: 2,
  LEFT_EYE_OUTER: 3,
  RIGHT_EYE_INNER: 4,
  RIGHT_EYE: 5,
  RIGHT_EYE_OUTER: 6,
  LEFT_EAR: 7,
  RIGHT_EAR: 8,
  MOUTH_LEFT: 9,
  MOUTH_RIGHT: 10,
  LEFT_SHOULDER: 11,
  RIGHT_SHOULDER: 12,
  LEFT_ELBOW: 13,
  RIGHT_ELBOW: 14,
  LEFT_WRIST: 15,
  RIGHT_WRIST: 16,
  LEFT_PINKY: 17,
  RIGHT_PINKY: 18,
  LEFT_INDEX: 19,
  RIGHT_INDEX: 20,
  LEFT_THUMB: 21,
  RIGHT_THUMB: 22,
  LEFT_HIP: 23,
  RIGHT_HIP: 24,
  LEFT_KNEE: 25,
  RIGHT_KNEE: 26,
  LEFT_ANKLE: 27,
  RIGHT_ANKLE: 28,
  LEFT_HEEL: 29,
  RIGHT_HEEL: 30,
  LEFT_FOOT_INDEX: 31,
  RIGHT_FOOT_INDEX: 32,
} as const;

export type LandmarkIndex = (typeof LANDMARK_NAMES)[keyof typeof LANDMARK_NAMES];

// ============================================================
// Body Region Groups for Validation
// ============================================================

export const BODY_REGIONS = {
  HEAD: [
    LANDMARK_NAMES.NOSE,
    LANDMARK_NAMES.LEFT_EAR,
    LANDMARK_NAMES.RIGHT_EAR,
  ],
  UPPER_BODY: [
    LANDMARK_NAMES.LEFT_SHOULDER,
    LANDMARK_NAMES.RIGHT_SHOULDER,
    LANDMARK_NAMES.LEFT_ELBOW,
    LANDMARK_NAMES.RIGHT_ELBOW,
    LANDMARK_NAMES.LEFT_WRIST,
    LANDMARK_NAMES.RIGHT_WRIST,
  ],
  TORSO: [
    LANDMARK_NAMES.LEFT_SHOULDER,
    LANDMARK_NAMES.RIGHT_SHOULDER,
    LANDMARK_NAMES.LEFT_HIP,
    LANDMARK_NAMES.RIGHT_HIP,
  ],
  LOWER_BODY: [
    LANDMARK_NAMES.LEFT_HIP,
    LANDMARK_NAMES.RIGHT_HIP,
    LANDMARK_NAMES.LEFT_KNEE,
    LANDMARK_NAMES.RIGHT_KNEE,
    LANDMARK_NAMES.LEFT_ANKLE,
    LANDMARK_NAMES.RIGHT_ANKLE,
  ],
  FEET: [
    LANDMARK_NAMES.LEFT_ANKLE,
    LANDMARK_NAMES.RIGHT_ANKLE,
    LANDMARK_NAMES.LEFT_HEEL,
    LANDMARK_NAMES.RIGHT_HEEL,
  ],
} as const;

// ============================================================
// Angle Calculation Types
// ============================================================

export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export interface JointAngle {
  name: string;
  angleDeg: number;
  confidence: number;
}

// ============================================================
// Exercise Types
// ============================================================

export type ExerciseId =
  | 'sit-to-stand'
  | 'squat'
  | 'shoulder-raise'
  | 'side-leg-raise';

export interface ExerciseInfo {
  id: ExerciseId;
  name: string;
  description: string;
  icon: string;
  datasetSource: string; // Tên và mã bài tập tương ứng trong EHE / KIMORE / UI-PRMD
  instructions: string[];
  cameraAdvice?: string;
  targetAngleDescription?: string;
}

/** Configurable thresholds for each exercise */
export interface ExerciseThresholds {
  /** Angles that define state transitions */
  angles: Record<string, { min: number; max: number }>;
  /** Minimum visibility confidence for required landmarks */
  minVisibility: number;
  /** Minimum frames to hold a state before transitioning */
  minHoldFrames: number;
  /** Hysteresis margin to prevent state oscillation (degrees) */
  hysteresisDeg: number;
  /** Minimum rep duration in milliseconds to prevent false-positive twitches */
  minRepDurationMs?: number;
  /** Name of primary angle tracked on the live gauge */
  primaryAngleKey?: string;
  /** Ideal target minimum angle */
  targetAngleMin?: number;
  /** Ideal target maximum angle */
  targetAngleMax?: number;
}

// ============================================================
// State Machine Types
// ============================================================

export type ExerciseState =
  | 'IDLE'
  | 'READY'
  | 'DESCENDING'
  | 'BOTTOM'
  | 'ASCENDING'
  | 'TOP'
  | 'COMPLETE';

export interface StateTransition {
  from: ExerciseState;
  to: ExerciseState;
  timestamp: number;
}

export interface RepetitionResult {
  repNumber: number;
  startTime: number;
  endTime: number;
  duration: number;
  meetsBasicCriteria: boolean;
  feedback: string[];
  angles: Record<string, number>;
}

// ============================================================
// Feedback Types
// ============================================================

export type FeedbackPriority = 'critical' | 'warning' | 'info' | 'success';

export interface FeedbackMessage {
  id: string;
  text: string;
  priority: FeedbackPriority;
  category: 'form' | 'tracking' | 'counting' | 'safety';
  cooldownMs: number;
}

// ============================================================
// Workout / Session Types
// ============================================================

export type WorkoutStatus = 'not_started' | 'active' | 'paused' | 'completed';

export interface WorkoutSession {
  id: string;
  patientId?: string;
  patientName?: string;
  exerciseId: ExerciseId;
  exerciseName: string;
  status: WorkoutStatus;
  startTime: number;
  endTime?: number;
  totalDuration: number;
  activeDuration: number;
  repetitions: RepetitionResult[];
  totalReps: number;
  goodReps: number;
  qualityRatio: number | null; // null when no reps evaluated
  warnings: string[];
  createdAt: string;
}

export interface WorkoutSummaryData {
  session: WorkoutSession;
  disclaimer: string;
}

// ============================================================
// Calibration / Camera Types
// ============================================================

export type CalibrationStatus =
  | 'checking_camera'
  | 'no_camera'
  | 'camera_denied'
  | 'detecting_pose'
  | 'partial_body'
  | 'ready'
  | 'error';

export interface CalibrationResult {
  status: CalibrationStatus;
  missingRegions: string[];
  message: string;
  canStart: boolean;
  lighting?: {
    status: 'good' | 'too_dark' | 'too_bright';
    brightness: number;
    message?: string;
  };
  distance?: {
    status: 'ideal' | 'too_close' | 'too_far';
    advice?: string;
  };
}

// ============================================================
// Validation Types
// ============================================================

export interface LandmarkValidation {
  isValid: boolean;
  overallConfidence: number;
  missingLandmarks: number[];
  lowConfidenceLandmarks: number[];
  bodyInFrame: boolean;
  headVisible: boolean;
  handsVisible: boolean;
  hipsVisible: boolean;
  kneesVisible: boolean;
  feetVisible: boolean;
}

// ============================================================
// History / Database Types
// ============================================================

export interface WorkoutHistoryEntry {
  id: string;
  patientId?: string;
  patientName?: string;
  exerciseId: ExerciseId;
  exerciseName: string;
  date: string;
  totalReps: number;
  goodReps: number;
  qualityRatio: number | null;
  durationSeconds: number;
}
