import modelData from './uiprmdQualityModel.json';
import { ExerciseId, NormalizedLandmark } from '@/types';

interface ExerciseModel {
  movement: string;
  featureCount: number;
  mean: number[];
  scale: number[];
  weights: number[];
  bias: number;
  validation: {
    subjects: number[];
    samples: number;
    correctSamples: number;
    incorrectSamples: number;
    accuracy: number;
  };
}

interface ModelArtifact {
  dataset: string;
  doi: string;
  warning: string;
  exercises: Partial<Record<ExerciseId, ExerciseModel>>;
}

export interface DatasetQualityAssessment {
  label: 'good' | 'needs_adjustment' | 'uncertain';
  score: number;
}

const artifact: ModelArtifact = modelData;
const LANDMARK = {
  nose: 0,
  leftShoulder: 11,
  rightShoulder: 12,
  leftElbow: 13,
  rightElbow: 14,
  leftWrist: 15,
  rightWrist: 16,
  leftIndex: 19,
  rightIndex: 20,
  leftHip: 23,
  rightHip: 24,
  leftKnee: 25,
  rightKnee: 26,
  leftAnkle: 27,
  rightAnkle: 28,
  leftFoot: 31,
  rightFoot: 32,
} as const;

function midpoint(a: NormalizedLandmark, b: NormalizedLandmark): number[] {
  return [(a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2];
}

function toPoint(landmark: NormalizedLandmark): number[] {
  return [landmark.x, landmark.y, landmark.z];
}

function interpolate(a: number[], b: number[], amount: number): number[] {
  return a.map((value, index) => value + (b[index] - value) * amount);
}

/**
 * Convert MediaPipe's world landmarks to UI-PRMD's 22-joint, torso-normalized
 * representation so the browser can use the locally trained model.
 */
export function getQualityModelFrame(
  landmarks: NormalizedLandmark[] | undefined
): number[] | null {
  if (!landmarks || landmarks.length < 33) return null;

  const required = [
    LANDMARK.nose,
    LANDMARK.leftShoulder, LANDMARK.rightShoulder,
    LANDMARK.leftElbow, LANDMARK.rightElbow,
    LANDMARK.leftWrist, LANDMARK.rightWrist,
    LANDMARK.leftIndex, LANDMARK.rightIndex,
    LANDMARK.leftHip, LANDMARK.rightHip,
    LANDMARK.leftKnee, LANDMARK.rightKnee,
    LANDMARK.leftAnkle, LANDMARK.rightAnkle,
    LANDMARK.leftFoot, LANDMARK.rightFoot,
  ];
  if (required.some((index) => (landmarks[index]?.visibility ?? 0) < 0.35)) return null;

  const waist = midpoint(landmarks[LANDMARK.leftHip], landmarks[LANDMARK.rightHip]);
  const chest = midpoint(landmarks[LANDMARK.leftShoulder], landmarks[LANDMARK.rightShoulder]);
  const nose = toPoint(landmarks[LANDMARK.nose]);
  const torsoLength = Math.hypot(...chest.map((value, i) => value - waist[i]));
  if (!Number.isFinite(torsoLength) || torsoLength < 0.05) return null;

  const points = [
    waist,
    interpolate(waist, chest, 0.5),
    chest,
    interpolate(chest, nose, 0.5),
    nose,
    nose,
    toPoint(landmarks[LANDMARK.leftShoulder]),
    toPoint(landmarks[LANDMARK.leftElbow]),
    toPoint(landmarks[LANDMARK.leftWrist]),
    toPoint(landmarks[LANDMARK.leftIndex]),
    toPoint(landmarks[LANDMARK.rightShoulder]),
    toPoint(landmarks[LANDMARK.rightElbow]),
    toPoint(landmarks[LANDMARK.rightWrist]),
    toPoint(landmarks[LANDMARK.rightIndex]),
    toPoint(landmarks[LANDMARK.leftHip]),
    toPoint(landmarks[LANDMARK.leftKnee]),
    toPoint(landmarks[LANDMARK.leftAnkle]),
    toPoint(landmarks[LANDMARK.leftFoot]),
    toPoint(landmarks[LANDMARK.rightHip]),
    toPoint(landmarks[LANDMARK.rightKnee]),
    toPoint(landmarks[LANDMARK.rightAnkle]),
    toPoint(landmarks[LANDMARK.rightFoot]),
  ];

  return points.flatMap((point) =>
    point.map((value, axis) => (value - waist[axis]) / torsoLength)
  );
}

function summarizeFrames(frames: number[][]): number[] | null {
  if (frames.length < 5) return null;
  const dimensions = frames[0].length;
  const mean = Array(dimensions).fill(0) as number[];
  const variance = Array(dimensions).fill(0) as number[];
  for (const frame of frames) {
    if (frame.length !== dimensions) return null;
    for (let i = 0; i < dimensions; i++) mean[i] += frame[i];
  }
  for (let i = 0; i < dimensions; i++) mean[i] /= frames.length;
  for (const frame of frames) {
    for (let i = 0; i < dimensions; i++) variance[i] += (frame[i] - mean[i]) ** 2;
  }
  for (let i = 0; i < dimensions; i++) variance[i] = Math.sqrt(variance[i] / frames.length);
  return [...mean, ...variance];
}

function sigmoid(value: number): number {
  if (value >= 0) return 1 / (1 + Math.exp(-value));
  const exp = Math.exp(value);
  return exp / (1 + exp);
}

export function assessUiprmdQuality(
  exerciseId: ExerciseId,
  frames: number[][]
): DatasetQualityAssessment | null {
  const model = artifact.exercises[exerciseId];
  const features = summarizeFrames(frames);
  if (!model || !features || features.length !== model.featureCount) return null;

  let logit = model.bias;
  for (let i = 0; i < features.length; i++) {
    logit += model.weights[i] * ((features[i] - model.mean[i]) / model.scale[i]);
  }
  const correctProbability = sigmoid(logit);
  const confidence = correctProbability >= 0.5 ? correctProbability : 1 - correctProbability;

  return {
    label:
      correctProbability >= 0.7
        ? 'good'
        : correctProbability <= 0.3
          ? 'needs_adjustment'
          : 'uncertain',
    score: confidence,
  };
}
