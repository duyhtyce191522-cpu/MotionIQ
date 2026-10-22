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
    "phục hồi chức năng",
  ],
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: "#0a0f1e",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
