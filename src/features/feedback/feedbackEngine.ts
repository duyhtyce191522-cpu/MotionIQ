/**
 * feedbackEngine.ts
 * 
 * Quản lý phản hồi cho người dùng:
 * - Chọn thông báo ưu tiên cao nhất
 * - Cooldown để không lặp lại liên tục
 * - Hàng đợi để không bỏ sót phản hồi quan trọng
 */

import { FeedbackMessage, FeedbackPriority } from '@/types';

const PRIORITY_ORDER: Record<FeedbackPriority, number> = {
  critical: 0,
  warning: 1,
  info: 2,
  success: 3,
};

const DEFAULT_COOLDOWN_MS = 3000;
const CRITICAL_COOLDOWN_MS = 1500;

export class FeedbackEngine {
  private lastMessageTimes: Map<string, number> = new Map();
  private currentMessage: FeedbackMessage | null = null;

  /**
   * Xử lý danh sách feedback từ exercise analyzer
   * Trả về message phù hợp nhất để hiển thị
   */
  processRawFeedback(feedbackTexts: string[]): FeedbackMessage | null {
    if (feedbackTexts.length === 0) return this.currentMessage;

    const now = Date.now();
    const messages: FeedbackMessage[] = feedbackTexts.map((text) =>
      this.classifyFeedback(text)
    );

    // Sắp xếp theo ưu tiên
    messages.sort(
      (a, b) => PRIORITY_ORDER[a.priority] - PRIORITY_ORDER[b.priority]
    );

    // Tìm message chưa hết cooldown
    for (const msg of messages) {
      const lastTime = this.lastMessageTimes.get(msg.id);
      if (!lastTime || now - lastTime >= msg.cooldownMs) {
        this.lastMessageTimes.set(msg.id, now);
        this.currentMessage = msg;
        return msg;
      }
    }

    // Tất cả đang cooldown — giữ message hiện tại
    return this.currentMessage;
  }

  /**
   * Phân loại feedback text thành FeedbackMessage
   */
  private classifyFeedback(text: string): FeedbackMessage {
    const lowerText = text.toLowerCase();

    // Critical — tracking issues
    if (
      lowerText.includes('chưa thấy rõ') ||
      lowerText.includes('điều chỉnh vị trí') ||
      lowerText.includes('lùi ra xa')
    ) {
      return {
        id: `tracking_${this.hashText(text)}`,
        text,
        priority: 'critical',
        category: 'tracking',
        cooldownMs: CRITICAL_COOLDOWN_MS,
      };
    }

    // Success — completion
    if (lowerText.includes('hoàn thành') || lowerText.includes('tốt!')) {
      return {
        id: `success_${this.hashText(text)}`,
        text,
        priority: 'success',
        category: 'counting',
        cooldownMs: DEFAULT_COOLDOWN_MS,
      };
    }

    // Warning — form issues
    if (
      lowerText.includes('thẳng hơn') ||
      lowerText.includes('không đều') ||
      lowerText.includes('chưa đứng thẳng') ||
      lowerText.includes('hạ sâu hơn') ||
      lowerText.includes('nâng tay cao hơn')
    ) {
      return {
        id: `form_${this.hashText(text)}`,
        text,
        priority: 'warning',
        category: 'form',
        cooldownMs: DEFAULT_COOLDOWN_MS * 1.5,
      };
    }

    // Info — general guidance
    return {
      id: `info_${this.hashText(text)}`,
      text,
      priority: 'info',
      category: 'form',
      cooldownMs: DEFAULT_COOLDOWN_MS,
    };
  }

  /** Simple hash for deduplication */
  private hashText(text: string): string {
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash |= 0;
    }
    return Math.abs(hash).toString(36);
  }

  /** Reset cooldowns */
  reset(): void {
    this.lastMessageTimes.clear();
    this.currentMessage = null;
  }

  /** Get current message */
  getCurrentMessage(): FeedbackMessage | null {
    return this.currentMessage;
  }
}
