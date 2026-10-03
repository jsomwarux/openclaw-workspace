import type { Config } from "tailwindcss";
import cockpitTokens from "./docs/design/mission-control-redesign/tokens/tailwind.config";
import { densitySpacing } from "./lib/cockpit/density";

// The /cockpit design tokens, read from the design bundle by name. The bundle's sans/mono
// families are exposed as mc-sans/mc-mono so the current interface keeps its fonts.
const cockpit = cockpitTokens.theme.extend;

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: "#111111",
          raised: "#1a1a1a",
          border: "#2a2a2a",
        },
        accent: {
          DEFAULT: "#10b981",    // emerald
          dim: "#059669",
          glow: "#34d399",
        },
        ...cockpit.colors,
      },
      fontFamily: {
        mono: ["'JetBrains Mono'", "Menlo", "monospace"],
        "mc-sans": cockpit.fontFamily.sans,
        "mc-mono": cockpit.fontFamily.mono,
      },
      spacing: densitySpacing,
      fontSize: cockpit.fontSize,
      borderRadius: cockpit.borderRadius,
      maxWidth: cockpit.maxWidth,
      height: cockpit.height,
      width: cockpit.width,
    },
  },
  plugins: [],
};

export default config;
