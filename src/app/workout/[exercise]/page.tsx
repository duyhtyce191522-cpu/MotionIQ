'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { useRouter, useParams } from 'next/navigation';
import {
  ExerciseId,
  ExerciseState,
  NormalizedLandmark,
  CalibrationResult,
  FeedbackMessage,
  WorkoutSession,
  WorkoutStatus,
} from '@/types';
import { EXERCISES, POSE_CONNECTIONS, EXERCISE_THRESHOLDS } from '@/features/exercises/exerciseRules';
import { PoseService } from '@/features/pose/poseService';
import { checkCalibration } from '@/features/pose/landmarkValidator';
import { RepetitionStateMachine } from '@/features/exercises/stateMachine';
import { createExerciseAnalyzer } from '@/features/exercises/exerciseFactory';
import { FeedbackEngine } from '@/features/feedback/feedbackEngine';
import { SpeechService } from '@/features/feedback/speechService';
import { SoundService } from '@/features/feedback/soundService';
import { WorkoutRecorder } from '@/features/workout/workoutRecorder';
import { saveCompletedWorkout, getPatientProfile } from '@/features/storage/storageService';
import { getAuthSession } from '@/features/auth/authService';

type Phase = 'instructions' | 'calibrating' | 'workout' | 'summary';

export default function WorkoutPage() {
  const router = useRouter();
  const params = useParams();
  const exerciseId = params.exercise as ExerciseId;
  const exercise = EXERCISES[exerciseId];

  // Refs
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const poseServiceRef = useRef<PoseService | null>(null);
  const stateMachineRef = useRef<RepetitionStateMachine | null>(null);
  const analyzerRef = useRef<ReturnType<typeof createExerciseAnalyzer> | null>(null);
  const feedbackEngineRef = useRef<FeedbackEngine>(new FeedbackEngine());
  const speechServiceRef = useRef<SpeechService | null>(null);
  const soundServiceRef = useRef<SoundService | null>(null);
  const recorderRef = useRef<WorkoutRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const calibrationIntervalRef = useRef<number | null>(null);

  // State
  const [phase, setPhase] = useState<Phase>('instructions');
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('user');
  const [isModelLoading, setIsModelLoading] = useState(false);
  const [modelLoadProgress, setModelLoadProgress] = useState('');
  const [calibration, setCalibration] = useState<CalibrationResult | null>(null);
  const [repCount, setRepCount] = useState(0);
  const [currentAngle, setCurrentAngle] = useState<number | null>(null);
  const [exerciseState, setExerciseState] = useState<ExerciseState>('IDLE');
  const [currentFeedback, setCurrentFeedback] = useState<FeedbackMessage | null>(null);
  const [workoutStatus, setWorkoutStatus] = useState<WorkoutStatus>('not_started');
  const [elapsedTime, setElapsedTime] = useState(0);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [targetReps, setTargetReps] = useState<number>(10);
  const [goalReached, setGoalReached] = useState<boolean>(false);
  const targetRepsRef = useRef<number>(10);
  const goalReachedRef = useRef<boolean>(false);
  const [autoStartCountdown, setAutoStartCountdown] = useState<number | null>(null);
  const countdownTimerRef = useRef<NodeJS.Timeout | null>(null);
  const autoStartCountdownRef = useRef<number | null>(null);
  const stableReadyFramesRef = useRef<number>(0);
  const startWorkoutRef = useRef<() => void>(() => {});
  const [currentFps, setCurrentFps] = useState<number>(30);
  const [isAdaptiveMode, setIsAdaptiveMode] = useState<boolean>(false);
  const [sessionData, setSessionData] = useState<WorkoutSession | null>(null);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [shareToast, setShareToast] = useState<string | null>(null);
  const [safetyAlert, setSafetyAlert] = useState<{ type: 'fall' | 'inactivity'; message: string } | null>(null);
  const lastStateChangeTimeRef = useRef<number>(Date.now());

  // Check auth session & valid exercise
  useEffect(() => {
    const session = getAuthSession();
    if (!session) {
      router.push('/login');
      return;
    }
    if (!exercise) {
      router.push('/exercises');
    }
  }, [exercise, router]);

  // Initialize speech & sound services
  useEffect(() => {
    speechServiceRef.current = new SpeechService();
    soundServiceRef.current = new SoundService();
    return () => {
      speechServiceRef.current?.destroy();
      soundServiceRef.current?.destroy();
    };
  }, []);

  // Timer for elapsed time
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (workoutStatus === 'active') {
      interval = setInterval(() => {
        if (recorderRef.current) {
          setElapsedTime(recorderRef.current.getActiveDuration());
        }
      }, 500);
    }
    return () => clearInterval(interval);
  }, [workoutStatus]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanupAll();
    };
  }, []);

  const cleanupAll = useCallback(() => {
    poseServiceRef.current?.destroy();
    poseServiceRef.current = null;
    
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    if (calibrationIntervalRef.current) {
      clearInterval(calibrationIntervalRef.current);
      calibrationIntervalRef.current = null;
    }

    if (countdownTimerRef.current) {
      clearInterval(countdownTimerRef.current);
      countdownTimerRef.current = null;
    }
    autoStartCountdownRef.current = null;
    setAutoStartCountdown(null);
    stableReadyFramesRef.current = 0;

    speechServiceRef.current?.cancel();
  }, []);

  // ============================================================
  // Camera Setup
  // ============================================================

  const startCamera = async (mode: 'user' | 'environment' = facingMode) => {
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: mode },
          aspectRatio: { ideal: 3 / 4 },
          width: { ideal: 720 },
          height: { ideal: 960 },
          frameRate: { ideal: 30, max: 30 },
        },
        audio: false,
      });

      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      setCameraError(null);
      return true;
    } catch (error: any) {
      console.error('[Camera] Error:', error);
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        setCameraError('denied');
      } else {
        setCameraError('unavailable');
      }
      return false;
    }
  };

  const toggleCameraFacing = async () => {
    const nextMode = facingMode === 'user' ? 'environment' : 'user';
    setFacingMode(nextMode);

    poseServiceRef.current?.stopProcessing();
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    const ok = await startCamera(nextMode);
    if (ok && phase === 'workout') {
      startWorkoutLoop();
    }
  };

  // ============================================================
  // MediaPipe Initialization
  // ============================================================

  const initializePose = async () => {
    setIsModelLoading(true);
    setModelLoadProgress('Đang tải mô hình AI...');

    try {
      const poseService = new PoseService();
      await poseService.initialize();
      poseServiceRef.current = poseService;
      setModelLoadProgress('Mô hình AI đã sẵn sàng');
      return true;
    } catch (error) {
      console.error('[PoseService] Init failed:', error);
      setModelLoadProgress('Không thể tải mô hình AI');
      return false;
    } finally {
      setIsModelLoading(false);
    }
  };

  // ============================================================
  // Hands-free Auto-Start Countdown
  // ============================================================

  const abortAutoCountdown = useCallback(() => {
    if (countdownTimerRef.current) {
      clearInterval(countdownTimerRef.current);
      countdownTimerRef.current = null;
    }
    if (autoStartCountdownRef.current !== null) {
      autoStartCountdownRef.current = null;
      setAutoStartCountdown(null);
      stableReadyFramesRef.current = 0;
    }
  }, []);

  const triggerAutoCountdown = useCallback(() => {
    if (autoStartCountdownRef.current !== null) return; // already counting down

    let count = 3;
    autoStartCountdownRef.current = count;
    setAutoStartCountdown(count);

    soundServiceRef.current?.playCountdownTick(false);
    speechServiceRef.current?.speak('Ba', true);

    if (countdownTimerRef.current) {
      clearInterval(countdownTimerRef.current);
    }

    countdownTimerRef.current = setInterval(() => {
      count -= 1;
      autoStartCountdownRef.current = count;
      setAutoStartCountdown(count);

      if (count === 2) {
        soundServiceRef.current?.playCountdownTick(false);
        speechServiceRef.current?.speak('Hai', true);
      } else if (count === 1) {
        soundServiceRef.current?.playCountdownTick(false);
        speechServiceRef.current?.speak('Một', true);
      } else if (count <= 0) {
        if (countdownTimerRef.current) {
          clearInterval(countdownTimerRef.current);
          countdownTimerRef.current = null;
        }
        autoStartCountdownRef.current = null;
        setAutoStartCountdown(null);
        soundServiceRef.current?.playCountdownTick(true);
        speechServiceRef.current?.speak('Bắt đầu', true);
        startWorkoutRef.current();
      }
    }, 1000);
  }, []);

  // ============================================================
  // Calibration
  // ============================================================

  const startCalibration = async () => {
    setPhase('calibrating');
    abortAutoCountdown();
    stableReadyFramesRef.current = 0;

    const cameraOk = await startCamera(facingMode);
    if (!cameraOk) return;

    const poseOk = await initializePose();
    if (!poseOk) return;

    if (calibrationIntervalRef.current) {
      clearInterval(calibrationIntervalRef.current);
    }

    // Poll for calibration
    calibrationIntervalRef.current = window.setInterval(async () => {
      if (!poseServiceRef.current || !videoRef.current) return;

      const landmarks = await poseServiceRef.current.detectSingle(videoRef.current);
      const result = checkCalibration(
        landmarks,
        streamRef.current !== null,
        cameraError,
        videoRef.current
      );
      setCalibration(result);

      // Draw skeleton during calibration
      if (landmarks) {
        drawSkeleton(landmarks);
      }

      // Hands-free auto start: when all required joints are detected
      if (result.canStart) {
        stableReadyFramesRef.current += 1;
        // Require 2 consecutive checks (~0.8s) of full body detection to avoid accidental triggers
        if (stableReadyFramesRef.current >= 2 && autoStartCountdownRef.current === null) {
          triggerAutoCountdown();
        }
      } else {
        // If joints are lost while counting down, cancel countdown
        if (autoStartCountdownRef.current !== null) {
          abortAutoCountdown();
        } else {
          stableReadyFramesRef.current = 0;
        }
      }
    }, 400);
  };

  // ============================================================
  // Skeleton Drawing with Live Angle Arc & Joint Badge
  // ============================================================

  const drawSkeleton = useCallback(
    (
      landmarks: NormalizedLandmark[],
      activeAngle?: number | null,
      targetReached?: boolean
    ) => {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      if (!canvas || !video) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (landmarks.length === 0) return;

      // Dynamic color: Emerald Green when target reached, Neon Cyan during movement
      const skeletonColor = targetReached
        ? 'rgba(16, 185, 129, 0.95)'
        : 'rgba(6, 182, 212, 0.85)';
      const jointDotColor = targetReached ? '#34d399' : '#38bdf8';

      // Draw connections
      ctx.strokeStyle = skeletonColor;
      ctx.lineWidth = targetReached ? 5 : 4;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      for (const [startIdx, endIdx] of POSE_CONNECTIONS) {
        const start = landmarks[startIdx];
        const end = landmarks[endIdx];
        if (!start || !end) continue;

        const startVis = start.visibility ?? 0;
        const endVis = end.visibility ?? 0;
        if (startVis < 0.3 || endVis < 0.3) continue;

        ctx.beginPath();
        ctx.moveTo(start.x * canvas.width, start.y * canvas.height);
        ctx.lineTo(end.x * canvas.width, end.y * canvas.height);
        ctx.stroke();
      }

      // Draw landmark points
      for (let i = 0; i < landmarks.length; i++) {
        const lm = landmarks[i];
        if (!lm || (lm.visibility ?? 0) < 0.3) continue;

        const x = lm.x * canvas.width;
        const y = lm.y * canvas.height;

        // Outer glow
        ctx.beginPath();
        ctx.arc(x, y, 7, 0, Math.PI * 2);
        ctx.fillStyle = targetReached ? 'rgba(16, 185, 129, 0.35)' : 'rgba(6, 182, 212, 0.35)';
        ctx.fill();

        // Inner dot
        ctx.beginPath();
        ctx.arc(x, y, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = jointDotColor;
        ctx.fill();
      }

      // Draw Live Angle Badge directly on key joint (Knee or Shoulder)
      if (activeAngle !== null && activeAngle !== undefined) {
        let keyIdx = 26;
        if (exerciseId === 'shoulder-raise') {
          const leftVis = landmarks[11]?.visibility ?? 0;
          const rightVis = landmarks[12]?.visibility ?? 0;
          keyIdx = leftVis > rightVis ? 11 : 12;
        } else if (exerciseId === 'side-leg-raise') {
          const leftVis = landmarks[23]?.visibility ?? 0;
          const rightVis = landmarks[24]?.visibility ?? 0;
          keyIdx = leftVis > rightVis ? 23 : 24;
        } else {
          const leftVis = landmarks[25]?.visibility ?? 0;
          const rightVis = landmarks[26]?.visibility ?? 0;
          keyIdx = leftVis > rightVis ? 25 : 26;
        }

        const targetLm = landmarks[keyIdx];
        if (targetLm && (targetLm.visibility ?? 0) > 0.35) {
          const jx = targetLm.x * canvas.width;
          const jy = targetLm.y * canvas.height;

          const badgeWidth = 64;
          const badgeHeight = 28;
          const bx = jx + 16;
          const by = jy - 14;

          ctx.save();
          // Badge background
          ctx.fillStyle = targetReached ? 'rgba(6, 78, 59, 0.9)' : 'rgba(15, 23, 42, 0.85)';
          ctx.strokeStyle = targetReached ? '#34d399' : '#38bdf8';
          ctx.lineWidth = 2;
          ctx.beginPath();
          if (typeof ctx.roundRect === 'function') {
            ctx.roundRect(bx, by, badgeWidth, badgeHeight, 8);
          } else {
            ctx.rect(bx, by, badgeWidth, badgeHeight);
          }
          ctx.fill();
          ctx.stroke();

          // Angle Text
          ctx.fillStyle = targetReached ? '#34d399' : '#38bdf8';
          ctx.font = 'bold 14px monospace';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(`${activeAngle}°`, bx + badgeWidth / 2, by + badgeHeight / 2);
          ctx.restore();
        }
      }
    },
    [exerciseId]
  );

  // ============================================================
  // Workout Processing Loop
  // ============================================================

  const startWorkoutLoop = useCallback(() => {
    if (!poseServiceRef.current || !videoRef.current) return;
    const thresholds = EXERCISE_THRESHOLDS[exerciseId];
    const primaryKey = thresholds?.primaryAngleKey || 'knee';

    let lastStateLocal: ExerciseState = 'IDLE';

    poseServiceRef.current.startProcessing(videoRef.current, (result) => {
      if (!analyzerRef.current || !stateMachineRef.current) return;

      const landmarks = result.landmarks[0] as NormalizedLandmark[] | undefined;
      if (!landmarks || landmarks.length < 33) {
        drawSkeleton([]);
        return;
      }

      // Analyze frame
      const analysis = analyzerRef.current.analyzeFrame(landmarks);

      // Process through state machine
      const smResult = stateMachineRef.current.processFrame(analysis);

      // Update UI state
      setExerciseState(smResult.state);
      setRepCount(smResult.totalReps);

      // Track real-time FPS & adaptive performance
      if (poseServiceRef.current) {
        const fpsVal = poseServiceRef.current.getFps();
        if (fpsVal > 0) setCurrentFps(fpsVal);
        setIsAdaptiveMode(poseServiceRef.current.getIsAdaptiveMode());
      }

      // Live Angle Gauge update
      const angleVal =
        smResult.angles && smResult.angles[primaryKey] !== undefined
          ? Math.round(smResult.angles[primaryKey])
          : null;

      if (angleVal !== null) {
        setCurrentAngle(angleVal);
      }

      const isTargetMet = smResult.state === 'TOP' || smResult.state === 'BOTTOM';

      // Draw skeleton with live angle badge & target glow
      drawSkeleton(landmarks, angleVal, isTargetMet);

      // Safety Monitoring: Check for sudden fall drop (hip Y > 0.88)
      const leftHipY = landmarks[23]?.y;
      const rightHipY = landmarks[24]?.y;
      if (leftHipY !== undefined && rightHipY !== undefined) {
        const avgHipY = (leftHipY + rightHipY) / 2;
        if (avgHipY > 0.88) {
          poseServiceRef.current?.stopProcessing();
          setSafetyAlert({
            type: 'fall',
            message: 'Hệ thống nhận thấy bạn có thể đã ngã hoặc ngồi bệt xuống sàn. Bạn có ổn không?',
          });
          soundServiceRef.current?.playWarning();
          speechServiceRef.current?.speak('Cảnh báo an toàn! Bạn có cần trợ giúp không?');
          return;
        }
      }

      // Safety Monitoring: Prolonged inactivity in bottom position (> 15 seconds)
      const now = Date.now();
      if (smResult.state === 'BOTTOM') {
        if (lastStateLocal !== 'BOTTOM') {
          lastStateChangeTimeRef.current = now;
        } else if (now - lastStateChangeTimeRef.current > 15000) {
          poseServiceRef.current?.stopProcessing();
          setSafetyAlert({
            type: 'inactivity',
            message: 'Bạn đã ở tư thế hạ người hơn 15 giây. Bạn có cảm thấy đau mỏi không?',
          });
          soundServiceRef.current?.playWarning();
          speechServiceRef.current?.speak('Bạn có cần nghỉ ngơi không? Hãy đứng dậy từ từ.');
          return;
        }
      } else {
        lastStateChangeTimeRef.current = now;
      }

      // Peak hold chime when reaching TOP / BOTTOM
      if (
        (smResult.state === 'TOP' || smResult.state === 'BOTTOM') &&
        lastStateLocal !== smResult.state
      ) {
        soundServiceRef.current?.playPeakHold();
      }
      lastStateLocal = smResult.state;

      // Process feedback
      const feedbackMsg = feedbackEngineRef.current.processRawFeedback(smResult.feedback);
      if (feedbackMsg) {
        setCurrentFeedback(feedbackMsg);
        if (feedbackMsg.priority === 'warning' || feedbackMsg.priority === 'critical') {
          soundServiceRef.current?.playWarning();
        }
        if (speechServiceRef.current?.getIsEnabled()) {
          speechServiceRef.current.speak(feedbackMsg.text);
        }
      }

      // Audio cue on rep completion
      if (smResult.repCompleted) {
        soundServiceRef.current?.playRepSuccess();

        const curTarget = targetRepsRef.current;
        if (curTarget > 0 && smResult.totalReps >= curTarget && !goalReachedRef.current) {
          goalReachedRef.current = true;
          setGoalReached(true);
          soundServiceRef.current?.playCelebration();
          if (speechServiceRef.current?.getIsEnabled()) {
            speechServiceRef.current.speak(
              `${smResult.totalReps} lần! Xuất sắc! Bác đã hoàn thành mục tiêu ${curTarget} lần tập!`,
              true
            );
          }
        } else if (speechServiceRef.current?.getIsEnabled()) {
          speechServiceRef.current.speak(`${smResult.totalReps} lần`);
        }
      }
    });
  }, [exerciseId, drawSkeleton]);

  const startWorkout = useCallback(() => {
    if (countdownTimerRef.current) {
      clearInterval(countdownTimerRef.current);
      countdownTimerRef.current = null;
    }
    autoStartCountdownRef.current = null;
    setAutoStartCountdown(null);

    if (calibrationIntervalRef.current) {
      clearInterval(calibrationIntervalRef.current);
      calibrationIntervalRef.current = null;
    }

    // Initialize exercise engine
    const thresholds = EXERCISE_THRESHOLDS[exerciseId];
    const analyzer = createExerciseAnalyzer(exerciseId);
    const sm = new RepetitionStateMachine(thresholds.minHoldFrames, thresholds.minRepDurationMs ?? 1000);
    
    const auth = getAuthSession();
    const currentPatientId = auth?.user?.patientId || (auth?.role === 'patient' ? auth.user.id : undefined);
    const currentPatientName = auth?.user?.name || getPatientProfile().name;
    const recorder = new WorkoutRecorder(exerciseId, currentPatientId, currentPatientName);

    analyzerRef.current = analyzer;
    stateMachineRef.current = sm;
    recorderRef.current = recorder;

    sm.start();
    recorder.start();
    feedbackEngineRef.current.reset();

    targetRepsRef.current = targetReps;
    goalReachedRef.current = false;
    setGoalReached(false);

    setPhase('workout');
    setWorkoutStatus('active');
    setRepCount(0);
    setCurrentAngle(null);

    soundServiceRef.current?.playCountdownTick(true);

    startWorkoutLoop();
  }, [exerciseId, targetReps, startWorkoutLoop]);

  // Keep startWorkoutRef up to date for timer callbacks
  useEffect(() => {
    startWorkoutRef.current = startWorkout;
  }, [startWorkout]);

  // ============================================================
  // Pause / Resume / Stop
  // ============================================================

  const handlePause = () => {
    poseServiceRef.current?.stopProcessing();
    recorderRef.current?.pause();
    setWorkoutStatus('paused');
  };

  const handleResume = () => {
    recorderRef.current?.resume();
    setWorkoutStatus('active');
    startWorkoutLoop();
  };

  const handleStop = () => {
    poseServiceRef.current?.stopProcessing();

    const reps = stateMachineRef.current?.getRepetitions() ?? [];
    const session = recorderRef.current?.finish(reps);

    if (session) {
      if (!session.patientId) {
        const auth = getAuthSession();
        session.patientId = auth?.user?.patientId || (auth?.role === 'patient' ? auth.user.id : undefined);
        session.patientName = auth?.user?.name || getPatientProfile().name;
      }
      setSessionData(session);
      // Save to local storage (history entry + full session)
      saveCompletedWorkout(session);
    }

    // Stop camera
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setPhase('summary');
    setWorkoutStatus('completed');
  };

  const toggleSound = () => {
    const nextVal = !soundEnabled;
    setSoundEnabled(nextVal);
    if (nextVal) {
      speechServiceRef.current?.enable();
      soundServiceRef.current?.setEnabled(true);
    } else {
      speechServiceRef.current?.disable();
      soundServiceRef.current?.setEnabled(false);
    }
  };

  const handleShareSummary = async () => {
    if (!sessionData) return;
    const dateStr = new Date(sessionData.createdAt).toLocaleDateString('vi-VN');
    const textToShare = `🏃 MotionIQ — Kết quả tập luyện\n📅 Ngày: ${dateStr}\nBài tập: ${sessionData.exerciseName}\n- Tổng số lần: ${sessionData.totalReps}\n- Đạt tiêu chuẩn: ${sessionData.goodReps}\n- Tỷ lệ chất lượng: ${sessionData.qualityRatio !== null ? Math.round(sessionData.qualityRatio) + '%' : 'N/A'}\n- Thời gian: ${formatTime(sessionData.activeDuration)}\n💪 Cùng duy trì vận động mỗi ngày với MotionIQ!`;

    if (typeof navigator !== 'undefined' && navigator.share) {
      try {
        await navigator.share({
          title: `MotionIQ — ${sessionData.exerciseName}`,
          text: textToShare,
        });
        return;
      } catch {
        // User dismissed
      }
    }

    try {
      await navigator.clipboard.writeText(textToShare);
      setShareToast('✅ Đã sao chép kết quả! Bạn có thể dán vào Zalo hoặc tin nhắn.');
      setTimeout(() => setShareToast(null), 4000);
    } catch {
      setShareToast('Không thể sao chép kết quả.');
      setTimeout(() => setShareToast(null), 3000);
    }
  };

  // ============================================================
  // Time formatting
  // ============================================================

  const formatTime = (ms: number): string => {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  // ============================================================
  // Render — Guard
  // ============================================================

  if (!exercise) return null;

  // ============================================================
  // Render — Instructions Phase
  // ============================================================

  if (phase === 'instructions') {
    return (
      <div className="page">
        <div className="container page-content">
          <button className="back-nav" onClick={() => router.push('/exercises')}>
            ← Chọn bài tập
          </button>

          <h1>{exercise.icon} {exercise.name}</h1>
          <p className="text-muted">{exercise.description}</p>

          {/* Camera Advice */}
          {exercise.cameraAdvice && (
            <div className="card" style={{ marginBottom: 'var(--space-4)', borderLeft: '4px solid var(--color-accent-primary)' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                <span>📐</span> Góc đặt camera khuyến nghị
              </h3>
              <p style={{ margin: 0, fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>
                {exercise.cameraAdvice}
              </p>
            </div>
          )}

          {/* Movement target */}
          {exercise.targetAngleDescription && (
            <div style={{
              marginBottom: 'var(--space-4)',
              padding: 'var(--space-3) var(--space-4)',
              background: 'rgba(6, 182, 212, 0.1)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid rgba(6, 182, 212, 0.25)',
              fontSize: 'var(--font-size-sm)',
            }}>
              🎯 <strong>Mục tiêu:</strong> {exercise.targetAngleDescription}
            </div>
          )}

          <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
            <h3>📋 Các bước thực hiện</h3>
            <ol className="instructions-list">
              {exercise.instructions.map((instruction, idx) => (
                <li key={idx} className="instruction-item">
                  {instruction}
                </li>
              ))}
            </ol>
          </div>

          <div className="privacy-notice" style={{ marginBottom: 'var(--space-6)' }}>
            <span className="privacy-notice-icon">🛡️</span>
            <span>
              Camera chỉ hoạt động khi bạn cho phép.
              Video được xử lý trực tiếp trên thiết bị (Edge AI), không gửi lên máy chủ.
            </span>
          </div>

          {/* Target Rep Goal Selector */}
          <div className="card" style={{
            marginBottom: 'var(--space-6)',
            padding: 'var(--space-4) var(--space-5)',
            border: '1px solid var(--color-border)',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
              <div style={{ fontWeight: 'bold', fontSize: 'var(--font-size-sm)', display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                <span>🎯</span> Mục tiêu buổi tập này
              </div>
              <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-accent-primary)', fontWeight: 'bold' }}>
                {targetReps > 0 ? `${targetReps} lần tập` : 'Tự do'}
              </span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-2)' }}>
              {[
                { label: '5 lần', val: 5, desc: 'Khởi động' },
                { label: '10 lần', val: 10, desc: 'Tiêu chuẩn' },
                { label: '15 lần', val: 15, desc: 'Tăng cường' },
                { label: 'Tự do', val: 0, desc: 'Không giới hạn' },
              ].map((item) => (
                <button
                  key={item.val}
                  type="button"
                  onClick={() => setTargetReps(item.val)}
                  style={{
                    padding: 'var(--space-2) var(--space-1)',
                    borderRadius: 'var(--radius-md)',
                    border: targetReps === item.val ? '2px solid var(--color-accent-primary)' : '1px solid var(--color-border)',
                    background: targetReps === item.val ? 'rgba(6, 182, 212, 0.25)' : 'rgba(255, 255, 255, 0.05)',
                    color: targetReps === item.val ? 'var(--color-accent-primary)' : 'var(--color-text-secondary)',
                    fontWeight: targetReps === item.val ? 'bold' : 'normal',
                    fontSize: 'var(--font-size-xs)',
                    cursor: 'pointer',
                    textAlign: 'center',
                    transition: 'all var(--transition-fast)',
                  }}
                >
                  <div>{item.label}</div>
                  <div style={{ fontSize: '10px', opacity: 0.8, marginTop: '2px' }}>{item.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Voice Preview / Test */}
          <div className="card" style={{
            marginBottom: 'var(--space-6)',
            padding: 'var(--space-3) var(--space-4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 'var(--space-3)',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
              <span style={{ fontSize: '1.4rem' }}>🗣️</span>
              <div>
                <div style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'bold' }}>
                  Giọng nói: Tiếng Việt
                </div>
                <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
                  Hỗ trợ đếm nhịp và phản hồi tư thế bằng tiếng Việt
                </div>
              </div>
            </div>
            <button
              type="button"
              className="btn btn-secondary"
              style={{
                padding: 'var(--space-2) var(--space-3)',
                fontSize: 'var(--font-size-xs)',
                minHeight: 'auto',
                whiteSpace: 'nowrap',
              }}
              onClick={() => {
                speechServiceRef.current?.speak('Xin chào! MotionIQ sẵn sàng hỗ trợ bạn tập luyện.', true);
              }}
            >
              🔊 Thử giọng
            </button>
          </div>

          <button className="btn btn-primary btn-full" onClick={startCalibration}>
            📷 Mở camera và kiểm tra
          </button>
        </div>
      </div>
    );
  }

  // ============================================================
  // Render — Calibrating Phase
  // ============================================================

  if (phase === 'calibrating') {
    return (
      <div className="camera-container">
        <div className="camera-viewport-3x4">
          <video
            ref={videoRef}
            className={`camera-video ${facingMode === 'user' ? 'mirrored' : ''}`}
            playsInline
            muted
            autoPlay
          />
          <canvas
            ref={canvasRef}
            className={`camera-canvas ${facingMode === 'user' ? 'mirrored' : ''}`}
          />

          {/* 3:4 Framing Guide & Corner Brackets */}
          <div className={`camera-frame-guide ${calibration?.status === 'ready' ? 'ready' : ''}`}>
            <span className="corner-marker tl" />
            <span className="corner-marker tr" />
            <span className="corner-marker bl" />
            <span className="corner-marker br" />
          </div>

          <div className={`camera-frame-badge ${calibration?.status === 'ready' ? 'ready' : ''}`}>
            <span>📐</span> Khung hình 3:4 (Toàn thân)
          </div>

          {/* Hands-free Auto-Start Countdown Overlay (Toàn màn hình camera, phông chữ lớn dễ nhìn từ xa) */}
          {autoStartCountdown !== null && (
            <div className="auto-start-overlay">
              <div className="auto-start-badge">
                <span>⚡</span> Đã nhận diện đủ toàn bộ khớp
              </div>
              <div className="auto-start-circle">
                <span className="auto-start-number">{autoStartCountdown}</span>
              </div>
              <div className="auto-start-text">
                Tự động bắt đầu trong {autoStartCountdown} giây...
              </div>
              <div className="auto-start-subtext">
                Bác hãy giữ nguyên tư thế đứng, hệ thống sẽ tự động vào bài tập!
              </div>
            </div>
          )}

        {/* Top Controls: Switch Camera & Back */}
        <div style={{
          position: 'absolute',
          top: 'var(--space-4)',
          left: 'var(--space-4)',
          right: 'var(--space-4)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          zIndex: 60,
        }}>
          <button
            className="btn-icon"
            onClick={() => {
              cleanupAll();
              setPhase('instructions');
            }}
            title="Quay lại"
          >
            ←
          </button>

          <button className="camera-switch-btn" onClick={toggleCameraFacing} title="Đổi camera">
            🔄 {facingMode === 'user' ? 'Dùng camera sau' : 'Dùng camera trước'}
          </button>
        </div>

        <div className="calibration-overlay">
          <div className="calibration-status">
            {isModelLoading ? (
              <>
                <div className="calibration-icon calibration-detecting">🤖</div>
                <div className="calibration-message">{modelLoadProgress}</div>
                <div className="spinner" style={{ margin: '0 auto' }} />
              </>
            ) : cameraError ? (
              <>
                <div className="calibration-icon">❌</div>
                <div className="calibration-message">
                  {cameraError === 'denied'
                    ? 'Vui lòng cấp quyền truy cập camera trong cài đặt trình duyệt.'
                    : 'Không thể truy cập camera. Vui lòng thử lại.'}
                </div>
                <button className="btn btn-secondary" onClick={() => router.push('/exercises')}>
                  Quay lại
                </button>
              </>
            ) : calibration ? (
              <>
                <div className="calibration-icon">
                  {calibration.status === 'ready' ? '✅' :
                   calibration.status === 'partial_body' ? '👤' :
                   calibration.status === 'detecting_pose' ? '🔍' : '⏳'}
                </div>
                <div className={`calibration-message ${
                  calibration.status === 'detecting_pose' ? 'calibration-detecting' : ''
                }`}>
                  {calibration.message}
                </div>

                {calibration.missingRegions.length > 0 && (
                  <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: 'var(--space-2)',
                    justifyContent: 'center',
                    marginBottom: 'var(--space-4)',
                  }}>
                    {calibration.missingRegions.map((region) => (
                      <span
                        key={region}
                        style={{
                          padding: 'var(--space-1) var(--space-3)',
                          background: 'rgba(239, 68, 68, 0.2)',
                          borderRadius: 'var(--radius-full)',
                          fontSize: 'var(--font-size-xs)',
                          color: 'var(--color-accent-danger)',
                        }}
                      >
                        ❌ {region}
                      </span>
                    ))}
                  </div>
                )}

                {exercise.cameraAdvice && (
                  <div style={{
                    fontSize: 'var(--font-size-xs)',
                    color: 'var(--color-text-secondary)',
                    marginBottom: 'var(--space-4)',
                    lineHeight: 1.5,
                  }}>
                    💡 {exercise.cameraAdvice}
                  </div>
                )}

                {/* Chẩn đoán ánh sáng tự động */}
                {calibration.lighting?.status !== 'good' && calibration.lighting?.message && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                    padding: '8px 14px',
                    background: 'rgba(234, 179, 8, 0.16)',
                    border: '1px solid rgba(234, 179, 8, 0.45)',
                    borderRadius: 'var(--radius-full)',
                    fontSize: 'var(--font-size-xs)',
                    color: '#fde047',
                    marginBottom: 'var(--space-3)',
                    textAlign: 'center',
                  }}>
                    {calibration.lighting.message}
                  </div>
                )}

                {/* Chẩn đoán khoảng cách */}
                {calibration.distance && calibration.distance.status !== 'ideal' && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px',
                    padding: '8px 14px',
                    background: 'rgba(56, 189, 248, 0.16)',
                    border: '1px solid rgba(56, 189, 248, 0.45)',
                    borderRadius: 'var(--radius-full)',
                    fontSize: 'var(--font-size-xs)',
                    color: '#38bdf8',
                    marginBottom: 'var(--space-3)',
                    textAlign: 'center',
                  }}>
                    {calibration.distance.advice}
                  </div>
                )}

                {calibration.canStart && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)', width: '100%' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '8px',
                      padding: '10px 16px',
                      background: 'rgba(16, 185, 129, 0.18)',
                      border: '1px solid #10b981',
                      borderRadius: 'var(--radius-md)',
                      color: '#34d399',
                      fontWeight: 700,
                      fontSize: 'var(--font-size-sm)',
                    }}>
                      <span>⚡</span> Tự động vào bài sau {autoStartCountdown ?? 3}s (Không cần bấm)
                    </div>
                    <button
                      className="btn btn-secondary btn-full"
                      onClick={startWorkout}
                      style={{ opacity: 0.85, fontSize: 'var(--font-size-xs)', padding: 'var(--space-2) var(--space-3)' }}
                    >
                      ▶️ Bắt đầu ngay (Bỏ qua đếm ngược)
                    </button>
                  </div>
                )}
              </>
            ) : (
              <>
                <div className="calibration-icon calibration-detecting">📷</div>
                <div className="calibration-message">Đang kết nối camera...</div>
                <div className="spinner" style={{ margin: '0 auto' }} />
              </>
            )}
          </div>
        </div>
      </div>
    </div>
    );
  }

  // ============================================================
  // Render — Workout Phase
  // ============================================================

  if (phase === 'workout') {
    return (
      <div className="camera-container">
        <div className="camera-viewport-3x4">
          <video
            ref={videoRef}
            className={`camera-video ${facingMode === 'user' ? 'mirrored' : ''}`}
            playsInline
            muted
            autoPlay
          />
          <canvas
            ref={canvasRef}
            className={`camera-canvas ${facingMode === 'user' ? 'mirrored' : ''}`}
          />

          {/* Real-time FPS & Performance Mode Indicator */}
          <div className="camera-fps-badge">
            <span>⚡</span> {currentFps} FPS {isAdaptiveMode ? '• Tiết kiệm pin' : '• Mượt mà'}
          </div>

        {/* Goal celebration toast */}
        {goalReached && (
          <div style={{
            position: 'absolute',
            top: '72px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'linear-gradient(135deg, #059669, #10b981)',
            color: '#ffffff',
            padding: 'var(--space-2) var(--space-4)',
            borderRadius: 'var(--radius-full)',
            boxShadow: '0 8px 24px rgba(16, 185, 129, 0.5)',
            fontSize: 'var(--font-size-sm)',
            fontWeight: 'bold',
            zIndex: 100,
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-2)',
            animation: 'fadeIn 0.3s ease',
            whiteSpace: 'nowrap',
          }}>
            <span>🎉</span> Đã hoàn thành mục tiêu {targetReps} lần!
          </div>
        )}

        {/* HUD — Top stats bar */}
        <div className="workout-hud">
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: 'var(--space-2)',
          }}>
            <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
              {exercise.icon} {exercise.name}
            </span>
            <button className="camera-switch-btn" onClick={toggleCameraFacing} title="Đổi camera">
              🔄 {facingMode === 'user' ? 'Sau' : 'Trước'}
            </button>
          </div>

          <div className="workout-hud-stats">
            <div className="workout-stat workout-stat-reps">
              <div className="workout-stat-value">
                {repCount}
                {targetReps > 0 && (
                  <span style={{ fontSize: '0.55em', opacity: 0.65, marginLeft: '2px' }}>
                    /{targetReps}
                  </span>
                )}
              </div>
              <div className="workout-stat-label">Lần tập</div>
            </div>
            <div className="workout-stat">
              <div className="workout-stat-value">{formatTime(elapsedTime)}</div>
              <div className="workout-stat-label">Thời gian</div>
            </div>
            <div className="workout-stat">
              <div className="workout-stat-value" style={{
                fontSize: 'var(--font-size-xs)',
                color: exerciseState === 'READY' ? 'var(--color-accent-info)' :
                       exerciseState === 'COMPLETE' ? 'var(--color-accent-success)' :
                       'var(--color-accent-warning)',
              }}>
                {exerciseState === 'IDLE' ? 'Chờ' :
                 exerciseState === 'READY' ? 'Sẵn sàng' :
                 exerciseState === 'ASCENDING' ? 'Đang lên' :
                 exerciseState === 'DESCENDING' ? 'Đang xuống' :
                 exerciseState === 'TOP' ? 'Đỉnh' :
                 exerciseState === 'BOTTOM' ? 'Đáy' :
                 'Hoàn thành'}
              </div>
              <div className="workout-stat-label">Trạng thái</div>
            </div>
          </div>

          {/* Live Angle Gauge */}
          {currentAngle !== null && (
            <div className="workout-angle-gauge">
              <div className="workout-angle-value">
                <span>📐</span> {currentAngle}°
              </div>
              <div className="workout-angle-label">
                {exerciseId === 'shoulder-raise' ? 'Góc nâng vai' : 'Góc gối'}
              </div>
              <div className="workout-angle-target">
                {exerciseState === 'BOTTOM' || exerciseState === 'TOP'
                  ? '🎯 Đã đạt góc'
                  : (exercise.targetAngleDescription || 'Giữ chuyển động đều')}
              </div>
            </div>
          )}
        </div>

        {/* Feedback Banner */}
        {currentFeedback && (
          <div
            className={`feedback-banner feedback-${currentFeedback.priority}`}
            key={currentFeedback.id + currentFeedback.text}
          >
            {currentFeedback.text}
          </div>
        )}

        {/* Bottom Controls */}
        <div className="workout-controls">
          <button className="btn-icon" onClick={toggleSound} title="Bật/tắt âm thanh và giọng nói">
            {soundEnabled ? '🔊' : '🔇'}
          </button>

          {workoutStatus === 'active' ? (
            <button className="btn btn-secondary" onClick={handlePause}>
              ⏸ Tạm dừng
            </button>
          ) : (
            <button className="btn btn-primary" onClick={handleResume}>
              ▶️ Tiếp tục
            </button>
          )}

          <button className="btn btn-danger" onClick={handleStop}>
            ⏹ Kết thúc
          </button>
        </div>

        {/* Pause overlay */}
        {workoutStatus === 'paused' && (
          <div className="calibration-overlay">
            <div className="calibration-status">
              <div className="calibration-icon">⏸</div>
              <div className="calibration-message">Tạm dừng</div>
              <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-4)' }}>
                <button className="btn btn-primary" onClick={handleResume}>
                  ▶️ Tiếp tục
                </button>
                <button className="btn btn-danger" onClick={handleStop}>
                  ⏹ Kết thúc
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Safety Alert Modal */}
        {safetyAlert && (
          <div className="safety-modal-overlay">
            <div className="safety-modal-card">
              <div className="safety-modal-icon">⚠️</div>
              <h2 style={{ color: '#ef4444', marginBottom: 'var(--space-2)' }}>Cảnh báo an toàn</h2>
              <p style={{ color: '#e2e8f0', fontSize: 'var(--font-size-sm)', marginBottom: 'var(--space-6)', lineHeight: 1.6 }}>
                {safetyAlert.message}
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                <button
                  className="btn btn-primary btn-full"
                  style={{ background: '#10b981', borderColor: '#10b981' }}
                  onClick={() => {
                    setSafetyAlert(null);
                    lastStateChangeTimeRef.current = Date.now();
                    startWorkoutLoop();
                  }}
                >
                  ✅ Tôi an toàn, tiếp tục tập
                </button>
                <a
                  href={`tel:${getPatientProfile().emergencyContact || '115'}`}
                  className="btn btn-danger btn-full"
                  style={{
                    textDecoration: 'none',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px',
                    fontWeight: 'bold',
                    background: '#dc2626',
                  }}
                >
                  📞 Gọi Khẩn Cấp ({getPatientProfile().emergencyContact || '115'})
                </a>
                <button
                  className="btn btn-secondary btn-full"
                  onClick={() => {
                    setSafetyAlert(null);
                    handleStop();
                  }}
                >
                  ⏹ Dừng buổi tập ngay
                </button>
              </div>
            </div>
          </div>
        )}
        </div>
      </div>
    );
  }

  // ============================================================
  // Render — Summary Phase
  // ============================================================

  if (phase === 'summary' && sessionData) {
    const qualityClass =
      sessionData.qualityRatio === null ? '' :
      sessionData.qualityRatio >= 80 ? 'quality-good' :
      sessionData.qualityRatio >= 50 ? 'quality-medium' :
      'quality-low';

    return (
      <div className="page">
        <div className="container page-content">
          <div className="summary-header">
            <div className="summary-icon">🎉</div>
            <h1>Hoàn thành buổi tập!</h1>
            <p className="text-muted">{exercise.icon} {exercise.name}</p>
            {targetReps > 0 && sessionData.totalReps >= targetReps && (
              <div style={{
                display: 'inline-block',
                marginTop: 'var(--space-2)',
                padding: 'var(--space-1) var(--space-3)',
                background: 'rgba(16, 185, 129, 0.2)',
                border: '1px solid #10b981',
                borderRadius: 'var(--radius-full)',
                color: '#34d399',
                fontSize: 'var(--font-size-xs)',
                fontWeight: 'bold',
              }}>
                🎯 Đạt mục tiêu đề ra ({sessionData.totalReps}/{targetReps} lần)
              </div>
            )}
          </div>

          {/* Quality ratio */}
          <div className="card summary-quality">
            <div className={`summary-quality-value ${qualityClass}`}>
              {sessionData.qualityRatio !== null
                ? `${Math.round(sessionData.qualityRatio)}%`
                : 'Chưa đủ dữ liệu'}
            </div>
            <div className="text-muted" style={{ fontSize: 'var(--font-size-sm)' }}>
              {sessionData.qualityRatio !== null
                ? 'Tỷ lệ đạt tiêu chí cơ bản'
                : 'Không có repetition được đánh giá'}
            </div>
          </div>

          {/* Stats grid */}
          <div className="summary-grid">
            <div className="card summary-stat">
              <div className="summary-stat-value">{sessionData.totalReps}</div>
              <div className="summary-stat-label">Tổng lần tập</div>
            </div>
            <div className="card summary-stat">
              <div className="summary-stat-value">{sessionData.goodReps}</div>
              <div className="summary-stat-label">Lần đạt tiêu chí</div>
            </div>
            <div className="card summary-stat">
              <div className="summary-stat-value">
                {formatTime(sessionData.activeDuration)}
              </div>
              <div className="summary-stat-label">Thời gian tập</div>
            </div>
            <div className="card summary-stat">
              <div className="summary-stat-value">
                {formatTime(sessionData.totalDuration)}
              </div>
              <div className="summary-stat-label">Tổng thời gian</div>
            </div>
          </div>

          {/* Warnings */}
          {sessionData.warnings.length > 0 && (
            <div className="card summary-warnings">
              <h3>⚠️ Lưu ý thường gặp</h3>
              {sessionData.warnings.map((warning, idx) => (
                <div key={idx} className="summary-warning-item">
                  <span>⚠️</span>
                  <span>{warning}</span>
                </div>
              ))}
            </div>
          )}

          {/* Disclaimer */}
          <div className="summary-disclaimer">
            📋 Kết quả trên chỉ mang tính tham khảo, được ước tính từ camera RGB.
            Không phải đánh giá y khoa hoặc kết luận về chất lượng vận động.
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)', marginTop: 'var(--space-6)' }}>
            <button
              className="btn btn-secondary btn-full"
              style={{
                background: 'rgba(56, 189, 248, 0.15)',
                borderColor: 'rgba(56, 189, 248, 0.4)',
                color: '#38bdf8',
                fontWeight: 'bold',
              }}
              onClick={handleShareSummary}
            >
              📤 Chia sẻ kết quả (Zalo / Tin nhắn)
            </button>
            <button
              className="btn btn-primary btn-full"
              onClick={() => {
                setPhase('instructions');
                setSessionData(null);
                setRepCount(0);
                setCurrentFeedback(null);
                setCurrentAngle(null);
                setExerciseState('IDLE');
                setElapsedTime(0);
                setWorkoutStatus('not_started');
              }}
            >
              🔄 Tập lại
            </button>
            <button
              className="btn btn-secondary btn-full"
              onClick={() => router.push('/exercises')}
            >
              📋 Chọn bài tập khác
            </button>
            <button
              className="btn btn-secondary btn-full"
              onClick={() => router.push('/history')}
            >
              📊 Xem lịch sử
            </button>
          </div>
        </div>

        {shareToast && <div className="toast-notification">{shareToast}</div>}
      </div>
    );
  }

  return null;
}
