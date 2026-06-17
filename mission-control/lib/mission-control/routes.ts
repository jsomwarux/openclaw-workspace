import {
  Activity,
  Bot,
  BriefcaseBusiness,
  Command,
  HeartPulse,
  Rocket,
  ShieldCheck,
  type LucideIcon,
} from "lucide-react";

export type MissionControlNavItem = {
  href: string;
  icon: LucideIcon;
  label: string;
  desc: string;
  aliases: string[];
};

export const missionControlNav: MissionControlNavItem[] = [
  {
    href: "/",
    icon: Command,
    label: "Command",
    desc: "Decisions",
    aliases: ["/"],
  },
  {
    href: "/work",
    icon: Activity,
    label: "Work",
    desc: "Tasks",
    aliases: ["/work", "/history"],
  },
  {
    href: "/consulting",
    icon: BriefcaseBusiness,
    label: "Revenue",
    desc: "Cash path",
    aliases: ["/consulting"],
  },
  {
    href: "/ship",
    icon: Rocket,
    label: "Ship",
    desc: "Apps",
    aliases: ["/ship", "/vibe", "/passive-income"],
  },
  {
    href: "/machine",
    icon: Bot,
    label: "Machine",
    desc: "Agents",
    aliases: ["/machine", "/agents", "/calendar"],
  },
  {
    href: "/evidence",
    icon: ShieldCheck,
    label: "Evidence",
    desc: "Proof",
    aliases: ["/evidence", "/audit", "/memory", "/overnight", "/skills", "/systems"],
  },
  {
    href: "/health",
    icon: HeartPulse,
    label: "Health",
    desc: "Ops",
    aliases: ["/health", "/monitor", "/costs"],
  },
];

export const mobileNav = missionControlNav.slice(0, 5);

export const legacyRedirects: Record<string, string> = {
  "/tasks": "/work",
  "/vibe": "/ship",
  "/agents": "/machine",
  "/audit": "/evidence",
  "/monitor": "/health",
  "/costs": "/health",
};
