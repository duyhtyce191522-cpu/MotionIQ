/**
 * stateMachine.ts
 * 
 * Generic exercise state machine framework.
 * Mỗi bài tập implement ExerciseAnalyzer interface.
 * State machine đảm bảo:
 * - Mỗi cycle chỉ đếm 1 rep
 * - Hysteresis chống dao động
 * - Không đếm khi tracking kém
 * - Xử lý pause/resume
 */

import { ExerciseState, RepetitionResult, NormalizedLandmark } from '@/types';

export interface FrameAnalysis {
  /** Trạng thái mới dựa trên frame hiện tại */
  suggestedState: ExerciseState;
  /** Các góc khớp đã tính */
  angles: Record<string, number>;
  /** Frame có đủ chất lượng không */
  isUsable: boolean;
  /** Phản hồi cho frame này */
  feedback: string[];
  /** Rep hiện tại đạt tiêu chí cơ bản */
  meetsBasicCriteria: boolean;
}

export interface ExerciseAnalyzer {
  /** Phân tích frame và đề xuất trạng thái */
  analyzeFrame(landmarks: NormalizedLandmark[]): FrameAnalysis;
  /** Reset analyzer */
  reset(): void;
}

/**
 * State machine quản lý chuyển trạng thái và đếm repetition
 */
export class RepetitionStateMachine {
  private state: ExerciseState = 'IDLE';
  private stateStartTime: number = 0;
  private stateFrameCount: number = 0;
  private repStartTime: number = 0;
  
  private repetitions: RepetitionResult[] = [];
  private currentRepFeedback: string[] = [];
  private currentRepAngles: Record<string, number> = {};
  private currentRepMeetsCriteria: boolean = true;
  
  private minHoldFrames: number;
  private minRepDurationMs: number;
  private unusableFrameCount: number = 0;
  private maxUnusableFrames: number = 15; // ~0.5s at 30fps

  constructor(minHoldFrames: number = 3, minRepDurationMs: number = 1000) {
    this.minHoldFrames = minHoldFrames;
    this.minRepDurationMs = minRepDurationMs;
  }

  /**
   * Xử lý kết quả phân tích frame
   */
  processFrame(analysis: FrameAnalysis): {
    state: ExerciseState;
    repCompleted: boolean;
    totalReps: number;
    feedback: string[];
    angles: Record<string, number>;
  } {
    // Nếu frame không usable, đếm số frame liên tiếp không usable
    if (!analysis.isUsable) {
      this.unusableFrameCount++;
      
      // Nếu mất tracking quá lâu, reset về IDLE
      if (this.unusableFrameCount > this.maxUnusableFrames && this.state !== 'IDLE') {
        this.state = 'IDLE';
        this.stateFrameCount = 0;
      }
      
      return {
        state: this.state,
        repCompleted: false,
        totalReps: this.repetitions.length,
        feedback: ['Chưa thấy rõ cơ thể. Hãy điều chỉnh vị trí.'],
        angles: {},
      };
    }

    this.unusableFrameCount = 0;
    const { suggestedState, angles, feedback, meetsBasicCriteria } = analysis;

    // Collect feedback và angles cho rep hiện tại
    if (this.state !== 'IDLE' && this.state !== 'READY') {
      this.currentRepFeedback.push(...feedback);
      Object.assign(this.currentRepAngles, angles);
      if (!meetsBasicCriteria) {
        this.currentRepMeetsCriteria = false;
      }
    }

    let repCompleted = false;

    // Chuyển trạng thái với hysteresis (minHoldFrames)
    if (suggestedState !== this.state) {
      this.stateFrameCount++;
      
      if (this.stateFrameCount >= this.minHoldFrames) {
        const previousState = this.state;
        this.state = suggestedState;
        this.stateStartTime = Date.now();
        this.stateFrameCount = 0;

        // Bắt đầu rep mới khi rời khỏi READY sang trạng thái vận động
        if (
          previousState === 'READY' &&
          (suggestedState === 'ASCENDING' ||
            suggestedState === 'DESCENDING' ||
            suggestedState === 'TOP' ||
            suggestedState === 'BOTTOM')
        ) {
          this.repStartTime = Date.now();
          this.currentRepFeedback = [];
          this.currentRepAngles = {};
          this.currentRepMeetsCriteria = true;
        }

        // Hoàn thành rep
        if (suggestedState === 'COMPLETE') {
          const now = Date.now();
          const duration = this.repStartTime > 0 ? now - this.repStartTime : 0;

          // Chống đếm ảo: Chỉ ghi nhận nếu thời gian thực hiện tối thiểu >= minRepDurationMs
          if (duration >= this.minRepDurationMs) {
            const rep: RepetitionResult = {
              repNumber: this.repetitions.length + 1,
              startTime: this.repStartTime,
              endTime: now,
              duration,
              meetsBasicCriteria: this.currentRepMeetsCriteria,
              feedback: Array.from(new Set(this.currentRepFeedback)), // Deduplicate
              angles: { ...this.currentRepAngles },
            };
            this.repetitions.push(rep);
            repCompleted = true;
          } else {
            console.log(`[StateMachine] Rep ignored as jitter/too fast: ${duration}ms < ${this.minRepDurationMs}ms`);
          }

          // Chuyển về READY để sẵn sàng cho rep tiếp theo
          this.state = 'READY';
          this.currentRepFeedback = [];
          this.currentRepAngles = {};
          this.currentRepMeetsCriteria = true;
        }
      }
    } else {
      this.stateFrameCount = 0;
    }

    return {
      state: this.state,
      repCompleted,
      totalReps: this.repetitions.length,
      feedback,
      angles,
    };
  }

  /** Lấy tất cả repetitions */
  getRepetitions(): RepetitionResult[] {
    return [...this.repetitions];
  }

  /** Lấy số rep đạt tiêu chí */
  getGoodReps(): number {
    return this.repetitions.filter((r) => r.meetsBasicCriteria).length;
  }

  /** Lấy trạng thái hiện tại */
  getState(): ExerciseState {
    return this.state;
  }

  /** Chuyển sang READY khi bắt đầu tập */
  start(): void {
    this.state = 'READY';
    this.stateStartTime = Date.now();
    this.stateFrameCount = 0;
  }

  /** Reset state machine */
  reset(): void {
    this.state = 'IDLE';
    this.stateStartTime = 0;
    this.stateFrameCount = 0;
    this.repStartTime = 0;
    this.repetitions = [];
    this.currentRepFeedback = [];
    this.currentRepAngles = {};
    this.currentRepMeetsCriteria = true;
    this.unusableFrameCount = 0;
  }
}
