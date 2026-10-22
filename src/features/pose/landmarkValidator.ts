/**
 * landmarkValidator.ts
 * 
 * Đánh giá chất lượng landmarks từ MediaPipe:
 * - Visibility/presence của từng landmark
 * - Kiểm tra body regions (đầu, tay, hông, gối, bàn chân)
 * - Quyết định frame có đủ chất lượng để phân tích
 */

import {
  NormalizedLandmark,
  LandmarkValidation,
  LANDMARK_NAMES,
  BODY_REGIONS,
  CalibrationResult,
  CalibrationStatus,
} from '@/types';

const DEFAULT_MIN_VISIBILITY = 0.5;
const FULL_BODY_MIN_VISIBILITY = 0.4;

/**
 * Kiểm tra một landmark có đủ visibility không
 */
function isLandmarkVisible(
  landmark: NormalizedLandmark | undefined,
  minVisibility: number = DEFAULT_MIN_VISIBILITY
): boolean {
  if (!landmark) return false;
  return (landmark.visibility ?? 0) >= minVisibility;
}

/**
 * Kiểm tra một nhóm landmark có đủ visible không
 * Trả về true nếu >= ratio landmarks visible
 */
function isRegionVisible(
  landmarks: NormalizedLandmark[],
  indices: readonly number[],
  minVisibility: number = DEFAULT_MIN_VISIBILITY,
  requiredRatio: number = 0.5
): boolean {
  if (indices.length === 0) return false;
  const visibleCount = indices.filter((idx) =>
    isLandmarkVisible(landmarks[idx], minVisibility)
  ).length;
  return visibleCount / indices.length >= requiredRatio;
}

/**
 * Validate toàn bộ pose landmarks
 */
export function validateLandmarks(
  landmarks: NormalizedLandmark[],
  minVisibility: number = DEFAULT_MIN_VISIBILITY
): LandmarkValidation {
  if (!landmarks || landmarks.length < 33) {
    return {
      isValid: false,
      overallConfidence: 0,
      missingLandmarks: [],
      lowConfidenceLandmarks: [],
      bodyInFrame: false,
      headVisible: false,
      handsVisible: false,
      hipsVisible: false,
      kneesVisible: false,
      feetVisible: false,
    };
  }

  const missingLandmarks: number[] = [];
  const lowConfidenceLandmarks: number[] = [];
  let totalVisibility = 0;

  for (let i = 0; i < 33; i++) {
    const lm = landmarks[i];
    if (!lm) {
      missingLandmarks.push(i);
    } else {
      const vis = lm.visibility ?? 0;
      totalVisibility += vis;
      if (vis < minVisibility) {
        lowConfidenceLandmarks.push(i);
      }
    }
  }

  const overallConfidence = totalVisibility / 33;

  const headVisible = isRegionVisible(landmarks, BODY_REGIONS.HEAD, FULL_BODY_MIN_VISIBILITY);
  const handsVisible =
    isLandmarkVisible(landmarks[LANDMARK_NAMES.LEFT_WRIST], FULL_BODY_MIN_VISIBILITY) ||
    isLandmarkVisible(landmarks[LANDMARK_NAMES.RIGHT_WRIST], FULL_BODY_MIN_VISIBILITY);
  const hipsVisible = isRegionVisible(
    landmarks,
    [LANDMARK_NAMES.LEFT_HIP, LANDMARK_NAMES.RIGHT_HIP],
    FULL_BODY_MIN_VISIBILITY,
    0.5
  );
  const kneesVisible = isRegionVisible(
    landmarks,
    [LANDMARK_NAMES.LEFT_KNEE, LANDMARK_NAMES.RIGHT_KNEE],
    FULL_BODY_MIN_VISIBILITY,
    0.5
  );
  const feetVisible = isRegionVisible(
    landmarks,
    BODY_REGIONS.FEET,
    FULL_BODY_MIN_VISIBILITY,
    0.25
  );

  const bodyInFrame = headVisible && hipsVisible && kneesVisible;

  return {
    isValid: bodyInFrame && overallConfidence > 0.3,
    overallConfidence,
    missingLandmarks,
    lowConfidenceLandmarks,
    bodyInFrame,
    headVisible,
    handsVisible,
    hipsVisible,
    kneesVisible,
    feetVisible,
  };
}

