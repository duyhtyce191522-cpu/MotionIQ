/**
 * poseService.ts
 * 
 * Khởi tạo và quản lý MediaPipe Pose Landmarker.
 * Chạy trên thiết bị (Edge AI), không gửi video lên server.
 * 
 * Sử dụng @mediapipe/tasks-vision PoseLandmarker API.
 */

import { PoseResult, NormalizedLandmark } from '@/types';

// MediaPipe model URLs
const WASM_URL = 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.18/wasm';
const MODEL_URL = 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task';

export type PoseCallback = (result: PoseResult) => void;

export interface PoseServiceConfig {
  /** GPU hoặc CPU delegate */
  delegate: 'GPU' | 'CPU';
  /** Số poses tối đa (mặc định 1) */
  numPoses: number;
  /** Confidence tối thiểu */
  minDetectionConfidence: number;
  minTrackingConfidence: number;
  minPresenceConfidence: number;
}

const DEFAULT_CONFIG: PoseServiceConfig = {
  delegate: 'GPU',
  numPoses: 1,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5,
  minPresenceConfidence: 0.5,
};

/**
 * Service quản lý MediaPipe Pose Landmarker
 */
export class PoseService {
  private static cachedFilesetResolver: any = null;
  private static prewarmPromise: Promise<void> | null = null;

  private poseLandmarker: any = null; // MediaPipe PoseLandmarker
  private isInitialized: boolean = false;
  private isInitializing: boolean = false;
  private config: PoseServiceConfig;
  private onResult: PoseCallback | null = null;
  private animationFrameId: number | null = null;
  private videoElement: HTMLVideoElement | null = null;
  private lastTimestamp: number = -1;

  // Real-time FPS & Adaptive performance
  private frameCount: number = 0;
  private fps: number = 30;
  private lastFpsUpdateTime: number = performance.now();
  private skipAlternateFrames: boolean = false;
  private lowFpsCounter: number = 0;

