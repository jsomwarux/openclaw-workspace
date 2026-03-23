"use client";
import { cn } from "@/lib/utils";

interface SystemCardProps {
  name: string;
  subtitle: string;
  dark: boolean;
  children: React.ReactNode;
}

export default function SystemCard({
  name,
  subtitle,
  dark,
  children,
}: SystemCardProps) {
  return (
    <div
      className={cn(
        "rounded-xl border p-5 transition-colors",
        dark ? "bg-gray-900 border-gray-700" : "bg-white border-gray-200"
      )}
    >
      <h2
        className={cn(
          "text-base font-bold tracking-tight",
          dark ? "text-zinc-100" : "text-zinc-900"
        )}
      >
        {name}
      </h2>
      <p
        className={cn(
          "text-[11px] mt-0.5 mb-4",
          dark ? "text-zinc-500" : "text-zinc-400"
        )}
      >
        {subtitle}
      </p>
      {children}
    </div>
  );
}
