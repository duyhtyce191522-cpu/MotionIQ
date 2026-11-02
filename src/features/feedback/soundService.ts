/**
 * soundService.ts
 * 
 * Web Audio API synthesizer for real-time sound cues (chimes, beeps, warnings).
 * 100% offline, zero external audio asset dependencies, low latency on mobile.
 * Optimized for elderly users: maximum audio output (100% Volume Boost),
 * with master dynamic compression to prevent harsh clipping or speaker distortion.
 */

export class SoundService {
  private ctx: AudioContext | null = null;
  private isEnabled: boolean = true;
  private masterGain: GainNode | null = null;
  private compressor: DynamicsCompressorNode | null = null;
  private volumeLevel: 'max' | 'high' | 'medium' = 'max';

  private getContext(): AudioContext | null {
    if (typeof window === 'undefined') return null;
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();

        // Master Dynamics Compressor: ensures punchy, maximum volume without harsh distortion on phone speakers
        this.compressor = this.ctx.createDynamicsCompressor();
        this.compressor.threshold.setValueAtTime(-6, this.ctx.currentTime);
        this.compressor.knee.setValueAtTime(20, this.ctx.currentTime);
        this.compressor.ratio.setValueAtTime(10, this.ctx.currentTime);
        this.compressor.attack.setValueAtTime(0.003, this.ctx.currentTime);
        this.compressor.release.setValueAtTime(0.15, this.ctx.currentTime);

        // Master Gain
        this.masterGain = this.ctx.createGain();
        this.applyMasterGain();

        this.masterGain.connect(this.compressor);
        this.compressor.connect(this.ctx.destination);
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume().catch(() => {});
    }
    return this.ctx;
  }

  private applyMasterGain(): void {
    if (!this.masterGain || !this.ctx) return;
    const factor = this.volumeLevel === 'max' ? 1.0 : this.volumeLevel === 'high' ? 0.8 : 0.6;
    this.masterGain.gain.setValueAtTime(factor, this.ctx.currentTime);
  }

  public setVolumeLevel(level: 'max' | 'high' | 'medium'): void {
    this.volumeLevel = level;
    this.applyMasterGain();
  }

  public getVolumeLevel(): 'max' | 'high' | 'medium' {
    return this.volumeLevel;
  }

  public setEnabled(enabled: boolean): void {
    this.isEnabled = enabled;
  }

  public getIsEnabled(): boolean {
    return this.isEnabled;
  }

  public toggle(): boolean {
    this.isEnabled = !this.isEnabled;
    return this.isEnabled;
  }

  private connectToMaster(node: AudioNode, ctx: AudioContext): void {
    if (this.masterGain) {
      node.connect(this.masterGain);
    } else {
      node.connect(ctx.destination);
    }
  }

  /**
   * Âm thanh hoàn thành 1 lần tập (Rep Success) - 2 nốt ngân vui tươi, âm lượng tối đa
   */
  public playRepSuccess(): void {
    if (!this.isEnabled) return;
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    // Arpeggio: E5 (659Hz) -> A5 (880Hz)
    osc.frequency.setValueAtTime(659.25, now);
    osc.frequency.setValueAtTime(880.0, now + 0.08);

    gain.gain.setValueAtTime(0.001, now);
    // Tăng âm lượng lên mức tối đa (0.95)
    gain.gain.exponentialRampToValueAtTime(0.95, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);

    osc.connect(gain);
    this.connectToMaster(gain, ctx);

    osc.start(now);
    osc.stop(now + 0.40);
  }

  /**
   * Âm thanh chạm đỉnh/đáy tư thế chuẩn (Peak hold ping) - Âm lượng tối đa
   */
  public playPeakHold(): void {
    if (!this.isEnabled) return;
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(523.25, now); // C5

    gain.gain.setValueAtTime(0.001, now);
    // Tăng âm lượng lên mức tối đa (0.90)
    gain.gain.exponentialRampToValueAtTime(0.90, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);

    osc.connect(gain);
    this.connectToMaster(gain, ctx);

    osc.start(now);
    osc.stop(now + 0.24);
  }

  /**
   * Âm cảnh báo nhẹ khi tư thế sai hoặc mất thăng bằng - Âm lượng tối đa
   */
  public playWarning(): void {
    if (!this.isEnabled) return;
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(329.63, now); // E4
    osc.frequency.setValueAtTime(261.63, now + 0.1); // C4

    gain.gain.setValueAtTime(0.001, now);
    // Tăng âm lượng lên mức tối đa (0.92)
    gain.gain.exponentialRampToValueAtTime(0.92, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);

    osc.connect(gain);
    this.connectToMaster(gain, ctx);

    osc.start(now);
    osc.stop(now + 0.30);
  }

  /**
   * Đếm nhịp đếm ngược (3, 2, 1, Bắt đầu) - Âm lượng tối đa
   */
  public playCountdownTick(isFinal: boolean = false): void {
    if (!this.isEnabled) return;
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    const freq = isFinal ? 880 : 440;
    osc.frequency.setValueAtTime(freq, now);

    gain.gain.setValueAtTime(0.001, now);
    // Tăng âm lượng lên mức tối đa (0.95)
    gain.gain.exponentialRampToValueAtTime(0.95, now + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, now + (isFinal ? 0.38 : 0.15));

    osc.connect(gain);
    this.connectToMaster(gain, ctx);

    osc.start(now);
    osc.stop(now + (isFinal ? 0.40 : 0.16));
  }

  /**
   * Âm thanh chúc mừng hoàn thành mục tiêu (Fanfare / Celebration) - Âm lượng tối đa
   */
  public playCelebration(): void {
    if (!this.isEnabled) return;
    const ctx = this.getContext();
    if (!ctx) return;

    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    const now = ctx.currentTime;

    notes.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now + idx * 0.1);

      gain.gain.setValueAtTime(0.001, now + idx * 0.1);
      // Tăng âm lượng lên mức tối đa (0.95)
      gain.gain.exponentialRampToValueAtTime(0.95, now + idx * 0.1 + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.1 + 0.42);

      osc.connect(gain);
      this.connectToMaster(gain, ctx);

      osc.start(now + idx * 0.1);
      osc.stop(now + idx * 0.1 + 0.45);
    });
  }

  /**
   * Còi báo động khẩn cấp (2 tông xen kẽ, ~1.6s).
   * Phát ở mức 100% công suất loa, BẤT KỂ người dùng đã tắt âm thanh thông thường.
   */
  public playEmergencyAlarm(): void {
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'square';
    for (let i = 0; i < 8; i++) {
      osc.frequency.setValueAtTime(i % 2 === 0 ? 960 : 640, now + i * 0.2);
    }

    gain.gain.setValueAtTime(0.001, now);
    // Tối đa 100% công suất
    gain.gain.exponentialRampToValueAtTime(1.0, now + 0.03);
    gain.gain.setValueAtTime(1.0, now + 1.5);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 1.6);

    osc.connect(gain);
    // Báo động kết nối thẳng tới loa đích để đảm bảo to nhất
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 1.62);
  }

  public destroy(): void {
    if (this.ctx) {
      this.ctx.close().catch(() => {});
      this.ctx = null;
      this.masterGain = null;
      this.compressor = null;
    }
  }
}