  constructor(config: Partial<PoseServiceConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Tải trước WASM và mô hình trong nền để giảm thời gian khởi động về 0 giây
   */
  static prewarm(): Promise<void> {
    if (typeof window === 'undefined') return Promise.resolve();
    if (this.prewarmPromise) return this.prewarmPromise;

    this.prewarmPromise = (async () => {
      try {
        const vision = await import('@mediapipe/tasks-vision');
        const { FilesetResolver } = vision;
        this.cachedFilesetResolver = await FilesetResolver.forVisionTasks(WASM_URL);
        // Pre-fetch model to browser HTTP cache in parallel
        fetch(MODEL_URL, { mode: 'cors' }).catch(() => {});
        console.log('[PoseService] Prewarm completed');
      } catch (err) {
        console.warn('[PoseService] Prewarm warning (non-fatal):', err);
      }
    })();

    return this.prewarmPromise;
  }

  /**
   * Khởi tạo MediaPipe Pose Landmarker
   */
  async initialize(): Promise<void> {
    if (this.isInitialized || this.isInitializing) return;
    this.isInitializing = true;

    try {
      const vision = await import('@mediapipe/tasks-vision');
      const { FilesetResolver, PoseLandmarker } = vision;

      const filesetResolver =
        PoseService.cachedFilesetResolver || (await FilesetResolver.forVisionTasks(WASM_URL));
      PoseService.cachedFilesetResolver = filesetResolver;

      this.poseLandmarker = await PoseLandmarker.createFromOptions(
        filesetResolver,
        {
          baseOptions: {
            modelAssetPath: MODEL_URL,
            delegate: this.config.delegate,
          },
          runningMode: 'VIDEO',
          numPoses: this.config.numPoses,
          minPoseDetectionConfidence: this.config.minDetectionConfidence,
          minTrackingConfidence: this.config.minTrackingConfidence,
          minPosePresenceConfidence: this.config.minPresenceConfidence,
        }
      );

      this.isInitialized = true;
      console.log('[PoseService] Initialized successfully');
    } catch (error) {
      console.error('[PoseService] Failed to initialize:', error);
      
      // Fallback to CPU if GPU fails
      if (this.config.delegate === 'GPU') {
        console.log('[PoseService] Retrying with CPU delegate...');
        this.config.delegate = 'CPU';
        this.isInitializing = false;
        return this.initialize();
      }
      
      throw error;
    } finally {
      this.isInitializing = false;
    }
  }

  /**
   * Bắt đầu xử lý frames từ video element
   */
  startProcessing(
    videoElement: HTMLVideoElement,
    callback: PoseCallback
  ): void {
    this.videoElement = videoElement;
    this.onResult = callback;
    this.lastTimestamp = -1;
    this.frameCount = 0;
    this.lastFpsUpdateTime = performance.now();
    this.processFrame();
  }

  /**
   * Xử lý một frame
   */
  private processFrame = (): void => {
    if (!this.poseLandmarker || !this.videoElement || !this.onResult) {
      return;
    }

    const video = this.videoElement;
    
    if (video.readyState >= 2) {
      const timestamp = performance.now();

      // Cập nhật FPS & Kiểm tra điều chỉnh hiệu năng mượt mà cho máy cấu hình yếu
      this.frameCount++;
      if (timestamp - this.lastFpsUpdateTime >= 1000) {
        this.fps = Math.round((this.frameCount * 1000) / (timestamp - this.lastFpsUpdateTime));
        this.frameCount = 0;
        this.lastFpsUpdateTime = timestamp;

        if (this.fps < 18) {
          this.lowFpsCounter++;
          if (this.lowFpsCounter >= 2) {
            this.skipAlternateFrames = true; // Bật chế độ tiết kiệm tài nguyên
          }
        } else if (this.fps >= 26 && this.skipAlternateFrames) {
          this.lowFpsCounter = 0;
          this.skipAlternateFrames = false;
        }
      }

      // Nếu đang ở chế độ tiết kiệm/máy yếu, xử lý cách quãng 1 frame
      if (this.skipAlternateFrames && this.frameCount % 2 !== 0) {
        this.animationFrameId = requestAnimationFrame(this.processFrame);
        return;
      }
      
      // Tránh xử lý cùng timestamp
      if (timestamp !== this.lastTimestamp) {
        try {
          const result = this.poseLandmarker.detectForVideo(video, timestamp);
          
          const poseResult: PoseResult = {
            landmarks: result.landmarks || [],
            worldLandmarks: result.worldLandmarks || [],
            timestamp,
          };

          this.onResult(poseResult);
        } catch (error) {
          console.warn('[PoseService] Frame processing error:', error);
        }
        
        this.lastTimestamp = timestamp;
      }
    }

    this.animationFrameId = requestAnimationFrame(this.processFrame);
  };

  /** Lấy FPS xử lý hiện tại */
  getFps(): number {
    return this.fps;
  }

  /** Kiểm tra có đang bật chế độ thích ứng tiết kiệm tải không */
  getIsAdaptiveMode(): boolean {
    return this.skipAlternateFrames;
  }

  /**
   * Dừng xử lý
   */
  stopProcessing(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
    this.onResult = null;
    this.videoElement = null;
  }

  /**
   * Xử lý một frame duy nhất (dùng cho calibration)
   */
  async detectSingle(videoElement: HTMLVideoElement): Promise<NormalizedLandmark[] | null> {
    if (!this.poseLandmarker || !this.isInitialized) return null;
    
    try {
      const timestamp = performance.now();
      const result = this.poseLandmarker.detectForVideo(videoElement, timestamp);
      
      if (result.landmarks && result.landmarks.length > 0) {
        return result.landmarks[0] as NormalizedLandmark[];
      }
      return null;
    } catch {
      return null;
    }
  }

  /**
   * Giải phóng tài nguyên
   */
  destroy(): void {
    this.stopProcessing();
    if (this.poseLandmarker) {
      this.poseLandmarker.close();
      this.poseLandmarker = null;
    }
    this.isInitialized = false;
  }

  /** Kiểm tra đã khởi tạo */
  getIsInitialized(): boolean {
    return this.isInitialized;
  }

  /** Kiểm tra đang khởi tạo */
  getIsInitializing(): boolean {
    return this.isInitializing;
  }
}
