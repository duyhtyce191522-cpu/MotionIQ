/**
 * signalSmoother.ts
 * 
 * Exponential Moving Average (EMA) filter để làm mượt tín hiệu góc khớp.
 * Giảm nhiễu và dao động từ landmark estimation.
 * 
 * EMA formula: smoothed = alpha * current + (1 - alpha) * previous
 * alpha nhỏ hơn = mượt hơn nhưng trễ hơn
 */

export interface SmootherConfig {
  /** EMA alpha factor (0-1). Lower = smoother but more lag. Default: 0.3 */
  alpha: number;
  /** Maximum jump between frames to consider valid (degrees). Default: 45 */
  maxJump: number;
}

const DEFAULT_CONFIG: SmootherConfig = {
  alpha: 0.3,
  maxJump: 45,
};

/**
 * Signal smoother cho một kênh tín hiệu (ví dụ: một góc khớp)
 */
export class SignalSmoother {
  private config: SmootherConfig;
  private previousValue: number | null = null;
  private consecutiveJumps: number = 0;

  constructor(config: Partial<SmootherConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Cập nhật với giá trị mới và trả về giá trị đã làm mượt.
   * 
   * @param value - Giá trị hiện tại (hoặc null nếu không có)
   * @returns Giá trị đã smooth, hoặc null nếu chưa có dữ liệu
   */
  update(value: number | null): number | null {
    if (value === null) {
      return this.previousValue;
    }

    // Lần đầu tiên
    if (this.previousValue === null) {
      this.previousValue = value;
      return value;
    }

    const jump = Math.abs(value - this.previousValue);

    // Phát hiện nhảy bất thường
    if (jump > this.config.maxJump) {
      this.consecutiveJumps++;
      
      // Nếu liên tiếp 3 frame đều nhảy lớn, chấp nhận giá trị mới
      // (có thể người dùng thực sự chuyển động nhanh)
      if (this.consecutiveJumps >= 3) {
        this.previousValue = value;
        this.consecutiveJumps = 0;
        return value;
      }
      
      // Giữ nguyên giá trị cũ
      return this.previousValue;
    }

    this.consecutiveJumps = 0;

    // EMA smoothing
    const smoothed =
      this.config.alpha * value + (1 - this.config.alpha) * this.previousValue;
    this.previousValue = smoothed;
    return smoothed;
  }

  /** Reset về trạng thái ban đầu */
  reset(): void {
    this.previousValue = null;
    this.consecutiveJumps = 0;
  }

  /** Lấy giá trị hiện tại (đã smooth) */
  getCurrentValue(): number | null {
    return this.previousValue;
  }
}

/**
 * Quản lý nhiều smoothers cho nhiều góc khớp
 */
export class MultiSignalSmoother {
  private smoothers: Map<string, SignalSmoother> = new Map();
  private config: Partial<SmootherConfig>;

  constructor(config: Partial<SmootherConfig> = {}) {
    this.config = config;
  }

  /**
   * Cập nhật một kênh tín hiệu
   */
  update(channel: string, value: number | null): number | null {
    if (!this.smoothers.has(channel)) {
      this.smoothers.set(channel, new SignalSmoother(this.config));
    }
    return this.smoothers.get(channel)!.update(value);
  }

  /**
   * Cập nhật nhiều kênh cùng lúc
   */
  updateAll(values: Record<string, number | null>): Record<string, number | null> {
    const result: Record<string, number | null> = {};
    for (const [channel, value] of Object.entries(values)) {
      result[channel] = this.update(channel, value);
    }
    return result;
  }

  /** Reset tất cả smoothers */
  reset(): void {
    this.smoothers.clear();
  }

  /** Lấy giá trị hiện tại của một kênh */
  getValue(channel: string): number | null {
    return this.smoothers.get(channel)?.getCurrentValue() ?? null;
  }
}
