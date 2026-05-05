/**
 * Root layout.
 * Defines global metadata and imports Tailwind/global styles.
 */

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Photo Upgrader",
  description: "AI-powered product photo relighting and enhancement studio.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}