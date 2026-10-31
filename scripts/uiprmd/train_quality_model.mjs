import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const dataDir = path.join(scriptDir, 'data');
const outputPath = path.resolve(scriptDir, '..', '..', 'src', 'features', 'pose', 'uiprmdQualityModel.json');
const exercises = {
  m01: 'squat',
  m06: 'side-leg-raise',
  m05: 'sit-to-stand',
  m07: 'shoulder-raise',
};
const validationSubjects = new Set([9, 10]);
const epochs = 500;
const learningRate = 0.08;
const regularization = 0.02;

function eulerMatrix(degrees) {
  const [x, y, z] = degrees.map((value) => (value * Math.PI) / 180);
  const cx = Math.cos(x), sx = Math.sin(x);
  const cy = Math.cos(y), sy = Math.sin(y);
  const cz = Math.cos(z), sz = Math.sin(z);
  return [
    [cz * cy, cz * sy * sx - sz * cx, cz * sy * cx + sz * sx],
    [sz * cy, sz * sy * sx + cz * cx, sz * sy * cx - cz * sx],
    [-sy, cy * sx, cy * cx],
  ];
}

function multiplyMatrices(a, b) {
  return a.map((row, i) =>
    row.map((_, j) => row.reduce((sum, value, k) => sum + value * b[k][j], 0))
  );
}

function rotate(matrix, vector) {
  return matrix.map((row) => row.reduce((sum, value, i) => sum + value * vector[i], 0));
}

function transformSkeleton(position, angle) {
  const points = Array.from({ length: 22 }, () => [0, 0, 0]);
  const rotations = Array.from({ length: 22 }, () => eulerMatrix([0, 0, 0]));
  points[0] = position.slice(0, 3);
  rotations[0] = eulerMatrix(angle.slice(0, 3));

  const links = [
    [1, 0, 0], [2, 1, 1], [3, 2, 2], [4, 3, 3], [5, 4, 4],
    [6, 2, 2], [7, 6, 6], [8, 7, 7], [9, 8, 8],
    [10, 2, 2], [11, 10, 10], [12, 11, 11], [13, 12, 12],
    [14, 0, 0], [15, 14, 14], [16, 15, 15], [17, 16, 16],
    [18, 0, 0], [19, 18, 18], [20, 19, 19], [21, 20, 20],
  ];

  for (const [joint, parent, parentRotation] of links) {
    const local = position.slice(joint * 3, joint * 3 + 3);
    const rotated = rotate(rotations[parentRotation], local);
    points[joint] = points[parent].map((value, axis) => value + rotated[axis]);
    rotations[joint] = multiplyMatrices(
      rotations[parentRotation],
      eulerMatrix(angle.slice(joint * 3, joint * 3 + 3))
    );
  }

  return points;
}

function normalizeFrame(points) {
  const waist = points[0];
  const chest = points[2];
  const scale = Math.hypot(...chest.map((value, i) => value - waist[i]));
  if (!Number.isFinite(scale) || scale < 1) return null;
  return points.flatMap((point) => point.map((value, axis) => (value - waist[axis]) / scale));
}

function parseRows(filePath) {
  const rows = fs.readFileSync(filePath, 'utf8').trim().split(/\r?\n/).map((line) =>
    line.split(',').map(Number)
  );
  if (rows.some((row) => row.length !== 66 || row.some((value) => !Number.isFinite(value)))) {
    throw new Error(`Unexpected 22-joint frame in ${filePath}`);
  }
  return rows;
}

function loadSequences(movement, label) {
  const folder = path.join(dataDir, label, 'Positions');
  const names = fs.readdirSync(folder).filter((name) =>
    name.startsWith(`${movement}_`) && name.includes('_positions')
  );
  return names.map((name) => {
    const match = name.match(/_s(\d+)_/);
    if (!match) throw new Error(`Cannot read subject ID from ${name}`);
    const positionRows = parseRows(path.join(folder, name));
    const angleName = name.replace('_positions', '_angles');
    const anglePath = path.join(dataDir, label, 'Angles', angleName);
    if (!fs.existsSync(anglePath)) throw new Error(`Missing paired angle file: ${anglePath}`);
    const angleRows = parseRows(anglePath);
    if (positionRows.length !== angleRows.length) {
      throw new Error(`Position/angle frame count mismatch: ${name}`);
    }

    const frames = [];
    for (let frame = 0; frame < positionRows.length; frame++) {
      const normalized = normalizeFrame(
        transformSkeleton(positionRows[frame], angleRows[frame])
      );
      if (normalized) frames.push(normalized);
    }
    if (frames.length < 5) throw new Error(`Too few usable frames: ${name}`);
    return {
      subject: Number(match[1]),
      label: label === 'correct' ? 1 : 0,
      frames,
      name,
    };
  });
}

