/**
 * exerciseRules.ts
 * 
 * Cấu hình tập trung cho tất cả ngưỡng bài tập.
 * Tách riêng khỏi logic xử lý để dễ điều chỉnh.
 * 
 * LƯU Ý: Các ngưỡng này là giá trị tham khảo ban đầu,
 * chưa được kiểm chứng lâm sàng. Cần điều chỉnh dựa trên
 * dữ liệu kiểm thử thực tế.
 */

import { ExerciseId, ExerciseInfo, ExerciseThresholds, LANDMARK_NAMES } from '@/types';

// ============================================================
// Thông tin bài tập
// ============================================================

export const EXERCISES: Record<ExerciseId, ExerciseInfo> = {
  'sit-to-stand': {
    id: 'sit-to-stand',
    name: 'Đứng lên – Ngồi xuống',
    description: 'Tập đứng lên từ ghế và ngồi xuống. Giúp tăng sức mạnh chân và cải thiện thăng bằng.',
    icon: '🪑',
    datasetSource: 'UI-PRMD (m05) & KIMORE (Es4)',
    cameraAdvice: 'Đặt điện thoại ngang tầm hông, góc nghiêng 45°–90° bên cạnh, cách bạn 2–3 mét.',
    targetAngleDescription: 'Đứng thẳng (gối ≥ 150°), ngồi xuống hoàn toàn (gối ≤ 105°)',
    instructions: [
      'Ngồi trên ghế vững chắc, hai chân đặt bằng trên sàn.',
      'Đặt điện thoại chếch góc nghiêng hoặc bên hông cách 2–3 mét.',
      'Đứng lên từ từ, giữ thẳng lưng.',
      'Đứng thẳng hoàn toàn, giữ 1–2 giây.',
      'Ngồi xuống từ từ về ghế.',
    ],
  },
  squat: {
    id: 'squat',
    name: 'Squat',
    description: 'Tập hạ thấp người và đứng lên. Tăng sức mạnh đùi, mông và cải thiện linh hoạt.',
    icon: '🏋️',
    datasetSource: 'UI-PRMD (m01) & KIMORE (Es5)',
    cameraAdvice: 'Đặt điện thoại góc nghiêng 45° phía trước–bên, ngang tầm ngực/hông, cách 2–3 mét.',
    targetAngleDescription: 'Hạ gối đến khoảng 90°–125° có kiểm soát, sau đó đứng thẳng trở lại',
    instructions: [
      'Đứng thẳng, hai chân rộng bằng vai.',
      'Đặt điện thoại cách 2–3 mét ở góc hơi chếch để nhìn rõ gối.',
      'Hạ người xuống từ từ, gối hướng cùng chiều bàn chân.',
      'Hạ đến mức thoải mái, giữ 1–2 giây.',
      'Đứng lên từ từ về vị trí ban đầu.',
    ],
  },
  'shoulder-raise': {
    id: 'shoulder-raise',
    name: 'Nâng tay',
    description: 'Nâng hai tay lên ngang vai hoặc cao hơn. Cải thiện khả năng vận động vai và cánh tay.',
    icon: '🙆',
    datasetSource: 'EHE (LA), KIMORE (Es1) & UI-PRMD (m07)',
    cameraAdvice: 'Đặt điện thoại chính diện phía trước, cách bạn khoảng 2–2.5 mét.',
    targetAngleDescription: 'Nâng hai tay lên ngang vai hoặc cao hơn (góc vai ≥ 75°)',
    instructions: [
      'Đứng thẳng đối diện camera, hai tay xuôi theo thân.',
      'Đặt điện thoại ngang tầm ngực cách 2–2.5 mét.',
      'Nâng hai tay lên từ từ, càng cao càng tốt.',
      'Giữ ở vị trí cao nhất 1–2 giây.',
      'Hạ tay xuống từ từ.',
    ],
  },
  'side-leg-raise': {
    id: 'side-leg-raise',
    name: 'Giạng chân sang bên',
    description: 'Đứng thẳng và giạng một chân sang bên. Tăng cường cơ mông nhỡ và cải thiện thăng bằng chống té ngã.',
    icon: '🦵',
    datasetSource: 'UI-PRMD (m06 - Active Straight Leg Raise)',
    cameraAdvice: 'Đặt điện thoại chính diện phía trước, cách bạn khoảng 2–2.5 mét để thấy toàn thân.',
    targetAngleDescription: 'Giạng chân sang bên góc ≥ 25°–35°, giữ 1–2 giây rồi hạ về',
    instructions: [
      'Đứng thẳng đối diện camera, hai tay có thể vịn nhẹ vào tường hoặc tựa ghế.',
      'Giữ lưng và chân trụ thẳng.',
      'Giạng một chân sang bên từ từ đến khi thấy căng cơ hông.',
      'Giữ ở vị trí cao nhất 1–2 giây.',
      'Hạ chân xuống nhẹ nhàng về vị trí ban đầu.',
    ],
  },
};

