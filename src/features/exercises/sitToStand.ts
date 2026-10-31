/**
 * sitToStand.ts
 * 
 * Phân tích bài tập Đứng lên – Ngồi xuống (Sit-to-Stand).
 * 
 * State flow: READY → ASCENDING → TOP → DESCENDING → COMPLETE
 * (Bắt đầu từ tư thế ngồi, đứng lên, ngồi xuống = 1 rep)
 * 
 * Đặc trưng phân tích:
 * - Góc gối (hip-knee-ankle)
 * - Góc hông (shoulder-hip-knee)
 * - Vị trí tương đối hông vs gối
 * - Sự thay đổi theo thời gian
 */

import { NormalizedLandmark, LANDMARK_NAMES, ExerciseState } from '@/types';
import { ExerciseAnalyzer, FrameAnalysis } from './stateMachine';
import { computeJointAngle } from '../pose/angleCalculator';
import { MultiSignalSmoother } from '../pose/signalSmoother';
import { isFrameUsable } from '../pose/landmarkValidator';
import { EXERCISE_THRESHOLDS, REQUIRED_LANDMARKS } from './exerciseRules';

const LM = LANDMARK_NAMES;
const THRESHOLDS = EXERCISE_THRESHOLDS['sit-to-stand'];

export class SitToStandAnalyzer implements ExerciseAnalyzer {
  private smoother = new MultiSignalSmoother({ alpha: 0.3 });
  private lastState: ExerciseState = 'READY';

  analyzeFrame(landmarks: NormalizedLandmark[]): FrameAnalysis {
    // Kiểm tra landmarks cần thiết
    const usable = isFrameUsable(
      landmarks,
      REQUIRED_LANDMARKS['sit-to-stand'],
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

    // Tính góc gối (2 bên, lấy trung bình)
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

    // Tính trung bình có trọng số theo confidence
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

    // Smooth signals
    const smoothKnee = this.smoother.update('knee', kneeAngle) ?? kneeAngle;
    const smoothHip = this.smoother.update('hip', hipAngle) ?? hipAngle;

    const angles = {
      knee: smoothKnee,
      hip: smoothHip,
    };

    // Xác định trạng thái
    const feedback: string[] = [];
    let meetsBasicCriteria = true;
    let suggestedState = this.lastState;

    const isSitting =
      smoothKnee <= THRESHOLDS.angles.knee_sitting.max &&
      smoothHip <= THRESHOLDS.angles.hip_sitting.max;
    
    const isStanding =
      smoothKnee >= THRESHOLDS.angles.knee_standing.min &&
      smoothHip >= THRESHOLDS.angles.hip_standing.min;

    // Hysteresis: thêm margin khi chuyển trạng thái
    const H = THRESHOLDS.hysteresisDeg;

    switch (this.lastState) {
      case 'READY':
        // Chờ ở tư thế ngồi hoặc đứng
        if (isSitting) {
          // Người đang ngồi, bắt đầu đợi đứng lên
          suggestedState = 'READY';
          feedback.push('Sẵn sàng. Hãy đứng lên từ từ.');
        } else if (isStanding) {
          suggestedState = 'READY';
          feedback.push('Hãy ngồi xuống ghế trước khi bắt đầu.');
        } else {
          // Đang chuyển động — bắt đầu ascending
          if (smoothKnee > THRESHOLDS.angles.knee_sitting.max + H) {
            suggestedState = 'ASCENDING';
          }
        }
        break;

      case 'ASCENDING':
        // Đang đứng lên
        if (isStanding) {
          suggestedState = 'TOP';
          feedback.push('Tốt! Đứng thẳng.');
        } else {
          feedback.push('Tiếp tục đứng lên.');
          // Kiểm tra hông có mở đủ không
          if (smoothHip < 100) {
            feedback.push('Giữ lưng thẳng hơn.');
          }
        }
        break;

      case 'TOP':
        // Đã đứng thẳng, chờ ngồi xuống
        if (smoothKnee < THRESHOLDS.angles.knee_standing.min - H) {
          suggestedState = 'DESCENDING';
          feedback.push('Ngồi xuống từ từ.');
        } else {
          feedback.push('Giữ tư thế đứng thẳng.');
        }
        break;

      case 'DESCENDING':
        // Đang ngồi xuống
        if (isSitting) {
          suggestedState = 'COMPLETE';
          feedback.push('Hoàn thành!');
        } else {
          feedback.push('Từ từ ngồi xuống ghế.');
        }
        // Kiểm tra có ngồi xuống quá nhanh
        break;

      case 'COMPLETE':
        // State machine sẽ tự chuyển về READY
        suggestedState = 'COMPLETE';
        break;
    }

    // Kiểm tra tiêu chí cơ bản
    if (this.lastState === 'TOP' || suggestedState === 'TOP') {
      if (smoothKnee < THRESHOLDS.angles.knee_standing.min - 5) {
        meetsBasicCriteria = false;
        feedback.push('Chưa đứng thẳng hoàn toàn.');
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