function summarize(frames) {
  const dimensions = frames[0].length;
  const mean = Array(dimensions).fill(0);
  const variance = Array(dimensions).fill(0);
  for (const frame of frames) {
    for (let i = 0; i < dimensions; i++) mean[i] += frame[i];
  }
  for (let i = 0; i < dimensions; i++) mean[i] /= frames.length;
  for (const frame of frames) {
    for (let i = 0; i < dimensions; i++) variance[i] += (frame[i] - mean[i]) ** 2;
  }
  for (let i = 0; i < dimensions; i++) variance[i] = Math.sqrt(variance[i] / frames.length);
  return [...mean, ...variance];
}

function sigmoid(value) {
  if (value >= 0) return 1 / (1 + Math.exp(-value));
  const exp = Math.exp(value);
  return exp / (1 + exp);
}

function train(samples) {
  const featureCount = samples[0].features.length;
  const mean = Array(featureCount).fill(0);
  const scale = Array(featureCount).fill(0);
  for (const sample of samples) {
    for (let i = 0; i < featureCount; i++) mean[i] += sample.features[i];
  }
  for (let i = 0; i < featureCount; i++) mean[i] /= samples.length;
  for (const sample of samples) {
    for (let i = 0; i < featureCount; i++) scale[i] += (sample.features[i] - mean[i]) ** 2;
  }
  for (let i = 0; i < featureCount; i++) {
    scale[i] = Math.max(Math.sqrt(scale[i] / samples.length), 0.0001);
  }

  const weights = Array(featureCount).fill(0);
  let bias = 0;
  for (let epoch = 0; epoch < epochs; epoch++) {
    const gradient = Array(featureCount).fill(0);
    let biasGradient = 0;
    for (const sample of samples) {
      let logit = bias;
      for (let i = 0; i < featureCount; i++) {
        logit += weights[i] * ((sample.features[i] - mean[i]) / scale[i]);
      }
      const error = sigmoid(logit) - sample.label;
      biasGradient += error;
      for (let i = 0; i < featureCount; i++) {
        gradient[i] += error * ((sample.features[i] - mean[i]) / scale[i]);
      }
    }
    const rate = learningRate / samples.length;
    bias -= rate * biasGradient;
    for (let i = 0; i < featureCount; i++) {
      weights[i] -= rate * (gradient[i] + regularization * weights[i]);
    }
  }

  return { mean, scale, weights, bias };
}

function probability(model, features) {
  let logit = model.bias;
  for (let i = 0; i < features.length; i++) {
    logit += model.weights[i] * ((features[i] - model.mean[i]) / model.scale[i]);
  }
  return sigmoid(logit);
}

const output = {
  dataset: 'UI-PRMD',
  doi: '10.5281/zenodo.23104965',
  input: '22-joint Kinect positions reconstructed using the paired Euler-angle rotations',
  warning: 'Experimental movement-quality estimate only; not a medical diagnosis or safety monitor.',
  validationSubjects: [...validationSubjects],
  exercises: {},
};

for (const [movement, exerciseId] of Object.entries(exercises)) {
  const all = [
    ...loadSequences(movement, 'correct'),
    ...loadSequences(movement, 'incorrect'),
  ].map((sample) => ({ ...sample, features: summarize(sample.frames) }));
  const correctCount = all.filter((sample) => sample.label === 1).length;
  const incorrectCount = all.filter((sample) => sample.label === 0).length;
  if (correctCount !== 100 || incorrectCount !== 100) {
    throw new Error(
      `${movement} requires 100 correct and 100 incorrect sequences; found ${correctCount} and ${incorrectCount}`
    );
  }
  const training = all.filter((sample) => !validationSubjects.has(sample.subject));
  const validation = all.filter((sample) => validationSubjects.has(sample.subject));
  if (training.length === 0 || validation.length === 0) {
    throw new Error(`Incomplete subject-separated split for ${movement}`);
  }

  const model = train(training);
  const correct = validation.filter((sample) => sample.label === 1);
  const incorrect = validation.filter((sample) => sample.label === 0);
  const accuracy = validation.filter(
    (sample) => (probability(model, sample.features) >= 0.5 ? 1 : 0) === sample.label
  ).length / validation.length;

  output.exercises[exerciseId] = {
    movement,
    featureCount: model.weights.length,
    mean: model.mean,
    scale: model.scale,
    weights: model.weights,
    bias: model.bias,
    validation: {
      subjects: [...validationSubjects],
      samples: validation.length,
      correctSamples: correct.length,
      incorrectSamples: incorrect.length,
      accuracy: Number(accuracy.toFixed(4)),
    },
  };
  console.log(`${exerciseId}: held-out-subject accuracy ${(accuracy * 100).toFixed(1)}% (${validation.length} reps)`);
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(`Saved experimental model to ${outputPath}`);
