/**
 * sideLegRaise.ts
 * 
 * Phân tích bài tập Standing Active Straight Leg Raise.
 * 
 * State flow: READY → ASCENDING → TOP → DESCENDING → COMPLETE
 * (Đứng thẳng, nâng chân thẳng ra trước ≥ 25°, hạ về = 1 rep)
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

    // Hip flexion is 0° when the torso and leg are aligned.
    const leftHipAngle = computeJointAngle(
      'left_hip_flexion', landmarks, LM.LEFT_SHOULDER, LM.LEFT_HIP, LM.LEFT_KNEE
    );
    const rightHipAngle = computeJointAngle(
      'right_hip_flexion', landmarks, LM.RIGHT_SHOULDER, LM.RIGHT_HIP, LM.RIGHT_KNEE
    );
    const leftRaiseAngle = leftHipAngle ? Math.max(0, 180 - leftHipAngle.angleDeg) : 0;
    const rightRaiseAngle = rightHipAngle ? Math.max(0, 180 - rightHipAngle.angleDeg) : 0;

    // Identify the leg with the greater forward raise.
    const isLeftRaising = leftRaiseAngle > rightRaiseAngle;
    const activeRawAngle = isLeftRaising ? leftRaiseAngle : rightRaiseAngle;

    // Smooth the hip-flexion signal.
    const smoothHipAngle = this.smoother.update('hip_flexion', activeRawAngle) ?? activeRawAngle;

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

    // State machine transitions
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
          suggestedState = 'COMPLETE';
          feedback.push('Hoàn thành!');
        }
        break;
      }
    }

    // Basic movement-quality criteria
    if (suggestedState === 'TOP') {
      if (activeKneeAngle < 135) {
        meetsBasicCriteria = false;
        feedback.push('Hãy giữ chân nâng tương đối thẳng.');
      }
      if (smoothHipAngle < 25) {
        feedback.push('Cố gắng nâng chân cao hơn một chút.');
      }
    }

    this.lastState = suggestedState === 'COMPLETE' ? 'READY' : suggestedState;

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
