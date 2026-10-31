/**
 * speechService.ts
 * 
 * Dịch vụ phát âm giọng nói Tiếng Việt cho MotionIQ.
 * Hỗ trợ đa tầng:
 * 1. Web Speech API với bộ lọc chọn lọc giọng Tiếng Việt chuẩn (Google Tiếng Việt, Microsoft Hoài My/Nam Minh, iOS Linh).
 * 2. Tự động lắng nghe sự kiện `onvoiceschanged` để không bị mất giọng khi trình duyệt tải bất đồng bộ.
 * 3. Fallback thông minh: Nếu máy tính/hệ điều hành chưa cài gói giọng nói Tiếng Việt,
 *    tự động phát âm thanh Tiếng Việt chuẩn qua Audio Stream.
 * 4. Bộ nhớ đệm (Cache) các cụm từ phổ biến ("1 lần", "2 lần", "Tốt lắm",...) để phát tức thì 0ms trễ.
 */

export class SpeechService {
  private synthesis: SpeechSynthesis | null = null;
  private isEnabled: boolean = true;
  private isSupported: boolean = false;
  private lastSpokenText: string = '';
  private lastSpokenTime: number = 0;
  private cooldownMs: number = 2500;
  private viVoice: SpeechSynthesisVoice | null = null;
  private audioCache: Map<string, HTMLAudioElement> = new Map();
  private currentAudio: HTMLAudioElement | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      if ('speechSynthesis' in window) {
        this.synthesis = window.speechSynthesis;
        this.isSupported = true;
        this.loadVoices();

        if (this.synthesis.onvoiceschanged !== undefined) {
          this.synthesis.onvoiceschanged = () => {
            this.loadVoices();
          };
        }
      }
      // Khởi động nạp trước các cụm từ tiếng Việt quen thuộc để phát tức thì 0ms
      this.preloadCommonPhrases();
    }
  }

  /**
   * Tải và nạp trước âm thanh cho các câu đếm nhịp và phản hồi phổ biến
   */
  private preloadCommonPhrases(): void {
    const common = [
      '1 lần', '2 lần', '3 lần', '4 lần', '5 lần',
      '6 lần', '7 lần', '8 lần', '9 lần', '10 lần',
      '15 lần', '20 lần',
      'Đứng thẳng người', 'Hạ gối sâu hơn', 'Rất tốt',
      'Giữ đều nhịp thở', 'Thẳng lưng', 'Tốt lắm', 'Cố lên',
      'Bắt đầu tập luyện', 'Tạm dừng', 'Tiếp tục', 'Hoàn thành buổi tập',
      'Xin chào! MotionIQ sẵn sàng hỗ trợ bạn tập luyện.',
      'Đã nhận diện đủ khớp', 'Ba', 'Hai', 'Một', 'Bắt đầu',
      'Đã nhận diện đủ khớp, chuẩn bị bắt đầu',
      'Hãy vào tư thế sẵn sàng',
      'Giạng chân cao hơn', 'Thẳng gối', 'Nhón cao gót chân', 'Hạ gót từ từ', 'Giữ thăng bằng tốt lắm',
    ];

    common.forEach((phrase) => {
      try {
        const url = `/api/tts?text=${encodeURIComponent(phrase)}`;
        const audio = new Audio(url);
        audio.preload = 'auto';
        this.audioCache.set(phrase, audio);
      } catch {
        // ignore preload errors
      }
    });
  }

  /**
   * Tải và tìm kiếm giọng tiếng Việt tối ưu trên thiết bị
   */
  private loadVoices(): void {
    if (!this.synthesis) return;
    const voices = this.synthesis.getVoices();
    if (!voices || voices.length === 0) return;

    // Tìm giọng tiếng Việt chuẩn xác (loại bỏ hoàn toàn các trường hợp nhận nhầm voice tiếng Anh/Đức)
    const vi = voices.find((v) => {
      const lang = (v.lang || '').toLowerCase().replace('_', '-');
      const name = (v.name || '').toLowerCase();
      
      const isViLang = lang === 'vi' || lang === 'vi-vn' || lang.startsWith('vi-');
      const isViName =
        name.includes('tiếng việt') ||
        name.includes('vietnam') ||
        name.includes('vietnamese') ||
        name.includes('hoai my') ||
        name.includes('hoaimy') ||
        name.includes('nam minh') ||
        name.includes('namminh') ||
        (name.includes('linh') && !name.includes('english'));

      return isViLang || isViName;
    });

    if (vi) {
      this.viVoice = vi;
      console.log(`[SpeechService] Đã kích hoạt giọng tiếng Việt: ${vi.name} (${vi.lang})`);
    } else {
      this.viVoice = null;
      console.log('[SpeechService] Không có voice tiếng Việt cục bộ. Kích hoạt giọng đọc tiếng Việt chuẩn qua /api/tts.');
    }
  }

  /** Lấy tên giọng nói đang dùng */
  public getVoiceName(): string {
    if (this.viVoice) {
      return this.viVoice.name;
    }
    return 'Giọng Tiếng Việt chuẩn (AI)';
  }

  /** Kiểm tra thiết bị có sẵn giọng tiếng Việt offline không */
  public hasNativeViVoice(): boolean {
    return this.viVoice !== null;
  }

  /**
   * Phát giọng nói tiếng Việt
   * @param text Câu cần đọc
   * @param force Bỏ qua cooldown (ví dụ khi người dùng bấm thử giọng)
   */
  public speak(text: string, force: boolean = false): void {
    if (!this.isEnabled) return;

    const trimmed = text.trim();
    if (!trimmed) return;

    const now = Date.now();
    if (!force && trimmed === this.lastSpokenText && now - this.lastSpokenTime < this.cooldownMs) {
      return;
    }

    this.cancel();

    // 1. Ưu tiên Web Speech API NẾU và CHỈ NẾU thiết bị có voice tiếng Việt thật
    if (this.synthesis && this.viVoice) {
      try {
        const utterance = new SpeechSynthesisUtterance(trimmed);
        utterance.voice = this.viVoice;
        utterance.lang = 'vi-VN';
        utterance.rate = 0.92; // Tốc độ vừa phải cho người cao tuổi dễ nghe
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        this.synthesis.speak(utterance);
        this.lastSpokenText = trimmed;
        this.lastSpokenTime = now;
        return;
      } catch (e) {
        console.warn('[SpeechService] Lỗi phát Web Speech API, chuyển sang phát trực tuyến:', e);
      }
    }

    // 2. Phát qua API âm thanh Tiếng Việt chuẩn 100% không lo lỗi phát âm tiếng Anh
    this.speakViaAudioFallback(trimmed);
    this.lastSpokenText = trimmed;
    this.lastSpokenTime = now;
  }

  /**
   * Phát cảnh báo khẩn cấp — BỎ QUA trạng thái tắt giọng nói và cooldown.
   * Chỉ dùng cho cảnh báo an toàn (mất dấu người tập, nghi ngã...).
   */
  public speakUrgent(text: string): void {
    const wasEnabled = this.isEnabled;
    this.isEnabled = true;
    try {
      this.speak(text, true);
    } finally {
      this.isEnabled = wasEnabled;
    }
  }

  /**
   * Phát qua Audio Stream tiếng Việt chuẩn (chất lượng cao qua Next.js /api/tts)
   */
  private speakViaAudioFallback(text: string): void {
    if (typeof window === 'undefined') return;

    try {
      let audio = this.audioCache.get(text);
      if (!audio) {
        const url = `/api/tts?text=${encodeURIComponent(text)}`;
        audio = new Audio(url);
        // Lưu cache các câu ngắn thường dùng để phát không độ trễ
        if (text.length <= 40) {
          this.audioCache.set(text, audio);
        }
      }

      audio.currentTime = 0;
      this.currentAudio = audio;
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch((err) => {
          console.warn('[SpeechService] Không thể phát âm thanh:', err);
        });
      }
    } catch (e) {
      console.warn('[SpeechService] Lỗi phát audio:', e);
    }
  }

  /** Hủy giọng đang nói */
  public cancel(): void {
    if (this.synthesis) {
      this.synthesis.cancel();
    }
    if (this.currentAudio) {
      try {
        this.currentAudio.pause();
        this.currentAudio.currentTime = 0;
      } catch {}
      this.currentAudio = null;
    }
  }

  public enable(): void {
    this.isEnabled = true;
  }

  public disable(): void {
    this.isEnabled = false;
    this.cancel();
  }

  public toggle(): boolean {
    this.isEnabled = !this.isEnabled;
    if (!this.isEnabled) {
      this.cancel();
    }
    return this.isEnabled;
  }

  public getIsEnabled(): boolean {
    return this.isEnabled;
  }

  public getIsSupported(): boolean {
    return this.isSupported;
  }

  public setCooldown(ms: number): void {
    this.cooldownMs = ms;
  }

  public destroy(): void {
    this.cancel();
    this.audioCache.clear();
    this.synthesis = null;
  }
}
