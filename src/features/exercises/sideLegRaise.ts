/**
 * sideLegRaise.ts
 * 
 * Phân tích bài tập Giạng chân sang bên (Side Leg Raise / Hip Abduction).
 * Bài tập lâm sàng quan trọng nhất để tăng cường cơ mông nhỡ và chống té ngã ở người cao tuổi.
 * 
 * State flow: READY → ASCENDING → TOP → DESCENDING → COMPLETE
 * (Đứng thẳng, giạng một chân sang bên góc ≥ 25°, hạ về = 1 rep)
 */

import { NormalizedLandmark, LANDMARK_NAMES, ExerciseState } from '@/types';
import { ExerciseAnalyzer, FrameAnalysis } from './stateMachine';
import { computeJointAngle } from '../pose/angleCalculator';
import { MultiSignalSmoother } from '../pose/signalSmoother';
import { isFrameUsable } from '../pose/landmarkValidator';
import { EXERCISE_THRESHOLDS, REQUIRED_LANDMARKS } from './exerciseRules';

const LM = LANDMARK_NAMES;
const THRESHOLDS = EXERCISE_THRESHOLDS['side-leg-raise'];

export class SideLegRaiseAnalyzer implements ExerciseAnalyzer {
  private smoother = new MultiSignalSmoother({ alpha: 0.35 });
  private lastState: ExerciseState = 'READY';

  analyzeFrame(landmarks: NormalizedLandmark[]): FrameAnalysis {
    const usable = isFrameUsable(
      landmarks,
      REQUIRED_LANDMARKS['side-leg-raise'],
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

    // Góc giạng chân trái và phải so với trục giữa hai hông
    const leftAbduction = computeJointAngle(
      'left_hip_abd', landmarks, LM.RIGHT_HIP, LM.LEFT_HIP, LM.LEFT_KNEE, false
    );
    const rightAbduction = computeJointAngle(
      'right_hip_abd', landmarks, LM.LEFT_HIP, LM.RIGHT_HIP, LM.RIGHT_KNEE, false
    );

    // Chuyển sang góc nâng (0 độ khi đứng thẳng)
    const leftRaiseAngle = leftAbduction ? Math.max(0, Math.abs(leftAbduction.angleDeg - 90)) : 0;
    const rightRaiseAngle = rightAbduction ? Math.max(0, Math.abs(rightAbduction.angleDeg - 90)) : 0;

    // Xác định chân nào đang được nâng tích cực
    const isLeftRaising = leftRaiseAngle > rightRaiseAngle;
    const activeRawAngle = isLeftRaising ? leftRaiseAngle : rightRaiseAngle;

    // Làm mượt tín hiệu góc giạng chân
    const smoothHipAngle = this.smoother.update('hip_abd', activeRawAngle) ?? activeRawAngle;

    // Kiểm tra độ thẳng của gối chân đang nâng
    const activeKneeAngle = isLeftRaising
      ? computeJointAngle('left_knee', landmarks, LM.LEFT_HIP, LM.LEFT_KNEE, LM.LEFT_ANKLE)?.angleDeg ?? 170
      : computeJointAngle('right_knee', landmarks, LM.RIGHT_HIP, LM.RIGHT_KNEE, LM.RIGHT_ANKLE)?.angleDeg ?? 170;

    const angles: Record<string, number> = {
      hip: Math.round(smoothHipAngle),
      activeKnee: Math.round(activeKneeAngle),
    };

    const feedback: string[] = [];
    let meetsBasicCriteria = true;
    let suggestedState = this.lastState;

    // State Machine Transitions
    switch (this.lastState) {
      case 'READY':
      case 'BOTTOM': {
        if (smoothHipAngle >= 14) {
          suggestedState = 'ASCENDING';
        }
        break;
      }
      case 'ASCENDING': {
        if (smoothHipAngle >= 25) {
          suggestedState = 'TOP';
        } else if (smoothHipAngle < 8) {
          suggestedState = 'READY';
        }
        break;
      }
      case 'TOP': {
        if (smoothHipAngle < 22) {
          suggestedState = 'DESCENDING';
        }
        break;
      }
      case 'DESCENDING': {
        if (smoothHipAngle <= 10) {
          suggestedState = 'BOTTOM';
        }
        break;
      }
    }

    // Tiêu chí chất lượng lâm sàng
    if (suggestedState === 'TOP') {
      if (activeKneeAngle < 135) {
        meetsBasicCriteria = false;
        feedback.push('Hãy giữ chân nâng tương đối thẳng');
      }
      if (smoothHipAngle < 25) {
        feedback.push('Cố gắng giạng chân cao hơn một chút');
      }
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
}
