import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import { Geist_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Ayuda Venezuela — Información de emergencia en Telegram",
  description:
    "Pregunta en español y obtén información clara sobre refugios, agua potable, salud y ayuda humanitaria. Gratis, sin app, sin registro. Un bot de Telegram construido sobre surfcall.",
  openGraph: {
    type: "website",
    title: "Ayuda Venezuela — Información de emergencia en Telegram",
    description:
      "Pregunta en español. Refugios, agua, salud y ayuda — respuestas claras, al instante. Gratis, sin app, sin registro.",
  },
};

export const viewport: Viewport = {
  themeColor: "#0b1f3a",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={`${inter.variable} ${geistMono.variable} bg-bg`}
    >
      <body className="font-sans text-foreground">{children}</body>
    </html>
  );
}