// ============================================================
// Ngưỡng bài tập
// ============================================================

export const EXERCISE_THRESHOLDS: Record<ExerciseId, ExerciseThresholds> = {
  'sit-to-stand': {
    angles: {
      // Góc gối khi ngồi (thường ~90°)
      knee_sitting: { min: 60, max: 120 },
      // Góc gối khi đứng (thường ~160-180°)
      knee_standing: { min: 150, max: 180 },
      // Góc hông khi ngồi
      hip_sitting: { min: 60, max: 120 },
      // Góc hông khi đứng
      hip_standing: { min: 150, max: 180 },
    },
    minVisibility: 0.5,
    minHoldFrames: 3,
    hysteresisDeg: 10,
    minRepDurationMs: 1200,
    primaryAngleKey: 'knee',
    targetAngleMin: 150,
    targetAngleMax: 180,
  },
  squat: {
    angles: {
      // Góc gối khi đứng
      knee_standing: { min: 150, max: 180 },
      // Góc gối tại đáy squat (tùy người)
      knee_bottom: { min: 60, max: 130 },
      // Góc hông khi đứng
      hip_standing: { min: 150, max: 180 },
      // Góc hông tại đáy
      hip_bottom: { min: 50, max: 120 },
      // Trunk lean — góc trunk so với vertical
      trunk_lean_max: { min: 0, max: 45 },
    },
    minVisibility: 0.5,
    minHoldFrames: 3,
    hysteresisDeg: 10,
    minRepDurationMs: 1200,
    primaryAngleKey: 'knee',
    targetAngleMin: 80,
    targetAngleMax: 125,
  },
  'shoulder-raise': {
    angles: {
      // Góc vai khi tay hạ (tay xuôi theo thân)
      shoulder_down: { min: 0, max: 40 },
      // Góc vai khi tay nâng (ngang vai trở lên)
      shoulder_up: { min: 70, max: 180 },
      // Góc khuỷu tay (thẳng hoặc hơi cong)
      elbow_min: { min: 140, max: 180 },
    },
    minVisibility: 0.45,
    minHoldFrames: 3,
    hysteresisDeg: 8,
    minRepDurationMs: 900,
    primaryAngleKey: 'shoulder',
    targetAngleMin: 75,
    targetAngleMax: 180,
  },
  'side-leg-raise': {
    angles: {
      hip_rest: { min: 0, max: 15 },
      hip_abduction: { min: 25, max: 65 },
    },
    minVisibility: 0.45,
    minHoldFrames: 3,
    hysteresisDeg: 6,
    minRepDurationMs: 1000,
    primaryAngleKey: 'hip',
    targetAngleMin: 25,
    targetAngleMax: 65,
  },
};

// ============================================================
// Landmarks cần thiết cho từng bài tập
// ============================================================

