import { NextRequest, NextResponse } from 'next/server';

/**
 * Next.js API Route: /api/tts
 * 
 * Server-side Vietnamese Text-to-Speech proxy.
 * Solves browser CORS and origin blocking, providing 100% reliable, natural
 * Vietnamese voice stream (audio/mpeg) on all browsers and devices.
 */
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const rawText = searchParams.get('text');

  if (!rawText) {
    return new NextResponse('Missing text parameter', { status: 400 });
  }

  const text = rawText.trim();
  if (!text) {
    return new NextResponse('Empty text', { status: 400 });
  }

  try {
    const url = `https://translate.google.com/translate_tts?ie=UTF-8&tl=vi&client=tw-ob&q=${encodeURIComponent(text)}`;
    const response = await fetch(url, {
      headers: {
        'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        Referer: 'https://translate.google.com/',
      },
    });

    if (!response.ok) {
      console.warn(`[TTS API] Provider returned status ${response.status}`);
      return new NextResponse('TTS provider error', { status: response.status });
    }

    const audioData = await response.arrayBuffer();

    return new NextResponse(audioData, {
      status: 200,
      headers: {
        'Content-Type': 'audio/mpeg',
        'Cache-Control': 'public, max-age=604800, immutable',
      },
    });
  } catch (error) {
    console.error('[TTS API Error]', error);
    return new NextResponse('Internal server error', { status: 500 });
  }
}
