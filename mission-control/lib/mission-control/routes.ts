import { Bot, BriefcaseBusiness, Command, Library, Users, type LucideIcon } from "lucide-react";

export type MissionControlNavItem = {
  href: string;
  icon: LucideIcon;
  label: string;
  desc: string;
  aliases: string[];
};

/**
 * Five lanes, each answering one question: Today (what do I do now), Clients
 * (where does each client stand), Money (where is the cash), Library (what tools
 * do I have), Systems (is the machine healthy). Work, Ship, Evidence, and Health
 * routes still resolve and are reachable from their cockpits, but they are not
 * nav entries — Systems absorbs the machine/evidence/health surfaces.
 */
export const missionControlNav: MissionControlNavItem[] = [
  {
    href: "/",
    icon: Command,
    label: "Today",
    desc: "Next decision",
    aliases: ["/"],
  },
  {
    href: "/clients",
    icon: Users,
    label: "Clients",
    desc: "Who stands where",
    aliases: ["/clients"],
  },
  {
    href: "/consulting",
    icon: BriefcaseBusiness,
    label: "Money",
    desc: "Cash path",
    aliases: ["/consulting"],
  },
  {
    href: "/library",
    icon: Library,
    label: "Library",
    desc: "Tools & agents",
    aliases: ["/library", "/skills"],
  },
  {
    href: "/machine",
    icon: Bot,
    label: "Systems",
    desc: "Machine health",
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
  // Library aliases the existing skills surface until the dedicated lane lands.
  "/library": "/skills",
};
