/**
 * squat.ts
 * 
 * Phân tích bài tập Squat.
 * 
 * State flow: READY → DESCENDING → BOTTOM → ASCENDING → COMPLETE
 * (Từ đứng, hạ xuống, đứng lên = 1 rep)
 * 
 * Đặc trưng phân tích:
 * - Góc gối
 * - Góc hông
 * - Độ nghiêng thân (trunk lean)
 * - Tính đối xứng hai bên
 */

import { NormalizedLandmark, LANDMARK_NAMES, ExerciseState } from '@/types';
import { ExerciseAnalyzer, FrameAnalysis } from './stateMachine';
import { computeJointAngle, midpoint } from '../pose/angleCalculator';
import { MultiSignalSmoother } from '../pose/signalSmoother';
import { isFrameUsable } from '../pose/landmarkValidator';
import { EXERCISE_THRESHOLDS, REQUIRED_LANDMARKS } from './exerciseRules';

const LM = LANDMARK_NAMES;
const THRESHOLDS = EXERCISE_THRESHOLDS['squat'];

export class SquatAnalyzer implements ExerciseAnalyzer {
  private smoother = new MultiSignalSmoother({ alpha: 0.3 });
  private lastState: ExerciseState = 'READY';

  analyzeFrame(landmarks: NormalizedLandmark[]): FrameAnalysis {
    const usable = isFrameUsable(
      landmarks,
      REQUIRED_LANDMARKS['squat'],
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

    // Tính góc
    const leftKnee = computeJointAngle(
      'left_knee', landmarks, LM.LEFT_HIP, LM.LEFT_KNEE, LM.LEFT_ANKLE
    );
    const rightKnee = computeJointAngle(
      'right_knee', landmarks, LM.RIGHT_HIP, LM.RIGHT_KNEE, LM.RIGHT_ANKLE
    );
    const leftHip = computeJointAngle(
      'left_hip', landmarks, LM.LEFT_SHOULDER, LM.LEFT_HIP, LM.LEFT_KNEE
    );
    const rightHip = computeJointAngle(
      'right_hip', landmarks, LM.RIGHT_SHOULDER, LM.RIGHT_HIP, LM.RIGHT_KNEE
    );

    const kneeAngle = this.averageAngle(leftKnee, rightKnee);
    const hipAngle = this.averageAngle(leftHip, rightHip);

    if (kneeAngle === null || hipAngle === null) {
      return {
        suggestedState: this.lastState,
        angles: {},
        isUsable: false,
        feedback: [],
        meetsBasicCriteria: true,
      };
    }

    // Tính trunk lean (góc thân người so với vertical)
    const midShoulder = midpoint(landmarks[LM.LEFT_SHOULDER], landmarks[LM.RIGHT_SHOULDER]);
    const midHip = midpoint(landmarks[LM.LEFT_HIP], landmarks[LM.RIGHT_HIP]);
    const trunkLean = Math.abs(
      Math.atan2(midShoulder.x - midHip.x, midHip.y - midShoulder.y) * (180 / Math.PI)
    );

    // Tính đối xứng
    const kneeSymmetry = leftKnee && rightKnee
      ? Math.abs(leftKnee.angleDeg - rightKnee.angleDeg)
      : null;

    // Smooth
    const smoothKnee = this.smoother.update('knee', kneeAngle) ?? kneeAngle;
    const smoothHip = this.smoother.update('hip', hipAngle) ?? hipAngle;
    const smoothTrunk = this.smoother.update('trunk', trunkLean) ?? trunkLean;

    const angles = {
      knee: smoothKnee,
      hip: smoothHip,
      trunkLean: smoothTrunk,
      kneeSymmetry: kneeSymmetry ?? 0,
    };

    const feedback: string[] = [];
    let meetsBasicCriteria = true;
    let suggestedState = this.lastState;

    const isStanding =
      smoothKnee >= THRESHOLDS.angles.knee_standing.min;

    const isBottom =
      smoothKnee <= THRESHOLDS.angles.knee_bottom.max;

    const H = THRESHOLDS.hysteresisDeg;

    switch (this.lastState) {
      case 'READY':
        if (isStanding) {
          feedback.push('Sẵn sàng. Hạ người xuống từ từ.');
        }
        if (smoothKnee < THRESHOLDS.angles.knee_standing.min - H) {
          suggestedState = 'DESCENDING';
        }
        break;

      case 'DESCENDING':
        if (isBottom) {
          suggestedState = 'BOTTOM';
          feedback.push('Tốt! Giữ tư thế.');
        } else {
          feedback.push('Tiếp tục hạ người.');
        }

        // Kiểm tra trunk lean
        if (smoothTrunk > THRESHOLDS.angles.trunk_lean_max.max) {
          feedback.push('Giữ thân người thẳng hơn.');
        }
        break;

      case 'BOTTOM':
        if (smoothKnee > THRESHOLDS.angles.knee_bottom.max + H) {
          suggestedState = 'ASCENDING';
          feedback.push('Đứng lên từ từ.');
        } else {
          feedback.push('Giữ tư thế đáy.');
        }
        break;

      case 'ASCENDING':
        if (isStanding) {
          suggestedState = 'COMPLETE';
          feedback.push('Hoàn thành!');
        } else {
          feedback.push('Tiếp tục đứng lên.');
        }
        break;

      case 'COMPLETE':
        suggestedState = 'COMPLETE';
        break;
    }

    // Kiểm tra tiêu chí
    if (suggestedState === 'BOTTOM' || this.lastState === 'BOTTOM') {
      // Biên độ chưa đủ sâu
      if (smoothKnee > THRESHOLDS.angles.knee_bottom.max + 15) {
        meetsBasicCriteria = false;
        feedback.push('Hạ sâu hơn nếu có thể.');
      }
    }

    // Đối xứng — chỉ cảnh báo tham khảo khi đủ dữ liệu
    if (kneeSymmetry !== null && kneeSymmetry > 20) {
      feedback.push('Hai bên gối đang không đều (chỉ báo tham khảo).');
    }

    // Trunk lean quá nhiều
    if (smoothTrunk > THRESHOLDS.angles.trunk_lean_max.max + 10) {
      meetsBasicCriteria = false;
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
