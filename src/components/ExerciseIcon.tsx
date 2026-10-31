import Image from 'next/image';
import { ExerciseInfo } from '@/types';

interface ExerciseIconProps {
  exercise: ExerciseInfo;
  size: number;
}

export default function ExerciseIcon({ exercise, size }: ExerciseIconProps) {
  if (!exercise.iconImage) {
    return (
      <span
        aria-hidden="true"
        style={{ display: 'inline-flex', alignItems: 'center', fontSize: size * 0.75, lineHeight: 1 }}
      >
        {exercise.icon}
      </span>
    );
  }

  return (
    <Image
      src={exercise.iconImage}
      alt={`Minh họa ${exercise.name}`}
      width={size}
      height={size}
      unoptimized
      style={{ width: size, height: size, objectFit: 'cover', borderRadius: 'var(--radius-md)', verticalAlign: 'middle' }}
    />
  );
}
