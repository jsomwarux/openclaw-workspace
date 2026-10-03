import type { Metadata } from "next";
import { Hanken_Grotesk, JetBrains_Mono } from "next/font/google";
import "@/docs/design/mission-control-redesign/tokens/tokens.css";

const hanken = Hanken_Grotesk({ subsets: ["latin"], weight: ["400", "500", "600", "700"], variable: "--font-hanken", display: "swap" });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-jetbrains", display: "swap" });

export const metadata: Metadata = {
  title: "Mission Control · Today's run",
};

export default function CockpitLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* tokens.css resolves --mc-font-sans/mono on :root, so the font variables must exist there too. */}
      <style>{`:root{--font-hanken:${hanken.style.fontFamily};--font-jetbrains:${jetbrains.style.fontFamily};}`}</style>
      <div className={`${hanken.variable} ${jetbrains.variable}`}>{children}</div>
    </>
  );
}