export const REQUIRED_LANDMARKS: Record<ExerciseId, number[]> = {
  'sit-to-stand': [
    LANDMARK_NAMES.LEFT_SHOULDER,
    LANDMARK_NAMES.RIGHT_SHOULDER,
    LANDMARK_NAMES.LEFT_HIP,
    LANDMARK_NAMES.RIGHT_HIP,
    LANDMARK_NAMES.LEFT_KNEE,
    LANDMARK_NAMES.RIGHT_KNEE,
    LANDMARK_NAMES.LEFT_ANKLE,
    LANDMARK_NAMES.RIGHT_ANKLE,
  ],
  squat: [
    LANDMARK_NAMES.LEFT_SHOULDER,
    LANDMARK_NAMES.RIGHT_SHOULDER,
    LANDMARK_NAMES.LEFT_HIP,
    LANDMARK_NAMES.RIGHT_HIP,
    LANDMARK_NAMES.LEFT_KNEE,
    LANDMARK_NAMES.RIGHT_KNEE,
    LANDMARK_NAMES.LEFT_ANKLE,
    LANDMARK_NAMES.RIGHT_ANKLE,
  ],
  'shoulder-raise': [
    LANDMARK_NAMES.LEFT_SHOULDER,
    LANDMARK_NAMES.RIGHT_SHOULDER,
    LANDMARK_NAMES.LEFT_ELBOW,
    LANDMARK_NAMES.RIGHT_ELBOW,
    LANDMARK_NAMES.LEFT_WRIST,
    LANDMARK_NAMES.RIGHT_WRIST,
    LANDMARK_NAMES.LEFT_HIP,
    LANDMARK_NAMES.RIGHT_HIP,
  ],
  'side-leg-raise': [
    LANDMARK_NAMES.LEFT_SHOULDER,
    LANDMARK_NAMES.RIGHT_SHOULDER,
    LANDMARK_NAMES.LEFT_HIP,
    LANDMARK_NAMES.RIGHT_HIP,
    LANDMARK_NAMES.LEFT_KNEE,
    LANDMARK_NAMES.RIGHT_KNEE,
    LANDMARK_NAMES.LEFT_ANKLE,
    LANDMARK_NAMES.RIGHT_ANKLE,
  ],
};

// ============================================================
// Skeleton connections để vẽ overlay
// ============================================================

export const POSE_CONNECTIONS: [number, number][] = [
  // Torso
  [LANDMARK_NAMES.LEFT_SHOULDER, LANDMARK_NAMES.RIGHT_SHOULDER],
  [LANDMARK_NAMES.LEFT_SHOULDER, LANDMARK_NAMES.LEFT_HIP],
  [LANDMARK_NAMES.RIGHT_SHOULDER, LANDMARK_NAMES.RIGHT_HIP],
  [LANDMARK_NAMES.LEFT_HIP, LANDMARK_NAMES.RIGHT_HIP],
  // Left arm
  [LANDMARK_NAMES.LEFT_SHOULDER, LANDMARK_NAMES.LEFT_ELBOW],
  [LANDMARK_NAMES.LEFT_ELBOW, LANDMARK_NAMES.LEFT_WRIST],
  // Right arm
  [LANDMARK_NAMES.RIGHT_SHOULDER, LANDMARK_NAMES.RIGHT_ELBOW],
  [LANDMARK_NAMES.RIGHT_ELBOW, LANDMARK_NAMES.RIGHT_WRIST],
  // Left leg
  [LANDMARK_NAMES.LEFT_HIP, LANDMARK_NAMES.LEFT_KNEE],
  [LANDMARK_NAMES.LEFT_KNEE, LANDMARK_NAMES.LEFT_ANKLE],
  // Right leg
  [LANDMARK_NAMES.RIGHT_HIP, LANDMARK_NAMES.RIGHT_KNEE],
  [LANDMARK_NAMES.RIGHT_KNEE, LANDMARK_NAMES.RIGHT_ANKLE],
  // Face (simplified)
  [LANDMARK_NAMES.LEFT_EAR, LANDMARK_NAMES.LEFT_EYE],
  [LANDMARK_NAMES.RIGHT_EAR, LANDMARK_NAMES.RIGHT_EYE],
  [LANDMARK_NAMES.LEFT_EYE, LANDMARK_NAMES.NOSE],
  [LANDMARK_NAMES.RIGHT_EYE, LANDMARK_NAMES.NOSE],
  // Feet
  [LANDMARK_NAMES.LEFT_ANKLE, LANDMARK_NAMES.LEFT_HEEL],
  [LANDMARK_NAMES.LEFT_ANKLE, LANDMARK_NAMES.LEFT_FOOT_INDEX],
  [LANDMARK_NAMES.RIGHT_ANKLE, LANDMARK_NAMES.RIGHT_HEEL],
  [LANDMARK_NAMES.RIGHT_ANKLE, LANDMARK_NAMES.RIGHT_FOOT_INDEX],
];