let offscreenCanvas: HTMLCanvasElement | null = null;
let offscreenCtx: CanvasRenderingContext2D | null = null;

export interface LightingReport {
  status: 'good' | 'too_dark' | 'too_bright';
  brightness: number;
  message?: string;
}

/**
 * Kiểm tra điều kiện ánh sáng từ khung hình video
 */
export function checkLighting(video: HTMLVideoElement | null | undefined): LightingReport {
  if (typeof window === 'undefined' || !video || video.readyState < 2) {
    return { status: 'good', brightness: 128 };
  }

  try {
    if (!offscreenCanvas) {
      offscreenCanvas = document.createElement('canvas');
      offscreenCanvas.width = 32;
      offscreenCanvas.height = 24;
      offscreenCtx = offscreenCanvas.getContext('2d', { willReadFrequently: true });
    }

    if (!offscreenCtx) return { status: 'good', brightness: 128 };

    offscreenCtx.drawImage(video, 0, 0, 32, 24);
    const imgData = offscreenCtx.getImageData(0, 0, 32, 24).data;

    let totalLuminance = 0;
    const pixelCount = 32 * 24;

    for (let i = 0; i < imgData.length; i += 4) {
      const r = imgData[i];
      const g = imgData[i + 1];
      const b = imgData[i + 2];
      totalLuminance += 0.299 * r + 0.587 * g + 0.114 * b;
    }

    const avg = totalLuminance / pixelCount;

    if (avg < 48) {
      return {
        status: 'too_dark',
        brightness: Math.round(avg),
        message: '💡 Phòng hơi tối: Bác hãy bật thêm đèn để AI nhận diện rõ hơn.',
      };
    }

    if (avg > 225) {
      return {
        status: 'too_bright',
        brightness: Math.round(avg),
        message: '☀️ Ánh sáng quá chói hoặc ngược sáng: Bác hãy chỉnh lại góc camera.',
      };
    }

    return {
      status: 'good',
      brightness: Math.round(avg),
    };
  } catch {
    return { status: 'good', brightness: 128 };
  }
}

export interface DistanceReport {
  status: 'ideal' | 'too_close' | 'too_far';
  bodyHeightRatio: number;
  advice?: string;
}

/**
 * Đánh giá khoảng cách của người dùng so với camera
 */
export function checkDistance(landmarks: NormalizedLandmark[] | null | undefined): DistanceReport {
  if (!landmarks || landmarks.length < 33) {
    return { status: 'ideal', bodyHeightRatio: 0.5 };
  }

  let minY = 1;
  let maxY = 0;
  for (let i = 0; i < landmarks.length; i++) {
    const lm = landmarks[i];
    if (lm && (lm.visibility ?? 0) > 0.35) {
      if (lm.y < minY) minY = lm.y;
      if (lm.y > maxY) maxY = lm.y;
    }
  }

  const bodyHeightRatio = Math.max(0, maxY - minY);

  if (bodyHeightRatio > 0.90) {
    return {
      status: 'too_close',
      bodyHeightRatio,
      advice: '⚠️ Bác đang đứng hơi gần: Hãy lùi ra xa 1–2 bước.',
    };
  }

  if (bodyHeightRatio < 0.35) {
    return {
      status: 'too_far',
      bodyHeightRatio,
      advice: '⚠️ Bác đang đứng hơi xa: Hãy tiến lại gần camera một chút.',
    };
  }

  return {
    status: 'ideal',
    bodyHeightRatio,
    advice: '🎯 Khoảng cách hoàn hảo.',
  };
}

