/**
 * shoulderRaise.ts
 * 
 * Phân tích bài tập Nâng tay (Shoulder/Arm Raise).
 * 
 * State flow: READY → ASCENDING → TOP → DESCENDING → COMPLETE
 * (Từ tay hạ, nâng lên, hạ xuống = 1 rep)
 * 
 * Đặc trưng phân tích:
 * - Góc vai (hip-shoulder-elbow hoặc hip-shoulder-wrist)
 * - Góc khuỷu tay
 * - Vị trí cổ tay so với vai
 * - Đối xứng hai bên
 */

import { NormalizedLandmark, LANDMARK_NAMES, ExerciseState } from '@/types';
import { ExerciseAnalyzer, FrameAnalysis } from './stateMachine';
import { computeJointAngle } from '../pose/angleCalculator';
import { MultiSignalSmoother } from '../pose/signalSmoother';
import { isFrameUsable } from '../pose/landmarkValidator';
import { EXERCISE_THRESHOLDS, REQUIRED_LANDMARKS } from './exerciseRules';

const LM = LANDMARK_NAMES;
const THRESHOLDS = EXERCISE_THRESHOLDS['shoulder-raise'];

export class ShoulderRaiseAnalyzer implements ExerciseAnalyzer {
  private smoother = new MultiSignalSmoother({ alpha: 0.3 });
  private lastState: ExerciseState = 'READY';

  analyzeFrame(landmarks: NormalizedLandmark[]): FrameAnalysis {
    const usable = isFrameUsable(
      landmarks,
      REQUIRED_LANDMARKS['shoulder-raise'],
      THRESHOLDS.minVisibility
    );

    if (!usable) {
      return {
        suggestedState: this.lastState,
        angles: {},
        isUsable: false,
        feedback: [],
        meetsBasicCriteria: true,
      };
    }

    // Tính góc vai (hip-shoulder-elbow)
    const leftShoulder = computeJointAngle(
      'left_shoulder', landmarks, LM.LEFT_HIP, LM.LEFT_SHOULDER, LM.LEFT_ELBOW
    );
    const rightShoulder = computeJointAngle(
      'right_shoulder', landmarks, LM.RIGHT_HIP, LM.RIGHT_SHOULDER, LM.RIGHT_ELBOW
    );

    // Tính góc khuỷu tay
    const leftElbow = computeJointAngle(
      'left_elbow', landmarks, LM.LEFT_SHOULDER, LM.LEFT_ELBOW, LM.LEFT_WRIST
    );
    const rightElbow = computeJointAngle(
      'right_elbow', landmarks, LM.RIGHT_SHOULDER, LM.RIGHT_ELBOW, LM.RIGHT_WRIST
    );

    const shoulderAngle = this.averageAngle(leftShoulder, rightShoulder);
    const elbowAngle = this.averageAngle(leftElbow, rightElbow);

    if (shoulderAngle === null) {
      return {
        suggestedState: this.lastState,
        angles: {},
        isUsable: false,
        feedback: [],
        meetsBasicCriteria: true,
      };
    }

    // Đối xứng vai
    const shoulderSymmetry = leftShoulder && rightShoulder
      ? Math.abs(leftShoulder.angleDeg - rightShoulder.angleDeg)
      : null;

    // Wrist position relative to shoulder (y-axis)
    const leftWristAboveShoulder =
      landmarks[LM.LEFT_WRIST].y < landmarks[LM.LEFT_SHOULDER].y;
    const rightWristAboveShoulder =
      landmarks[LM.RIGHT_WRIST].y < landmarks[LM.RIGHT_SHOULDER].y;

    // Smooth
    const smoothShoulder = this.smoother.update('shoulder', shoulderAngle) ?? shoulderAngle;
    const smoothElbow = this.smoother.update('elbow', elbowAngle) ?? elbowAngle;

    const angles = {
      shoulder: smoothShoulder,
      elbow: smoothElbow ?? 0,
      shoulderSymmetry: shoulderSymmetry ?? 0,
    };

    const feedback: string[] = [];
    let meetsBasicCriteria = true;
    let suggestedState = this.lastState;

    const isDown = smoothShoulder <= THRESHOLDS.angles.shoulder_down.max;
    const isUp = smoothShoulder >= THRESHOLDS.angles.shoulder_up.min;

    const H = THRESHOLDS.hysteresisDeg;

    switch (this.lastState) {
      case 'READY':
        if (isDown) {
          feedback.push('Sẵn sàng. Nâng tay lên từ từ.');
        }
        if (smoothShoulder > THRESHOLDS.angles.shoulder_down.max + H) {
          suggestedState = 'ASCENDING';
        }
        break;

      case 'ASCENDING':
        if (isUp) {
          suggestedState = 'TOP';
          feedback.push('Tốt! Giữ tay ở vị trí cao.');
        } else {
          feedback.push('Tiếp tục nâng tay.');
        }
        break;

      case 'TOP':
        if (smoothShoulder < THRESHOLDS.angles.shoulder_up.min - H) {
          suggestedState = 'DESCENDING';
          feedback.push('Hạ tay xuống từ từ.');
        } else {
          feedback.push('Giữ tay cao.');
        }
        break;

      case 'DESCENDING':
        if (isDown) {
          suggestedState = 'COMPLETE';
          feedback.push('Hoàn thành!');
        } else {
          feedback.push('Hạ tay từ từ.');
        }
        break;

      case 'COMPLETE':
        suggestedState = 'COMPLETE';
        break;
    }

    // Kiểm tra tiêu chí
    if (suggestedState === 'TOP' || this.lastState === 'TOP') {
      if (smoothShoulder < THRESHOLDS.angles.shoulder_up.min - 10) {
        meetsBasicCriteria = false;
        feedback.push('Nâng tay cao hơn nếu có thể.');
      }
    }

    // Đối xứng — chỉ báo tham khảo
    if (shoulderSymmetry !== null && shoulderSymmetry > 25) {
      feedback.push('Hai bên tay đang nâng không đều (chỉ báo tham khảo).');
    }

    this.lastState = suggestedState;

    return {
      suggestedState,
      angles,
      isUsable: true,
      feedback,
      meetsBasicCriteria,
    };
  }

  reset(): void {
    this.smoother.reset();
    this.lastState = 'READY';
  }

  private averageAngle(
    left: { angleDeg: number; confidence: number } | null,
    right: { angleDeg: number; confidence: number } | null
  ): number | null {
    if (left && right) {
      const totalConf = left.confidence + right.confidence;
      if (totalConf === 0) return (left.angleDeg + right.angleDeg) / 2;
      return (
        (left.angleDeg * left.confidence + right.angleDeg * right.confidence) /
        totalConf
      );
    }
    if (left) return left.angleDeg;
    if (right) return right.angleDeg;
    return null;
  }
}
