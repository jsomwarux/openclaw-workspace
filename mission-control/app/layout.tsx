import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import { ConvexClientProvider } from "./ConvexClientProvider";
import { mobileMainClassName } from "@/lib/mission-control/nav-layout";

export const metadata: Metadata = {
  title: "Mission Control",
  description: "Eve & JT — Central Command",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0a0a0a] text-zinc-100">
        <ConvexClientProvider>
          <Sidebar />
          {/* pt-12 for mobile top bar, pb-16 for mobile bottom nav; md: uses sidebar instead */}
          <main className={mobileMainClassName}>
            {children}
          </main>
        </ConvexClientProvider>
      </body>
    </html>
  );
}
