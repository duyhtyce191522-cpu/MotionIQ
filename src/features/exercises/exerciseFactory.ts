/**
 * exerciseFactory.ts
 * 
 * Factory pattern để tạo exercise analyzer phù hợp.
 * Cho phép mở rộng thêm bài tập mới mà không sửa logic hiện tại.
 */

import { ExerciseId } from '@/types';
import { ExerciseAnalyzer } from './stateMachine';
import { SitToStandAnalyzer } from './sitToStand';
import { SquatAnalyzer } from './squat';
import { ShoulderRaiseAnalyzer } from './shoulderRaise';
import { SideLegRaiseAnalyzer } from './sideLegRaise';

/**
 * Tạo analyzer cho bài tập được chỉ định
 */
export function createExerciseAnalyzer(exerciseId: ExerciseId): ExerciseAnalyzer {
  switch (exerciseId) {
    case 'sit-to-stand':
      return new SitToStandAnalyzer();
    case 'squat':
      return new SquatAnalyzer();
    case 'shoulder-raise':
      return new ShoulderRaiseAnalyzer();
    case 'side-leg-raise':
      return new SideLegRaiseAnalyzer();
    default:
      throw new Error(`Unknown exercise: ${exerciseId}`);
  }
}