/**
 * Kiểm tra điều kiện calibration cho camera kèm chẩn đoán ánh sáng & khoảng cách
 */
export function checkCalibration(
  landmarks: NormalizedLandmark[] | null,
  hasCameraAccess: boolean,
  cameraError: string | null,
  videoElement?: HTMLVideoElement | null
): CalibrationResult {
  const lighting = checkLighting(videoElement);
  const distance = checkDistance(landmarks);

  if (cameraError === 'denied') {
    return {
      status: 'camera_denied',
      missingRegions: [],
      message: 'Vui lòng cấp quyền truy cập camera để tiếp tục.',
      canStart: false,
      lighting,
      distance,
    };
  }

  if (!hasCameraAccess) {
    return {
      status: 'checking_camera',
      missingRegions: [],
      message: 'Đang kết nối camera...',
      canStart: false,
      lighting,
      distance,
    };
  }

  if (!landmarks || landmarks.length < 33) {
    return {
      status: 'detecting_pose',
      missingRegions: [],
      message: 'Đang tìm kiếm cơ thể. Hãy đứng cách camera 2–3 mét và để toàn thân trong khung hình.',
      canStart: false,
      lighting,
      distance,
    };
  }

  const validation = validateLandmarks(landmarks, FULL_BODY_MIN_VISIBILITY);
  const missingRegions: string[] = [];

  if (!validation.headVisible) missingRegions.push('Đầu');
  if (!validation.handsVisible) missingRegions.push('Tay');
  if (!validation.hipsVisible) missingRegions.push('Hông');
  if (!validation.kneesVisible) missingRegions.push('Đầu gối');
  if (!validation.feetVisible) missingRegions.push('Bàn chân');

  if (missingRegions.length > 0) {
    let specificMessage = '';
    if (missingRegions.length === 1) {
      if (missingRegions[0] === 'Bàn chân') {
        specificMessage = 'Chưa thấy rõ bàn chân: Bác hãy chúc camera xuống một chút hoặc lùi lại xa hơn.';
      } else if (missingRegions[0] === 'Đầu') {
        specificMessage = 'Chưa thấy rõ đầu: Bác hãy ngửa camera lên một chút hoặc đứng lùi lại.';
      } else if (missingRegions[0] === 'Đầu gối') {
        specificMessage = 'Chưa thấy rõ đầu gối: Bác hãy dọn dẹp vật cản hoặc lùi lại.';
      } else {
        specificMessage = `Chưa thấy rõ: ${missingRegions[0]}. Hãy điều chỉnh vị trí đứng.`;
      }
    } else {
      specificMessage = `Chưa thấy rõ: ${missingRegions.join(', ')}. Hãy lùi ra xa hơn để lấy trọn thân người.`;
    }

    return {
      status: 'partial_body',
      missingRegions,
      message: specificMessage,
      canStart: false,
      lighting,
      distance,
    };
  }

  if (distance.status === 'too_close') {
    return {
      status: 'partial_body',
      missingRegions: [],
      message: 'Bác đang đứng hơi gần camera. Hãy lùi ra xa 1–2 bước để có góc nhìn tốt nhất.',
      canStart: false,
      lighting,
      distance,
    };
  }

  return {
    status: 'ready',
    missingRegions: [],
    message: 'Đã nhận diện đầy đủ toàn bộ khớp! Bài tập sẽ tự động bắt đầu ngay...',
    canStart: true,
    lighting,
    distance,
  };
}

/**
 * Kiểm tra nhanh frame có đủ chất lượng để phân tích bài tập
 */
export function isFrameUsable(
  landmarks: NormalizedLandmark[] | null,
  requiredIndices: number[],
  minVisibility: number = DEFAULT_MIN_VISIBILITY
): boolean {
  if (!landmarks || landmarks.length < 33) return false;

  return requiredIndices.every((idx) =>
    isLandmarkVisible(landmarks[idx], minVisibility)
  );
}
