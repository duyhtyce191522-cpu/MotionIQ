import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MotionIQ — Hỗ trợ tập vận động tại nhà",
  description:
    "Ứng dụng AI hỗ trợ người cao tuổi tập vận động tại nhà thông qua camera smartphone. Theo dõi tư thế, đếm số lần tập và nhận phản hồi thời gian thực.",
  keywords: [
    "tập vận động",
    "người cao tuổi",
    "AI",
    "pose estimation",
    "hỗ trợ thể chất",
  ],
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: "#FAF0DF",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi" data-theme="light">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body
        style={{
          margin: 0,
          padding: 0,
          minHeight: "100dvh",
          backgroundColor: "#EDE1CC", // Soft warm desktop wallpaper
          backgroundImage:
            "radial-gradient(circle at 50% 15%, #F7EFE2 0%, #EDE1CC 100%)",
          display: "flex",
          justifyContent: "center",
          alignItems: "stretch",
          overflowX: "hidden",
          fontFamily: "var(--font-family)",
        }}
      >
        {/* ========================================================
            GLOBAL MOBILE PHONE FRAME CONTAINER (SIZE ĐIỆN THOẠI)
            ======================================================== */}
        <div
          id="mobile-phone-root"
          style={{
            width: "100%",
            maxWidth: "430px", // Standard modern smartphone width
            minHeight: "100dvh",
            backgroundColor: "var(--color-bg-primary, #FAF0DF)",
            color: "var(--color-text-primary, #4A1E14)",
            boxShadow:
              "0 0 50px rgba(158, 59, 36, 0.15), 0 0 0 1px rgba(158, 59, 36, 0.12)",
            display: "flex",
            flexDirection: "column",
            position: "relative",
            overflowX: "hidden",
            fontFamily: "var(--font-family)",
          }}
        >
          {children}
        </div>
      </body>
    </html>
  );
}
