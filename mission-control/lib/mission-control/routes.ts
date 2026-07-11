import { Bot, BriefcaseBusiness, Command, type LucideIcon } from "lucide-react";

export type MissionControlNavItem = {
  href: string;
  icon: LucideIcon;
  label: string;
  desc: string;
  aliases: string[];
};

/**
 * Three lanes only. Work, Ship, Evidence, and Health routes still resolve — they
 * are reachable from their cockpits — but a nav with seven entries is a menu,
 * not a cockpit, so Systems absorbs the machine/evidence/health surfaces.
 */
export const missionControlNav: MissionControlNavItem[] = [
  {
    href: "/",
    icon: Command,
    label: "Cockpit",
    desc: "Decisions",
    aliases: ["/"],
  },
  {
    href: "/consulting",
    icon: BriefcaseBusiness,
    label: "Money",
    desc: "Cash path",
    aliases: ["/consulting"],
  },
  {
    href: "/machine",
    icon: Bot,
    label: "Systems",
    desc: "Agents · proof · ops",
    aliases: [
      "/machine",
      "/agents",
      "/calendar",
      "/evidence",
      "/audit",
      "/health",
      "/monitor",
      "/costs",
      "/memory",
      "/overnight",
      "/skills",
      "/systems",
    ],
  },
];

export const mobileNav = missionControlNav;

export const legacyRedirects: Record<string, string> = {
  "/tasks": "/work",
  "/vibe": "/ship",
  "/agents": "/machine",
  "/audit": "/evidence",
  "/monitor": "/health",
  "/costs": "/health",
};
