/**
 * angleCalculator.ts
 * 
 * Tính góc khớp từ 3 điểm landmark.
 * Sử dụng vector dot product: angle = arccos(dot(BA, BC) / (|BA| × |BC|))
 * 
 * Xử lý:
 * - Vector có độ dài gần 0
 * - Clamp giá trị cos để tránh NaN từ floating point
 * - Hỗ trợ cả 2D và 3D
 */

import { Landmark, Vector3D, JointAngle, NormalizedLandmark } from '@/types';

const MIN_VECTOR_LENGTH = 1e-6;

/** Subtract two 3D points to get a vector */
function subtractVectors(a: Landmark, b: Landmark): Vector3D {
  return {
    x: a.x - b.x,
    y: a.y - b.y,
    z: a.z - b.z,
  };
}

/** Dot product of two 3D vectors */
function dotProduct(a: Vector3D, b: Vector3D): number {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}

/** Magnitude (length) of a 3D vector */
function magnitude(v: Vector3D): number {
  return Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

/** Clamp value between min and max */
function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

/** Convert radians to degrees */
function radToDeg(rad: number): number {
  return (rad * 180) / Math.PI;
}

/**
 * Tính góc tại điểm B, tạo bởi ba điểm A, B, C.
 * Góc ABC = arccos(dot(BA, BC) / (|BA| × |BC|))
 * 
 * @param a - Điểm A
 * @param b - Điểm B (đỉnh góc)
 * @param c - Điểm C
 * @returns Góc tính bằng độ (0–180), hoặc null nếu không tính được
 */
export function calculateAngle(
  a: Landmark,
  b: Landmark,
  c: Landmark
): number | null {
  const ba = subtractVectors(a, b);
  const bc = subtractVectors(c, b);

  const magBA = magnitude(ba);
  const magBC = magnitude(bc);

  // Kiểm tra vector có độ dài gần 0
  if (magBA < MIN_VECTOR_LENGTH || magBC < MIN_VECTOR_LENGTH) {
    return null;
  }

  const cosAngle = clamp(dotProduct(ba, bc) / (magBA * magBC), -1, 1);
  const angleRad = Math.acos(cosAngle);

  return radToDeg(angleRad);
}

/**
 * Tính góc tại điểm B chỉ dùng tọa độ 2D (x, y).
 * Hữu ích khi z không đáng tin cậy.
 */
export function calculateAngle2D(
  a: Landmark,
  b: Landmark,
  c: Landmark
): number | null {
  const ba: Vector3D = { x: a.x - b.x, y: a.y - b.y, z: 0 };
  const bc: Vector3D = { x: c.x - b.x, y: c.y - b.y, z: 0 };

  const magBA = magnitude(ba);
  const magBC = magnitude(bc);

  if (magBA < MIN_VECTOR_LENGTH || magBC < MIN_VECTOR_LENGTH) {
    return null;
  }

  const cosAngle = clamp(dotProduct(ba, bc) / (magBA * magBC), -1, 1);
  return radToDeg(Math.acos(cosAngle));
}

/**
 * Tính confidence trung bình cho một nhóm landmarks
 */
export function averageConfidence(landmarks: NormalizedLandmark[]): number {
  if (landmarks.length === 0) return 0;
  const total = landmarks.reduce(
    (sum, lm) => sum + (lm.visibility ?? 0),
    0
  );
  return total / landmarks.length;
}

/**
 * Tính góc khớp kèm confidence, dùng cho các bài tập.
 * 
 * @param name - Tên góc (ví dụ: "left_knee")
 * @param landmarks - Mảng 33 landmarks
 * @param aIdx - Index landmark A
 * @param bIdx - Index landmark B (đỉnh góc)
 * @param cIdx - Index landmark C
 * @param use3D - Sử dụng tọa độ 3D (mặc định true)
 */
export function computeJointAngle(
  name: string,
  landmarks: NormalizedLandmark[],
  aIdx: number,
  bIdx: number,
  cIdx: number,
  use3D: boolean = true
): JointAngle | null {
  if (!landmarks[aIdx] || !landmarks[bIdx] || !landmarks[cIdx]) {
    return null;
  }

  const a = landmarks[aIdx];
  const b = landmarks[bIdx];
  const c = landmarks[cIdx];

  const confidence = averageConfidence([a, b, c]);
  
  const angleDeg = use3D
    ? calculateAngle(a, b, c)
    : calculateAngle2D(a, b, c);

  if (angleDeg === null) {
    return null;
  }

  return { name, angleDeg, confidence };
}

/**
 * Tính khoảng cách 2D giữa hai landmarks (normalized coordinates)
 */
export function distance2D(a: Landmark, b: Landmark): number {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy);
}

/**
 * Tính điểm giữa hai landmarks
 */
export function midpoint(a: Landmark, b: Landmark): Landmark {
  return {
    x: (a.x + b.x) / 2,
    y: (a.y + b.y) / 2,
    z: (a.z + b.z) / 2,
    visibility: Math.min(a.visibility ?? 0, b.visibility ?? 0),
  };
}
